"""The integration, in full: an OpenAI client pointed at Noesis, and the alias as the model.

Set CAPTURE=1 to append every call to captures/<alias>.csv, which is the file format Noesis
asks for (you fill in `expected`).
"""
import csv
import os
from pathlib import Path

from openai import OpenAI

from app.steps import Step

client = OpenAI(
    base_url=os.environ.get("NOESIS_BASE_URL", "http://localhost:8000/v1"),
    api_key=os.environ.get("NOESIS_API_KEY", "demo-key"),
)
CAPTURES = Path("captures")


def capture(alias: str, user: str, actual: str) -> None:
    path = CAPTURES / f"{alias.replace('/', '_')}.csv"
    path.parent.mkdir(exist_ok=True)
    new = not path.exists()
    next_id = 1 if new else sum(1 for _ in csv.reader(path.open(newline=""))) # header line = rows so far + 1
    with path.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["id", "input", "expected", "actual"])
        w.writerow([next_id, user, "", actual])


def chat(step: Step, user: str) -> str:
    resp = client.chat.completions.create(
        model=step.alias,  # the only change vs. calling a provider directly
        messages=[{"role": "system", "content": step.system}, {"role": "user", "content": user}],
        temperature=0,
    )
    out = resp.choices[0].message.content.strip()
    if os.environ.get("CAPTURE"):
        capture(step.alias, user, out)
    return out
