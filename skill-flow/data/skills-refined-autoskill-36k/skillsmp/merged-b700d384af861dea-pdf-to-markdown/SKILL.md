---
name: pdf-to-markdown
description: Use this skill when you need to extract text from PDF files and convert it into Markdown format for editable documentation or further analysis.
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

### With Page Limits

To extract a specific number of pages:

```python
result = await pdf_to_markdown(
    file_path="<input_path>",
    max_pages=<number_of_pages>
)
```

## Output Format

The output will be in JSON format:

```json
{
  "success": true,
  "data": {
    "markdown": "extracted markdown content",
    "page_count": <total_pages>,
    "file_path": "<input_path>"
  }
}
```

## Requirements

- **Python**: Requires `pymupdf` package for PDF processing.
- **Node.js**: Requires `pdf-parse` package. Install with:

```bash
cd <path_to_skill>
npm install
```

## Supported Elements

- Text extraction from digital PDFs
- Headings, paragraphs, basic lists, and links

## Known Limitations

- Limited support for tables and multi-column layouts
- Scanned PDFs require OCR for text extraction
- Images and complex formatting may not be accurately converted

## Alternatives for Unsupported Cases

- For scanned PDFs, consider using OCR libraries or commercial services.
- For complex tables, manual review or AI-based extraction may be necessary.

## Troubleshooting

- If dependencies are not found, run `npm install` in the skill directory.
- Empty output may indicate a scanned PDF requiring OCR.
- For memory issues with large PDFs, use the `--max-old-space-size=4096` flag.

## Task Planning Notes

- Break tasks into smaller steps and include a final review to ensure quality.