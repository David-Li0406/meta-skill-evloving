---
name: pdf-processing
description: Use this skill when you need to read, create, modify, or analyze PDF documents.
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
pdfinfo document.pdf | grep Pages
```

## Key Libraries

| Task | Library | Install |
|------|---------|---------|
| Read/Write/Merge | PyMuPDF | `pip install pymupdf` |
| Create from scratch | ReportLab | `pip install reportlab` |
| HTML to PDF | pdfkit | `pip install pdfkit` + wkhtmltopdf |
| Text extraction | pdftotext | `brew install poppler` / `apt install poppler-utils` |

## Best Practices

1. **Always check if tools are installed** before using them.
2. **Handle encoding issues** - PDFs may contain various character encodings.
3. **Large PDFs**: Process page by page to avoid memory issues.