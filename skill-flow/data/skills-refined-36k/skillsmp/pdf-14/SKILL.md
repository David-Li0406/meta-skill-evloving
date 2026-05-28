---
name: pdf
description: |
  このスキルは、ユーザーが「PDFを作成」「PDFからテキストを抽出」「PDFを結合」「PDFフォームに記入」「PDFを分割」「PDFからテーブルを抽出」「PDF OCR」「PDFを暗号化」「PDFメタデータを編集」などを要求した際に使用する。
---

# PDF処理スキル

PDFファイルの操作に必要なPythonライブラリとコマンドラインツールを提供する。

## 依存関係

```bash
# コマンドラインツール
brew install poppler qpdf  # macOS
apt-get install poppler-utils qpdf  # Ubuntu/Debian

# Pythonライブラリ
pip install pypdf pdfplumber reportlab pdf2image pillow pytesseract
```

## 主要操作

### テキスト抽出

```bash
# レイアウトを保持してテキスト抽出
pdftotext -layout input.pdf output.txt
```

```python
import pdfplumber

with pdfplumber.open("input.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

### テーブル抽出

```python
import pdfplumber
import pandas as pd

with pdfplumber.open("input.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            df = pd.DataFrame(table[1:], columns=table[0])
            print(df)
```

### PDF作成

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 日本語フォント登録（必要に応じて）
# pdfmetrics.registerFont(TTFont('IPAGothic', '/path/to/ipag.ttf'))

c = canvas.Canvas("output.pdf", pagesize=A4)
c.drawString(100, 750, "Hello, PDF!")
c.save()
```

### PDF結合

```bash
qpdf --empty --pages input1.pdf input2.pdf -- merged.pdf
```

```python
from pypdf import PdfWriter

writer = PdfWriter()
writer.append("input1.pdf")
writer.append("input2.pdf")
writer.write("merged.pdf")
```

### PDF分割

```bash
# 各ページを個別ファイルに
qpdf input.pdf --split-pages output_%d.pdf

# 特定ページを抽出
qpdf input.pdf --pages . 1-3,5 -- output.pdf
```

### 画像抽出

```bash
pdfimages -j input.pdf output_prefix
```

### OCR（スキャン文書）

```python
from pdf2image import convert_from_path
import pytesseract

images = convert_from_path("scanned.pdf")
for i, image in enumerate(images):
    text = pytesseract.image_to_string(image, lang='jpn')  # 日本語
    print(f"Page {i+1}:\n{text}")
```

## フォーム処理

PDFフォームの記入方法は `references/forms.md` を参照。2つのパスがある：

1. **フィル可能フィールドがある場合**: `scripts/check_fillable_fields.py` で確認後、`scripts/fill_fillable_fields.py` を使用
2. **フィル可能フィールドがない場合**: 画像解析でフィールド位置を特定し、`scripts/fill_pdf_form_with_annotations.py` でアノテーションとして追加

## 詳細リファレンス

- 高度なライブラリ使用法: `references/advanced-reference.md`
- フォーム記入ワークフロー: `references/forms.md`

## クイックリファレンス

| 操作 | ツール/コマンド |
|------|----------------|
| テキスト抽出 | `pdftotext`, `pdfplumber` |
| テーブル抽出 | `pdfplumber` |
| PDF作成 | `reportlab` |
| 結合 | `qpdf`, `pypdf` |
| 分割 | `qpdf` |
| 画像抽出 | `pdfimages` |
| OCR | `pytesseract` + `pdf2image` |
| フォーム記入 | `scripts/` 内のスクリプト |
| 暗号化/復号 | `qpdf` |
| メタデータ | `pypdf` |
