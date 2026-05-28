# PDF処理 詳細リファレンス

## Pythonライブラリ

### pypdfium2（高速レンダリング）

```python
import pypdfium2 as pdfium
from PIL import Image

# PDFを開く
pdf = pdfium.PdfDocument("input.pdf")

# ページを画像にレンダリング
for i, page in enumerate(pdf):
    bitmap = page.render(scale=2)  # 2倍スケール
    pil_image = bitmap.to_pil()
    pil_image.save(f"page_{i+1}.png")
```

### pdfplumber（詳細テキスト抽出）

```python
import pdfplumber

with pdfplumber.open("input.pdf") as pdf:
    page = pdf.pages[0]

    # 文字単位の座標情報
    chars = page.chars
    for char in chars:
        print(f"{char['text']} at ({char['x0']}, {char['top']})")

    # カスタム設定でテーブル抽出
    table_settings = {
        "vertical_strategy": "text",
        "horizontal_strategy": "text",
        "snap_tolerance": 3,
        "join_tolerance": 3,
    }
    tables = page.extract_tables(table_settings)
```

### reportlab（プロフェッショナル文書作成）

```python
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

doc = SimpleDocTemplate("report.pdf", pagesize=A4)
data = [
    ["ヘッダー1", "ヘッダー2", "ヘッダー3"],
    ["データ1", "データ2", "データ3"],
    ["データ4", "データ5", "データ6"],
]

table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

doc.build([table])
```

### pypdf（暗号化・ページ操作）

```python
from pypdf import PdfReader, PdfWriter

# パスワード保護されたPDFを開く
reader = PdfReader("encrypted.pdf")
if reader.is_encrypted:
    reader.decrypt("password")

# ページをクロップ
writer = PdfWriter()
page = reader.pages[0]
page.mediabox.upper_right = (400, 400)  # ポイント単位
writer.add_page(page)
writer.write("cropped.pdf")
```

## JavaScriptライブラリ

### pdf-lib（PDF操作）

```javascript
import { PDFDocument, StandardFonts, rgb } from 'pdf-lib';

async function createPdf() {
    const pdfDoc = await PDFDocument.create();
    const page = pdfDoc.addPage([595, 842]); // A4サイズ
    const font = await pdfDoc.embedFont(StandardFonts.Helvetica);

    page.drawText('Hello, World!', {
        x: 50,
        y: 750,
        size: 24,
        font: font,
        color: rgb(0, 0, 0),
    });

    const pdfBytes = await pdfDoc.save();
    return pdfBytes;
}

// PDFの結合
async function mergePdfs(pdf1Bytes, pdf2Bytes) {
    const pdfDoc = await PDFDocument.create();
    const pdf1 = await PDFDocument.load(pdf1Bytes);
    const pdf2 = await PDFDocument.load(pdf2Bytes);

    const pages1 = await pdfDoc.copyPages(pdf1, pdf1.getPageIndices());
    const pages2 = await pdfDoc.copyPages(pdf2, pdf2.getPageIndices());

    pages1.forEach(page => pdfDoc.addPage(page));
    pages2.forEach(page => pdfDoc.addPage(page));

    return await pdfDoc.save();
}
```

### pdfjs-dist（ブラウザレンダリング）

```javascript
import * as pdfjsLib from 'pdfjs-dist';

async function renderPage(pdfUrl, pageNum, canvas) {
    const pdf = await pdfjsLib.getDocument(pdfUrl).promise;
    const page = await pdf.getPage(pageNum);

    const viewport = page.getViewport({ scale: 1.5 });
    const context = canvas.getContext('2d');
    canvas.height = viewport.height;
    canvas.width = viewport.width;

    await page.render({
        canvasContext: context,
        viewport: viewport,
    }).promise;
}

// テキスト抽出
async function extractText(pdfUrl) {
    const pdf = await pdfjsLib.getDocument(pdfUrl).promise;
    let fullText = '';

    for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const textContent = await page.getTextContent();
        const pageText = textContent.items.map(item => item.str).join(' ');
        fullText += pageText + '\n';
    }

    return fullText;
}
```

## コマンドラインツール

### poppler-utils

```bash
# バウンディングボックス付きテキスト抽出
pdftotext -bbox-layout input.pdf output.html

# 高解像度で画像変換
pdftoppm -r 300 -png input.pdf output

# 埋め込み画像を抽出
pdfimages -all input.pdf output
```

### qpdf

```bash
# 複雑なページ抽出
qpdf input.pdf --pages . 1,3,5-7 -- output.pdf

# 複数PDFから特定ページを抽出して結合
qpdf --empty --pages file1.pdf 1-3 file2.pdf 5,7 -- combined.pdf

# ストリーミング用に最適化（線形化）
qpdf --linearize input.pdf output.pdf

# 暗号化
qpdf --encrypt user_pass owner_pass 256 \
    --modify=none --extract=n -- input.pdf encrypted.pdf

# 破損PDFの修復
qpdf --qdf --object-streams=disable damaged.pdf repaired.pdf
```

## パフォーマンス最適化

### 大容量ファイル処理

```python
# ストリーミング処理
from pypdf import PdfReader, PdfWriter

reader = PdfReader("large.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    writer.write(f"page_{i+1}.pdf")
    # メモリ解放
    del writer
```

### バッチ処理

```python
import os
from concurrent.futures import ProcessPoolExecutor

def process_pdf(pdf_path):
    try:
        # 処理ロジック
        return {"status": "success", "file": pdf_path}
    except Exception as e:
        return {"status": "error", "file": pdf_path, "error": str(e)}

pdf_files = [f for f in os.listdir(".") if f.endswith(".pdf")]

with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_pdf, pdf_files))
```

## トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| 日本語が文字化け | フォントを明示的に指定、`pdftotext -enc UTF-8` |
| テーブル抽出が不正確 | `pdfplumber` の `table_settings` を調整 |
| メモリ不足 | ページ単位で処理、ストリーミング使用 |
| OCR精度が低い | DPIを上げる、前処理で画像を鮮明化 |
| 暗号化PDFが開けない | `qpdf --decrypt` でまず復号化 |
