# Pandoc Quick Reference

Fast reference for common pandoc document conversion commands.

## Common Conversions

### Markdown to PDF
```bash
pandoc input.md -o output.pdf
pandoc input.md -o output.pdf --pdf-engine=xelatex  # Unicode support
```

### Markdown to DOCX
```bash
pandoc input.md -o output.docx
pandoc input.md -o output.docx --reference-doc=template.docx  # Custom styling
```

### DOCX to Markdown
```bash
pandoc input.docx -o output.md
pandoc input.docx -t markdown-smart -o output.md  # Preserve smart quotes
```

### Markdown to HTML
```bash
pandoc input.md -o output.html -s  # Standalone with headers
pandoc input.md -o output.html -s --toc  # With table of contents
```

### Reveal.js Slides
```bash
pandoc slides.md -o slides.html -t revealjs -s
pandoc slides.md -o slides.html -t revealjs -s --slide-level=2
```

## Academic Writing

### With Bibliography
```bash
pandoc paper.md --bibliography=refs.bib --csl=harvard.csl -o paper.pdf
```

### Custom LaTeX Template
```bash
pandoc input.md --template=custom.latex -o output.pdf
```

### Cross-References (with pandoc-crossref)
```bash
pandoc paper.md --filter pandoc-crossref --bibliography=refs.bib -o paper.pdf
```

## Filters

### Lua Filter
```bash
pandoc input.md --lua-filter=custom.lua -o output.html
```

### Multiple Filters
```bash
pandoc input.md --filter pandoc-crossref --filter pandoc-citeproc -o output.pdf
```

## Common Options

| Option | Purpose |
|--------|---------|
| `-o FILE` | Output file (format detected from extension) |
| `-s, --standalone` | Produce standalone document with headers |
| `-t FORMAT` | Target format (markdown, html, latex, etc.) |
| `-f FORMAT` | Source format (auto-detected usually) |
| `--pdf-engine=ENGINE` | PDF engine (xelatex, lualatex, pdflatex) |
| `--toc` | Include table of contents |
| `--number-sections` | Number section headings |
| `--metadata KEY=VAL` | Set metadata field |
| `--variable KEY=VAL` | Set template variable |
| `--template=FILE` | Use custom template |
| `--bibliography=FILE` | Bibliography file (.bib) |
| `--csl=FILE` | Citation style (.csl) |
| `--lua-filter=FILE` | Apply Lua filter |
| `--reference-doc=FILE` | Reference DOCX for styling |

## Troubleshooting

### PDF Generation Fails
```bash
# Install LaTeX (Fedora)
sudo dnf install texlive-scheme-full

# Use alternative PDF engine
pandoc input.md -o output.pdf --pdf-engine=xelatex
```

### Unicode Characters Missing
```bash
# Use XeLaTeX or LuaLaTeX for Unicode support
pandoc input.md -o output.pdf --pdf-engine=xelatex
```

### Bibliography Not Working
```bash
# Ensure .bib file exists and is referenced correctly
pandoc paper.md --bibliography=refs.bib --csl=harvard.csl -o paper.pdf

# For older pandoc versions, use pandoc-citeproc filter
pandoc paper.md --filter pandoc-citeproc --bibliography=refs.bib -o paper.pdf
```

### Images Not Appearing
```bash
# Use --resource-path to specify image directory
pandoc input.md -o output.pdf --resource-path=.:images/

# Embed images as base64
pandoc input.md -o output.html --embed-resources --standalone
```

## Resources

- **Official Manual**: https://pandoc.org/MANUAL.html
- **Templates**: https://pandoc.org/MANUAL.html#templates
- **Lua Filters**: https://pandoc.org/lua-filters.html
- **CSL Styles**: https://www.zotero.org/styles
- **User Guide**: https://pandoc.org/getting-started.html
- **GitHub**: https://github.com/jgm/pandoc
