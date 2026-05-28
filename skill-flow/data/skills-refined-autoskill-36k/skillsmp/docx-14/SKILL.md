---
name: docx
description: Work with Word documents (DOCX/DOC) - read, extract content, create documents, convert formats, and process templates. Use when the user asks to work with Word files or .docx documents.
allowed-tools: Read, Bash, Write
---

# Word Document (DOCX) Processing Skill

When working with Word documents, follow these guidelines:

## 1. Reading & Extracting from DOCX

**Extract text content**:
```bash
# Using pandoc
pandoc document.docx -t plain -o output.txt

# Using python-docx
python3 -c "
import docx
doc = docx.Document('document.docx')
for para in doc.paragraphs:
    print(para.text)
"

# Using antiword (for .doc files)
antiword document.doc > output.txt
```

**Extract with formatting**:
```bash
# Convert to markdown (preserves structure)
pandoc document.docx -t markdown -o output.md

# Convert to HTML
pandoc document.docx -t html -o output.html
```

**Extract images**:
```bash
# DOCX files are ZIP archives
unzip -j document.docx 'word/media/*' -d extracted_images/

# Or using python
python3 << 'EOF'
import docx
import os

doc = docx.Document('document.docx')
os.makedirs('images', exist_ok=True)

for i, rel in enumerate(doc.part.rels.values()):
    if "image" in rel.target_ref:
        img = rel.target_part.blob
        with open(f'images/image_{i}.png', 'wb') as f:
            f.write(img)
EOF
```

## 2. Creating DOCX Files

**From plain text**:
```bash
# Using pandoc
pandoc input.txt -o output.docx
```

**From markdown**:
```bash
# Basic conversion
pandoc input.md -o output.docx

# With custom styling
pandoc input.md --reference-doc=template.docx -o output.docx
```

**From HTML**:
```bash
pandoc input.html -o output.docx
```

**Using Python**:
```python
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Create new document
doc = Document()

# Add heading
doc.add_heading('Document Title', 0)

# Add paragraph
p = doc.add_paragraph('This is a paragraph with ')
p.add_run('bold').bold = True
p.add_run(' and ')
p.add_run('italic').italic = True
p.add_run(' text.')

# Add table
table = doc.add_table(rows=3, cols=3)
table.style = 'Light Grid Accent 1'

# Add image
doc.add_picture('image.png', width=Inches(4))

# Save
doc.save('output.docx')
```

## 3. Converting DOCX

**DOCX to PDF**:
```bash
# Using LibreOffice (headless)
libreoffice --headless --convert-to pdf document.docx

# With output directory
libreoffice --headless --convert-to pdf --outdir ./output document.docx

# Using pandoc (requires LaTeX)
pandoc document.docx -o output.pdf
```

**DOCX to HTML**:
```bash
# Using pandoc
pandoc document.docx -o output.html

# With standalone HTML
pandoc document.docx -s -o output.html
```

**DOCX to Markdown**:
```bash
# Clean markdown output
pandoc document.docx -t markdown -o output.md

# GitHub-flavored markdown
pandoc document.docx -t gfm -o output.md
```

**DOC to DOCX**:
```bash
# Using LibreOffice
libreoffice --headless --convert-to docx document.doc
```

## 4. Template Processing

**Mail merge / Variable substitution**:
```python
from docx import Document

def fill_template(template_path, output_path, data):
    doc = Document(template_path)

    # Replace in paragraphs
    for paragraph in doc.paragraphs:
        for key, value in data.items():
            if f'{{{key}}}' in paragraph.text:
                paragraph.text = paragraph.text.replace(f'{{{key}}}', str(value))

    # Replace in tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in data.items:
                    if f'{{{key}}}' in cell.text:
                        cell.text = cell.text.replace(f'{{{key}}}', str(value))

    doc.save(output_path)

# Usage
data = {
    'name': 'John Doe',
    'date': '2026-01-22',
    'company': 'Acme Corp'
}
fill_template('template.docx', 'output.docx', data)
```

## 5. Analyzing DOCX Structure

**Get document stats**:
```python
from docx import Document

doc = Document('document.docx')

print(f"Paragraphs: {len(doc.paragraphs)}")
print(f"Tables: {len(doc.tables)}")
print(f"Sections: {len(doc.sections)}")

# Word count
text = ' '.join([p.text for p in doc.paragraphs])
print(f"Words: {len(text.split())}")
```

**Extract all headings**:
```python
from docx import Document

doc = Document('document.docx')

for para in doc.paragraphs:
    if para.style.name.startswith('Heading'):
        print(f"{para.style.name}: {para.text}")
```

**List styles used**:
```python
from docx import Document

doc = Document('document.docx')
styles = set(p.style.name for p in doc.paragraphs)
print("Styles used:", styles)
```

## 6. Modifying Existing DOCX

**Add content to existing document**:
```python
from docx import Document

doc = Document('existing.docx')

# Add new paragraph
doc.add_paragraph('New paragraph added')

# Add page break
doc.add_page_break()

# Save
doc.save('modified.docx')
```

**Replace text globally**:
```python
from docx import Document

def replace_text(doc_path, search, replace):
    doc = Document(doc_path)

    for paragraph in doc.paragraphs:
        if search in paragraph.text:
            paragraph.text = paragraph.text.replace(search, replace)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if search in cell.text:
                    cell.text = cell.text.replace(search, replace)

    doc.save(doc_path)
```

## 7. Working with Tables

**Extract table data**:
```python
from docx import Document

doc = Document('document.docx')

for i, table in enumerate(doc.tables):
    print(f"\nTable {i+1}:")
    for row in table.rows:
        cells = [cell.text for cell in row.cells]
        print('\t'.join(cells))
```

**Create formatted table**:
```python
from docx import Document

doc = Document()

# Create table
table = doc.add_table(rows=1, cols=3)
table.style = 'Light List Accent 1'

# Header row
header_cells = table.rows[0].cells
header_cells[0].text = 'Name'
header_cells[1].text = 'Age'
header_cells[2].text = 'City'

# Data rows
data = [
    ('John', '30', 'New York'),
    ('Jane', '25', 'London')
]

for name, age, city in data:
    row = table.add_row().cells
    row[0].text = name
    row[1].text = age
    row[2].text = city

doc.save('table.docx')
```

## 8. Common Workflows

### Create report from data
```bash
# Generate from JSON data
python3 << 'EOF'
import json
from docx import Document
from docx.shared import Inches

# Load data
with open('data.json') as f:
    data = json.load(f)

# Create document
doc = Document()
doc.add_heading(data['title'], 0)

for section in data['sections']:
    doc.add_heading(section['heading'], 1)
    doc.add_paragraph(section['content'])

doc.save('report.docx')
EOF
```

### Batch convert DOC to DOCX
```bash
# Convert all .doc files in directory
for file in *.doc; do
    libreoffice --headless --convert-to docx "$file"
done
```

### Extract all links
```python
from docx import Document

doc = Document('document.docx')

for paragraph in doc.paragraphs:
    for run in paragraph.runs:
        if run.font.underline and 'http' in run.text:
            print(run.text)
```

## Tools Required

Install necessary tools:

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get install pandoc libreoffice python3-pip antiword
pip3 install python-docx
```

**macOS**:
```bash
brew install pandoc libreoffice
pip3 install python-docx
```

**Windows**:
```powershell
# Install Pandoc and LibreOffice manually
pip install python-docx
```

## Security Notes

- ✅ Validate file paths before processing
- ✅ Check file sizes to prevent memory issues
- ✅ Sanitize user input in templates
- ✅ Be cautious with macro-enabled documents (.docm)
- ✅ Scan documents from untrusted sources
- ✅ Don't execute embedded scripts automatically

## When to Use This Skill

Use `/docx` when the user:
- Wants to read or extract text from Word documents
- Needs to create DOCX files from templates or data
- Wants to convert DOCX to other formats (PDF, HTML, Markdown)
- Asks to process mail merge or template variables
- Needs to extract tables, images, or structure from documents
- Wants to batch process multiple Word files
- Asks to modify existing Word documents

Always confirm before overwriting existing files.
