# Other kinds of input and answer

In the main README, the restaurant app is simple: a sentence goes in (a review), and a short answer
comes out (a word, a number, a reply). Real apps often send more than a sentence, or expect more than
a word back. The question is then: how does that fit in the two CSV files you send us,
`data/demo.csv` and `data/steps.csv`?

These three made-up cases answer that. Each one is a small app with a single LLM call, and changes only
one thing compared with the restaurant app. Nothing here runs; they only show how to fill in the files.

## When what your app sends is JSON

Say your app sends the model a customer's history as a JSON record, and asks how likely that customer
is to come back, from 0 to 100. The answer is still a plain number, so nothing changes for the answer
or the scoring. The only question is how to put a whole JSON record in one CSV cell. Short answer:
paste it as it is.

See [`json-input/`](json-input/).

## When what you expect back is JSON

Now the other way round: your app sends a plain booking email, and the model answers with the details
as JSON (name, number of people, day, time). Here the answer you write in `data/demo.csv` is JSON too,
and we score it field by field: getting 3 of 4 fields right scores 0.75.

See [`json-output/`](json-output/).

## When what your app sends is an image

Your app sends a photo of a receipt and asks for the total. A photo doesn't fit in a CSV cell, so you
put the photos in a folder and write each file name in the cell instead. The answer is a number, as
usual.

See [`image-input/`](image-input/).

## What stays the same

Whatever your app sends or expects, it's always the same two files:

- **`data/demo.csv`**, one row per example: what goes into your app (`input`), then the answer you
  expect from each LLM call, one column per call.
- **`data/steps.csv`**, one row per LLM call: its prompt, what it receives, and its settings.

The details are in the [main README](../README.md).
