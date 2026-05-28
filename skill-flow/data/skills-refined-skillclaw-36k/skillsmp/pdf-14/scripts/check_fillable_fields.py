#!/usr/bin/env python3
"""PDFにフィル可能なフォームフィールドがあるか確認するスクリプト。"""

import sys
from pypdf import PdfReader

if len(sys.argv) != 2:
    print("Usage: check_fillable_fields.py <file.pdf>")
    sys.exit(1)

reader = PdfReader(sys.argv[1])
if reader.get_fields():
    print("This PDF has fillable form fields")
else:
    print("This PDF does not have fillable form fields; you will need to visually determine where to enter data")
