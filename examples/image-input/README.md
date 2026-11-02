# Input is an image

This example shows how to fill in the two CSV files you send us, `data/demo.csv` (examples) and
`data/steps.csv` (prompts), when your input is an image. See the [main README](../../README.md) for the basics.

Compared with the restaurant app, only one thing changes: **what your app sends** is a photo. Images don't fit in a CSV
cell, so the `input` cell holds the image's file name instead.

**The call** (`demo/receipt`): your app sends a photo of a receipt, and your current model reads the total.

## `data/demo.csv`

Put the images in a folder next to the CSV and write each file name in `input`. You could write it
like this:

| input | demo/receipt |
|---|---|
| images/receipt-001.jpg | 23.50 |
| images/receipt-002.jpg | 8.90 |

Send the folder together with the files:

    data/
      demo.csv
      steps.csv
      images/
        receipt-001.jpg
        receipt-002.jpg

Send the images as your app sends them: same size, same quality.

## `data/steps.csv`

| step | alias | prompt | receives | settings |
|---|---|---|---|---|
| 1 | `demo/receipt` | What is the total on this receipt? Reply with the number only. | input | temperature=0 |

If your app sends text along with the image (a question, instructions), that text is the prompt: write
it here.

## Scoring

**How far off is still fine?** For a total, probably nothing: it's right or wrong. Tell us.

**How we score it:** like the stars, with your tolerance. With none, the total must match exactly.
