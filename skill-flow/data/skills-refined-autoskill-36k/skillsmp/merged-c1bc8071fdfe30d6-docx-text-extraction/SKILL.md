---
name: docx-text-extraction
description: Use this skill when you need to extract text content from Microsoft Word (.docx) files for analysis or processing.
---

# DOCX Text Extraction

This skill extracts text from Microsoft Word (.docx) files, including text from paragraphs and tables.

## Quick Start

### Basic Usage

To extract text from a .docx file, run the following command:

```bash
python3 scripts/extract_docx.py <path_to_docx>
```

### Prerequisites

This skill requires the `python-docx` package. Install it using:

```bash
pip install python-docx
```

## Workflow

### Single File Extraction

1. Specify the absolute path to the .docx file.
2. Run the extraction script.
3. View or save the extracted text.

### Batch Processing

1. Use a glob pattern to find multiple .docx files.
2. Execute the extraction script for each file.
3. Compile and report the results.

## Example Usage

### Example 1: Displaying Content

```bash
python3 scripts/extract_docx.py "/path/to/file.docx"
```

### Example 2: Saving to Markdown

1. Extract text using the script.
2. Format the text as Markdown.
3. Save the output to a .md file.

## Limitations

- Images and complex layouts are not extracted.
- Font styles and colors are lost during extraction.
- Embedded objects are not processed.

## Troubleshooting

### Installation Issues

If you encounter a "No module named 'docx'" error, ensure the package is installed:

```bash
pip uninstall docx
pip install python-docx
```

### File Access Issues

- Verify the file path is correct.
- Ensure the file is not open in another program.
- Check file permissions.

## Path Conversion

When using Windows paths, convert them to the appropriate format:

- `C:\Users\...` → `/mnt/c/Users/...`
- `D:\Projects\...` → `/mnt/d/Projects/...`

## Related Tools

- **pandoc**: For advanced document conversion.
- **python-docx2txt**: A lightweight alternative for text extraction.
- **mammoth**: For converting to HTML format.

## Version History

- v1.0.0 (2026-01-06): Initial release with basic text extraction capabilities.