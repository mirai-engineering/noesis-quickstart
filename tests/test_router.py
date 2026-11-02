import json
import os

os.environ["NOESIS_API_KEY"] = "k"

import httpx  # noqa: E402
import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from router import main  # noqa: E402

AUTH = {"authorization": "Bearer k"}


@pytest.fixture
def backend(monkeypatch):
    """A fake model server behind the router; `seen` collects what the router forwarded."""
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if request.url.path.endswith("/models"):
            return httpx.Response(200, json={"data": []})
        return httpx.Response(200, json={"choices": [{"message": {"content": "hi"}}]})

    monkeypatch.setattr(main, "client", httpx.AsyncClient(transport=httpx.MockTransport(handler)))
    monkeypatch.setattr(main, "MODELS", {"small": {"base_url": "http://small/v1", "served_name": "small-served"}})
    monkeypatch.setattr(main, "ALIASES", {"demo/write": "small"})
    return seen


def post(model):
    return TestClient(main.app).post("/v1/chat/completions", headers=AUTH, content=json.dumps({"model": model}))


def test_alias_is_resolved_and_rewritten(backend):
    assert post("demo/write").status_code == 200
    assert backend[0].url == "http://small/v1/chat/completions"
    assert json.loads(backend[0].content)["model"] == "small-served"


def test_model_name_works_directly(backend):
    assert post("small").status_code == 200


def test_unknown_is_404(backend):
    assert post("zzz").status_code == 404


def test_models_requires_key():
    assert TestClient(main.app).get("/v1/models").status_code == 401


def test_models_lists_aliases_and_models_that_are_up(backend):
    r = TestClient(main.app).get("/v1/models", headers=AUTH)
    assert [m["id"] for m in r.json()["data"]] == ["small", "demo/write"]


def test_backend_down_is_502(monkeypatch, backend):
    def boom(request):
        raise httpx.ConnectError("down")

    monkeypatch.setattr(main, "client", httpx.AsyncClient(transport=httpx.MockTransport(boom)))
    assert post("demo/write").status_code == 502
