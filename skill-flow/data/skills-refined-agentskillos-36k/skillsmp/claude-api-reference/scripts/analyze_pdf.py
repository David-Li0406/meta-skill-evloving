#!/usr/bin/env python3
"""
PDF Document Analysis Example Script
Usage: python analyze_pdf.py <pdf_path> [prompt]
"""

import anthropic
import base64
import sys
from pathlib import Path


def analyze_pdf(pdf_path: str, prompt: str = "Please analyze the key points of this document") -> str:
    """
    Analyze PDF document using Claude API
    
    Args:
        pdf_path: Path to PDF file
        prompt: Analysis prompt
        
    Returns:
        Claude's analysis result
    """
    client = anthropic.Anthropic()
    
    # Read and encode PDF
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        raise FileNotFoundError(f"File not found: {pdf_path}")
    
    if pdf_file.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported")
    
    # Check file size (32 MB limit)
    file_size_mb = pdf_file.stat().st_size / (1024 * 1024)
    if file_size_mb > 32:
        raise ValueError(f"File too large: {file_size_mb:.1f} MB (limit 32 MB)")
    
    with open(pdf_file, "rb") as f:
        pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")
    
    # Call API
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_data
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    
    return message.content[0].text


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_pdf.py <pdf_path> [prompt]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else "Please analyze the key points of this document"
    
    try:
        result = analyze_pdf(pdf_path, prompt)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()