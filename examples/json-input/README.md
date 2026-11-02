# Input is a JSON record

This example shows how to fill in the two CSV files you send us, `data/demo.csv` (examples) and
`data/steps.csv` (prompts), when your input is JSON. See the [main README](../../README.md) for the basics.

Compared with the restaurant app, only one thing changes: **what your app sends** is JSON, not a sentence. The answer is
still a plain number, so it's scored the usual way.

**The call** (`demo/loyalty`): your app sends a customer's history as JSON, and your current model rates
how likely they are to come back, from 0 to 100.

## `data/demo.csv`

Paste the JSON into the `input` cell as it is. You could write it like this:

| input | demo/loyalty |
|---|---|
| `{"visits": 12, "last_visit": "2026-10-20", "avg_spend": 45, "last_review": "Great as always"}` | 90 |
| `{"visits": 1, "last_visit": "2025-03-02", "avg_spend": 18, "last_review": "Too slow"}` | 10 |

Saved as a file, the JSON gets wrapped in quotes and its own quotes are doubled. A spreadsheet tool
does this for you; if you write the file by hand or with a script, it looks like this:

```csv
input,demo/loyalty
"{""visits"": 12, ""last_visit"": ""2026-10-20"", ""avg_spend"": 45, ""last_review"": ""Great as always""}",90
"{""visits"": 1, ""last_visit"": ""2025-03-02"", ""avg_spend"": 18, ""last_review"": ""Too slow""}",10
```

Send the same JSON your app sends, with the same fields. If your app builds it from several sources,
send what it looks like at the moment it reaches the model.

## `data/steps.csv`

| step | alias | prompt | receives | settings |
|---|---|---|---|---|
| 1 | `demo/loyalty` | Rate from 0 to 100 how likely this customer is to come back. Reply with the number only. | input | temperature=0 |

## Scoring

**How far off is still fine?** Tell us, as with the stars: for example, within 10 points.

**How we score it:** like the stars. Exact scores 1, and the score drops as the answer gets further off.
