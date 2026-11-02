"""A stand-in model server so the demo runs with no GPU and no keys.

    uv run uvicorn tools.fake_backend:app --port 9000

It answers every scoring request with 72 and every writing request with a generic message.
"""
from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/v1/models")
async def models():
    return {"object": "list", "data": [{"id": "fake-small", "object": "model"}]}


@app.post("/v1/chat/completions")
async def chat(request: Request):
    body = await request.json()
    system, user = body["messages"][0]["content"], body["messages"][-1]["content"]
    if "0 to 100" in system:
        text = "72"
    else:
        text = (f"Hi {user.split('.')[0].split()[0]}, your background caught our eye. We are hiring a "
                "senior backend engineer and would love to talk. Open to a short chat?")
    return {"id": "fake", "object": "chat.completion", "model": body["model"],
            "choices": [{"index": 0, "finish_reason": "stop", "message": {"role": "assistant", "content": text}}],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}}
