"""The Noesis router: one OpenAI-compatible URL that resolves an alias or model name to a backend.

    NOESIS_API_KEY=demo-key uv run uvicorn router.main:app --port 8000

Streaming works. One JSON line per call goes to stdout.
"""
import asyncio
import json
import os
import time
import tomllib
from pathlib import Path

import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.background import BackgroundTask

with open(os.environ.get("ROUTER_CONFIG", Path(__file__).with_name("config.toml")), "rb") as f:
    CONFIG = tomllib.load(f)
MODELS = CONFIG["models"]
ALIASES = CONFIG.get("aliases", {})
KEY = os.environ["NOESIS_API_KEY"]

# Long generations: 10 minutes to read.
client = httpx.AsyncClient(timeout=httpx.Timeout(600.0, connect=5.0))
app = FastAPI()


def log(**kw):
    print(json.dumps(kw), flush=True)


def error(status, message):
    return JSONResponse({"error": {"message": message, "code": status}}, status_code=status)


# TODO: per-client keys (one key per client, so calls can be attributed and revoked).
def authorized(request: Request) -> bool:
    return request.headers.get("authorization") == f"Bearer {KEY}"


def backend_headers(model: dict) -> dict:
    headers = {"content-type": "application/json"}
    if model.get("api_key_env"):
        headers["authorization"] = f"Bearer {os.environ[model['api_key_env']]}"
    return headers


async def is_up(model: dict) -> bool:
    try:
        r = await client.get(f"{model['base_url']}/models", headers=backend_headers(model), timeout=2.0)
        return r.status_code == 200
    except httpx.HTTPError:
        return False


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/v1/models")
async def models(request: Request):
    if not authorized(request):
        return error(401, "invalid API key")
    up = dict(zip(MODELS, await asyncio.gather(*(is_up(m) for m in MODELS.values()))))
    names = [n for n, ok in up.items() if ok] + [a for a, n in ALIASES.items() if up.get(n)]
    return {"object": "list", "data": [{"id": n, "object": "model"} for n in names]}


@app.post("/v1/{path:path}")
async def proxy(path: str, request: Request):
    if not authorized(request):
        return error(401, "invalid API key")
    try:
        payload = json.loads(await request.body())
        requested = payload["model"]
    except (ValueError, KeyError, TypeError):
        return error(400, "request body must be JSON with a 'model' field")
    name = ALIASES.get(requested, requested)
    model = MODELS.get(name)
    if model is None:
        return error(404, f"unknown model or alias '{requested}'; known: {sorted(ALIASES) + sorted(MODELS)}")
    payload["model"] = model.get("served_name", name)
    t0 = time.time()
    req = client.build_request(
        "POST", f"{model['base_url']}/{path}", content=json.dumps(payload), headers=backend_headers(model),
    )
    try:
        resp = await client.send(req, stream=True)
    except httpx.HTTPError as e:
        log(requested=requested, model=name, status=502, seconds=round(time.time() - t0, 1), error=type(e).__name__)
        return error(502, f"backend for '{requested}' is not reachable: {type(e).__name__}")
    log(requested=requested, model=name, status=resp.status_code, stream=bool(payload.get("stream")),
        seconds_to_first_byte=round(time.time() - t0, 1))
    ctype = resp.headers.get("content-type", "application/json")
    if payload.get("stream"):
        return StreamingResponse(resp.aiter_raw(), status_code=resp.status_code,
                                 media_type=ctype, background=BackgroundTask(resp.aclose))
    content = await resp.aread()
    await resp.aclose()
    return Response(content, status_code=resp.status_code, media_type=ctype)
