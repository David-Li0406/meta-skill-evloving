# PDF Reader Reference

## Libraries Comparison

### PyPDF2
- **Best for**: Basic text extraction, PDF manipulation
- **Pros**: Lightweight, simple API
- **Cons**: Sometimes misses text formatting, less accurate than pdfplumber

### pdfplumber
- **Best for**: Accurate text extraction, table detection
- **Pros**: Better text extraction quality, can detect tables, provides layout info
- **Cons**: Slightly slower than PyPDF2

## PyPDF2 API Reference

### Reading PDFs

```python
import PyPDF2

# Open and read
with open('file.pdf', 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    
    # Get page count
    num_pages = len(reader.pages)
    
    # Get specific page (0-indexed)
    page = reader.pages[0]
    
    # Extract text from page
    text = page.extract_text()
    
    # Get metadata
    metadata = reader.metadata
    # metadata.title, metadata.author, etc.
```

### Common PyPDF2 Operations

```python
# Check if PDF is encrypted
is_encrypted = reader.is_encrypted

# Get page dimensions
page = reader.pages[0]
width = page.mediabox.width
height = page.mediabox.height

# Extract images (requires pillow)
for image_file_object in page.images:
    image_data = image_file_object.data
```

## pdfplumber API Reference

### Opening PDFs

```python
import pdfplumber

# Context manager (recommended)
with pdfplumber.open('file.pdf') as pdf:
    # work with pdf
    pass

# Or manual open/close
pdf = pdfplumber.open('file.pdf')
# work with pdf
pdf.close()
```

### Page Object Properties

```python
page = pdf.pages[0]

# Dimensions
page.width      # Page width in points
page.height     # Page height in points
page.bbox       # Bounding box (x0, top, x1, bottom)

# Content
page.chars      # List of individual characters
page.lines      # List of lines
page.rects      # List of rectangles
page.curves     # List of curves
```

### Text Extraction Methods

```python
# Extract all text
text = page.extract_text()

# Extract text with layout
text = page.extract_text(layout=True)

# Extract words as list
words = page.extract_words()
# Returns list of dicts: {'text', 'x0', 'top', 'x1', 'bottom'}

# Extract text from specific region
bbox = (x0, top, x1, bottom)
cropped = page.crop(bbox)
text = cropped.extract_text()
```

### Table Extraction

```python
# Extract all tables
tables = page.extract_tables()
# Returns list of tables (each table is a list of rows)

# Extract with custom settings
tables = page.extract_tables({
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "intersection_tolerance": 3,
})

# Get table settings that were detected
settings = page.find_tables()
```

### Working with Images in Text

```python
# Get image coordinates
page.images  # List of image dicts with bbox info

# Filter content by type
page.filter(lambda obj: obj["object_type"] == "char")
```

## Advanced pdfplumber Usage

### Custom Text Extraction

```python
def extract_text_custom(page):
    """Custom text extraction with filtering"""
    # Get all words
    words = page.extract_words()
    
    # Filter words (e.g., minimum font size)
    filtered = [w for w in words if w.get('height', 0) > 6]
    
    # Combine into text
    text = ' '.join([w['text'] for w in filtered])
    return text
```

### Handling Rotated Pages

```python
# Get page rotation
rotation = page.rotation

# For rotated PDFs, pdfplumber handles it automatically
# But you can check if needed
if rotation == 90:
    # Page is rotated 90 degrees clockwise
    pass
```

### Performance Tips

```python
# For large PDFs, process pages lazily
def extract_text_lazy(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            # Process one page at a time
            text = page.extract_text()
            yield i, text

# Usage
for page_num, text in extract_text_lazy("large.pdf"):
    print(f"Page {page_num}: {len(text)} chars")
```

## Common Patterns

### Pattern 1: Safe text extraction

```python
def safe_extract(page):
    """Safely extract text with fallback"""
    try:
        text = page.extract_text()
        if not text or text.strip() == "":
            return "[No readable text on this page]"
        return text
    except Exception as e:
        return f"[Error extracting text: {e}]"
```

### Pattern 2: Progress tracking

```python
def extract_with_progress(pdf_path):
    """Extract text with progress indicator"""
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        texts = []
        
        for i, page in enumerate(pdf.pages, 1):
            print(f"Processing page {i}/{total}...", end='\r')
            texts.append(page.extract_text())
        
        print(f"\nCompleted! Processed {total} pages.")
        return texts
```

### Pattern 3: Structured data extraction

```python
def extract_structured(pdf_path):
    """Extract text with structure preserved"""
    result = {
        'metadata': {},
        'pages': []
    }
    
    with pdfplumber.open(pdf_path) as pdf:
        # Get metadata
        result['metadata'] = {
            'title': pdf.metadata.get('Title', ''),
            'author': pdf.metadata.get('Author', ''),
            'pages': len(pdf.pages)
        }
        
        # Get pages
        for i, page in enumerate(pdf.pages, 1):
            page_data = {
                'number': i,
                'text': page.extract_text(),
                'tables': page.extract_tables(),
                'images_count': len(page.images)
            }
            result['pages'].append(page_data)
    
    return result
```

## Error Handling

```python
from pdfplumber.utils import PDFSyntaxError

def robust_pdf_read(pdf_path):
    """Read PDF with comprehensive error handling"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if len(pdf.pages) == 0:
                return None, "PDF has no pages"
            
            texts = []
            for page in pdf.pages:
                try:
                    text = page.extract_text()
                    texts.append(text or "")
                except Exception as e:
                    texts.append(f"[Error on this page: {e}]")
            
            return texts, None
    
    except FileNotFoundError:
        return None, f"File not found: {pdf_path}"
    except PDFSyntaxError:
        return None, "Invalid or corrupted PDF file"
    except Exception as e:
        return None, f"Unexpected error: {e}"

# Usage
texts, error = robust_pdf_read("document.pdf")
if error:
    print(f"Error: {error}")
else:
    print(f"Successfully read {len(texts)} pages")
```

## Installation Commands

```bash
# Install PyPDF2
pip install PyPDF2

# Install pdfplumber
pip install pdfplumber

# Install both
pip install PyPDF2 pdfplumber

# For additional features (image extraction)
pip install pillow

# For OCR on image-based PDFs
pip install pytesseract pdf2image
```

## Further Resources

- PyPDF2 Documentation: https://pypdf2.readthedocs.io/
- pdfplumber Documentation: https://github.com/jsvine/pdfplumber
- PDF Specification: https://www.adobe.com/devnet/pdf/pdf_reference.html
