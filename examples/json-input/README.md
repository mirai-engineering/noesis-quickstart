# Input is a JSON record

**The call** (`demo/loyalty`): your app sends a customer's history as JSON, and your current model rates
how likely they are to come back, from 0 to 100.

**The CSV.** Paste the JSON into the `input` cell as it is; your spreadsheet tool adds the quoting.
You could write it like this:

| id | input | expected |
|---|---|---|
| 1 | `{"visits": 12, "last_visit": "2026-10-20", "avg_spend": 45, "last_review": "Great as always"}` | 90 |
| 2 | `{"visits": 1, "last_visit": "2025-03-02", "avg_spend": 18, "last_review": "Too slow"}` | 10 |

Send the same JSON your app sends, with the same fields. If your app builds it from several sources,
send what it looks like at the moment it reaches the model.

**How far off is still fine?** Tell us, as with the stars: for example, within 10 points.

**How we score it:** like the stars. Exact scores 1, and the score drops as the answer gets further off.
