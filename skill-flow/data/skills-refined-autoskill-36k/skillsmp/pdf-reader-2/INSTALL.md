# PDF Reader Skill - Installation & Testing

## Installation

The PDF reader skill requires Python libraries. Install them with:

```bash
# Install pdfplumber (recommended - better text extraction)
pip install pdfplumber

# Or install PyPDF2 (lightweight alternative)
pip install PyPDF2

# Or install both
pip install pdfplumber PyPDF2
```

## Quick Test

### Test 1: Check if libraries are installed

```python
# Run this to verify installation
try:
    import pdfplumber
    print("✓ pdfplumber is installed")
except ImportError:
    print("✗ pdfplumber not found - install with: pip install pdfplumber")

try:
    import PyPDF2
    print("✓ PyPDF2 is installed")
except ImportError:
    print("✗ PyPDF2 not found - install with: pip install PyPDF2")
```

### Test 2: Read a sample PDF

Create a simple test script:

```python
import pdfplumber

# Replace with path to your PDF
pdf_path = "test.pdf"

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    
    # Read first page
    first_page = pdf.pages[0]
    text = first_page.extract_text()
    
    print("\nFirst 500 characters:")
    print(text[:500] if text else "[No text found]")
```

## Using the Helper Script

The skill includes a ready-to-use command-line script:

```bash
# Navigate to the scripts directory
cd /Users/nhat/repo-fun/Nhat-Learn-In-Public/.claude/skills/pdf-reader/scripts

# Make it executable (optional)
chmod +x pdf_reader.py

# Read entire PDF
python pdf_reader.py /path/to/your/file.pdf

# Read specific pages only
python pdf_reader.py /path/to/your/file.pdf --pages 1,2,5

# Use specific library
python pdf_reader.py /path/to/your/file.pdf --library pdfplumber
python pdf_reader.py /path/to/your/file.pdf --library pypdf2
```

## Verify Skill is Active

To check if Claude can see your PDF reader skill:

1. Ask Claude: "What skills are available?"
2. Look for "pdf-reader" in the list
3. Test it by asking: "Can you help me read a PDF file?"

## Common Issues

### Issue: "No module named 'pdfplumber'"

**Solution**: Install the library
```bash
pip install pdfplumber
```

### Issue: "No text extracted from PDF"

**Possible causes**:
1. PDF is image-based (scanned document) - needs OCR
2. PDF has security restrictions
3. Corrupted PDF file

**Solution**: Try with different PDF or use OCR tools

### Issue: Garbled or incorrect text

**Solution**: Try switching from PyPDF2 to pdfplumber or vice versa
```python
# If PyPDF2 gives bad results, try pdfplumber
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Next Steps

Once installed, you can:

1. **Ask Claude to read PDFs**: "Read this PDF file for me"
2. **Extract specific content**: "Find all mentions of 'revenue' in this PDF"
3. **Convert to text**: "Convert this PDF to a text file"
4. **Extract tables**: "Get all tables from this PDF"

The skill will automatically use the appropriate code examples and handle the task!
