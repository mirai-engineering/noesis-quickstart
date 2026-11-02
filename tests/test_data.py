from app.client import capture
from evals import EVALS
from tools.replay import read_rows, replay
from tools.validate import validate


def test_shipped_csvs_are_valid():
    assert validate("data/score.csv") == [] and validate("data/write.csv") == []


def test_validate_names_the_problem(tmp_path):
    f = tmp_path / "bad.csv"
    f.write_text("id,input,expected,actual\n1,x,,y\n1,a,b,c\n")
    assert validate(str(f)) == ["row 2: 'expected' is empty", "row 3: duplicate id 1"]
    f.write_text("id,input\n1,x\n")
    assert "missing: expected, actual" in validate(str(f))[0]


def test_score_eval():
    fn = EVALS["demo/score"]
    assert fn("80", "80") == 1.0 and fn("80", "no number") == 0.0 and fn("80", "55") == 0.0


def test_write_eval():
    fn = EVALS["demo/write"]
    assert fn("Rust", "Hi Jonas, your Rust work is great.") == 1.0
    assert fn("Rust", "I hope this finds you well. Rust.") < 1.0


def test_baseline_is_not_perfect():
    """The shipped data shows a baseline with room to improve."""
    for alias, path in (("demo/score", "data/score.csv"), ("demo/write", "data/write.csv")):
        assert 0.5 < replay(alias, read_rows(path), [], None)["baseline"][0] < 1.0


def test_replay_scores_each_model():
    rows = read_rows("data/score.csv")
    out = replay("demo/score", rows, ["perfect"], lambda m, s, u: next(r["expected"] for r in rows if r["input"] == u))
    assert out["perfect"][0] == 1.0


def test_capture_appends_in_the_expected_format(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    capture("demo/score", "p1", "70")
    capture("demo/score", "p2", "55")
    assert (tmp_path / "captures/demo_score.csv").read_text().splitlines() == [
        "id,input,expected,actual", "1,p1,,70", "2,p2,,55"]
