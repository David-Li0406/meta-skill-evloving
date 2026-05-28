---
name: pdf-processing
description: Use this skill when you need to read, create, modify, merge, split, or analyze PDF documents.
---

# PDF Processing Skill

You now have expertise in PDF manipulation. Follow these workflows:

## 1. Reading & Extracting from PDFs

### Text Extraction
```bash
# Extract all text
pdftotext input.pdf output.txt

# Extract specific pages
pdftotext -f <first_page> -l <last_page> input.pdf output.txt

# Preserve layout
pdftotext -layout input.pdf output.txt
```

### Extracting Images
```bash
# Extract all images
pdfimages -all input.pdf output_prefix

# Extract as PNG
pdfimages -png input.pdf images/page
```

### Metadata
```bash
# Get PDF info
pdfinfo document.pdf

# Get detailed metadata
exiftool document.pdf
```

## 2. Creating PDFs

### From Text/Markdown
```bash
# From markdown using pandoc
pandoc input.md -o output.pdf

# From text with formatting
enscript input.txt -o - | ps2pdf - output.pdf
```

### From HTML
```bash
# Using wkhtmltopdf
wkhtmltopdf input.html output.pdf

# With options
wkhtmltopdf --page-size A4 --margin-top 10mm input.html output.pdf
```

### From Images
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
pdftk input.pdf cat <page_range> output selected.pdf
```

## 5. Converting PDFs

### PDF to Images
```bash
# To PNG (high quality)
pdftoppm -png -r 300 input.pdf output

# To JPG
pdftoppm -jpeg -r 150 input.pdf output
```

### PDF to DOCX
```bash
# Using libreoffice
libreoffice --headless --convert-to docx input.pdf

# Using pandoc
pandoc input.pdf -o output.docx
```

### PDF to Text
```bash
# Simple conversion
pdftotext input.pdf output.txt

# Maintain layout
pdftotext -layout input.pdf output.txt
```

## 6. PDF Analysis & Information

### Get Page Count
```bash
pdfinfo document.pdf | grep "Pages:" | awk '{print $2}'
```

### Check PDF Version
```bash
pdfinfo document.pdf | grep "PDF version"
```

### Analyze Structure
```bash
# Get detailed structure
mutool show input.pdf outline

# Extract fonts
pdffonts input.pdf
```

## 7. PDF Optimization

### Compress PDF
```bash
# Using ghostscript (screen quality - smallest)
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen \
   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=compressed.pdf input.pdf
```

### Remove Password
```bash
# If you know the password
pdftk secured.pdf input_pw PASSWORD output unsecured.pdf
```

## 8. Common Workflows

### Extract Tables from PDF
```bash
# Using tabula-py
tabula-py input.pdf --output-format csv --pages all

# Or use pdfplumber for complex tables
```

### Add Watermark
```bash
pdftk input.pdf stamp watermark.pdf output watermarked.pdf
```

### Rotate Pages
```bash
# Rotate all pages 90 degrees clockwise
pdftk input.pdf cat 1-endright output rotated.pdf
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

Use this skill when the user:
- Wants to read or extract text from a PDF
- Needs to create a PDF from other formats
- Wants to merge or split PDFs
- Needs to convert PDFs to images or other formats
- Asks to analyze PDF structure or metadata
- Wants to compress or optimize PDFs

Always confirm destructive operations before executing.