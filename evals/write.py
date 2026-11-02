"""Free-text output: you decide what good means. Here, three checks you could do by eye.

`expected` holds the skill the message must mention. Swap this body for an LLM judge or a human
score lookup if "good" is harder to write down; Noesis only needs a number from 0 to 1.
"""
MAX_WORDS = 60
FILLERS = ("hope this finds you well", "i came across your profile")


def eval_fn(expected: str, actual: str) -> float:
    text = actual.lower()
    checks = [
        expected.lower() in text,
        len(actual.split()) <= MAX_WORDS,
        not any(f in text for f in FILLERS),
    ]
    return sum(checks) / len(checks)
