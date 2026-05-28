#!/usr/bin/env python3
"""
Extract text content from Word documents (.docx) using pandoc.
Outputs markdown for easy parsing.

Usage: python3 extract_docx.py <path_to_docx>
"""

import subprocess
import sys
import os


def extract_docx(filepath: str) -> str:
    """Extract all text content from a .docx file using pandoc."""
    try:
        result = subprocess.run(
            ["pandoc", filepath, "-t", "markdown"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running pandoc: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: pandoc is not installed. Install with: brew install pandoc", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_docx.py <path_to_docx>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]

    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    if not filepath.endswith('.docx'):
        print(f"Error: File must be a .docx file: {filepath}", file=sys.stderr)
        sys.exit(1)

    markdown = extract_docx(filepath)
    print(markdown)


if __name__ == "__main__":
    main()
