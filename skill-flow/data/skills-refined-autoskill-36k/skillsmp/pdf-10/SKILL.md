---
name: pdf
description: This skill should be used when the user asks to "read pdf", "view pdf", "extract text from pdf", "summarize pdf", or shares a PDF file path.
---

# /pdf

Read, extract, and analyze PDF documents.

## Instructions

When the user provides a PDF path or asks about PDF content:

### 1. Reading PDFs

Use the `Read` tool directly on the PDF file. Claude Code supports reading PDF files natively:

```
Read: /path/to/document.pdf
```

This extracts both text and visual content for analysis.

### 2. Common Tasks

**Summarize**: Provide a concise summary of the document

- Key points and main arguments
- Document structure overview
- Important figures, tables, or data

**Extract specific info**: Find and extract:

- Tables (convert to markdown format)
- Code snippets
- Citations/references
- Contact information
- Dates and deadlines

**Compare PDFs**: When given multiple PDFs:

- Identify differences
- Highlight common themes
- Cross-reference information

### 3. Python Utility

For batch operations or programmatic access:

```bash
uv run tools/pdf_util.py extract /path/to/file.pdf
uv run tools/pdf_util.py info /path/to/file.pdf
uv run tools/pdf_util.py search /path/to/file.pdf "search term"
```

### 4. Output Format

When presenting PDF content:

- Use markdown headers for document sections
- Convert tables to markdown tables
- Note page numbers for reference: `(p. 5)`
- Flag any extraction issues (scanned images, encrypted content)

### 5. Limitations

- Scanned PDFs may have limited text extraction (OCR not included)
- Some PDFs have copy-protection that prevents text extraction
- Very large PDFs (100+ pages) may need pagination
