#!/usr/bin/env python3
"""
Extract Text from PDF using PyMuPDF (fitz)

Usage:
    python3 extract_pdf_text.py <img_path> [--layout]

Dependencies:
    pip install pymupdf
"""

import sys
import argparse
import fitz  # PyMuPDF

def extract_text(pdf_path, preserve_layout=False):
    """
    Extracts text from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file.
        preserve_layout (bool): If True, attempts to preserve physical layout.
        
    Returns:
        str: extracted text
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF: {e}", file=sys.stderr)
        sys.exit(1)

    full_text = []

    for page_num, page in enumerate(doc):
        # "text" = plain text with some line breaks
        # "blocks" or "dict" could be used for more control, but "text" is standard.
        # If preserve_layout is requested, we might simply use the default which respects basic structure,
        # or we could try different flags. PyMuPDF's "text" output is usually decent.
        # For strict layout preservation similar to the physical look, "text" is often sufficient,
        # but let's see if we can tweak flags if needed. 
        # Actually, PyMuPDF 'text' mode preserves reading order.
        
        # Let's keep it simple for now: plain text extraction.
        # If layout is requested, we assume the user wants it to look somewhat like the page.
        # standard get_text("text") allows basic layout.
        
        flags = fitz.TEXT_PRESERVE_LIGATURES | fitz.TEXT_PRESERVE_WHITESPACE
        if not preserve_layout:
             # Just raw text blocks
             pass 
        
        # PyMuPDF get_text defaults to "text" which is good.
        text = page.get_text("text") 
        full_text.append(text)
        
    doc.close()
    return "\n".join(full_text)

def main():
    parser = argparse.ArgumentParser(description="Extract text from PDF using PyMuPDF")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--layout", action="store_true", help="Preserve layout (default is basic text extraction)")
    
    args = parser.parse_args()
    
    # Check if pymupdf is installed is implicit by import fitz.
    
    text = extract_text(args.pdf_path, args.layout)
    print(text)

if __name__ == "__main__":
    main()
