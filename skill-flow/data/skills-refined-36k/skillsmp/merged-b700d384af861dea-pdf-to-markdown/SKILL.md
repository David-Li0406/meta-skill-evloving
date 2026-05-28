---
name: pdf-to-markdown
description: Use this skill when you need to extract text from PDF files and convert it to Markdown format for editable documentation or further analysis.
---

# PDF to Markdown Conversion

This skill provides tools for converting PDF files into Markdown format, allowing for easy text extraction and document editing.

## Basic Usage

### Python Example

To extract text from a PDF file and convert it to Markdown:

```python
result = await pdf_to_markdown(file_path="<input_path>")
# Returns: {"success": True, "data": {"markdown": "# Document Title\n\nContent..."}}
```

### Node.js Example

For a basic conversion using the command line:

```bash
node <path_to_skill>/scripts/convert.cjs --file <input_path>
```

### Custom Output Path

To specify a custom output path:

```bash
node <path_to_skill>/scripts/convert.cjs --file <input_path> --output <output_path>
```

## Response Format

The output will be in JSON format:

```json
{
  "success": true,
  "data": {
    "markdown": "extracted markdown content",
    "input": "<input_path>",
    "output": "<output_path>",
    "wordCount": 1523,
    "warnings": ["Tables may not be accurately converted"]
  }
}
```

## Supported Elements

- Text extraction from digital PDFs
- Headings, paragraphs, and basic lists
- Links embedded in the PDF

## Known Limitations

- **Tables**: Limited support; may not render correctly.
- **Multi-column layouts**: Text may interleave between columns.
- **Scanned PDFs**: Not supported (requires OCR).
- **Images**: Not extracted.
- **Complex formatting**: May be simplified or lost.
- **Password-protected PDFs**: Not supported.

## Alternatives for Unsupported Cases

- For scanned PDFs, consider using OCR libraries or commercial services.
- For complex tables, consider AI-based extraction or manual review.
- For image extraction, use dedicated libraries and process images separately.

## Requirements

- Python: `pymupdf` package for PDF processing.
- Node.js: `pdf-parse` dependency.

## Troubleshooting

- If dependencies are not found, run `npm install` in the skill directory.
- Empty output may indicate a scanned PDF (requires OCR).
- Garbled text may result from unsupported embedded fonts.
- For large PDFs, increase memory allocation with `--max-old-space-size=4096`.

## Task Planning Notes

- Break tasks into smaller steps and include a final review to ensure quality.