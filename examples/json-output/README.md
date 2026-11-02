# Answer is a JSON object

**The call** (`demo/booking`): your app sends a booking email, and your current model pulls out the
details as JSON.

**The CSV.** Put the JSON you expect in the `demo/booking` column. You could write it like this:

| input | demo/booking |
|---|---|
| Hi, a table for 4 this Friday at 8pm please, name is Ana Ruiz. | `{"name": "Ana Ruiz", "people": 4, "day": "Friday", "time": "20:00"}` |
| Can we come Sunday lunch, around 1? Two of us. Tom | `{"name": "Tom", "people": 2, "day": "Sunday", "time": "13:00"}` |

Use the same field names your app reads. If a field doesn't matter to you, leave it out
and we won't check it.

**How we score it:** field by field. Each field the candidate model gets right counts; 3 out of 4 fields
right scores 0.75. If one field matters more (a wrong time is worse than a misspelt name), tell us.
