"""Score a CSV: first your baseline `actual` column, then each candidate model through the endpoint.

    uv run python -m tools.replay demo/score data/score.csv
    uv run python -m tools.replay demo/write data/write.csv --models fake-small

Without --models it tries every model the endpoint lists (aliases excluded).
"""
import argparse
import csv
import time
from statistics import mean
from typing import Callable

from app.steps import STEPS
from evals import EVALS


def read_rows(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# TODO: hand the search to agentopt (same eval_fn shape) instead of looping over every model.
def replay(alias: str, rows: list[dict], models: list[str], complete: Callable[[str, str, str], str]) -> dict:
    """{name: (mean score, seconds)}; `complete(model, system, user)` returns the model's text."""
    eval_fn, system = EVALS[alias], STEPS[alias].system
    results = {"baseline": (mean(eval_fn(r["expected"], r["actual"]) for r in rows), 0.0)}
    for model in models:
        t0 = time.time()
        scores = [eval_fn(r["expected"], complete(model, system, r["input"])) for r in rows]
        results[model] = (mean(scores), time.time() - t0)
    return results


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("alias")
    p.add_argument("csv")
    p.add_argument("--models", nargs="*")
    args = p.parse_args()

    from app.client import client  # imported here so the unit tests need no endpoint

    def complete(model: str, system: str, user: str) -> str:
        r = client.chat.completions.create(
            model=model, temperature=0,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        )
        return r.choices[0].message.content.strip()

    models = args.models or [m.id for m in client.models.list().data if "/" not in m.id]
    rows = read_rows(args.csv)
    print(f"{args.alias}: {len(rows)} rows")
    print(f"{'model':<28}{'score':>8}{'seconds':>10}")
    for name, (score, seconds) in replay(args.alias, rows, models, complete).items():
        print(f"{name:<28}{score:>8.2f}{seconds:>10.1f}")


if __name__ == "__main__":
    main()
