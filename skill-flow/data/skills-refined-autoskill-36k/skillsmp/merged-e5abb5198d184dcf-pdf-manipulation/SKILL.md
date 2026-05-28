---
name: pdf-manipulation
description: Use this skill for comprehensive PDF manipulation, including extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms.
---

# PDF Processing Guide

## Overview

This guide covers essential PDF processing operations using Python libraries and command-line tools. For advanced features, JavaScript libraries, and detailed examples, see reference.md. If you need to fill out a PDF form, read forms.md and follow its instructions.

## Quick Start

```python
from pypdf import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Python Libraries

### pypdf - Basic Operations

#### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["<input_pdf1>", "<input_pdf2>", "<input_pdf3>"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("<output_merged_pdf>", "wb") as output:
    writer.write(output)
```

#### Split PDF
```python
reader = PdfReader("<input_pdf>")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

#### Extract Metadata
```python
reader = PdfReader("<input_pdf>")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

#### Rotate Pages
```python
reader = PdfReader("<input_pdf>")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
writer.add_page(page)

with open("<output_rotated_pdf>", "wb") as output:
    writer.write(output)
```

### pdfplumber - Text and Table Extraction

#### Extract Text with Layout
```python
import pdfplumber

with pdfplumber.open("<input_pdf>") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### Extract Tables
```python
with pdfplumber.open("<input_pdf>") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

#### Advanced Table Extraction
```python
import pandas as pd

with pdfplumber.open("<input_pdf>") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # Check if table is not empty
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Combine all tables
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("<output_excel>", index=False)
```

### reportlab - Create PDFs

#### Basic PDF Creation
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("<output_pdf>", pagesize=letter)
width, height = letter

# Add text
c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")

# Save
c.save()
```

## Command-Line Tools

### pdftotext (poppler-utils)
```bash
# Extract text
pdftotext <input_pdf> <output_txt>

# Extract text preserving layout
pdftotext -layout <input_pdf> <output_txt>

# Extract specific pages
pdftotext -f 1 -l 5 <input_pdf> <output_txt>  # Pages 1-5
```

### qpdf
```bash
# Merge PDFs
qpdf --empty --pages <input_pdf1> <input_pdf2> -- <output_merged_pdf>

# Split pages
qpdf <input_pdf> --pages . 1-5 -- <output_pages1-5.pdf>
```

### pdftk (if available)
```bash
# Merge
pdftk <input_pdf1> <input_pdf2> cat output <output_merged_pdf>

# Split
pdftk <input_pdf> burst
```

## Common Tasks

### Extract Text from Scanned PDFs
```python
# Requires: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path('<scanned_pdf>')

# OCR each page
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

### Add Watermark
```python
from pypdf import PdfReader, PdfWriter

# Create watermark (or load existing)
watermark = PdfReader("<watermark_pdf>").pages[0]

# Apply to all pages
reader = PdfReader("<input_pdf>")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("<output_watermarked_pdf>", "wb") as output:
    writer.write(output)
```

### Password Protection
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("<input_pdf>")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# Add password
writer.encrypt("<user_password>", "<owner_password>")

with open("<output_encrypted_pdf>", "wb") as output:
    writer.write(output)
```

## Quick Reference

| Task               | Best Tool                       | Command/Code               |
| ------------------ | ------------------------------- | -------------------------- |
| Merge PDFs         | pypdf                           | `writer.add_page(page)`    |
| Split PDFs         | pypdf                           | One page per file          |
| Extract text       | pdfplumber                      | `page.extract_text()`      |
| Extract tables     | pdfplumber                      | `page.extract_tables()`    |
| Create PDFs        | reportlab                       | Canvas or Platypus         |
| Command line merge | qpdf                            | `qpdf --empty --pages ...` |
| OCR scanned PDFs   | pytesseract                     | Convert to image first     |
| Fill PDF forms     | pdf-lib or pypdf (see forms.md) | See forms.md               |

## Next Steps

- For advanced pypdfium2 usage, see reference.md
- For JavaScript libraries (pdf-lib), see reference.md
- If you need to fill out a PDF form, follow the instructions in forms.md
- For troubleshooting guides, see reference.md