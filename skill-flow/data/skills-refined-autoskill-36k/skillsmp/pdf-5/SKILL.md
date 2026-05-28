---
name: pdf
description: Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When Claude needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale.
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Processing Guide

## Overview

This guide covers essential PDF processing operations using Python libraries and command-line tools. For advanced features, JavaScript libraries, and detailed examples, see reference.md. If you need to fill out a PDF form, read forms.md and follow its instructions.

## Quick Start

```python
from pypdf import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Python Libraries

### pypdf - Basic Operations

#### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

#### Split PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

#### Extract Metadata
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

#### Rotate Pages
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### pdfplumber - Text and Table Extraction

#### Extract Text with Layout
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### Extract Tables
```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

#### Advanced Table Extraction
```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # Check if table is not empty
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Combine all tables
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

### reportlab - Create PDFs

#### Basic PDF Creation
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

# Add text
c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")

# Add a line
c.line(100, height - 140, 400, height - 140)

# Save
c.save()
```

#### Create PDF with Multiple Pages
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add content
title = Paragraph("Report Title", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("This is the body of the report. " * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

# Page 2
story.append(Paragraph("Page 2", styles['Heading1']))
story.append(Paragraph("Content for page 2", styles['Normal']))

# Build PDF
doc.build(story)
```

#### 支持中文

```python
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT
import os

# 尝试多个可能的字体路径
font_candidates = [
    '/System/Library/Fonts/PingFang.ttc',
    '/System/Library/Fonts/Supplemental/Songti.ttc',
    '/System/Library/Fonts/Supplemental/STSong.ttf',
    '/System/Library/Fonts/Supplemental/Kaiti.ttc',
    '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
    '/Library/Fonts/Arial Unicode.ttf',
]

font_registered = False
for font_path in font_candidates:
    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
            print(f"✓ 成功加载字体: {font_path}")
            font_registered = True
            break
        except Exception as e:
            print(f"✗ 尝试加载 {font_path} 失败: {e}")

if not font_registered:
    print("\n❌ 未找到可用字体，请运行字体查找代码")
    print("或手动指定字体路径")
    exit(1)

# Create PDF
doc = SimpleDocTemplate("红腹锦鸡保护报告.pdf", pagesize=letter)
styles = getSampleStyleSheet()

# 创建支持中文的样式
styles.add(ParagraphStyle(
    name='ChineseTitle', 
    fontName='ChineseFont', 
    fontSize=24, 
    leading=30,
    alignment=TA_LEFT
))

styles.add(ParagraphStyle(
    name='ChineseHeading', 
    fontName='ChineseFont', 
    fontSize=16, 
    leading=20
))

styles.add(ParagraphStyle(
    name='ChineseNormal', 
    fontName='ChineseFont', 
    fontSize=12, 
    leading=18
))

story = []

# Title
story.append(Paragraph("红腹锦鸡保护报告", styles['ChineseTitle']))
story.append(Spacer(1, 12))

# 1. 红腹锦鸡的基本介绍
story.append(Paragraph("1. 红腹锦鸡的基本介绍", styles['ChineseHeading']))
story.append(Paragraph("红腹锦鸡（学名：Chrysolophus pictus），又名金鸡，是一种美丽的鸟类，属于雉科。雄性红腹锦鸡羽毛鲜艳，头部有金黄色羽冠，颈部和胸部呈橙红色，背部为绿色，尾羽长而华丽。雌性则较为朴素，全身以褐色为主，便于隐蔽。红腹锦鸡主要分布于中国中部和西南部山区，栖息于海拔1000-2500米的森林和灌木丛中。", styles['ChineseNormal']))
story.append(Spacer(1, 12))

# 2. 现存种群数量
story.append(Paragraph("2. 现存种群数量", styles['ChineseHeading']))
story.append(Paragraph("根据近年来的调查数据，红腹锦鸡的野生种群数量约为10,000至20,000只。由于栖息地破坏和非法捕猎，种群数量呈下降趋势。", styles['ChineseNormal']))
story.append(Spacer(1, 12))

# 3. 保护现状
story.append(Paragraph("3. 保护现状", styles['ChineseHeading']))
story.append(Paragraph("红腹锦鸡被列为中国国家一级保护动物，并被列入《世界自然保护联盟》（IUCN）濒危物种红色名录中的'近危'（NT）等级。中国已建立多个自然保护区，如四川卧龙自然保护区、贵州梵净山自然保护区等，以保护红腹锦鸡及其栖息地。", styles['ChineseNormal']))
story.append(Spacer(1, 12))

# 4. 繁殖生物学特性
story.append(Paragraph("4. 繁殖生物学特性", styles['ChineseHeading']))
story.append(Paragraph("红腹锦鸡的繁殖期为每年4月至6月。雄性通过展示华丽的羽毛和舞蹈来吸引雌性。雌性每次产卵4-8枚，孵化期约为22-24天。雏鸟为早成鸟，出生后不久即可跟随母鸟活动。", styles['ChineseNormal']))
story.append(Spacer(1, 12))

# 5. 主要威胁因素
story.append(Paragraph("5. 主要威胁因素", styles['ChineseHeading']))
story.append(Paragraph("红腹锦鸡面临的主要威胁包括：<br/>- 栖息地破坏：森林砍伐和农业开发导致栖息地减少。<br/>- 非法捕猎：因其羽毛美丽，常被非法捕猎用于装饰或贸易。<br/>- 气候变化：气候变化可能影响其栖息环境和食物来源。", styles['ChineseNormal']))

# Build PDF
doc.build(story)
print("\n✓ PDF 生成成功！")
```



## Command-Line Tools

### pdftotext (poppler-utils)
```bash
# Extract text
pdftotext input.pdf output.txt

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt  # Pages 1-5
```

### qpdf
```bash
# Merge PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf

# Rotate pages
qpdf input.pdf output.pdf --rotate=+90:1  # Rotate page 1 by 90 degrees

# Remove password
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### pdftk (if available)
```bash
# Merge
pdftk file1.pdf file2.pdf cat output merged.pdf

# Split
pdftk input.pdf burst

# Rotate
pdftk input.pdf rotate 1east output rotated.pdf
```

## Common Tasks

### Extract Text from Scanned PDFs
```python
# Requires: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path('scanned.pdf')

# OCR each page
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

### Add Watermark
```python
from pypdf import PdfReader, PdfWriter

# Create watermark (or load existing)
watermark = PdfReader("watermark.pdf").pages[0]

# Apply to all pages
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Extract Images
```bash
# Using pdfimages (poppler-utils)
pdfimages -j input.pdf output_prefix

# This extracts all images as output_prefix-000.jpg, output_prefix-001.jpg, etc.
```

### Password Protection
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# Add password
writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

## Quick Reference

| Task               | Best Tool                       | Command/Code               |
| ------------------ | ------------------------------- | -------------------------- |
| Merge PDFs         | pypdf                           | `writer.add_page(page)`    |
| Split PDFs         | pypdf                           | One page per file          |
| Extract text       | pdfplumber                      | `page.extract_text()`      |
| Extract tables     | pdfplumber                      | `page.extract_tables()`    |
| Create PDFs        | reportlab                       | Canvas or Platypus         |
| Command line merge | qpdf                            | `qpdf --empty --pages ...` |
| OCR scanned PDFs   | pytesseract                     | Convert to image first     |
| Fill PDF forms     | pdf-lib or pypdf (see forms.md) | See forms.md               |

## Next Steps

- For advanced pypdfium2 usage, see reference.md
- For JavaScript libraries (pdf-lib), see reference.md
- If you need to fill out a PDF form, follow the instructions in forms.md
- For troubleshooting guides, see reference.md
