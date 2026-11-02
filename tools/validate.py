"""Check an eval CSV against the format Noesis asks for.

    uv run python -m tools.validate data/score.csv

Columns, in any order: id, input, expected, actual. UTF-8, one header row, no empty cells.
"""
import csv
import sys

COLUMNS = ("id", "input", "expected", "actual")


def validate(path: str) -> list[str]:
    try:
        f = open(path, newline="", encoding="utf-8")
    except OSError as e:
        return [str(e)]
    with f:
        try:
            reader = csv.DictReader(f)
            missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
            if missing:
                return [f"header is missing: {', '.join(missing)} (expected {', '.join(COLUMNS)})"]
            errors, seen = [], set()
            for n, row in enumerate(reader, start=2):  # row 1 is the header
                errors += [f"row {n}: '{c}' is empty" for c in COLUMNS if not (row.get(c) or "").strip()]
                if None in row:
                    errors.append(f"row {n}: more cells than the header; quote text that contains commas")
                if row["id"] in seen:
                    errors.append(f"row {n}: duplicate id {row['id']}")
                seen.add(row["id"])
            return errors or ([] if seen else ["no data rows"])
        except UnicodeDecodeError:
            return ["file is not UTF-8"]


if __name__ == "__main__":
    problems = validate(sys.argv[1])
    print("\n".join(problems) if problems else "ok")
    sys.exit(1 if problems else 0)
