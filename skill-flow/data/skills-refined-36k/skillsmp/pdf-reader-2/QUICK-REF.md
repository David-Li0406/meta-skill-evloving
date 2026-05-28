# PDF Reader - Quick Reference Card

## Installation (One-Time Setup)
```bash
pip install pdfplumber  # Recommended
# OR
pip install PyPDF2      # Lightweight alternative
```

## 3-Line Quick Start
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    print(pdf.pages[0].extract_text())  # Read first page
```

## Common Tasks (Copy-Paste Ready)

### 1. Read All Pages
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    for page in pdf.pages:
        print(page.extract_text())
```

### 2. Read Specific Pages
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[2].extract_text()  # Page 3 (0-indexed)
```

### 3. Count Pages
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    print(f"Total pages: {len(pdf.pages)}")
```

### 4. Search for Text
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    for i, page in enumerate(pdf.pages, 1):
        text = page.extract_text()
        if "keyword" in text.lower():
            print(f"Found on page {i}")
```

### 5. Extract Tables
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    tables = pdf.pages[0].extract_tables()
    for table in tables:
        print(table)
```

### 6. Save to Text File
```python
import pdfplumber
with pdfplumber.open("input.pdf") as pdf:
    with open("output.txt", "w") as f:
        for page in pdf.pages:
            f.write(page.extract_text() or "")
```

### 7. Get Metadata
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    print(pdf.metadata)
    print(f"Pages: {len(pdf.pages)}")
```

### 8. Handle Errors
```python
import pdfplumber
try:
    with pdfplumber.open("file.pdf") as pdf:
        text = pdf.pages[0].extract_text()
except FileNotFoundError:
    print("PDF not found")
except Exception as e:
    print(f"Error: {e}")
```

## CLI Tool (scripts/pdf_reader.py)
```bash
# Read entire PDF
python pdf_reader.py document.pdf

# Specific pages
python pdf_reader.py document.pdf --pages 1,3,5
```

## When Things Go Wrong

| Problem           | Solution                          |
| ----------------- | --------------------------------- |
| No text extracted | PDF might be image-based, try OCR |
| Garbled text      | Try PyPDF2 instead of pdfplumber  |
| Module not found  | Run `pip install pdfplumber`      |
| Memory error      | Process pages one at a time       |

## PyPDF2 Alternative (If Needed)

```python
import PyPDF2
with open("file.pdf", "rb") as f:
    reader = PyPDF2.PdfReader(f)
    print(reader.pages[0].extract_text())
```

## Ask Claude

Simply ask:
- "Read this PDF"
- "Extract text from page 5"
- "Find 'keyword' in this PDF"
- "Get all tables from this PDF"

Claude will use this skill automatically!
