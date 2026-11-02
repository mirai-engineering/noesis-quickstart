# Other kinds of input and answer

The restaurant app in the main README uses one sentence in and a short answer out. Real apps often send
more. These are made-up cases, only to show how to fill in the CSV. Nothing here runs.

| Case | Your app sends | It expects back |
|---|---|---|
| [`json-input/`](json-input/) | a JSON record (a customer's history) | a number |
| [`json-output/`](json-output/) | an email | a JSON object (the booking details) |
| [`image-input/`](image-input/) | a photo (a receipt) | a number |

The rule stays the same: one CSV for your app, one row per example: `input`, then one column per LLM
call with the answer you expect. Each case here is an app with a single call, so a single column.
