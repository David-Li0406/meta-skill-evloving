---
name: image-ocr
description: Use this skill to extract text content from images using Tesseract OCR via Python, suitable for various image formats and languages.
---

# Image OCR Skill

This skill enables accurate text extraction from image files (JPG, PNG, etc.) using the Tesseract OCR engine via the `pytesseract` Python library. It is suitable for scanned documents, screenshots, photos of text, receipts, forms, and other visual content containing text.

## Capabilities

- Extract text from image files (PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP)
- Support for 100+ languages
- Optional image preprocessing for better accuracy
- Output in plain text or JSON format with confidence scores

## Usage

### Basic OCR Extraction

```python
import pytesseract
from PIL import Image

def extract_text_from_image(image_path):
    """Extract text from a single image using Tesseract OCR."""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text.strip()
```

### OCR with Confidence Data

```python
def extract_with_confidence(image_path):
    """Extract text with per-word confidence scores."""
    img = Image.open(image_path)
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    words = []
    confidences = []

    for i, word in enumerate(data['text']):
        if word.strip():  # Skip empty strings
            words.append(word)
            confidences.append(data['conf'][i])

    avg_confidence = sum(c for c in confidences if c > 0) / len([c for c in confidences if c > 0]) if confidences else 0

    return {
        'text': ' '.join(words),
        'average_confidence': avg_confidence,
        'word_count': len(words)
    }
```

### Full OCR with JSON Output

```python
import json
import os

def ocr_to_json(image_path):
    """Perform OCR and return results as JSON."""
    filename = os.path.basename(image_path)
    warnings = []

    try:
        img = Image.open(image_path)
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        text = pytesseract.image_to_string(img)

        confidences = [c for c in data['conf'] if c > 0]
        avg_conf = sum(confidences) / len(confidences) if confidences else 0

        confidence = "high" if avg_conf >= 80 else "medium" if avg_conf >= 50 else "low"
        if confidence == "low":
            warnings.append(f"Low OCR confidence: {avg_conf:.1f}%")

        block_nums = set(data['block_num'])
        text_regions = len([b for b in block_nums if b > 0])

        result = {
            "success": True,
            "filename": filename,
            "extracted_text": text.strip(),
            "confidence": confidence,
            "metadata": {
                "language_detected": "en",
                "text_regions": text_regions,
                "has_tables": False,
                "has_handwriting": False
            },
            "warnings": warnings
        }

    except Exception as e:
        result = {
            "success": False,
            "filename": filename,
            "extracted_text": "",
            "confidence": "low",
            "metadata": {
                "language_detected": "unknown",
                "text_regions": 0,
                "has_tables": False,
                "has_handwriting": False
            },
            "warnings": [f"OCR failed: {str(e)}"]
        }

    return result
```

### Batch Processing Multiple Images

```python
from pathlib import Path

def process_image_directory(directory_path, output_file):
    """Process all images in a directory and save results."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    results = []

    for file_path in sorted(Path(directory_path).iterdir()):
        if file_path.suffix.lower() in image_extensions:
            result = ocr_to_json(str(file_path))
            results.append(result)

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    return results
```

## Parameters

- `image_path` (required): Path to the local image file
- `output_file` (required): Path to output JSON file
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

## Limitations

- Tesseract works best with printed text; handwriting recognition is limited.
- Accuracy decreases with decorative fonts, artistic text, or extreme stylization.
- Mathematical equations and special notation may not extract accurately.
- Redacted or watermarked text cannot be recovered.
- Severe image degradation (blur, noise, low resolution) reduces accuracy.
- Complex multi-column layouts may require custom PSM configuration.

## Version History

- **1.0.0** (2026-01-13): Initial release with Tesseract/pytesseract OCR