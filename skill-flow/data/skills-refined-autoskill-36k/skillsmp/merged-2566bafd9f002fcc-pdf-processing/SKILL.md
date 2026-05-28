---
name: pdf-processing
description: Use this skill when you need to extract text and tables, create new PDFs, merge/split documents, or handle forms programmatically.
---

# PDF Processing

A comprehensive toolkit for PDF operations, including text extraction, table parsing, document merging/splitting, and form handling.

## 🎯 Overview

| Functionality      | Tools                     | Purpose                          |
|--------------------|---------------------------|----------------------------------|
| Text Extraction     | `pdftotext`, `pdfplumber` | Extract text content from PDFs   |
| Table Parsing       | `pdfplumber`, `tabula-py` | Extract table data               |
| Document Merging    | `PyPDF4`, `pdftk`, `qpdf` | Merge multiple PDFs into one     |
| Document Splitting   | `PyPDF4`, `pdftk`, `qpdf` | Split a PDF into multiple files  |
| Form Filling        | `pdftk`, `PyPDF4`        | Fill PDF form fields             |
| Format Conversion    | `libreoffice`, `ImageMagick` | Convert PDF to/from other formats |

---

## 📄 Text Extraction

### Using `pdftotext`

```bash
# Basic extraction
pdftotext <input_path> <output_path>

# Preserve layout
pdftotext -layout <input_path> <output_path>

# Extract specific pages
pdftotext -f <start_page> -l <end_page> <input_path> <output_path>
```

### Handling Scanned PDFs

```bash
# Check if the PDF is scanned (text < 50 characters)
pdftotext <input_path> - | wc -c

# Use OCR for scanned PDFs
brew install tesseract
tesseract <input_path> <output_path>
```

---

## 📊 Table Parsing

### Using `pdfplumber`

```python
import pdfplumber

# Extract all tables
with pdfplumber.open("<input_path>") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print(row)

# Extract from a specific area
with pdfplumber.open("<input_path>") as pdf:
    page = pdf.pages[0]
    crop = page.crop((<x0>, <y0>, <x1>, <y1>))
    table = crop.extract_table()
```

### Using `tabula-py`

```bash
# Command line usage
tabula <input_path> -o <output_path>

# Specify page and area
tabula <input_path> -p <page_number> -a <area> -o <output_path>
```

---

## 🔀 Merging and Splitting Documents

### Using `PyPDF4`

```python
from PyPDF4 import PdfFileReader, PdfFileWriter

# Merge PDFs
def merge_pdfs(input_files, output_file):
    writer = PdfFileWriter()
    for file in input_files:
        reader = PdfFileReader(file)
        for page in reader.pages:
            writer.addPage(page)
    with open(output_file, 'wb') as f:
        writer.write(f)

# Split PDF
def split_pdf(input_file, output_dir):
    reader = PdfFileReader(input_file)
    for i, page in enumerate(reader.pages):
        writer = PdfFileWriter()
        writer.addPage(page)
        with open(f"{output_dir}/page_{i+1}.pdf", 'wb') as f:
            writer.write(f)
```

### Using `pdftk`

```bash
# Merge
pdftk <file1> <file2> cat output <output_file>

# Split (extract specific pages)
pdftk <input_file> cat <page_range> output <output_file>

# Burst (extract each page as a separate file)
pdftk <input_file> burst output <output_prefix>_%02d.pdf
```

---

## 📝 Form Filling

### Using `pdftk`

```bash
# Export form fields
pdftk <form_file> dump_data_fields output <fields_file>

# Create fill file (fill.txt)
---
field1: value1
field2: value2
---

# Fill form
pdftk <form_file> fill_form <fill_file> output <filled_file>
```

### Using `PyPDF4`

```python
from PyPDF4 import PdfFileReader, PdfFileWriter

reader = PdfFileReader("<form_file>")
writer = PdfFileWriter()

# Copy page and fill
page = reader.getPage(0)
writer.addPage(page)

# Update fields
writer.updatePageFormFieldValues(writer.getPage(0), {
    'field1': 'value1',
    'field2': 'value2'
})

with open("<filled_file>", 'wb') as f:
    writer.write(f)
```

---

## 🔄 Format Conversion

### PDF to Image

```bash
# Using ImageMagick
convert <input_path> <output_path>

# Specify DPI and quality
convert -density 300 -quality 90 <input_path> <output_path>
```

### PDF to Word/Excel

```bash
# LibreOffice conversion
brew install libreoffice

# PDF to Word
soffice --headless --convert-to docx <input_path>

# PDF to Excel
soffice --headless --convert-to xlsx <input_path>
```

---

## 🧰 Tool Installation

```bash
# macOS
brew install poppler        # pdftotext, pdftk
brew install tesseract      # OCR
pip install pdfplumber PyPDF4 tabula-py

# Linux
apt-get install poppler-utils
apt-get install tesseract-ocr
pip3 install pdfplumber PyPDF4 tabula-py
```

---

## Common Use Cases

You might use this skill when you hear:
- "Extract PDF content"
- "Merge PDFs"
- "Parse PDF tables"
- "Fill PDF forms"
- "Convert PDF to Word"