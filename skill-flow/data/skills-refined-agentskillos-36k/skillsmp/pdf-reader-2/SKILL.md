---
name: pdf-reader
description: Extract and read text content from PDF files. Use when working with PDF documents, extracting text, analyzing PDF content, or when user mentions reading PDFs. Requires PyPDF2 or pdfplumber packages.
---

# PDF Reader

This skill helps you extract and read text content from PDF files using Python libraries.

## When to use this skill

Use this skill when:
- Reading text content from PDF files
- Extracting specific pages from PDFs
- Analyzing PDF document structure
- Converting PDF text to plain text
- The user mentions "PDF", "read PDF", "extract text from PDF"

## Requirements

Install required packages:
```bash
pip install PyPDF2 pdfplumber
```

## Quick start

### Basic text extraction with PyPDF2

```python
import PyPDF2

def read_pdf_pypdf2(pdf_path):
    """Extract all text from a PDF file using PyPDF2"""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Get number of pages
        num_pages = len(pdf_reader.pages)
        print(f"PDF has {num_pages} pages")
        
        # Extract text from all pages
        full_text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            full_text += f"\n--- Page {page_num + 1} ---\n{text}"
        
        return full_text

# Usage
text = read_pdf_pypdf2("document.pdf")
print(text)
```

### Advanced extraction with pdfplumber

pdfplumber provides better text extraction and table detection:

```python
import pdfplumber

def read_pdf_pdfplumber(pdf_path):
    """Extract text with better formatting using pdfplumber"""
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        
        for i, page in enumerate(pdf.pages):
            # Extract text
            text = page.extract_text()
            full_text += f"\n--- Page {i + 1} ---\n{text}\n"
            
            # Optionally extract tables
            tables = page.extract_tables()
            if tables:
                full_text += f"\n[Found {len(tables)} table(s) on page {i + 1}]\n"
        
        return full_text

# Usage
text = read_pdf_pdfplumber("document.pdf")
print(text)
```

### Extract specific pages

```python
def read_pdf_pages(pdf_path, page_numbers):
    """Extract text from specific pages only"""
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page_num in page_numbers:
            if 0 <= page_num < len(pdf.pages):
                page = pdf.pages[page_num]
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page.extract_text()
            else:
                print(f"Warning: Page {page_num + 1} doesn't exist")
        return text

# Usage: Read pages 1, 3, and 5 (0-indexed: 0, 2, 4)
text = read_pdf_pages("document.pdf", [0, 2, 4])
print(text)
```

### Get PDF metadata

```python
def get_pdf_info(pdf_path):
    """Get metadata and information about the PDF"""
    with pdfplumber.open(pdf_path) as pdf:
        info = {
            'num_pages': len(pdf.pages),
            'metadata': pdf.metadata,
        }
        
        # Get dimensions of first page
        if pdf.pages:
            first_page = pdf.pages[0]
            info['page_width'] = first_page.width
            info['page_height'] = first_page.height
    
    return info

# Usage
info = get_pdf_info("document.pdf")
print(f"Pages: {info['num_pages']}")
print(f"Title: {info['metadata'].get('Title', 'N/A')}")
print(f"Author: {info['metadata'].get('Author', 'N/A')}")
```

## Common use cases

### Search for text in PDF

```python
def search_in_pdf(pdf_path, search_term):
    """Search for a term and return pages where it appears"""
    results = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if search_term.lower() in text.lower():
                results.append({
                    'page': i + 1,
                    'text_snippet': text[:200]  # First 200 chars as preview
                })
    
    return results

# Usage
results = search_in_pdf("document.pdf", "important keyword")
for result in results:
    print(f"Found on page {result['page']}")
```

### Extract tables from PDF

```python
def extract_tables(pdf_path):
    """Extract all tables from PDF"""
    all_tables = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for j, table in enumerate(tables):
                all_tables.append({
                    'page': i + 1,
                    'table_number': j + 1,
                    'data': table
                })
    
    return all_tables

# Usage
tables = extract_tables("document.pdf")
for table_info in tables:
    print(f"Table {table_info['table_number']} from page {table_info['page']}")
    print(table_info['data'])
```

## Tips and best practices

1. **Choose the right library**:
   - Use `PyPDF2` for simple text extraction and PDF manipulation
   - Use `pdfplumber` for better text extraction and table detection
   - Use both if needed for different tasks

2. **Handle errors gracefully**:
   ```python
   try:
       text = read_pdf_pdfplumber("document.pdf")
   except FileNotFoundError:
       print("PDF file not found")
   except Exception as e:
       print(f"Error reading PDF: {e}")
   ```

3. **Memory management**: For large PDFs, process pages one at a time instead of loading all text at once

4. **Text quality**: Some PDFs (especially scanned images) may not have extractable text. Consider OCR tools like `pytesseract` for those cases.

## Troubleshooting

- **No text extracted**: The PDF might be image-based. Use OCR tools.
- **Garbled text**: Try `pdfplumber` instead of `PyPDF2`, it often handles formatting better.
- **Missing packages**: Run `pip install PyPDF2 pdfplumber`

## Related skills

- For PDF form filling: Consider creating a `pdf-forms` skill
- For PDF merging/splitting: Consider creating a `pdf-manipulation` skill
- For OCR on image PDFs: Consider using `pytesseract` with `pdf2image`
