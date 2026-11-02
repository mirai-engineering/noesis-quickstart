"""The two call sites of the demo app. Each has one alias; the alias is what Noesis optimizes."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Step:
    alias: str
    system: str


SCORE = Step(
    "demo/score",
    "You screen candidates for a senior backend engineer role. "
    "Reply with only an integer from 0 to 100: how well the profile fits.",
)
WRITE = Step(
    "demo/write",
    "Write a first-contact message of at most 60 words to the person described. "
    "Use their first name and mention their most relevant skill. No filler openers. Reply with the message only.",
)
STEPS = {s.alias: s for s in (SCORE, WRITE)}
