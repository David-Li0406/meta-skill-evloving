---
name: pdf-extractor
description: Extract text, tables, and metadata from PDF files. Use when working with PDFs, document extraction, or parsing PDF content.
version: 1.0.0
author: agentflow
triggers:
  - pdf
  - extract text
  - parse document
  - read pdf
requirements:
  - pypdf
  - pdfplumber
tags:
  - document
  - extraction
  - pdf
---

# PDF Extraction Instructions

## Overview
This skill extracts text and data from PDF files using Python libraries.

## Usage

### Basic Text Extraction
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

### Extract Tables
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            print(table)
```

### Get Metadata
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
- For scanned PDFs, consider using OCR libraries like `pytesseract`
- Large PDFs should be processed page by page to manage memory

