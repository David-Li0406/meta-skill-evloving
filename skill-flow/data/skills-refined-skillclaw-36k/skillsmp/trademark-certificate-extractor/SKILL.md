---
name: trademark-certificate-extractor
description: Extracts structured information from trademark registration certificates in PDF or image format. Use when user asks to extract trademark certificate data, parse trademark information, or convert trademark certificates to Excel format. Supports Chinese and English trademark certificates using Tesseract OCR for text extraction and LLM for information extraction. Extracts serial number, trademark logo (as image), registrant, registration number, international classification, and validity period, and outputs to Excel with embedded trademark images.
---

# Trademark Certificate Extractor

## Overview

Extracts structured information from trademark registration certificates (PDF or image formats) using OCR and LLM-based information extraction. Supports both Chinese and English trademark certificates with automatic logo image extraction.

## Quick Start

### Step 1: Extract Text with OCR

Use the OCR extraction script to extract text from the trademark certificate:

```bash
scripts/extract_ocr.py <path/to/certificate.pdf> [language_code]
```

- Default language: `chi_sim+eng` (Chinese and English)
- Supported formats: PDF, PNG, JPG, JPEG, BMP, TIFF
- Returns: Extracted text content

### Step 2: Extract Trademark Logo

Extract the trademark logo image from the certificate:

```bash
python scripts/extract_logo.py <path/to/certificate.pdf>
```

- Automatically detects and crops the trademark logo area
- Saves logo as PNG file in the same directory
- Supports both PDF and image formats

### Step 3: Extract Information with LLM

Pass the OCR text to an LLM to extract structured information. Use the prompt template from `references/llm_prompt.md`.

Example extraction request:

```
Extract the following fields from this trademark certificate text:
- 序号 (Serial Number)
- 注册人 (Registrant)
- 注册号 (Registration Number)
- 国际分类 (International Classification)
- 有效期限 (Validity Period)

[PASTE OCR TEXT HERE]

Return as JSON format.
```

### Step 4: Generate Excel File

Use the Excel generation script to create the output file with embedded trademark images:

```bash
python scripts/generate_excel.py <output.xlsx>
```

Pass the extracted JSON data as the second argument, or modify the script to accept data programmatically.

### Step 5: Review and Verify

The script automatically opens the Excel file after creation. Verify all extracted fields and trademark images for accuracy.

## Requirements

### System Dependencies

- **Tesseract OCR**: Required for text extraction
  - macOS: `brew install tesseract`
  - Ubuntu: `sudo apt-get install tesseract-ocr`
  - Windows: Download from https://github.com/tesseract-ocr/tesseract
  - Language data: Install `chi_sim` for Chinese support

- **Poppler** (for PDF processing):
  - macOS: `brew install poppler`
  - Ubuntu: `sudo apt-get install poppler-utils`

### Python Dependencies

Install required packages:

```bash
pip install openpyxl pdf2image Pillow opencv-python
```

- `openpyxl`: Excel file generation with image embedding
- `pdf2image`: PDF to image conversion (for PDF processing)
- `Pillow`: Image processing
- `opencv-python`: Image processing for logo detection

## Workflow

```
Input File (PDF/Image)
    ↓
OCR Extraction (extract_ocr.py)
    ↓
Extracted Text
    ↓
LLM Information Extraction (using llm_prompt.md)
    ↓
Structured Data (JSON)
    ↓
Logo Extraction (extract_logo.py)
    ↓
Excel Generation with Images (generate_excel.py)
    ↓
Output Excel File (with embedded logos)
```

## Common Issues

### Tesseract Not Found
- Error: "Tesseract OCR is not installed or not in PATH"
- Solution: Install Tesseract OCR and ensure it's in your system PATH

### Poor OCR Quality
- Cause: Low-resolution scans or poor image quality
- Solution:
  - Ensure scans are at 300 DPI or higher
  - Try pre-processing images (contrast adjustment, noise reduction)
  - Consider using Tesseract's advanced configuration options

### PDF Processing Fails
- Cause: `pdf2image` not installed or Poppler not available
- Solution:
  - Install pdf2image: `pip install pdf2image`
  - Install Poppler (required by pdf2image)
  - macOS: `brew install poppler`
  - Ubuntu: `sudo apt-get install poppler-utils`

### Logo Extraction Fails
- Cause: Unable to detect logo area in the certificate
- Solution:
  - Check if the certificate layout matches expected format
  - Try adjusting logo detection parameters in `extract_logo.py`
  - Manually crop and rename the logo image to `<filename>_logo.png`

### Missing Fields in Extraction
- Cause: LLM cannot locate specific information in the OCR text
- Solution:
  - Check OCR quality and completeness
  - Try adjusting the LLM prompt
  - Manually verify and fill missing fields

## Resources

### scripts/extract_ocr.py
Main OCR extraction script that handles both PDF and image files. Supports Chinese and English languages through Tesseract.

### scripts/extract_logo.py
Trademark logo extraction script that automatically detects and crops the logo area from trademark certificates. Supports both PDF and image formats.

### scripts/generate_excel.py
Excel file generation script with formatted output, auto-adjusted column widths, automatic image embedding, and intelligent sorting.

**Sorting Rules:**
- Primary sort: 注册人 (Registrant) - alphabetically grouped
- Secondary sort: 有效期限 (Validity Period) - ascending
- Visual grouping: Thick border lines separate different 注册人 groups

### references/llm_prompt.md
LLM prompt template for extracting structured trademark information from OCR text. Includes system prompt, usage instructions, and tips for better extraction.

## Example Usage

Complete workflow for processing a single trademark certificate:

```bash
# 1. Extract text from certificate
python scripts/extract_ocr.py certificate.pdf > extracted_text.txt

# 2. Extract trademark logo image
python scripts/extract_logo.py certificate.pdf

# 3. Use LLM to extract structured information (paste the extracted text)
# Then save the LLM response as extracted_data.json

# 4. Generate Excel file
python scripts/generate_excel.py trademark_list.json
```

For batch processing, create a wrapper script that:
1. Iterates through multiple certificate files
2. Extracts text from each file
3. Extracts logo images from each file
4. Calls LLM for information extraction
5. Aggregates all results with image paths
6. Generates a single Excel file with all trademarks and logos

## Testing

### Test Logo Extraction

To test the logo extraction functionality:

```bash
python scripts/extract_logo.py sample_certificate.pdf
```

This will:
- Extract the logo from the certificate
- Save it as `sample_certificate_logo.png`
- Display the extracted logo for verification

### Test Excel Generation

Generate an Excel file with sample data:

```bash
python scripts/test_demo.py
```

This will:
- Create sample trademark data
- Generate an Excel file with embedded logos
- Open the Excel file for review

## Customization

### Adjust Logo Detection

To modify the logo detection logic, edit the `extract_logo_from_image()` function in `scripts/extract_logo.py`:

- Change logo area coordinates based on certificate layout
- Adjust detection thresholds for different certificate formats
- Add support for additional certificate layouts

### Modify Sorting Rules

To change the sorting logic, edit the `sort_trademark_data()` function in `scripts/generate_excel.py`:

- Change primary/secondary sort keys
- Modify date format parsing
- Adjust the grouping criteria

## Output Format

The Excel file contains one row per trademark certificate with the following columns:

| Column | Description |
|--------|-------------|
| 序号 | Serial number |
| 商标标识 | Trademark logo (embedded image) |
| 注册人 | Registrant name |
| 注册号 | Registration number |
| 国际分类 | International classification |
| 有效期限 | Validity period (YYYY-MM-DD format) |

**Data Organization:**
- Grouped by 注册人 with visual separators (thick border lines)
- Trademark logos are embedded directly in the Excel cells
- Within each 注册人 group, trademarks are sorted by validity period
- Date formats automatically standardized to YYYY-MM-DD

The Excel file uses:
- Blue header row with white bold text
- Auto-adjusted column widths (max 50 characters)
- Left-aligned, top-aligned text with wrap enabled
- Visual grouping with border lines
- Embedded trademark images in cells
- Automatically opened in default spreadsheet application
