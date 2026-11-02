"""Numeric output: no judge needed. 1.0 for an exact score, 0.0 when 25 or more points off."""
import re


def eval_fn(expected: str, actual: str) -> float:
    match = re.search(r"\d+", actual)
    if not match:
        return 0.0
    return max(0.0, 1 - abs(int(match.group()) - int(expected)) / 25)
