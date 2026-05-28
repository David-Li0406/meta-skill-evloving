# Design Export Detailed Instructions

Complete step-by-step workflow for exporting design documentation to various
formats.

## Detailed Workflow

### 1. Parse Parameters

Extract module, format, and export options from user request.

**Parameter parsing examples:**

- `/design-export --format=pdf` → all modules, PDF format
- `/design-export effect-type-registry --format=html` → single module, HTML
- `/design-export module --format=markdown --standalone` → standalone file

### 2. Load Configuration

Read `.claude/design/design.config.json` to get:

- Module configuration
- Design docs paths
- Export settings (if configured)

### 3. Collect Documents

Find all design docs to export based on scope.

**Module-specific:**

```bash
glob "*.md" --path=".claude/design/{module}"
```

**All modules:**

```bash
for module in ${modules[@]}; do
  glob "*.md" --path=".claude/design/${module}"
done
```

**Filtering:**

- Exclude archived docs (unless --include-archived)
- Sort by module, then category, then filename

### 4. Prepare Content

Prepare documents for export.

**For each document:**

1. Read content
2. Process frontmatter (include or strip based on format)
3. Resolve relative links to absolute (for standalone exports)
4. Process images (embed or link)
5. Apply format-specific transformations

**Link resolution:**

```bash
# Relative link
./other-doc.md

# Absolute link (for standalone)
.claude/design/module/other-doc.md

# Web link (for HTML export)
https://example.com/docs/module/other-doc.html
```

### 5. Generate Export

See [export-formats.md](export-formats.md) for format specifications.

**PDF export (via Pandoc):**

```bash
pandoc input.md \
  --from=markdown \
  --to=pdf \
  --pdf-engine=xelatex \
  --metadata title="Design Documentation" \
  --toc \
  --toc-depth=3 \
  --output=output.pdf
```

**HTML export:**

```bash
pandoc input.md \
  --from=markdown \
  --to=html5 \
  --standalone \
  --css=style.css \
  --toc \
  --metadata title="Design Documentation" \
  --output=output.html
```

**Markdown export:**

Combine multiple markdown files with section dividers:

```markdown
# Design Documentation Export

---

# Module: effect-type-registry

## Document: observability.md

[Content...]

---

## Document: cache-optimization.md

[Content...]

---

# Module: rspress-plugin-api-extractor

[...]
```

### 6. Apply Styling

Apply format-specific styling and theming.

**PDF styling:**

- Custom LaTeX template
- Typography settings
- Page layout (margins, headers, footers)
- Syntax highlighting theme

**HTML styling:**

- CSS stylesheet
- Responsive layout
- Navigation menu
- Syntax highlighting

**Markdown styling:**

- Consistent heading levels
- Table of contents
- Code block formatting

### 7. Generate Table of Contents

Create navigation structure.

**Automatic TOC generation:**

```javascript
function generateTOC(documents) {
  const toc = []

  for (module of groupByModule(documents)) {
    toc.push({
      level: 1,
      title: module.name,
      children: []
    })

    for (doc of module.docs) {
      toc[toc.length - 1].children.push({
        level: 2,
        title: doc.title,
        link: doc.anchor
      })
    }
  }

  return renderTOC(toc)
}
```

### 8. Write Export File

Write final export to output path.

**Default paths:**

- PDF: `.claude/exports/design-docs-{date}.pdf`
- HTML: `.claude/exports/design-docs-{date}.html`
- Markdown: `.claude/exports/design-docs-{date}.md`

**Custom path:**

Use `--output` parameter to specify custom location.

### 9. Generate Metadata

Create metadata file alongside export.

```yaml
---
exported: 2026-01-17T15:30:00Z
format: pdf
modules: [effect-type-registry, rspress-plugin-api-extractor]
document_count: 12
export_size: 2.5 MB
---
```

### 10. Report Results

Generate export summary:

```markdown
# Export Complete

**Format:** PDF
**Modules:** 2
**Documents:** 12
**Output:** .claude/exports/design-docs-2026-01-17.pdf
**Size:** 2.5 MB

## Export Details

- effect-type-registry: 4 documents
- rspress-plugin-api-extractor: 8 documents

## Next Steps

1. Review exported file
2. Distribute to stakeholders
3. Archive export for records
```

## Export Formats

### PDF Export

**Requirements:**

- Pandoc installed
- LaTeX engine (xelatex or pdflatex)

**Features:**

- Professional typography
- Page numbers
- Headers/footers
- Table of contents with page numbers
- Syntax highlighting
- Cross-references

**Options:**

- `--toc-depth`: TOC depth (default: 3)
- `--paper-size`: a4, letter (default: letter)
- `--font-size`: 10pt, 11pt, 12pt (default: 11pt)

### HTML Export

**Requirements:**

- Pandoc installed
- CSS stylesheet (optional)

**Features:**

- Responsive design
- Navigation menu
- Syntax highlighting
- Search functionality (if JavaScript included)
- External links support

**Options:**

- `--css`: Custom CSS file
- `--self-contained`: Embed all resources
- `--standalone`: Complete HTML document

### Markdown Export

**Features:**

- Portable format
- Compatible with GitHub/GitLab
- Can be re-imported
- Preserves frontmatter

**Options:**

- `--flatten`: Single file vs. directory
- `--preserve-structure`: Keep file organization
- `--strip-frontmatter`: Remove YAML frontmatter

## Advanced Features

### Batch Export

Export to multiple formats at once:

```bash
/design-export --format=pdf,html,markdown
```

### Selective Export

Export specific categories or statuses:

```bash
/design-export --category=architecture
/design-export --status=current
```

### Incremental Export

Export only changed documents since last export:

```bash
/design-export --since=2026-01-01
```

### Template Customization

Use custom export templates:

```bash
/design-export --template=custom.latex
```
