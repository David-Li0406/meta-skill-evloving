---
name: pdf
description: Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When Claude needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale.
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Processing Guide

## Overview

This guide covers essential PDF processing operations. If you need to fill out a PDF form, read forms.md and follow its instructions.

**Prefer command-line tools and existing scripts over writing new Python code.** Only write a custom script if no existing tool covers the task.

## Form Filling

For filling PDF forms, follow the instructions in **forms.md**. It provides ready-made scripts for both fillable and non-fillable forms.

## Command-Line Tools (Preferred)

Use these directly — no dependencies to install.

### Text Extraction (pdftotext / poppler-utils)
```bash
# Extract text
pdftotext input.pdf output.txt

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt  # Pages 1-5

# Extract text with bounding box coordinates (for structured data)
pdftotext -bbox-layout document.pdf output.xml
```

### Merge and Split (qpdf)
```bash
# Merge PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split specific pages
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf

# Extract specific pages from multiple files
qpdf --empty --pages doc1.pdf 1-3 doc2.pdf 5-7 -- combined.pdf

# Split into individual pages
qpdf --split-pages input.pdf output_%02d.pdf
```

### Rotate Pages (qpdf)
```bash
qpdf input.pdf output.pdf --rotate=+90:1  # Rotate page 1 by 90 degrees
```

### Password Operations (qpdf)
```bash
# Add password protection
qpdf --encrypt user_pass owner_pass 256 -- input.pdf encrypted.pdf

# Remove password
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### Extract Images (pdfimages / poppler-utils)
```bash
# Extract all images as JPEG
pdfimages -j input.pdf output_prefix

# List image info without extracting
pdfimages -list document.pdf

# Extract in original format
pdfimages -all document.pdf images/img
```

### Convert to Images (pdftoppm / poppler-utils)
```bash
# Convert to PNG at 300 DPI
pdftoppm -png -r 300 document.pdf output_prefix

# Convert specific pages
pdftoppm -png -r 300 -f 1 -l 3 document.pdf pages
```

### PDF Repair (qpdf)
```bash
# Check PDF structure
qpdf --check input.pdf

# Linearize for web streaming
qpdf --linearize input.pdf optimized.pdf
```

## Existing Scripts (run from this skill's directory)

These scripts handle form-related operations. Dependencies are managed automatically by uv.

| Script | Purpose | Usage |
|--------|---------|-------|
| `check_fillable_fields.py` | Check if PDF has fillable form fields | `uv run scripts/check_fillable_fields.py <file.pdf>` |
| `extract_form_field_info.py` | Extract form field metadata to JSON | `uv run scripts/extract_form_field_info.py <input.pdf> <output.json>` |
| `convert_pdf_to_images.py` | Convert PDF pages to PNG images | `uv run scripts/convert_pdf_to_images.py <file.pdf> <output_dir>` |
| `fill_fillable_fields.py` | Fill fillable form fields | `uv run scripts/fill_fillable_fields.py <input.pdf> <values.json> <output.pdf>` |
| `fill_pdf_form_with_annotations.py` | Fill non-fillable forms via annotations | `uv run scripts/fill_pdf_form_with_annotations.py <input.pdf> <fields.json> <output.pdf>` |
| `create_validation_image.py` | Create bounding box validation images | `uv run scripts/create_validation_image.py <page_num> <fields.json> <input_img> <output_img>` |
| `check_bounding_boxes.py` | Validate bounding boxes don't overlap | `uv run scripts/check_bounding_boxes.py <fields.json>` |

## Writing Custom Scripts (only when needed)

If no existing tool covers the task, write a Python script with uv inline metadata so dependencies are installed automatically. **Never use `pip install`.**

```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pypdf>=4.0.0",
#     # add other deps as needed
# ]
# ///

# your code here
```

Run with: `uv run script.py`

### Available Python libraries

| Library | Use case | Dependency string |
|---------|----------|-------------------|
| pypdf | Read/write/merge/split PDFs, metadata, encryption | `"pypdf>=4.0.0"` |
| pdfplumber | Text extraction with layout, table extraction | `"pdfplumber>=0.10.0"` |
| reportlab | Create PDFs from scratch (text, tables, graphics) | `"reportlab>=4.0.0"` |
| pypdfium2 | Fast PDF rendering to images | `"pypdfium2>=4.0.0"` |
| pdf2image | Convert PDF pages to PIL images (needs poppler) | `"pdf2image>=1.16.0"` |
| pytesseract | OCR for scanned PDFs (needs tesseract installed) | `"pytesseract>=0.3.10"` |
| Pillow | Image manipulation | `"Pillow>=10.0.0"` |

For code examples using these libraries, see **reference.md**.

## Quick Reference

| Task | Best approach |
|------|---------------|
| Extract text | `pdftotext` (command line) |
| Extract tables | pdfplumber (custom script) |
| Merge PDFs | `qpdf --empty --pages ...` (command line) |
| Split PDFs | `qpdf --split-pages` or `--pages` (command line) |
| Rotate pages | `qpdf --rotate` (command line) |
| Create PDFs | reportlab (custom script) |
| Convert to images | `pdftoppm` (command line) |
| Extract images | `pdfimages` (command line) |
| OCR scanned PDFs | pytesseract + pdf2image (custom script) |
| Password protect | `qpdf --encrypt` (command line) |
| Fill PDF forms | Existing scripts (see forms.md) |
