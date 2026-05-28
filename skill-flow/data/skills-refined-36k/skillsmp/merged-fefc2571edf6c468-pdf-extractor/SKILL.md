---
name: pdf-extractor
description: Extract text, tables, images, and metadata from PDF files. Use when converting PDF documentation, manuals, or reports to searchable formats.
---

# PDF Extractor Skill

## Purpose

Single responsibility: Extract structured content (text, tables, images, metadata) from PDF files into organized, searchable formats.

## Grounding Checkpoint

Before executing, VERIFY:

- [ ] PDF file exists and is readable (`file <path>` confirms PDF format)
- [ ] PDF is not corrupted (`pdfinfo <path>` returns metadata)
- [ ] Password known if encrypted
- [ ] Output directory is writable
- [ ] Required tools available (pdfplumber, pytesseract for OCR)

**DO NOT proceed without verification. Inspect PDF metadata first.**

## Uncertainty Escalation

ASK USER instead of guessing when:

- PDF appears to be scanned (needs OCR) but OCR tools unavailable
- Multiple table formats detected - unclear which parser to use
- Password-protected but no password provided
- Image extraction quality unclear (resolution, format preferences)
- Language detection needed for OCR

**NEVER assume PDF structure without inspection.**

## Context Scope

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | Target PDF, extraction options, output path | Other PDF files |
| PERIPHERAL | Similar PDF structure examples | Unrelated documents |
| DISTRACTOR | Previous extraction attempts | Other file formats |

## Workflow Steps

### Step 1: Inspect PDF

```bash
# Check file type
file <input_path>

# Get PDF metadata
pdfinfo <input_path>

# Check page count
pdfinfo <input_path> | grep Pages

# Check if encrypted
pdfinfo <input_path> | grep Encrypted
```

### Step 2: Determine Extraction Strategy

| PDF Type | Detection | Strategy |
|----------|-----------|----------|
| Text-based | `pdftotext` produces readable text | Direct extraction |
| Scanned/Image | `pdftotext` produces empty/garbled | OCR required |
| Mixed | Some pages text, some images | Hybrid approach |
| Tables | Visual grid patterns | Table extraction mode |
| Forms | Interactive fields | Form field extraction |

### Step 3: Execute Extraction

**Option A: With skill-seekers (if installed)**

```bash
# Basic extraction
skill-seekers pdf --pdf <input_path> --name <output_name>

# With table extraction
skill-seekers pdf --pdf <input_path> --name <output_name> --extract-tables

# With OCR for scanned docs
skill-seekers pdf --pdf <input_path> --name <output_name> --ocr

# With parallel processing (large PDFs)
skill-seekers pdf --pdf <input_path> --name <output_name> --parallel --workers 8

# Password-protected
skill-seekers pdf --pdf <input_path> --name <output_name> --password "<password>"
```

**Option B: Manual extraction guidance**

```bash
# Basic text extraction
pdftotext -layout <input_path> output.txt

# Extract images
pdfimages -all <input_path> images/

# OCR scanned PDF (requires tesseract)
pdftoppm <input_path> page -png
tesseract page-*.png output -l eng
```

### Step 4: Validate Output

```bash
# Check extraction quality
head -100 output/<output_name>/references/content.md

# Verify table extraction
grep -A 10 "| " output/<output_name>/references/*.md

# Check image extraction
ls -la output/<output_name>/assets/images/
```

## Recovery Protocol

On error:

1. **PAUSE** - Stop extraction, preserve partial output
2. **DIAGNOSE** - Check error type:
   - `File not found` → Verify path
   - `Password required` → Ask user for password
   - `Corrupt PDF` → Try repair with `qpdf --check`
   - `OCR failed` → Check tesseract installation, language packs
   - `Memory error` → Process in chunks, reduce workers
3. **ADAPT** - Switch strategy based on diagnosis
4. **RETRY** - Resume with adapted approach (max 3 attempts)
5. **ESCALATE** - Ask user for guidance

## Output Structure

```
output/<output_name>/
├── SKILL.md              # Skill description with PDF summary
├── references/
│   ├── index.md          # Table of contents
│   ├── chapter_1.md      # Content by section
│   ├── chapter_2.md
│   └── tables.md         # Extracted tables
└── assets/
    └── images/           # Extracted images (if enabled)
        ├── page_1_fig_1.png
        └── page_5_chart_1.png
```

## Configuration Options

```json
{
  "name": "<output_name>",
  "description": "Description of the document being processed",
  "pdf_path": "<input_path>",
  "extract_options": {
    "chunk_size": 10,
    "min_quality": 6.0,
    "extract_images": true,
    "min_image_size": 150,
    "ocr_enabled": false,
    "ocr_language": "eng",
    "table_extraction": true
  },
  "categories": {
    "getting_started": ["introduction", "setup", "installation"],
    "usage": ["using", "operation", "guide"],
    "reference": ["appendix", "specifications", "api"]
  }
}
```

## Dependencies

**Required:**
- Python 3.10+
- pdfplumber or pypdf

**Optional (for advanced features):**
- pytesseract + tesseract-ocr (for OCR)
- Pillow (for image processing)
- camelot-py (for complex tables)

## References

- Skill Seekers PDF Support: https://github.com/jmagly/Skill_Seekers/blob/main/docs/PDF_MCP_TOOL.md
- REF-001: Production-Grade Agentic Workflows
- REF-002: LLM Failure Modes