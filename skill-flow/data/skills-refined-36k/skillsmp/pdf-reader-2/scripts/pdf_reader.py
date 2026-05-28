#!/usr/bin/env python3
"""
Simple PDF reader utility script
Usage: python pdf_reader.py <path_to_pdf> [--pages 1,2,3]
"""

import sys
import argparse
from pathlib import Path

try:
    import pdfplumber

    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    import PyPDF2

    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False


def read_pdf_pdfplumber(pdf_path, pages=None):
    """Read PDF using pdfplumber"""
    if not HAS_PDFPLUMBER:
        raise ImportError("pdfplumber not installed. Run: pip install pdfplumber")

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"\n{'='*60}")
        print(f"PDF: {Path(pdf_path).name}")
        print(f"Total pages: {total_pages}")
        print(f"{'='*60}\n")

        # Determine which pages to read
        if pages:
            page_list = [p - 1 for p in pages if 0 < p <= total_pages]
        else:
            page_list = range(total_pages)

        for i in page_list:
            page = pdf.pages[i]
            print(f"\n--- Page {i+1} ---")
            text = page.extract_text()

            if text:
                print(text)

                # Show table count if any
                tables = page.extract_tables()
                if tables:
                    print(f"\n[Found {len(tables)} table(s) on this page]")
            else:
                print("[No text found on this page]")

        return True


def read_pdf_pypdf2(pdf_path, pages=None):
    """Read PDF using PyPDF2"""
    if not HAS_PYPDF2:
        raise ImportError("PyPDF2 not installed. Run: pip install PyPDF2")

    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)

        print(f"\n{'='*60}")
        print(f"PDF: {Path(pdf_path).name}")
        print(f"Total pages: {total_pages}")
        print(f"{'='*60}\n")

        # Determine which pages to read
        if pages:
            page_list = [p - 1 for p in pages if 0 < p <= total_pages]
        else:
            page_list = range(total_pages)

        for i in page_list:
            page = pdf_reader.pages[i]
            print(f"\n--- Page {i+1} ---")
            text = page.extract_text()

            if text:
                print(text)
            else:
                print("[No text found on this page]")

        return True


def main():
    parser = argparse.ArgumentParser(description="Read text from PDF files")
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument(
        "--pages", help="Comma-separated page numbers (e.g., 1,2,5)", default=None
    )
    parser.add_argument(
        "--library",
        choices=["pdfplumber", "pypdf2", "auto"],
        default="auto",
        help="Which library to use",
    )

    args = parser.parse_args()

    # Check if file exists
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"Error: File not found: {pdf_path}")
        return 1

    # Parse page numbers
    pages = None
    if args.pages:
        try:
            pages = [int(p.strip()) for p in args.pages.split(",")]
        except ValueError:
            print("Error: Invalid page numbers. Use format: 1,2,3")
            return 1

    # Choose library
    if args.library == "auto":
        if HAS_PDFPLUMBER:
            library = "pdfplumber"
        elif HAS_PYPDF2:
            library = "pypdf2"
        else:
            print("Error: No PDF library installed!")
            print("Install one with: pip install pdfplumber")
            print("            or: pip install PyPDF2")
            return 1
    else:
        library = args.library

    # Read PDF
    try:
        print(f"Using library: {library}")

        if library == "pdfplumber":
            read_pdf_pdfplumber(pdf_path, pages)
        else:
            read_pdf_pypdf2(pdf_path, pages)

        print(f"\n{'='*60}")
        print("Done!")
        print(f"{'='*60}\n")
        return 0

    except Exception as e:
        print(f"Error reading PDF: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
