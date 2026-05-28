---
name: pdf
description: 全面的 PDF 操作工具包，用於擷取文字和表格、建立新 PDF、合併/分割文件，以及處理表單。當 Claude 需要填寫 PDF 表單或以程式化方式處理、產生或大規模分析 PDF 文件時使用。
license: Proprietary. LICENSE.txt has complete terms
---

# PDF 處理指南

## 概述

本指南涵蓋使用 Python 函式庫和命令列工具的基本 PDF 處理操作。如需進階功能、JavaScript 函式庫和詳細範例，請參閱 reference.md。如果您需要填寫 PDF 表單，請閱讀 forms.md 並遵循其說明。

## 快速開始

```python
from pypdf import PdfReader, PdfWriter

# 讀取 PDF
reader = PdfReader("document.pdf")
print(f"頁數: {len(reader.pages)}")

# 擷取文字
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Python 函式庫

### pypdf - 基本操作

#### 合併 PDF
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

#### 分割 PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

#### 擷取中繼資料
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"標題: {meta.title}")
print(f"作者: {meta.author}")
print(f"主題: {meta.subject}")
print(f"建立者: {meta.creator}")
```

#### 旋轉頁面
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # 順時針旋轉 90 度
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### pdfplumber - 文字和表格擷取

#### 擷取含版面配置的文字
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### 擷取表格
```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"第 {i+1} 頁的表格 {j+1}:")
            for row in table:
                print(row)
```

#### 進階表格擷取
```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # 檢查表格是否不為空
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# 合併所有表格
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

### reportlab - 建立 PDF

#### 基本 PDF 建立
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

# 新增文字
c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "這是使用 reportlab 建立的 PDF")

# 新增線條
c.line(100, height - 140, 400, height - 140)

# 儲存
c.save()
```

#### 建立多頁 PDF
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# 新增內容
title = Paragraph("報告標題", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("這是報告的內文。" * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

# 第 2 頁
story.append(Paragraph("第 2 頁", styles['Heading1']))
story.append(Paragraph("第 2 頁的內容", styles['Normal']))

# 建置 PDF
doc.build(story)
```

## 命令列工具

### pdftotext (poppler-utils)
```bash
# 擷取文字
pdftotext input.pdf output.txt

# 擷取文字並保留版面配置
pdftotext -layout input.pdf output.txt

# 擷取特定頁面
pdftotext -f 1 -l 5 input.pdf output.txt  # 第 1-5 頁
```

### qpdf
```bash
# 合併 PDF
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# 分割頁面
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf

# 旋轉頁面
qpdf input.pdf output.pdf --rotate=+90:1  # 將第 1 頁旋轉 90 度

# 移除密碼
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### pdftk（如果可用）
```bash
# 合併
pdftk file1.pdf file2.pdf cat output merged.pdf

# 分割
pdftk input.pdf burst

# 旋轉
pdftk input.pdf rotate 1east output rotated.pdf
```

## 常見任務

### 從掃描 PDF 擷取文字
```python
# 需要：pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

# 將 PDF 轉換為圖片
images = convert_from_path('scanned.pdf')

# 對每頁進行 OCR
text = ""
for i, image in enumerate(images):
    text += f"第 {i+1} 頁:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

### 新增浮水印
```python
from pypdf import PdfReader, PdfWriter

# 建立浮水印（或載入現有的）
watermark = PdfReader("watermark.pdf").pages[0]

# 套用到所有頁面
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### 擷取圖片
```bash
# 使用 pdfimages (poppler-utils)
pdfimages -j input.pdf output_prefix

# 這會將所有圖片擷取為 output_prefix-000.jpg、output_prefix-001.jpg 等
```

### 密碼保護
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# 新增密碼
writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

## 快速參考

| 任務 | 最佳工具 | 指令/程式碼 |
|------|-----------|--------------|
| 合併 PDF | pypdf | `writer.add_page(page)` |
| 分割 PDF | pypdf | 每頁一個檔案 |
| 擷取文字 | pdfplumber | `page.extract_text()` |
| 擷取表格 | pdfplumber | `page.extract_tables()` |
| 建立 PDF | reportlab | Canvas 或 Platypus |
| 命令列合併 | qpdf | `qpdf --empty --pages ...` |
| OCR 掃描 PDF | pytesseract | 先轉換為圖片 |
| 填寫 PDF 表單 | pdf-lib 或 pypdf（見 forms.md） | 見 forms.md |

## 下一步

- 如需進階 pypdfium2 用法，請參閱 reference.md
- 如需 JavaScript 函式庫（pdf-lib），請參閱 reference.md
- 如果需要填寫 PDF 表單，請遵循 forms.md 中的說明
- 如需疑難排解指南，請參閱 reference.md
