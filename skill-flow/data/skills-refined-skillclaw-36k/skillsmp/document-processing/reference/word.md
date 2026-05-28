# Word操作ガイド

## 目次
- ドキュメント作成
- テキスト操作
- スタイル設定
- 表の操作
- 画像挿入
- テンプレート処理

## ドキュメント作成

### 基本的な作成

```python
from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_document():
    """基本的なWord文書を作成"""
    doc = Document()
    
    # タイトル
    title = doc.add_heading("レポートタイトル", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 段落
    p = doc.add_paragraph("これは本文テキストです。")
    p.add_run("太字テキスト").bold = True
    p.add_run("と")
    p.add_run("斜体テキスト").italic = True
    
    # 見出し
    doc.add_heading("セクション1", level=1)
    doc.add_paragraph("セクション1の内容です。")
    
    doc.add_heading("サブセクション", level=2)
    doc.add_paragraph("サブセクションの内容です。")
    
    # 箇条書き
    doc.add_paragraph("項目1", style="List Bullet")
    doc.add_paragraph("項目2", style="List Bullet")
    doc.add_paragraph("項目3", style="List Bullet")
    
    # 番号付きリスト
    doc.add_paragraph("手順1", style="List Number")
    doc.add_paragraph("手順2", style="List Number")
    doc.add_paragraph("手順3", style="List Number")
    
    doc.save("document.docx")
```

## テキスト操作

### 読み込み

```python
from docx import Document

def read_document(path: str) -> str:
    """Word文書からテキストを抽出"""
    doc = Document(path)
    
    text_parts = []
    for para in doc.paragraphs:
        text_parts.append(para.text)
    
    return "\n".join(text_parts)

def read_with_structure(path: str) -> list[dict]:
    """構造付きで読み込み"""
    doc = Document(path)
    
    content = []
    for para in doc.paragraphs:
        content.append({
            "text": para.text,
            "style": para.style.name,
            "alignment": str(para.alignment)
        })
    
    return content
```

### 検索・置換

```python
from docx import Document

def find_and_replace(path: str, replacements: dict, output_path: str):
    """テキストを検索・置換"""
    doc = Document(path)
    
    for para in doc.paragraphs:
        for old_text, new_text in replacements.items():
            if old_text in para.text:
                # 段落全体を置換
                for run in para.runs:
                    if old_text in run.text:
                        run.text = run.text.replace(old_text, new_text)
    
    # テーブル内も検索
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for old_text, new_text in replacements.items():
                        if old_text in para.text:
                            for run in para.runs:
                                run.text = run.text.replace(old_text, new_text)
    
    doc.save(output_path)
```

## スタイル設定

```python
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.style import WD_STYLE_TYPE

def apply_styles():
    """スタイルを適用"""
    doc = Document()
    
    # カスタムスタイル作成
    styles = doc.styles
    custom_style = styles.add_style("CustomHeading", WD_STYLE_TYPE.PARAGRAPH)
    custom_style.font.name = "Arial"
    custom_style.font.size = Pt(16)
    custom_style.font.bold = True
    custom_style.font.color.rgb = RGBColor(0, 0, 128)
    
    # スタイル適用
    doc.add_paragraph("カスタム見出し", style="CustomHeading")
    
    # 直接フォント設定
    p = doc.add_paragraph()
    run = p.add_run("カスタムフォントテキスト")
    run.font.name = "游ゴシック"
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(255, 0, 0)
    
    doc.save("styled.docx")
```

## 表の操作

### 表の作成

```python
from docx import Document
from docx.shared import Inches, Cm
from docx.enum.table import WD_TABLE_ALIGNMENT

def create_table(data: list[list], headers: list[str], output_path: str):
    """表を作成"""
    doc = Document()
    
    # 表作成
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # ヘッダー行
    header_row = table.rows[0]
    for i, header in enumerate(headers):
        cell = header_row.cells[i]
        cell.text = header
        # ヘッダースタイル
        for para in cell.paragraphs:
            for run in para.runs:
                run.bold = True
    
    # データ行
    for row_data in data:
        row = table.add_row()
        for i, value in enumerate(row_data):
            row.cells[i].text = str(value)
    
    # 列幅設定
    for col in table.columns:
        for cell in col.cells:
            cell.width = Cm(3)
    
    doc.save(output_path)
```

### 表の読み込み

```python
import pandas as pd
from docx import Document

def read_tables(path: str) -> list[pd.DataFrame]:
    """Word文書から表を読み込み"""
    doc = Document(path)
    tables = []
    
    for table in doc.tables:
        data = []
        for row in table.rows:
            row_data = [cell.text for cell in row.cells]
            data.append(row_data)
        
        if data:
            df = pd.DataFrame(data[1:], columns=data[0])
            tables.append(df)
    
    return tables
```

## 画像挿入

```python
from docx import Document
from docx.shared import Inches

def insert_image(doc_path: str, image_path: str, output_path: str):
    """画像を挿入"""
    doc = Document(doc_path)
    
    # 画像挿入
    doc.add_picture(image_path, width=Inches(4))
    
    # キャプション
    doc.add_paragraph("図1: 画像の説明", style="Caption")
    
    doc.save(output_path)
```

## テンプレート処理

### Jinja2テンプレート

```python
from docx import Document
from jinja2 import Template
import re

def fill_template(template_path: str, data: dict, output_path: str):
    """テンプレートにデータを埋め込み"""
    doc = Document(template_path)
    
    # プレースホルダーパターン: {{変数名}}
    pattern = r"\{\{(\w+)\}\}"
    
    for para in doc.paragraphs:
        if re.search(pattern, para.text):
            # 段落内のすべてのrunを結合
            full_text = "".join(run.text for run in para.runs)
            
            # テンプレート処理
            template = Template(full_text)
            new_text = template.render(data)
            
            # 最初のrunに結果を設定、他はクリア
            if para.runs:
                para.runs[0].text = new_text
                for run in para.runs[1:]:
                    run.text = ""
    
    # テーブル内も処理
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    if re.search(pattern, para.text):
                        full_text = "".join(run.text for run in para.runs)
                        template = Template(full_text)
                        new_text = template.render(data)
                        
                        if para.runs:
                            para.runs[0].text = new_text
                            for run in para.runs[1:]:
                                run.text = ""
    
    doc.save(output_path)

# 使用例
data = {
    "company_name": "株式会社サンプル",
    "date": "2025年1月15日",
    "amount": "1,000,000",
    "customer_name": "田中太郎"
}
fill_template("template.docx", data, "output.docx")
```

### python-docx-template（推奨）

```python
from docxtpl import DocxTemplate

def fill_template_advanced(template_path: str, data: dict, output_path: str):
    """高度なテンプレート処理"""
    doc = DocxTemplate(template_path)
    
    # コンテキストとしてデータを渡す
    doc.render(data)
    doc.save(output_path)

# テンプレート例（template.docx内）:
# {{ company_name }} 御中
# 
# 請求日: {{ date }}
# 
# {% for item in items %}
# - {{ item.name }}: ¥{{ item.price }}
# {% endfor %}
# 
# 合計: ¥{{ total }}

data = {
    "company_name": "株式会社サンプル",
    "date": "2025-01-15",
    "items": [
        {"name": "商品A", "price": "10,000"},
        {"name": "商品B", "price": "20,000"},
    ],
    "total": "30,000"
}
```
