---
name: sysdoc-edit
description: Guide for editing markdown files in sysdoc system documentation repositories. Apply when creating or modifying .md files in src/ folders.
---

# sysdoc CLI Tool

## Initialize a Document

Create a new document from a DID template:

```sh
sysdoc init <TEMPLATE> [PATH]
```

Options:

- `-t, --title <TITLE>` - Set document title
- `-f, --force` - Overwrite existing files

Available templates:

| Alias | DID Number | Description |
| ----- | -------------- | --------------------------------- |
| SDD | DI-IPSC-81435B | Software Design Description |
| SRS | DI-IPSC-81433A | Software Requirements Specification |
| IDD | DI-IPSC-81436A | Interface Design Description |
| SSS | DI-IPSC-81431A | System/Subsystem Specification |
| SSDD | DI-IPSC-81437A | System/Subsystem Design Description |
| STP | DI-IPSC-81438 | Software Test Plan |
| STD | DI-IPSC-81439 | Software Test Description |
| STR | DI-IPSC-81440 | Software Test Report |
| TR | DI-MISC-80508B | Technical Report |

Example:

```sh
sysdoc init SDD ./my-document -t "My Project Design"
```

## Build Documentation

Build markdown sources to various output formats:

```sh
sysdoc build [PATH] -f <FORMAT> -o <OUTPUT>
```

Output formats:

- `docx` - Microsoft Word
- `markdown` - Markdown with images folder
- `html` - HTML with embedded images
- `pdf` - PDF with embedded images and TOC

Options:

- `-w, --watch` - Watch for changes and rebuild automatically
- `-v, --verbose` - Verbose output
- `--no-toc` - Skip table of contents generation

Examples:

```sh
sysdoc build ./src -f docx -o ./output/document.docx
sysdoc build -f pdf -w   # Watch mode with PDF output
```

## Validate Document

Check document structure and references:

```sh
sysdoc validate [PATH]
```

Options:

- `-v, --verbose` - Show detailed results
- `--check-links` - Validate internal references
- `--check-images` - Verify image files exist
- `--check-tables` - Validate CSV table references

Example:

```sh
sysdoc validate ./src --check-links --check-images
```

---

## Sysdoc Markdown Conventions

### Section Numbers

- sysdoc auto-generates section numbers from filenames - never include them in headings
- Write `# Purpose` not `# 1.1 Purpose`

### File Naming

- Format: `XX.YY_title-slug.md` (e.g., `01.02_scope.md`)
- The `XX.YY` becomes the section number in output
- Only one file per section number

### Parent Sections (.00)

- Files ending in `.00` (e.g., `02.00_architecture.md`) are parent section markers
- The `.00` is stripped in output: `02.00` → section 2

### Heading Rules

- Every `.md` file must have exactly one `# Heading` (H1)
- H2+ headings create nested subsections within the file

### H2 vs Separate Files

- H2 headings create subsections: `03.01_*.md` with H2s → 3.1.1, 3.1.2...
- Separate files do the same: `03.01.01_*.md`, `03.01.02_*.md`
- **Choose one approach per section** - mixing both is ambiguous

### Section Metadata Blocks

Add metadata with a fenced code block using `toml {sysdoc}` or `sysdoc`:

```toml
# Example (use toml {sysdoc} as language identifier)
section_id = "SDD-3.2.1"
traced_ids = ["SRS-REQ-001", "SRS-REQ-002"]
```

- **One metadata block per section** (per heading)
- `section_id` - unique identifier for traceability
- `traced_ids` - array of IDs this section traces to
- `generate_section_id_to_traced_ids_table = ["Col1", "Col2"]` - generates forward traceability table
- `generate_traced_ids_to_section_ids_table = ["Col1", "Col2"]` - generates reverse traceability table

### CSV Tables

Link to CSV files to inline them as tables:

```markdown
[Table Title](path/to/file.csv)
```

The CSV content is automatically rendered as a table in the output.

### Code Block Size

Keep code/text blocks sized to fit on a PDF page:

- Line width: ~80 characters max
- Block height: ~50 lines max (split larger blocks)
