---
name: pdf-to-markdown
description: Use this skill when you need to convert PDF files to Markdown format for easier editing, documentation, or version control.
---

# Skill body

## Overview

This skill allows you to convert PDF files into Markdown format, making it easier to extract and edit text from PDF documents.

## Installation Requirements

Make sure to install the necessary dependencies:

```bash
npm install pdf-parse
```

## Basic Usage

You can use the following command to convert a PDF file to Markdown:

```bash
node path/to/convert.cjs --file /path/to/document.pdf
```

### Custom Output Path

To specify a custom output path for the converted Markdown file, use:

```bash
node path/to/convert.cjs --file /path/to/document.pdf --output /path/to/output.md
```

## Response Format

The output will be in JSON format:

```json
{
  "success": true,
  "input": "/path/to/input.pdf",
  "output": "/path/to/output.md",
  "wordCount": 1523,
  "warnings": ["Tables may not be accurately converted"]
}
```

## Supported Elements

- Text extraction from digital PDFs
- Headings (detected by font size heuristics)
- Paragraphs
- Basic lists
- Links (when embedded in PDF)

## Known Limitations

- **Tables**: Limited support; may not render correctly.
- **Multi-column layouts**: Text may interleave between columns.
- **Scanned PDFs**: Not supported (requires OCR).
- **Images**: Not extracted.
- **Complex formatting**: May be simplified or lost.
- **Password-protected PDFs**: Not supported.

## Alternatives for Unsupported Cases

- For scanned PDFs, consider using OCR libraries or services.
- For complex tables, consider AI-based extraction or manual review.
- For image extraction, process images separately and reference them in Markdown.

## Troubleshooting

- If dependencies are not found, run `npm install` in the skill directory.
- If the output is empty, the PDF may be scanned or image-based (requires OCR).
- For garbled text, the PDF may use unsupported embedded fonts.
- For memory issues with large PDFs, increase the memory limit using `--max-old-space-size=4096`.

## When to Use

- Converting PDF reports to readable text.
- Extracting content from PDF documents for further analysis.
- Creating editable documentation from PDF reports.