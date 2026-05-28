---
name: office-to-md
description: Convert Office documents (Word, Excel, PowerPoint, PDF) to Markdown format. ONLY use this skill when the user explicitly requests to CONVERT, TRANSFORM or PARSE a specific office file into Markdown. Do NOT trigger for general questions, documentation reading, or discussions about files.
---

# Office Document to Markdown Converter

Convert various Office document formats to structured Markdown with text, table, and image extraction.

## File Description

- `enhanced_parser.py` - Core document parser
- `doc_converter.py` - DOC to DOCX converter (requires LibreOffice)
- `requirements.txt` - Python dependencies

## Install Dependencies

```bash
pip install -r requirements.txt
```

### Additional Dependencies for DOC Format

.doc format requires LibreOffice:

```bash
# Windows: Install LibreOffice from official website
# https://www.libreoffice.org/download/

# Linux
sudo apt install libreoffice

# Mac
brew install --cask libreoffice
```

## Quick Start

### Python Code

```python
from enhanced_parser import EnhancedDocumentParser

# Initialize parser
parser = EnhancedDocumentParser(
    image_base_url="http://localhost:5000",
    image_save_dir="./static/images",
    filter_headers_footers=True  # Filter headers and footers
)

# Parse document
result = parser.parse_document("document.docx")

if result["success"]:
    print(result["markdown"])
    print(f"Extracted {result['images_count']} images")
```

### Start API Service

```bash
# Start service using app.py from project root
python app.py

# Visit http://localhost:5000/analyzer to upload files
```

## Supported Formats

| Format | Extensions | Notes |
|--------|-----------|-------|
| Word | .docx, .doc | .doc requires LibreOffice |
| Excel | .xlsx, .xls | Supports multiple worksheets and date formats |
| PowerPoint | .pptx | Extracts slide text and images |
| PDF | .pdf | Auto-detects tables and images |

## Features

### Word Documents
- Automatic heading level detection
- Convert tables to Markdown tables
- Extract inline images
- Filter headers and footers
- Preserve list formatting

### Excel Workbooks
- Support for multiple worksheets
- Automatic date format detection (prevents display as numbers)
- Convert to Markdown tables
- Extract embedded images

### PowerPoint Presentations
- Extract content by slide
- Extract images and text boxes
- Preserve slide order

### PDF Documents
- Auto-detect tables (line detection + text position detection)
- Extract page images
- Intelligently identify headings and lists
- Output content in original order

## Advanced Options

### DOC Conversion

```bash
# Test LibreOffice configuration
python doc_converter.py
```

### PDF Table Strategy

```python
parser = EnhancedDocumentParser(
    pdf_table_strategy="lines_strict"  # Default: strict line detection, fastest
    # "lines": Normal line detection
    # "text": Based on text position, more accurate but slower
)
```

### Image Processing

```python
parser = EnhancedDocumentParser(
    image_base_url="https://your-domain.com",  # Image access URL
    image_save_dir="./static/images"           # Image save directory
)
```

## Return Format

```json
{
  "success": true,
  "markdown": "# Document Title\n\nContent...",
  "images_count": 2,
  "images": [
    {
      "filename": "uuid.png",
      "url": "http://localhost:5000/static/images/uuid.png",
      "size": 12345
    }
  ],
  "file_type": "docx",
  "file_info": {
    "name": "document.docx",
    "size": 45678,
    "paragraphs": 50,
    "tables": 3
  }
}
```

## Common Issues

### DOC Conversion Failed
- Ensure LibreOffice is installed
- Run `python doc_converter.py` to test configuration

### Dates Display as Numbers
- Excel parsing automatically handles date formats
- Ensure you're using the latest version of enhanced_parser.py

### PDF Table Recognition Inaccurate
- Try different pdf_table_strategy parameters
- Use "lines_strict" for standard tables
- Use "text" for complex tables

## File Limitations

- Maximum file size: 160MB
- Supported extensions: docx, doc, pdf, xlsx, xls, pptx
- Automatic cleanup of temporary files
