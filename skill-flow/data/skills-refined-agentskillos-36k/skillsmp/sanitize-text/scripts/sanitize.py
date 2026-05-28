#!/usr/bin/env python3
"""
Sanitize Text - Normalize raw text (spacing, noise cleanup)

Usage:
    python3 sanitize.py <input_file> [--output <output_file>]

Dependencies:
    None (standard library)
"""

import sys
import argparse
import re
import unicodedata


def sanitize_text(text):
    """
    Normalizes text by:
    1. Normalizing unicode (NFKC).
    2. Replacing multiple whitespace with single space.
    3. Removing non-printable characters.
    4. Trimming.

    Args:
        text (str): Raw input text.

    Returns:
        str: Cleaned text.
    """
    # Normalize unicode characters (e.g., separate accents)
    text = unicodedata.normalize("NFKC", text)

    # Replace layout control chars like newlines with spaces ONLY if we want single-line.
    # But usually for resumes we want to PRESERVE essential newlines but remove excessive spacing.
    # Let's clean up multiple newlines to max 2 (paragraph break).

    # Remove null bytes and other non-printable chars (except whitespace)
    text = "".join(ch for ch in text if ch.isprintable() or ch in "\n\r\t")

    # Replace multiple spaces with single space
    text = re.sub(r"[ \t]+", " ", text)

    # Unique strategy: condense multiple newlines to double newline
    text = re.sub(r"\n\s*\n", "\n\n", text)

    return text.strip()


def main():
    parser = argparse.ArgumentParser(description="Sanitize and normalize text")
    parser.add_argument("input_file", help="Path to input text file")
    parser.add_argument("--output", help="Path to output file (default: stdout)")

    args = parser.parse_args()

    try:
        with open(args.input_file, "r", encoding="utf-8") as f:
            raw_text = f.read()
    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)

    cleaned_text = sanitize_text(raw_text)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(cleaned_text)
        except Exception as e:
            print(f"Error writing output: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(cleaned_text)


if __name__ == "__main__":
    main()
