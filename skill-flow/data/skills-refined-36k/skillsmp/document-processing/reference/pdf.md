# PDF操作ガイド

## 目次
- テキスト抽出
- 表抽出
- PDF作成
- PDF編集
- フォーム操作
- OCR

## テキスト抽出

### pdfplumber（推奨）

```python
import pdfplumber

def extract_text(pdf_path: str) -> str:
    """PDFからテキストを抽出"""
    text_parts = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    
    return "\n\n".join(text_parts)
```

### PyMuPDF（高速）

```python
import fitz  # PyMuPDF

def extract_text_fast(pdf_path: str) -> str:
    """高速テキスト抽出"""
    doc = fitz.open(pdf_path)
    text = ""
    
    for page in doc:
        text += page.get_text()
    
    doc.close()
    return text
```

## 表抽出

### pdfplumberで表抽出

```python
import pdfplumber
import pandas as pd

def extract_tables(pdf_path: str) -> list[pd.DataFrame]:
    """PDFから表を抽出"""
    tables = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_tables = page.extract_tables()
            for table in page_tables:
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    tables.append(df)
    
    return tables
```

### Camelotで高精度抽出

```python
import camelot

def extract_tables_precise(pdf_path: str, pages: str = "all") -> list:
    """Camelotで高精度な表抽出"""
    # lattice: 罫線がある表
    tables = camelot.read_pdf(pdf_path, pages=pages, flavor="lattice")
    
    if len(tables) == 0:
        # stream: 罫線がない表
        tables = camelot.read_pdf(pdf_path, pages=pages, flavor="stream")
    
    return [table.df for table in tables]
```

## PDF作成

### reportlab

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

# 日本語フォント登録
pdfmetrics.registerFont(TTFont("IPAGothic", "/usr/share/fonts/truetype/ipag.ttf"))

def create_pdf(output_path: str, content: str):
    """シンプルなPDF作成"""
    c = canvas.Canvas(output_path, pagesize=A4)
    c.setFont("IPAGothic", 12)
    
    # テキスト描画
    y = 800
    for line in content.split("\n"):
        c.drawString(20*mm, y, line)
        y -= 15
        
        if y < 50:
            c.showPage()
            c.setFont("IPAGothic", 12)
            y = 800
    
    c.save()
```

### fpdf2（シンプル）

```python
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 15)
        self.cell(0, 10, "レポート", align="C", new_x="LMARGIN", new_y="NEXT")
    
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def create_report(output_path: str, title: str, content: str):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(output_path)
```

## PDF編集

### ページ操作

```python
import fitz

def merge_pdfs(pdf_paths: list[str], output_path: str):
    """複数PDFを結合"""
    result = fitz.open()
    
    for pdf_path in pdf_paths:
        doc = fitz.open(pdf_path)
        result.insert_pdf(doc)
        doc.close()
    
    result.save(output_path)
    result.close()

def split_pdf(pdf_path: str, output_dir: str):
    """PDFを1ページずつ分割"""
    import os
    
    doc = fitz.open(pdf_path)
    
    for i, page in enumerate(doc):
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=i, to_page=i)
        new_doc.save(os.path.join(output_dir, f"page_{i+1}.pdf"))
        new_doc.close()
    
    doc.close()

def extract_pages(pdf_path: str, pages: list[int], output_path: str):
    """特定ページを抽出"""
    doc = fitz.open(pdf_path)
    new_doc = fitz.open()
    
    for page_num in pages:
        new_doc.insert_pdf(doc, from_page=page_num-1, to_page=page_num-1)
    
    new_doc.save(output_path)
    new_doc.close()
    doc.close()
```

### テキスト追加

```python
def add_watermark(pdf_path: str, watermark_text: str, output_path: str):
    """透かしを追加"""
    doc = fitz.open(pdf_path)
    
    for page in doc:
        rect = page.rect
        text_point = fitz.Point(rect.width / 2, rect.height / 2)
        
        page.insert_text(
            text_point,
            watermark_text,
            fontsize=50,
            color=(0.8, 0.8, 0.8),
            rotate=45
        )
    
    doc.save(output_path)
    doc.close()
```

## フォーム操作

### フォーム読み取り

```python
import fitz

def get_form_fields(pdf_path: str) -> dict:
    """フォームフィールドを取得"""
    doc = fitz.open(pdf_path)
    fields = {}
    
    for page in doc:
        widgets = page.widgets()
        if widgets:
            for widget in widgets:
                fields[widget.field_name] = {
                    "type": widget.field_type_string,
                    "value": widget.field_value,
                    "rect": widget.rect
                }
    
    doc.close()
    return fields
```

### フォーム入力

```python
def fill_form(pdf_path: str, field_values: dict, output_path: str):
    """フォームに値を入力"""
    doc = fitz.open(pdf_path)
    
    for page in doc:
        widgets = page.widgets()
        if widgets:
            for widget in widgets:
                if widget.field_name in field_values:
                    widget.field_value = field_values[widget.field_name]
                    widget.update()
    
    doc.save(output_path)
    doc.close()
```

## OCR

### pytesseract

```python
from pdf2image import convert_from_path
import pytesseract

def ocr_pdf(pdf_path: str, lang: str = "jpn") -> str:
    """スキャンPDFのOCR"""
    images = convert_from_path(pdf_path)
    text_parts = []
    
    for image in images:
        text = pytesseract.image_to_string(image, lang=lang)
        text_parts.append(text)
    
    return "\n\n".join(text_parts)
```

### EasyOCR（高精度）

```python
import easyocr
from pdf2image import convert_from_path

def ocr_pdf_easyocr(pdf_path: str) -> str:
    """EasyOCRでOCR"""
    reader = easyocr.Reader(["ja", "en"])
    images = convert_from_path(pdf_path)
    
    text_parts = []
    for image in images:
        import numpy as np
        result = reader.readtext(np.array(image))
        page_text = " ".join([r[1] for r in result])
        text_parts.append(page_text)
    
    return "\n\n".join(text_parts)
```
