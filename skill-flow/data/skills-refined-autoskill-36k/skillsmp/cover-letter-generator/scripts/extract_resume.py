#!/usr/bin/env python3
"""Extract text content from a .docx resume file."""
import sys
import zipfile
import xml.etree.ElementTree as ET
import re

def extract_docx_text(filepath):
    """Extract all text from a .docx file."""
    with zipfile.ZipFile(filepath, 'r') as z:
        with z.open('word/document.xml') as f:
            content = f.read()

    root = ET.fromstring(content)
    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

    text_parts = []
    for elem in root.iter():
        if elem.tag == f'{{{ns}}}t' and elem.text:
            text_parts.append(elem.text)
        elif elem.tag == f'{{{ns}}}p':
            text_parts.append('\n')

    full_text = ''.join(text_parts)
    return re.sub(r'\n{3,}', '\n\n', full_text).strip()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python extract_resume.py <path_to_docx>")
        sys.exit(1)
    print(extract_docx_text(sys.argv[1]))
