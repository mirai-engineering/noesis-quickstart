# Answer is a JSON object

This example shows how to fill in the two CSV files you send us, `data/demo.csv` (examples) and
`data/steps.csv` (prompts), when your answer is JSON. See the [main README](../../README.md) for the basics.

Compared with the restaurant app, only one thing changes: **what your app expects back** is JSON, not one word or a
number. So the answer you write is JSON too, and we score it field by field.

**The call** (`demo/booking`): your app sends a booking email, and your current model pulls out the
details as JSON.

## `data/demo.csv`

Put the JSON you expect in the `demo/booking` column. You could write it like this:

| input | demo/booking |
|---|---|
| Hi, a table for 4 this Friday at 8pm please, name is Ana Ruiz. | `{"name": "Ana Ruiz", "people": 4, "day": "Friday", "time": "20:00"}` |
| Can we come Sunday lunch, around 1? Two of us. Tom | `{"name": "Tom", "people": 2, "day": "Sunday", "time": "13:00"}` |

Saved as a file, with the JSON's quotes doubled (a spreadsheet tool does this for you):

```csv
input,demo/booking
"Hi, a table for 4 this Friday at 8pm please, name is Ana Ruiz.","{""name"": ""Ana Ruiz"", ""people"": 4, ""day"": ""Friday"", ""time"": ""20:00""}"
"Can we come Sunday lunch, around 1? Two of us. Tom","{""name"": ""Tom"", ""people"": 2, ""day"": ""Sunday"", ""time"": ""13:00""}"
```

Use the same field names your app reads. If a field doesn't matter to you, leave it out and we won't
check it.

## `data/steps.csv`

| step | alias | prompt | receives | settings |
|---|---|---|---|---|
| 1 | `demo/booking` | Read this booking email. Reply with JSON only: name, people, day, time (24h). | input | temperature=0 |

If your app asks for JSON with a schema (a "response format" or "structured output" setting), put that
in `settings` too: candidate models must get the same constraint.

## Scoring

**How we score it:** field by field. Each field the candidate model gets right counts; 3 out of 4
fields right scores 0.75. If one field matters more (a wrong time is worse than a misspelt name), tell us.
