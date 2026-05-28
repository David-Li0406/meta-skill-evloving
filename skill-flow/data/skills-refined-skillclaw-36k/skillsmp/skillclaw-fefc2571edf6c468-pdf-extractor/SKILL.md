---
name: pdf-extractor
description: Use this skill to extract text, tables, and images from PDF files, converting them into organized, searchable formats.
---

# PDF Extractor Skill

## Purpose

This skill is designed to extract structured content (text, tables, images) from PDF files into organized, searchable formats.

## Grounding Checkpoint

Before executing, VERIFY:

- [ ] PDF file exists and is readable (`file <path>` confirms PDF format)
- [ ] PDF is not corrupted (`pdfinfo <path>` returns metadata)
- [ ] Password known if encrypted
- [ ] Output directory is writable
- [ ] Required tools available (pdfplumber, pytesseract for OCR)

**DO NOT proceed without verification. Inspect PDF metadata first.**

## Uncertainty Escalation

ASK USER instead of guessing when:

- PDF appears to be scanned (needs OCR) but OCR tools unavailable
- Multiple table formats detected - unclear which parser to use
- Password-protected but no password provided
- Image extraction quality unclear (resolution, format preferences)
- Language detection needed for OCR

**NEVER assume PDF structure without inspection.**

## Context Scope

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | Target PDF, extraction options, output path | Other PDF files |
| PERIPHERAL | Similar PDF structure examples | Unrelated documents |
| DISTRACTOR | Previous extraction attempts | Other file formats |

## Workflow Steps

### Step 1: Inspect PDF

```bash
# Check file type
file document.pdf

# Get PDF metadata
pdfinfo document.pdf

# Check page count
pdfinfo document.pdf | grep Pages

# Check if encrypted
pdfinfo document.pdf | grep Encrypted
```

### Step 2: Determine Extraction Strategy

| PDF Type | Detection | Strategy |
|----------|-----------|----------|
| Text-based | `pdftotext` produces readable text | Direct extraction |
| Scanned/Image | `pdftotext` produces empty/garbled | OCR required |
| Mixed | Some pages text, some images | Hybrid approach |
| Tables | Visual grid patterns | Table extraction mode |
| Forms | Interactive fields | Form field extraction |

### Step 3: Execute Extraction

**Option A: Using Python Libraries**

#### Basic Text Extraction
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### Extract Tables
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            print(table)
```

#### Get Metadata
```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
metadata = reader.metadata
print(f"Title: {metadata.title}")
print(f"Author: {metadata.author}")
print(f"Pages: {len(reader.pages)}")
```

## Requirements
Install the required packages:
```bash
pip install pypdf pdfplumber
```

## Notes
- For scanned PDFs, consider using OCR libraries like `pytesseract`.
- Large PDFs should be processed page by page to manage memory.