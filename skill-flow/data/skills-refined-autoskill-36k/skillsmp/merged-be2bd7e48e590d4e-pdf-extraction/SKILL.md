---
name: pdf-extraction
description: Use this skill to extract text, tables, and metadata from PDF files, and to fill forms or merge documents. Ideal for document extraction and processing tasks involving PDFs.
---

# PDF Extraction Skill

## Overview
This skill extracts structured content (text, tables, images, and metadata) from PDF files using Python libraries. It is designed for various document processing tasks, including text extraction, table scraping, form filling, and merging documents.

## Quick Start

### Basic Text Extraction
Use `pdfplumber` to extract text from PDFs:
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

### Extracting Tables
Extract tables from PDF pages:
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            print(table)
```

### Extracting Metadata
Retrieve metadata from a PDF file:
```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
metadata = reader.metadata
print(f"Title: {metadata.title}")
print(f"Author: {metadata.author}")
print(f"Pages: {len(reader.pages)}")
```

### Form Filling
Fill PDF forms programmatically. Refer to the comprehensive guide for form filling.

### Merging PDFs
Combine multiple PDF files:
```python
from pypdf import PdfMerger

merger = PdfMerger()
for pdf in ["file1.pdf", "file2.pdf", "file3.pdf"]:
    merger.append(pdf)
merger.write("merged.pdf")
merger.close()
```

### Splitting PDFs
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
- For large PDFs, process page-by-page to manage memory effectively.
- Use OCR tools like `pytesseract` for scanned PDFs.
- Handle UTF-8 encoding properly when extracting text.

## Error Handling
Handle common PDF issues:
```python
import pdfplumber

try:
    with pdfplumber.open("document.pdf") as pdf:
        if len(pdf.pages) == 0:
            print("PDF has no pages")
        else:
            text = pdf.pages[0].extract_text()
            if text is None or text.strip() == "":
                print("Page contains no extractable text (might be scanned)")
            else:
                print(text)
except Exception as e:
    print(f"Error processing PDF: {e}")
```

## Dependencies
**Required:**
- Python 3.10+
- `pdfplumber` for text and table extraction
- `pypdf` for PDF manipulation

**Optional (for advanced features):**
- `pytesseract` for OCR
- `Pillow` for image processing
- `camelot-py` for complex tables

## Output Structure
The output of the extraction process will be organized as follows:
```
output/<skill-name>/
├── SKILL.md              # Skill description with PDF summary
├── references/
│   ├── index.md          # Table of contents
│   ├── chapter_1.md      # Content by section
│   ├── chapter_2.md
│   └── tables.md         # Extracted tables
└── assets/
    └── images/           # Extracted images (if enabled)
```

## Troubleshooting
| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| Garbled text | Scanned PDF | Enable OCR mode |
| Missing tables | Complex layout | Use `--extract-tables` with pdfplumber |
| Poor OCR | Low resolution | Increase DPI, check language pack |
| Memory error | Large PDF | Use chunked extraction, reduce workers |
| Corrupt PDF | File damaged | Try `qpdf --check` or `mutool clean` |

## References
- Skill Seekers PDF Support: https://github.com/jmagly/Skill_Seekers/blob/main/docs/PDF_MCP_TOOL.md
- REF-001: Production-Grade Agentic Workflows
- REF-002: LLM Failure Modes