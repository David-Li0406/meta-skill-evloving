#!/usr/bin/env python3
"""Extract template variables from a docx template and generate JSON schema."""
import sys
import json
from docxtpl import DocxTemplate

def extract_schema(template_path):
    """Extract variables and return JSON schema."""
    doc = DocxTemplate(template_path)
    variables = doc.get_undeclared_template_variables()
    
    schema = {
        "type": "object",
        "properties": {var: {"type": "string"} for var in variables},
        "required": list(variables)
    }
    
    return {
        "variables": list(variables),
        "schema": schema
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_schema.py <template.docx>")
        sys.exit(1)
    
    result = extract_schema(sys.argv[1])
    print(json.dumps(result, indent=2, ensure_ascii=False))
