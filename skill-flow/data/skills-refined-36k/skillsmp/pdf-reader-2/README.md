# PDF Reader Skill

Extract and read text content from PDF files using Python.

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install pdfplumber
   ```

2. **Use the skill** - Just ask Claude:
   - "Read this PDF file"
   - "Extract text from document.pdf"
   - "Find all mentions of 'keyword' in this PDF"

## Files in this Skill

- **SKILL.md** - Main skill definition with quick start guide
- **EXAMPLES.md** - 7 ready-to-use code examples for common tasks
- **REFERENCE.md** - Complete API reference for PyPDF2 and pdfplumber
- **INSTALL.md** - Installation and testing instructions
- **scripts/pdf_reader.py** - Command-line utility for quick PDF reading

## Quick Examples

### Read entire PDF
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages, 1):
        print(f"--- Page {i} ---")
        print(page.extract_text())
```

### Extract specific pages
```python
def read_pages(pdf_path, page_numbers):
    with pdfplumber.open(pdf_path) as pdf:
        for i in page_numbers:
            text = pdf.pages[i-1].extract_text()
            print(f"Page {i}: {text}")

read_pages("doc.pdf", [1, 3, 5])
```

### Extract tables
```python
with pdfplumber.open("data.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            print(table)
```

## Command-Line Usage

Use the included script:

```bash
# Read entire PDF
python scripts/pdf_reader.py document.pdf

# Read specific pages
python scripts/pdf_reader.py document.pdf --pages 1,2,5

# Choose library
python scripts/pdf_reader.py document.pdf --library pdfplumber
```

## Libraries Used

- **pdfplumber** (recommended) - Better text extraction, table detection
- **PyPDF2** (alternative) - Lightweight, simple API

## Common Use Cases

1. **Text extraction** - Get all text from PDF
2. **Search** - Find keywords across pages
3. **Table extraction** - Extract tables as structured data
4. **Metadata** - Get PDF properties (title, author, page count)
5. **Batch processing** - Process multiple PDFs at once
6. **Conversion** - Convert PDF to text files

## When NOT to Use

- **Image-based PDFs** (scanned documents) - Use OCR tools instead
- **PDF editing** - This is read-only; use pypdf for merging/splitting
- **Form filling** - Use dedicated form libraries

## See Also

- [INSTALL.md](INSTALL.md) - Detailed installation guide
- [EXAMPLES.md](EXAMPLES.md) - More code examples
- [REFERENCE.md](REFERENCE.md) - Full API documentation
