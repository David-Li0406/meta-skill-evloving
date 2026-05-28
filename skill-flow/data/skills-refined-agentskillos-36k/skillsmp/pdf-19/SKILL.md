---
name: pdf
description: Use when extracting, creating, merging, splitting, or analyzing PDFs, or when filling PDF forms programmatically.
allowed-tools: ["shell", "read_file", "write_file"]
metadata:
  short-description: PDF processing and form handling
---

# PDF Processing Guide

## Preflight

- Prefer Python libraries if available (`pypdf`, `pdfplumber`, `reportlab`).
- If libraries are missing, fall back to CLI tools (`pdftotext`, `qpdf`, `pdftk`).
- For forms, read `forms.md` first.

## Overview

This guide covers essential PDF operations. This skill includes `reference.md` and `forms.md` in the same directory for advanced features and form handling.

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
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

#### Split PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

### pdfplumber - Text and Table Extraction

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

### reportlab - Create PDFs

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter
c.drawString(100, height - 100, "Hello World!")
c.save()
```

## Command-Line Tools

### pdftotext
```bash
pdftotext input.pdf output.txt
pdftotext -layout input.pdf output.txt
```

### qpdf
```bash
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf output.pdf --rotate=+90:1
```

## Quick Reference

| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Create PDFs | reportlab | Canvas or Platypus |
| Command line merge | qpdf | `qpdf --empty --pages ...` |
| Fill PDF forms | pypdf / pdf-lib | See `forms.md` |

## Next Steps

- For advanced usage, see `reference.md`
- For forms, follow `forms.md`

## Arguments

Target: ${ARGUMENTS}
