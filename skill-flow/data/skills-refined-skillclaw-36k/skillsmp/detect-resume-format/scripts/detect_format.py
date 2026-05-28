#!/usr/bin/env python3
"""
Detect Resume Format - Route to appropriate parser based on MIME or file extension

Usage:
    python3 detect_format.py <file_path>

Dependencies:
    pip install python-magic (optional, falls back to mimetypes)
"""

import argparse
import os
import mimetypes

# Try importing python-magic, handle if missing
try:
    import magic

    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False


def detect_format(file_path):
    """
    Detects the format of a resume file.

    Args:
        file_path (str): Path to file.

    Returns:
        str: 'pdf', 'docx', 'txt', or 'unknown'
    """
    if not os.path.exists(file_path):
        return "error: file not found"

    # Priority 1: python-magic (content inspection)
    mime_type = None
    if HAS_MAGIC:
        try:
            mime_type = magic.from_file(file_path, mime=True)
        except Exception:
            pass

    # Priority 2: mimetypes (extension based)
    if not mime_type:
        mime_type, _ = mimetypes.guess_type(file_path)

    # Map mime to simple format
    if mime_type:
        if "pdf" in mime_type:
            return "pdf"
        if "word" in mime_type or "officedocument" in mime_type:
            return "docx"
        if "text/plain" in mime_type:
            return "txt"

    # Fallback: Extension check
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return "pdf"
    if ext in [".doc", ".docx"]:
        return "docx"
    if ext == ".txt":
        return "txt"

    return "unknown"


def main():
    parser = argparse.ArgumentParser(description="Detect resume file format")
    parser.add_argument("file_path", help="Path to resume file")

    args = parser.parse_args()

    fmt = detect_format(args.file_path)
    print(fmt)


if __name__ == "__main__":
    main()
