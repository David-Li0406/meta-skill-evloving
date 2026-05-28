#!/usr/bin/env python3
"""Fill docx template with provided data."""
import sys
import json
from docxtpl import DocxTemplate

def fill_template(template_path, data_json, output_path):
    """Fill template with data and save result."""
    doc = DocxTemplate(template_path)
    data = json.loads(data_json) if isinstance(data_json, str) else data_json
    doc.render(data)
    doc.save(output_path)
    return output_path

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python fill_template.py <template.docx> <data.json> <output.docx>")
        sys.exit(1)
    
    with open(sys.argv[2], 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    result = fill_template(sys.argv[1], data, sys.argv[3])
    print(f"✓ Created: {result}")
