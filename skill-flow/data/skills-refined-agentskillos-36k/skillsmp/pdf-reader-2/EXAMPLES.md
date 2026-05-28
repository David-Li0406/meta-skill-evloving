# PDF Reader Examples

## Example 1: Simple text extraction

**User request**: "Can you read this PDF file and show me the content?"

**Code**:
```python
import pdfplumber

def read_pdf_simple(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            text += f"\n{'='*50}\nPage {i}\n{'='*50}\n"
            text += page.extract_text() or "[No text found]"
    return text

# Usage
content = read_pdf_simple("report.pdf")
print(content)
```

## Example 2: Extract first 5 pages only

**User request**: "I only need to read the first 5 pages of this PDF"

**Code**:
```python
import pdfplumber

def read_first_n_pages(pdf_path, n=5):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i in range(min(n, len(pdf.pages))):
            page = pdf.pages[i]
            text += f"\n--- Page {i+1} ---\n"
            text += page.extract_text()
    return text

# Usage
content = read_first_n_pages("large_document.pdf", 5)
print(content)
```

## Example 3: Find specific information

**User request**: "Search through this PDF and find all mentions of 'revenue'"

**Code**:
```python
import pdfplumber
import re

def find_mentions(pdf_path, keyword):
    results = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            # Find lines containing the keyword
            lines = text.split('\n')
            for line in lines:
                if keyword.lower() in line.lower():
                    results.append({
                        'page': i,
                        'line': line.strip()
                    })
    return results

# Usage
mentions = find_mentions("financial_report.pdf", "revenue")
for item in mentions:
    print(f"Page {item['page']}: {item['line']}")
```

## Example 4: Extract and save as text file

**User request**: "Convert this PDF to a text file"

**Code**:
```python
import pdfplumber

def pdf_to_text_file(pdf_path, output_path):
    with pdfplumber.open(pdf_path) as pdf:
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, page in enumerate(pdf.pages, 1):
                f.write(f"\n{'='*60}\n")
                f.write(f"Page {i}\n")
                f.write(f"{'='*60}\n\n")
                text = page.extract_text()
                f.write(text or "[No text on this page]")
                f.write("\n\n")
    print(f"Text extracted to {output_path}")

# Usage
pdf_to_text_file("document.pdf", "document.txt")
```

## Example 5: Extract tables and save as CSV

**User request**: "Get all tables from this PDF and save them as CSV files"

**Code**:
```python
import pdfplumber
import csv

def extract_tables_to_csv(pdf_path, output_prefix="table"):
    table_count = 0
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables()
            
            for j, table in enumerate(tables):
                if table:  # Make sure table is not empty
                    table_count += 1
                    csv_filename = f"{output_prefix}_page{i}_table{j+1}.csv"
                    
                    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerows(table)
                    
                    print(f"Saved: {csv_filename}")
    
    print(f"\nTotal tables extracted: {table_count}")

# Usage
extract_tables_to_csv("data_report.pdf", "output")
```

## Example 6: Get PDF summary

**User request**: "Give me a quick summary of this PDF"

**Code**:
```python
import pdfplumber

def get_pdf_summary(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        summary = {
            'filename': pdf_path,
            'total_pages': len(pdf.pages),
            'metadata': pdf.metadata,
            'first_page_preview': None,
            'tables_count': 0,
        }
        
        # Get preview of first page
        if pdf.pages:
            first_text = pdf.pages[0].extract_text()
            summary['first_page_preview'] = first_text[:500] if first_text else None
        
        # Count total tables
        for page in pdf.pages:
            summary['tables_count'] += len(page.extract_tables())
        
        return summary

# Usage
summary = get_pdf_summary("document.pdf")
print(f"File: {summary['filename']}")
print(f"Pages: {summary['total_pages']}")
print(f"Tables: {summary['tables_count']}")
print(f"Author: {summary['metadata'].get('Author', 'Unknown')}")
print(f"\nFirst page preview:\n{summary['first_page_preview']}")
```

## Example 7: Batch process multiple PDFs

**User request**: "Extract text from all PDFs in this folder"

**Code**:
```python
import pdfplumber
import os
from pathlib import Path

def batch_extract_pdfs(folder_path, output_folder="extracted_texts"):
    # Create output folder
    Path(output_folder).mkdir(exist_ok=True)
    
    # Find all PDF files
    pdf_files = list(Path(folder_path).glob("*.pdf"))
    
    print(f"Found {len(pdf_files)} PDF files")
    
    for pdf_path in pdf_files:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Create output filename
                output_name = pdf_path.stem + ".txt"
                output_path = Path(output_folder) / output_name
                
                # Extract text
                full_text = ""
                for page in pdf.pages:
                    full_text += page.extract_text() or ""
                
                # Save to file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(full_text)
                
                print(f"✓ Processed: {pdf_path.name}")
        
        except Exception as e:
            print(f"✗ Error processing {pdf_path.name}: {e}")

# Usage
batch_extract_pdfs("./pdfs", "extracted_texts")
```
