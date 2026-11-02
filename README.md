# noesis-quickstart

The smallest example of using a Noesis endpoint: change two things in your app, hand over a CSV,
and get a scored comparison of models. The demo app has two LLM calls and runs with no GPU and no keys.

## Try it (2 minutes)

    uv sync
    export NOESIS_API_KEY=demo-key
    uv run uvicorn tools.fake_backend:app --port 9000 &     # stand-in model server
    uv run uvicorn router.main:app --port 8000 &            # the router: aliases -> backends
    uv run python -m app.main "Ana Ruiz. Staff engineer at Lumio; 9 years of Go and Postgres."
    uv run python -m tools.replay demo/score data/score.csv

## What you do, in three steps

**1. Point your app at Noesis.** Find where you build your LLM client and change two things:
`base_url` and the `model`. Each place in your app that calls an LLM gets its own alias.

```python
client = OpenAI(base_url="https://<noesis-endpoint>/v1", api_key=NOESIS_API_KEY)
client.chat.completions.create(model="demo/score", messages=[...])   # was: model="gemini-2.5-flash"
```

This is the whole integration (`app/client.py`). It works the same with LangChain, LangGraph or any
framework that lets you set an OpenAI base URL. Set `CAPTURE=1` and your app writes the CSV below for you.

**2. Give us your data, one CSV per alias** (`data/score.csv`, `data/write.csv`):

| column | meaning |
|---|---|
| `id` | any unique value |
| `input` | what your app sent to the model |
| `expected` | what a good answer looks like (an answer, or the facts it must contain) |
| `actual` | what your current model answered |

UTF-8, one header row, no empty cells. Check yours with `uv run python -m tools.validate file.csv`.

**3. Say what good means: one function** `eval_fn(expected, actual) -> 0..1` per alias (`evals/`).
- Numeric answers need no judge (`evals/score.py`).
- Free text is up to you (`evals/write.py`): a few checks, an LLM judge, or scores a person gave.
  The better this is, the better the result.

`tools/replay.py` then scores your `actual` column and every candidate model on your data. Noesis
optimizes against the score you give it; it does not decide what good is.

## Layout

    app/      the demo app: two call sites (steps.py), the integration (client.py)
    data/     example CSVs (made up)
    evals/    one scoring function per alias
    router/   FastAPI router: alias -> {base_url, model}; config.toml is the only thing to edit
    tools/    validate.py, replay.py, fake_backend.py

## Moving servers

All backends are in `router/config.toml`. Moving from one GPU provider to another, or adding one,
means editing a `base_url`. Your app keeps using the same aliases.

## Not done yet

- **Real backends:** `router/config.toml` points at the fake server. The GCP vLLM servers need a public path
  from wherever the router runs, then a `[models.*]` entry each (Modal later is the same).
- **Optimizer:** `tools/replay.py` is a plain loop over candidate models. Wiring in `agentopt` is next; it takes
  the same `eval_fn(expected, actual)`.
- **Per-client keys:** the router has one `NOESIS_API_KEY`.

## Tests

    uv run pytest
