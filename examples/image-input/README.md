# Input is an image

**The call** (`demo/receipt`): your app sends a photo of a receipt, and your current model reads the total.

**The CSV.** Images don't fit in a CSV cell, so put the images in a folder and write each file name
in `input`. Send the folder together with the CSV. You could write it like this:

| input | receipt |
|---|---|
| images/receipt-001.jpg | 23.50 |
| images/receipt-002.jpg | 8.90 |

    receipt.csv
    images/
      receipt-001.jpg
      receipt-002.jpg

Send the images as your app sends them: same size, same quality. If your app also sends text with the
image (a question, instructions), that text is part of your prompt; send it with your prompts.

**How far off is still fine?** For a total, probably nothing: it's right or wrong. Tell us.

**How we score it:** like the stars, with your tolerance. With none, the total must match exactly.
