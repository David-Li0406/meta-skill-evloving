---
name: ocr-image-text-extraction
description: Use this skill when you need to extract text from images using the Tesseract OCR engine, suitable for various image formats and languages.
---

# Skill body

## Capabilities

- Extract text from image files (PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP)
- Support for 100+ languages
- Optional image preprocessing for better accuracy
- Output in plain text or JSON format with confidence scores

## Usage

### Basic OCR

```bash
python3 ocr.py <image_file> <output_file>
```

### With Options

```bash
# Specify language (default: eng)
python3 ocr.py image.png text.txt --lang eng

# Chinese text
python3 ocr.py image.png text.txt --lang chi_sim

# Multiple languages
python3 ocr.py image.png text.txt --lang eng+chi_sim

# With image preprocessing (improves accuracy)
python3 ocr.py image.png text.txt --preprocess

# JSON output with confidence scores
python3 ocr.py image.png output.json --format json
```

### Download and OCR from URL

```bash
# OCR from remote image
python3 ocr_url.py <image_url> <output_file>

# With options
python3 ocr_url.py https://example.com/image.jpg text.txt --lang eng --preprocess
```

## Parameters

- `image_file` / `image_url` (required): Path to local image or image URL
- `output_file` (required): Path to output text/JSON file
- `--lang`: Language code (e.g., eng, chi_sim, jpn, fra, deu). Default: eng
- `--preprocess`: Apply image preprocessing (grayscale, thresholding) for better accuracy
- `--format`: Output format (text/json, default: text)

## Common Languages

| Language | Code |
|----------|------|
| English | eng |
| Chinese (Simplified) | chi_sim |
| Chinese (Traditional) | chi_tra |
| Japanese | jpn |
| Korean | kor |
| French | fra |
| German | deu |
| Spanish | spa |
| Russian | rus |
| Arabic | ara |

## Supported Image Formats

PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP

## Dependencies

- Python 3.8+
- pytesseract
- Pillow (PIL)
- tesseract-ocr (system package)

## Installation

```bash
# Python packages
pip install pytesseract Pillow

# Tesseract OCR engine
sudo apt-get install tesseract-ocr  # Ubuntu/Debian
sudo yum install tesseract           # CentOS/RHEL
brew install tesseract               # macOS
```

## Output Schema

All extracted content must be returned as valid JSON conforming to this schema:

```json
{
  "success": true,
  "filename": "example.jpg",
  "extracted_text": "Full raw text extracted from the image...",
  "confidence": "high|medium|low",
  "metadata": {
    "language_detected": "en",
    "text_regions": 3,
    "has_tables": false,
    "has_handwriting": false
  },
  "warnings": [
    "Text partially obscured in bottom-right corner",
    "Low contrast detected in header section"
  ]
}
```

### Field Descriptions

- `success`: Boolean indicating whether text extraction completed
- `filename`: Original image filename
- `extracted_text`: Complete text content in reading order (top-to-bottom, left-to-right)
- `confidence`: Overall OCR confidence level based on image quality and text clarity
- `metadata.language_detected`: ISO 639-1 language code
- `metadata.text_regions`: Number of distinct text blocks identified
- `metadata.has_tables`: Whether tabular data structures were detected
- `metadata.has_handwriting`: Whether handwritten text was detected
- `warnings`: Array of quality issues or potential errors