"""One eval_fn(expected, actual) -> 0..1 per alias. This is the shape `agentopt` takes too."""
from evals import score, write

EVALS = {"demo/score": score.eval_fn, "demo/write": write.eval_fn}
