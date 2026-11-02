"""The demo app: step 1 scores a profile, step 2 writes to the ones that pass.

    uv run python -m app.main "Ana Ruiz. Staff engineer at Lumio; 9 years of Go and Postgres."
"""
import re
import sys

from app.client import chat
from app.steps import SCORE, WRITE

THRESHOLD = 70


def run(profile: str) -> dict:
    match = re.search(r"\d+", chat(SCORE, profile))
    score = int(match.group()) if match else 0
    message = chat(WRITE, profile) if score >= THRESHOLD else None
    return {"score": score, "message": message}


if __name__ == "__main__":
    print(run(" ".join(sys.argv[1:])))
