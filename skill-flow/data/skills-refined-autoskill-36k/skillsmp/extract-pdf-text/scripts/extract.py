#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "pdfplumber",
# ]
# ///
"""Extract text content from PDF files."""

from __future__ import annotations

import argparse
import sys

import pdfplumber  # ty:ignore[unresolved-import]


def extract_text(pdf_path: str, page: int | None = None) -> str:
    with pdfplumber.open(pdf_path) as pdf:
        if page is not None:
            if page < 0 or page >= len(pdf.pages):
                raise ValueError(f"Page {page} out of range (0-{len(pdf.pages) - 1})")
            return pdf.pages[page].extract_text() or ""
        return "\n".join(p.extract_text() or "" for p in pdf.pages)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", help="Path to PDF file")
    parser.add_argument("--page", type=int, help="Extract specific page (0-indexed)")
    args = parser.parse_args()
    try:
        text = extract_text(args.pdf, args.page)
        print(text)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
