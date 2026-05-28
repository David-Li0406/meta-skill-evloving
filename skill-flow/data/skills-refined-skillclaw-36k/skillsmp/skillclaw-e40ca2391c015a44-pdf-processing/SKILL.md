---
name: pdf-processing
description: Use this skill when working with PDF files to extract text and tables, fill forms, merge documents, or split PDFs.
---

# PDF Processing Skill

## Quick Start

Use `pdfplumber` to extract text from PDFs:

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    text = pdf.pages[0].extract_text()
    print(text)
```

## Capabilities

### 1. Text Extraction
Extract all text from a PDF document:

```python
def extract_all_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() or ""
        return full_text
```

### 2. Table Extraction
Extract tables from PDF pages:

```python
with pdfplumber.open("document.pdf") as pdf:
    tables = pdf.pages[0].extract_tables()
    for table in tables:
        print(table)
```

### 3. Form Filling
Fill PDF forms programmatically. For comprehensive form-filling guidance, refer to the relevant documentation.

### 4. Merging PDFs
Combine multiple PDF files:

```python
from pypdf import PdfMerger

merger = PdfMerger()

for pdf in ["file1.pdf", "file2.pdf", "file3.pdf"]:
    merger.append(pdf)

merger.write("merged.pdf")
merger.close()
```

### 5. Splitting PDFs
Extract specific pages or ranges:

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

# Extract pages 2-5
for page_num in range(1, 5):
    writer.add_page(reader.pages[page_num])

with open("output.pdf", "wb") as output:
    writer.write(output)
```

## Best Practices

- **Performance**: For large PDFs, process page-by-page to avoid memory issues.
- **OCR**: For scanned PDFs without a text layer, recommend using OCR tools first.
- **Encoding**: Handle UTF-8 encoding properly when extracting text.

## Common Use Cases

- Invoice text extraction
- Table data scraping from reports
- PDF form automation
- Document merging and splitting