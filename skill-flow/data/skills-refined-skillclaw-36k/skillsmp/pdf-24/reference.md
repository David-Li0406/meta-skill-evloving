# PDF 處理進階參考

本文件包含主要技能說明中未涵蓋的進階 PDF 處理功能、詳細範例和其他函式庫。

## pypdfium2 函式庫（Apache/BSD 授權）

### 概述
pypdfium2 是 PDFium（Chromium 的 PDF 函式庫）的 Python 繫結。它非常適合快速 PDF 渲染、圖片產生，並可作為 PyMuPDF 的替代品。

### 將 PDF 渲染為圖片
```python
import pypdfium2 as pdfium
from PIL import Image

# 載入 PDF
pdf = pdfium.PdfDocument("document.pdf")

# 將頁面渲染為圖片
page = pdf[0]  # 第一頁
bitmap = page.render(
    scale=2.0,  # 較高解析度
    rotation=0  # 不旋轉
)

# 轉換為 PIL Image
img = bitmap.to_pil()
img.save("page_1.png", "PNG")

# 處理多頁
for i, page in enumerate(pdf):
    bitmap = page.render(scale=1.5)
    img = bitmap.to_pil()
    img.save(f"page_{i+1}.jpg", "JPEG", quality=90)
```

### 使用 pypdfium2 擷取文字
```python
import pypdfium2 as pdfium

pdf = pdfium.PdfDocument("document.pdf")
for i, page in enumerate(pdf):
    text = page.get_text()
    print(f"第 {i+1} 頁文字長度: {len(text)} 字元")
```

## JavaScript 函式庫

### pdf-lib（MIT 授權）

pdf-lib 是一個強大的 JavaScript 函式庫，可在任何 JavaScript 環境中建立和修改 PDF 文件。

#### 載入和操作現有 PDF
```javascript
import { PDFDocument } from 'pdf-lib';
import fs from 'fs';

async function manipulatePDF() {
    // 載入現有 PDF
    const existingPdfBytes = fs.readFileSync('input.pdf');
    const pdfDoc = await PDFDocument.load(existingPdfBytes);

    // 取得頁數
    const pageCount = pdfDoc.getPageCount();
    console.log(`文件有 ${pageCount} 頁`);

    // 新增頁面
    const newPage = pdfDoc.addPage([600, 400]);
    newPage.drawText('由 pdf-lib 新增', {
        x: 100,
        y: 300,
        size: 16
    });

    // 儲存修改後的 PDF
    const pdfBytes = await pdfDoc.save();
    fs.writeFileSync('modified.pdf', pdfBytes);
}
```

#### 從頭建立複雜 PDF
```javascript
import { PDFDocument, rgb, StandardFonts } from 'pdf-lib';
import fs from 'fs';

async function createPDF() {
    const pdfDoc = await PDFDocument.create();

    // 新增字型
    const helveticaFont = await pdfDoc.embedFont(StandardFonts.Helvetica);
    const helveticaBold = await pdfDoc.embedFont(StandardFonts.HelveticaBold);

    // 新增頁面
    const page = pdfDoc.addPage([595, 842]); // A4 尺寸
    const { width, height } = page.getSize();

    // 新增帶樣式的文字
    page.drawText('發票 #12345', {
        x: 50,
        y: height - 50,
        size: 18,
        font: helveticaBold,
        color: rgb(0.2, 0.2, 0.8)
    });

    // 新增矩形（標題背景）
    page.drawRectangle({
        x: 40,
        y: height - 100,
        width: width - 80,
        height: 30,
        color: rgb(0.9, 0.9, 0.9)
    });

    // 新增類似表格的內容
    const items = [
        ['項目', '數量', '價格', '總計'],
        ['小工具', '2', '$50', '$100'],
        ['配件', '1', '$75', '$75']
    ];

    let yPos = height - 150;
    items.forEach(row => {
        let xPos = 50;
        row.forEach(cell => {
            page.drawText(cell, {
                x: xPos,
                y: yPos,
                size: 12,
                font: helveticaFont
            });
            xPos += 120;
        });
        yPos -= 25;
    });

    const pdfBytes = await pdfDoc.save();
    fs.writeFileSync('created.pdf', pdfBytes);
}
```

#### 進階合併和分割操作
```javascript
import { PDFDocument } from 'pdf-lib';
import fs from 'fs';

async function mergePDFs() {
    // 建立新文件
    const mergedPdf = await PDFDocument.create();

    // 載入來源 PDF
    const pdf1Bytes = fs.readFileSync('doc1.pdf');
    const pdf2Bytes = fs.readFileSync('doc2.pdf');

    const pdf1 = await PDFDocument.load(pdf1Bytes);
    const pdf2 = await PDFDocument.load(pdf2Bytes);

    // 從第一個 PDF 複製頁面
    const pdf1Pages = await mergedPdf.copyPages(pdf1, pdf1.getPageIndices());
    pdf1Pages.forEach(page => mergedPdf.addPage(page));

    // 從第二個 PDF 複製特定頁面（第 0、2、4 頁）
    const pdf2Pages = await mergedPdf.copyPages(pdf2, [0, 2, 4]);
    pdf2Pages.forEach(page => mergedPdf.addPage(page));

    const mergedPdfBytes = await mergedPdf.save();
    fs.writeFileSync('merged.pdf', mergedPdfBytes);
}
```

### pdfjs-dist（Apache 授權）

PDF.js 是 Mozilla 的 JavaScript 函式庫，用於在瀏覽器中渲染 PDF。

#### 基本 PDF 載入和渲染
```javascript
import * as pdfjsLib from 'pdfjs-dist';

// 設定 worker（對效能很重要）
pdfjsLib.GlobalWorkerOptions.workerSrc = './pdf.worker.js';

async function renderPDF() {
    // 載入 PDF
    const loadingTask = pdfjsLib.getDocument('document.pdf');
    const pdf = await loadingTask.promise;

    console.log(`載入了有 ${pdf.numPages} 頁的 PDF`);

    // 取得第一頁
    const page = await pdf.getPage(1);
    const viewport = page.getViewport({ scale: 1.5 });

    // 渲染到 canvas
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.height = viewport.height;
    canvas.width = viewport.width;

    const renderContext = {
        canvasContext: context,
        viewport: viewport
    };

    await page.render(renderContext).promise;
    document.body.appendChild(canvas);
}
```

#### 擷取帶座標的文字
```javascript
import * as pdfjsLib from 'pdfjs-dist';

async function extractText() {
    const loadingTask = pdfjsLib.getDocument('document.pdf');
    const pdf = await loadingTask.promise;

    let fullText = '';

    // 從所有頁面擷取文字
    for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const textContent = await page.getTextContent();

        const pageText = textContent.items
            .map(item => item.str)
            .join(' ');

        fullText += `\n--- 第 ${i} 頁 ---\n${pageText}`;

        // 取得帶座標的文字以進行進階處理
        const textWithCoords = textContent.items.map(item => ({
            text: item.str,
            x: item.transform[4],
            y: item.transform[5],
            width: item.width,
            height: item.height
        }));
    }

    console.log(fullText);
    return fullText;
}
```

#### 擷取註解和表單
```javascript
import * as pdfjsLib from 'pdfjs-dist';

async function extractAnnotations() {
    const loadingTask = pdfjsLib.getDocument('annotated.pdf');
    const pdf = await loadingTask.promise;

    for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const annotations = await page.getAnnotations();

        annotations.forEach(annotation => {
            console.log(`註解類型: ${annotation.subtype}`);
            console.log(`內容: ${annotation.contents}`);
            console.log(`座標: ${JSON.stringify(annotation.rect)}`);
        });
    }
}
```

## 進階命令列操作

### poppler-utils 進階功能

#### 擷取帶邊界框座標的文字
```bash
# 擷取帶邊界框座標的文字（對結構化資料至關重要）
pdftotext -bbox-layout document.pdf output.xml

# XML 輸出包含每個文字元素的精確座標
```

#### 進階圖片轉換
```bash
# 使用特定解析度轉換為 PNG 圖片
pdftoppm -png -r 300 document.pdf output_prefix

# 使用高解析度轉換特定頁面範圍
pdftoppm -png -r 600 -f 1 -l 3 document.pdf high_res_pages

# 使用品質設定轉換為 JPEG
pdftoppm -jpeg -jpegopt quality=85 -r 200 document.pdf jpeg_output
```

#### 擷取嵌入圖片
```bash
# 擷取所有帶中繼資料的嵌入圖片
pdfimages -j -p document.pdf page_images

# 列出圖片資訊而不擷取
pdfimages -list document.pdf

# 以原始格式擷取圖片
pdfimages -all document.pdf images/img
```

### qpdf 進階功能

#### 複雜頁面操作
```bash
# 將 PDF 分割成頁面群組
qpdf --split-pages=3 input.pdf output_group_%02d.pdf

# 使用複雜範圍擷取特定頁面
qpdf input.pdf --pages input.pdf 1,3-5,8,10-end -- extracted.pdf

# 從多個 PDF 合併特定頁面
qpdf --empty --pages doc1.pdf 1-3 doc2.pdf 5-7 doc3.pdf 2,4 -- combined.pdf
```

#### PDF 優化和修復
```bash
# 優化 PDF 以供網頁使用（線性化以供串流）
qpdf --linearize input.pdf optimized.pdf

# 移除未使用的物件並壓縮
qpdf --optimize-level=all input.pdf compressed.pdf

# 嘗試修復損壞的 PDF 結構
qpdf --check input.pdf
qpdf --fix-qdf damaged.pdf repaired.pdf

# 顯示詳細的 PDF 結構以供除錯
qpdf --show-all-pages input.pdf > structure.txt
```

#### 進階加密
```bash
# 使用特定權限新增密碼保護
qpdf --encrypt user_pass owner_pass 256 --print=none --modify=none -- input.pdf encrypted.pdf

# 檢查加密狀態
qpdf --show-encryption encrypted.pdf

# 移除密碼保護（需要密碼）
qpdf --password=secret123 --decrypt encrypted.pdf decrypted.pdf
```

## 進階 Python 技術

### pdfplumber 進階功能

#### 擷取帶精確座標的文字
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    page = pdf.pages[0]

    # 擷取所有帶座標的文字
    chars = page.chars
    for char in chars[:10]:  # 前 10 個字元
        print(f"字元: '{char['text']}' 位於 x:{char['x0']:.1f} y:{char['y0']:.1f}")

    # 依邊界框擷取文字（左、上、右、下）
    bbox_text = page.within_bbox((100, 100, 400, 200)).extract_text()
```

#### 使用自訂設定的進階表格擷取
```python
import pdfplumber
import pandas as pd

with pdfplumber.open("complex_table.pdf") as pdf:
    page = pdf.pages[0]

    # 使用自訂設定擷取複雜版面的表格
    table_settings = {
        "vertical_strategy": "lines",
        "horizontal_strategy": "lines",
        "snap_tolerance": 3,
        "intersection_tolerance": 15
    }
    tables = page.extract_tables(table_settings)

    # 表格擷取的視覺除錯
    img = page.to_image(resolution=150)
    img.save("debug_layout.png")
```

### reportlab 進階功能

#### 建立包含表格的專業報告
```python
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# 範例資料
data = [
    ['產品', 'Q1', 'Q2', 'Q3', 'Q4'],
    ['小工具', '120', '135', '142', '158'],
    ['配件', '85', '92', '98', '105']
]

# 建立帶表格的 PDF
doc = SimpleDocTemplate("report.pdf")
elements = []

# 新增標題
styles = getSampleStyleSheet()
title = Paragraph("季度銷售報告", styles['Title'])
elements.append(title)

# 新增帶進階樣式的表格
table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
elements.append(table)

doc.build(elements)
```

## 複雜工作流程

### 從 PDF 擷取圖形/圖片

#### 方法 1：使用 pdfimages（最快）
```bash
# 以原始品質擷取所有圖片
pdfimages -all document.pdf images/img
```

#### 方法 2：使用 pypdfium2 + 圖片處理
```python
import pypdfium2 as pdfium
from PIL import Image
import numpy as np

def extract_figures(pdf_path, output_dir):
    pdf = pdfium.PdfDocument(pdf_path)

    for page_num, page in enumerate(pdf):
        # 渲染高解析度頁面
        bitmap = page.render(scale=3.0)
        img = bitmap.to_pil()

        # 轉換為 numpy 以進行處理
        img_array = np.array(img)

        # 簡單的圖形偵測（非白色區域）
        mask = np.any(img_array != [255, 255, 255], axis=2)

        # 找到輪廓並擷取邊界框
        # （這是簡化版 - 實際實作需要更精密的偵測）

        # 儲存偵測到的圖形
        # ... 實作取決於特定需求
```

### 帶錯誤處理的批次 PDF 處理
```python
import os
import glob
from pypdf import PdfReader, PdfWriter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def batch_process_pdfs(input_dir, operation='merge'):
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))

    if operation == 'merge':
        writer = PdfWriter()
        for pdf_file in pdf_files:
            try:
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    writer.add_page(page)
                logger.info(f"已處理: {pdf_file}")
            except Exception as e:
                logger.error(f"處理 {pdf_file} 失敗: {e}")
                continue

        with open("batch_merged.pdf", "wb") as output:
            writer.write(output)

    elif operation == 'extract_text':
        for pdf_file in pdf_files:
            try:
                reader = PdfReader(pdf_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()

                output_file = pdf_file.replace('.pdf', '.txt')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                logger.info(f"已從 {pdf_file} 擷取文字")

            except Exception as e:
                logger.error(f"從 {pdf_file} 擷取文字失敗: {e}")
                continue
```

### 進階 PDF 裁切
```python
from pypdf import PdfWriter, PdfReader

reader = PdfReader("input.pdf")
writer = PdfWriter()

# 裁切頁面（左、下、右、上，單位為點）
page = reader.pages[0]
page.mediabox.left = 50
page.mediabox.bottom = 50
page.mediabox.right = 550
page.mediabox.top = 750

writer.add_page(page)
with open("cropped.pdf", "wb") as output:
    writer.write(output)
```

## 效能優化提示

### 1. 對於大型 PDF
- 使用串流方法而非將整個 PDF 載入記憶體
- 使用 `qpdf --split-pages` 分割大檔案
- 使用 pypdfium2 單獨處理頁面

### 2. 對於文字擷取
- `pdftotext -bbox-layout` 是純文字擷取最快的方法
- 對於結構化資料和表格使用 pdfplumber
- 對於非常大的文件避免使用 `pypdf.extract_text()`

### 3. 對於圖片擷取
- `pdfimages` 比渲染頁面快得多
- 預覽使用低解析度，最終輸出使用高解析度

### 4. 對於表單填寫
- pdf-lib 比大多數替代品更能維持表單結構
- 處理前預先驗證表單欄位

### 5. 記憶體管理
```python
# 分塊處理 PDF
def process_large_pdf(pdf_path, chunk_size=10):
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)

    for start_idx in range(0, total_pages, chunk_size):
        end_idx = min(start_idx + chunk_size, total_pages)
        writer = PdfWriter()

        for i in range(start_idx, end_idx):
            writer.add_page(reader.pages[i])

        # 處理分塊
        with open(f"chunk_{start_idx//chunk_size}.pdf", "wb") as output:
            writer.write(output)
```

## 常見問題疑難排解

### 加密 PDF
```python
# 處理密碼保護的 PDF
from pypdf import PdfReader

try:
    reader = PdfReader("encrypted.pdf")
    if reader.is_encrypted:
        reader.decrypt("password")
except Exception as e:
    print(f"解密失敗: {e}")
```

### 損壞的 PDF
```bash
# 使用 qpdf 修復
qpdf --check corrupted.pdf
qpdf --replace-input corrupted.pdf
```

### 文字擷取問題
```python
# 對掃描 PDF 回退到 OCR
import pytesseract
from pdf2image import convert_from_path

def extract_text_with_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for i, image in enumerate(images):
        text += pytesseract.image_to_string(image)
    return text
```

## 授權資訊

- **pypdf**: BSD 授權
- **pdfplumber**: MIT 授權
- **pypdfium2**: Apache/BSD 授權
- **reportlab**: BSD 授權
- **poppler-utils**: GPL-2 授權
- **qpdf**: Apache 授權
- **pdf-lib**: MIT 授權
- **pdfjs-dist**: Apache 授權
