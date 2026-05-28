---
name: office_document_analysis
description: PDF, Word, Excel, PowerPoint などのオフィスドキュメントからテキスト・構造・データを抽出して分析する
---

# Office Document Analysis

Extract and analyze text or structured data from binary office files using libraries or command-line tools.

## 1. PDF Analysis
*   **Text Extraction**: Use `pdfminer.six` or `PyPDF2` to read text information.
*   **Table Extraction**: Use `tabula-py` or `camelot-py` to collect tabular data from PDFs.
*   **Images and Metadata**: Use `PyMuPDF (fitz)` to retrieve embedded images, document titles, author information, etc.

## 2. Excel (xlsx/csv) Analysis
*   Utilize `pandas` `read_excel` or `read_csv` for advanced aggregation and statistical analysis.
*   Use `openpyxl` if metadata such as sheet structure, named ranges, or formulas are required.

## 3. Word (docx) Analysis
*   Use `python-docx` to extract text while maintaining chapter headings, paragraphs, styles (bold/bullets), and table structures.

## 4. PowerPoint (pptx) Analysis
*   Use `python-pptx` to scan slide titles, body text, notes, and text contained within shapes.

## Workflow Tips
*   **Convert to Intermediate Formats**: For large files, consider converting them to text (.txt) or CSV format first and saving them to `tmp/` within the project for analysis.
*   **OCR**: For scanned PDFs or documents converted to images, propose the introduction of OCR tools such as `Tesseract` or `EasyOCR`.
