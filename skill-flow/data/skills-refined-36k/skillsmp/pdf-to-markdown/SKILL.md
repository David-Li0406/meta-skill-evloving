---
name: pdf-to-markdown
description: Extracting text and tables, merging/splitting documents. Use when needing to convert PDFs while preserving some structure.
---

# PDF to Markdown

## Quick Start

### marker-pdf

- Preserves structure, math, tables, figures.
- This should be your go-to tool for converting PDFs to Markdown with good fidelity.

```bash
# pip install marker-pdf  # python 3.12 or 3.13
marker_single input.pdf --output_dir ./marker-output

# some flags
marker_single input.pdf --output_dir ./out --page_range "0,5-10"  # specific pages
marker_single input.pdf --output_dir ./out --force_ocr  # for scanned PDFs
OUTPUT_IMAGE_FORMAT=PNG marker_single input.pdf --output_dir ./out  # change image format to PNG
```

Output:

- `marker_output/<filename>/<filename>.md`
- extracted images as JPEGs by default.
  - `marker_output/<filename>/_page_<N>_Figure_<M>.jpeg`
