---
name: pdf
description: Work with PDF files - read, extract text/images/tables, create PDFs, merge, split, and convert PDFs. Use when the user asks to read, create, modify, or analyze PDF documents.
allowed-tools: Read, Bash, Write
---

# PDF Processing Skill

When working with PDF files, follow these guidelines:

## 1. Reading & Extracting from PDFs

For **text extraction**:
```bash
# Extract all text
pdftotext input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 10 input.pdf output.txt

# Preserve layout
pdftotext -layout input.pdf output.txt
```

For **extracting images**:
```bash
# Extract all images
pdfimages -all input.pdf output_prefix

# Extract as PNG
pdfimages -png input.pdf images/page
```

For **metadata**:
```bash
# Get PDF info
pdfinfo document.pdf

# Get detailed metadata
exiftool document.pdf
```

## 2. Creating PDFs

From **text/markdown**:
```bash
# From markdown using pandoc
pandoc input.md -o output.pdf

# From text with formatting
enscript input.txt -o - | ps2pdf - output.pdf
```

From **HTML**:
```bash
# Using wkhtmltopdf
wkhtmltopdf input.html output.pdf

# With options
wkhtmltopdf --page-size A4 --margin-top 10mm input.html output.pdf
```

From **images**:
```bash
# Convert images to PDF
convert image1.png image2.png output.pdf

# Multiple images
img2pdf img1.jpg img2.jpg -o output.pdf
```

## 3. Merging PDFs

```bash
# Merge multiple PDFs (using pdftk)
pdftk file1.pdf file2.pdf file3.pdf cat output merged.pdf

# Using ghostscript
gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=merged.pdf file1.pdf file2.pdf

# Using pdfunite
pdfunite file1.pdf file2.pdf output.pdf
```

## 4. Splitting PDFs

```bash
# Split into individual pages
pdftk input.pdf burst output page_%02d.pdf

# Extract specific pages
pdftk input.pdf cat 1-5 output first-5-pages.pdf

# Extract page ranges
pdftk input.pdf cat 1-10 25-30 output selected.pdf
```

## 5. Converting PDFs

**PDF to Images**:
```bash
# To PNG (high quality)
pdftoppm -png -r 300 input.pdf output

# To JPG
pdftoppm -jpeg -r 150 input.pdf output

# Specific pages
pdftoppm -png -f 1 -l 5 input.pdf output
```

**PDF to DOCX**:
```bash
# Using libreoffice
libreoffice --headless --convert-to docx input.pdf

# Using pandoc
pandoc input.pdf -o output.docx
```

**PDF to Text**:
```bash
# Simple conversion
pdftotext input.pdf output.txt

# Maintain layout
pdftotext -layout input.pdf output.txt
```

## 6. PDF Analysis & Information

**Get page count**:
```bash
pdfinfo document.pdf | grep "Pages:" | awk '{print $2}'
```

**Check PDF version**:
```bash
pdfinfo document.pdf | grep "PDF version"
```

**Analyze structure**:
```bash
# Get detailed structure
mutool show input.pdf outline

# Extract fonts
pdffonts input.pdf
```

## 7. PDF Optimization

**Compress PDF**:
```bash
# Using ghostscript (screen quality - smallest)
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen \
   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=compressed.pdf input.pdf

# Using ghostscript (ebook quality - medium)
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=compressed.pdf input.pdf
```

**Remove password**:
```bash
# If you know the password
pdftk secured.pdf input_pw PASSWORD output unsecured.pdf
```

## 8. Common Workflows

### Extract tables from PDF
```bash
# Using tabula-py
tabula-py input.pdf --output-format csv --pages all

# Or use pdfplumber for complex tables
```

### Add watermark
```bash
pdftk input.pdf stamp watermark.pdf output watermarked.pdf
```

### Rotate pages
```bash
# Rotate all pages 90 degrees clockwise
pdftk input.pdf cat 1-endright output rotated.pdf

# Rotate specific pages
pdftk input.pdf cat 1-5 6right 7-end output rotated.pdf
```

## Tools Required

Make sure these tools are installed:
- `poppler-utils` (pdftotext, pdfinfo, pdftoppm, pdfunite)
- `pdftk` or `pdftk-java`
- `ghostscript` (gs)
- `imagemagick` (convert)
- `pandoc` (for conversions)
- `img2pdf` (for image to PDF)
- `exiftool` (for metadata)

Install on Ubuntu/Debian:
```bash
sudo apt-get install poppler-utils pdftk ghostscript imagemagick pandoc python3-img2pdf exiftool
```

## Security Notes

- ✅ Always validate PDF file paths before processing
- ✅ Check file sizes to prevent resource exhaustion
- ✅ Sanitize output filenames
- ✅ Be cautious with password-protected PDFs
- ✅ Scan PDFs for malicious content if from untrusted sources

## When to Use This Skill

Use `/pdf` when the user:
- Wants to read or extract text from a PDF
- Needs to create a PDF from other formats
- Wants to merge or split PDFs
- Needs to convert PDFs to images or other formats
- Asks to analyze PDF structure or metadata
- Wants to compress or optimize PDFs

Always confirm destructive operations before executing.
