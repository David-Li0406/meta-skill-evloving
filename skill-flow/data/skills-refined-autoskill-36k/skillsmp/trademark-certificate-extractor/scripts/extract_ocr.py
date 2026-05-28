#!/usr/bin/env python3
"""
OCR extraction script for trademark certificates

Extracts text from PDF and image files using Tesseract OCR.
Supports Chinese and English text extraction.
"""

import sys
import subprocess
from pathlib import Path
from typing import List
import tempfile


def check_tesseract_installed():
    """Check if Tesseract OCR is installed"""
    try:
        result = subprocess.run(['tesseract', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def extract_from_image(image_path: Path, lang: str = 'chi_sim+eng') -> str:
    """
    Extract text from an image file using Tesseract OCR

    Args:
        image_path: Path to the image file
        lang: Language code (default: chi_sim+eng for Chinese and English)

    Returns:
        Extracted text as string
    """
    try:
        # Use Tesseract to extract text to stdout
        result = subprocess.run(
            ['tesseract', str(image_path), 'stdout', '-l', lang],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error extracting text from {image_path}: {e}", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"Unexpected error processing {image_path}: {e}", file=sys.stderr)
        return ""


def extract_from_pdf(pdf_path: Path, lang: str = 'chi_sim+eng') -> str:
    """
    Extract text from a PDF file using Tesseract OCR

    First converts PDF pages to images, then extracts text from each page.

    Args:
        pdf_path: Path to the PDF file
        lang: Language code (default: chi_sim+eng for Chinese and English)

    Returns:
        Extracted text from all pages as string
    """
    try:
        # Import PIL/Pillow here to avoid errors if not installed
        from PIL import Image

        # Try to use pdf2image to convert PDF to images
        try:
            from pdf2image import convert_from_path
            images = convert_from_path(str(pdf_path), dpi=300)
            full_text = []

            for page_num, image in enumerate(images, 1):
                # Save image to temp file
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                    image.save(tmp.name, 'PNG')
                    tmp_path = Path(tmp.name)

                # Extract text from this page
                page_text = extract_from_image(tmp_path, lang)
                if page_text:
                    full_text.append(f"--- Page {page_num} ---\n{page_text}")

                # Clean up temp file
                tmp_path.unlink()

            return "\n\n".join(full_text)

        except ImportError:
            print("pdf2image not installed. PDF processing may not work optimally.", file=sys.stderr)
            print("Install with: pip install pdf2image", file=sys.stderr)
            return ""

    except Exception as e:
        print(f"Error processing PDF {pdf_path}: {e}", file=sys.stderr)
        return ""


def extract_text(file_path: Path, lang: str = 'chi_sim+eng') -> str:
    """
    Extract text from a file (PDF or image) using Tesseract OCR

    Args:
        file_path: Path to the file
        lang: Language code (default: chi_sim+eng for Chinese and English)

    Returns:
        Extracted text as string
    """
    if not file_path.exists():
        print(f"File not found: {file_path}", file=sys.stderr)
        return ""

    # Check Tesseract is installed
    if not check_tesseract_installed():
        print("Tesseract OCR is not installed or not in PATH", file=sys.stderr)
        print("Install it from: https://github.com/tesseract-ocr/tesseract", file=sys.stderr)
        return ""

    suffix = file_path.suffix.lower()

    if suffix == '.pdf':
        return extract_from_pdf(file_path, lang)
    elif suffix in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif']:
        return extract_from_image(file_path, lang)
    else:
        print(f"Unsupported file type: {suffix}", file=sys.stderr)
        return ""


def main():
    """Command-line interface for the OCR extraction script"""
    if len(sys.argv) < 2:
        print("Usage: python extract_ocr.py <file_path> [language_code]")
        print("Example: python extract_ocr.py certificate.png")
        print("Example: python extract_ocr.py certificate.pdf chi_sim+eng")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    lang = sys.argv[2] if len(sys.argv) > 2 else 'chi_sim+eng'

    text = extract_text(file_path, lang)

    if text:
        print(text)
    else:
        print("No text extracted", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
