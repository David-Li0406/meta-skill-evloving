---
name: pdf-processing
description: PDF 处理工具集，支持文本提取、表格解析、合并拆分、表单填写。
当需要处理 PDF 文件、提取内容、转换格式时使用。
Use when extracting text/tables from PDFs, merging documents, or filling forms.
allowed-tools: "Bash,Read,Write,Edit"
---

# PDF Processing - PDF 处理

PDF 文件处理工具集，提取内容、合并拆分、表单操作。

## 🎯 功能概览

| 功能 | 工具 | 用途 |
|------|------|------|
| 文本提取 | `pdftotext` | 提取 PDF 文本内容 |
| 表格解析 | `pdfplumber` / `tabula-py` | 提取表格数据 |
| 合并文档 | `PyPDF4` / `pdftk` | 多个 PDF 合并为一个 |
| 拆分文档 | `PyPDF4` / `pdftk` | 一个 PDF 拆分为多个 |
| 表单填写 | `pdftk` / `PyPDF4` | 填写 PDF 表单字段 |
| 转换格式 | `libreoffice` | PDF ↔ 其他格式 |

---

## 📄 文本提取

### pdftotext（推荐）

```bash
# 基础提取
pdftotext document.pdf output.txt

# 保留布局
pdftotext -layout document.pdf output.txt

# 提取指定页码
pdftotext -f 1 -l 5 document.pdf output.txt

# 检查是否为扫描件（文本 < 50 字）
pdftotext document.pdf - | wc -c
```

### PDF 扫描件处理

```bash
# 文本少 → 可能是扫描件
pdftotext document.pdf - | head -c 50

# 使用 OCR
brew install tesseract
tesseract document.pdf output.txt
```

---

## 📊 表格解析

### pdfplumber（Python）

```python
import pdfplumber

# 提取所有表格
with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print(row)

# 提取指定区域
with pdfplumber.open("document.pdf") as pdf:
    page = pdf.pages[0]
    # x0, y0, x1, y1 (top, left, bottom, right)
    crop = page.crop((100, 100, 500, 300))
    table = crop.extract_table()
```

### tabula-py（Java 包装）

```bash
# 安装
pip install tabula-py

# 命令行使用
tabula document.pdf -o output.csv

# 指定页面和区域
tabula document.pdf -p 1 -a 100,100,500,300 -o output.csv
```

---

## 🔀 合并与拆分

### PyPDF4（Python）

```python
from PyPDF4 import PdfFileReader, PdfFileWriter

# 合并 PDF
def merge_pdfs(input_files, output_file):
    writer = PdfFileWriter()
    for file in input_files:
        reader = PdfFileReader(file)
        for page in reader.pages:
            writer.addPage(page)
    with open(output_file, 'wb') as f:
        writer.write(f)

# 拆分 PDF
def split_pdf(input_file, output_dir):
    reader = PdfFileReader(input_file)
    for i, page in enumerate(reader.pages):
        writer = PdfFileWriter()
        writer.addPage(page)
        with open(f"{output_dir}/page_{i+1}.pdf", 'wb') as f:
            writer.write(f)
```

### pdftk（命令行）

```bash
# 安装
brew install pdftk

# 合并
pdftk file1.pdf file2.pdf cat output merged.pdf

# 拆分（提取指定页）
pdftk input.pdf cat 1-5 output part1.pdf
pdftk input.pdf cat 6-end output part2.pdf

# 爆炸拆分（每页单独保存）
pdftk input.pdf burst output page_%02d.pdf
```

---

## 📝 表单填写

### pdftk 填写表单

```bash
# 1. 导出表单字段
pdftk form.pdf dump_data_fields output form_fields.txt

# 2. 创建填写文件 (fill.txt)
---
field1: value1
field2: value2
---

# 3. 填写表单
pdftk form.pdf fill_form fill.txt output filled.pdf

# 4. 压平（不可编辑）
pdftk filled.pdf output flattened.pdf
```

### PyPDF4 填写表单

```python
from PyPDF4 import PdfFileReader, PdfFileWriter

reader = PdfFileReader("form.pdf")
writer = PdfFileWriter()

# 复制页面并填写
page = reader.getPage(0)
writer.addPage(page)

# 更新字段
writer.updatePageFormFieldValues(writer.getPage(0), {
    'field1': 'value1',
    'field2': 'value2'
})

with open("filled.pdf", 'wb') as f:
    writer.write(f)
```

---

## 🔄 格式转换

### PDF → 图片

```bash
# 使用 ImageMagick
convert document.pdf page.png

# 指定 DPI 和质量
convert -density 300 -quality 90 document.pdf page.png
```

### PDF ↔ Word/Excel

```bash
# LibreOffice 转换
brew install libreoffice

# PDF → Word
soffice --headless --convert-to docx document.pdf

# PDF → Excel（需要表格数据）
soffice --headless --convert-to xlsx document.pdf
```

---

## 🧰 工具安装

```bash
# macOS
brew install poppler        # pdftotext, pdftk
brew install tesseract      # OCR
pip install pdfplumber PyPDF4 tabula-py

# Linux
apt-get install poppler-utils
apt-get install tesseract-ocr
pip3 install pdfplumber PyPDF4 tabula-py
```

---

## 与 deep-crawl 配合

```
deep-crawl              pdf-processing
   ↓                         ↓
爬取 PDF 文档          提取文本内容
   ↓                         ↓
发现更多 PDF            解析表格数据
   ↓                         ↓
汇总表格 ←──────────────────┘
```

---

## 常见触发场景

使用此技能时，你会听到：
- "提取 PDF 内容"
- "PDF 转文本"
- "合并 PDF"
- "解析 PDF 表格"
- "Extract PDF"
- "Parse PDF"
