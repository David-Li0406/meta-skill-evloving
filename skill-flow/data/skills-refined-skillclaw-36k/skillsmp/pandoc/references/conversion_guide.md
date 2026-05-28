# Pandoc Conversion Guide

Format-specific conversion instructions and best practices.

## PDF Conversion

### Basic PDF

```bash
pandoc document.md -o document.pdf
```

### With Smart Defaults

```bash
pandoc document.md -o document.pdf \
    --pdf-engine=pdflatex \
    --number-sections
```

### PDF Engines

**pdflatex (default)**
- Fast, widely available
- ASCII-only (no Unicode support)
- Good for most documents
```bash
pandoc doc.md -o doc.pdf --pdf-engine=pdflatex
```

**XeLaTeX**
- Unicode support
- Custom fonts
- Slightly slower
```bash
pandoc doc.md -o doc.pdf --pdf-engine=xelatex
```

**LuaLaTeX**
- Modern, full Unicode
- Advanced typography
- Slowest option
```bash
pandoc doc.md -o doc.pdf --pdf-engine=lualatex
```

### With Citations

```bash
pandoc paper.md -o paper.pdf \
    --pdf-engine=pdflatex \
    --citeproc \
    --number-sections
```

### Custom Margins

```bash
pandoc doc.md -o doc.pdf \
    -V geometry:margin=1.5in
```

### Table of Contents

```bash
pandoc doc.md -o doc.pdf \
    --toc \
    --toc-depth=3
```

### Custom Template

```bash
pandoc doc.md -o doc.pdf \
    --template=custom.tex
```

## HTML Conversion

### Standalone HTML

```bash
pandoc doc.md -o doc.html --standalone
```

### Self-Contained (Embed Resources)

```bash
pandoc doc.md -o doc.html \
    --standalone \
    --self-contained
```

### With Table of Contents

```bash
pandoc doc.md -o doc.html \
    --standalone \
    --toc \
    --toc-depth=3
```

### Custom CSS

```bash
pandoc doc.md -o doc.html \
    --standalone \
    --css=style.css
```

### Syntax Highlighting

```bash
pandoc doc.md -o doc.html \
    --standalone \
    --highlight-style=tango
```

Available highlight styles:
- `tango` (default)
- `pygments`
- `kate`
- `monochrome`
- `espresso`
- `zenburn`
- `haddock`
- `breezedark`

### Fragment (No HTML/Body Tags)

```bash
pandoc doc.md -o fragment.html
# No --standalone flag
```

## DOCX Conversion

### Basic DOCX

```bash
pandoc doc.md -o doc.docx
```

### With Reference Template

```bash
pandoc doc.md -o doc.docx \
    --reference-doc=template.docx
```

### With Citations

```bash
pandoc paper.md -o paper.docx \
    --citeproc
```

### Preserve Formatting

```bash
pandoc doc.md -o doc.docx \
    --standalone
```

## Presentation Conversion

### Beamer (PDF Slides)

**Basic:**
```bash
pandoc slides.md -o slides.pdf --to beamer
```

**With Theme:**
```yaml
---
title: "Presentation"
author: "Name"
theme: Madrid
colortheme: default
---
```

```bash
pandoc slides.md -o slides.pdf --to beamer
```

**Slide Breaks:**
```markdown
# Section Title

## Slide 1

Content

## Slide 2

More content
```

### reveal.js (Web Slides)

**Basic:**
```bash
pandoc slides.md -o slides.html \
    --to revealjs \
    --standalone
```

**With Theme:**
```bash
pandoc slides.md -o slides.html \
    --to revealjs \
    --standalone \
    -V theme=black \
    -V transition=slide
```

**Available Themes:**
- black (default)
- white
- league
- beige
- sky
- night
- serif
- simple
- solarized

**Custom Background:**
```markdown
## Slide Title {background-color="#2E3440"}

Content
```

**Two Columns:**
```markdown
::::: {.columns}

:::: {.column width="50%"}
Left content
::::

:::: {.column width="50%"}
Right content
::::

:::::
```

## Advanced Options

### Metadata Override

```bash
pandoc doc.md -o doc.pdf \
    -M title="New Title" \
    -M author="Author Name"
```

### Include Files

```bash
pandoc doc.md -o doc.pdf \
    --include-before-body=header.tex \
    --include-after-body=footer.tex
```

### Filters

```bash
pandoc doc.md -o doc.pdf \
    --filter pandoc-citeproc \
    --lua-filter=custom.lua
```

### Resource Path

```bash
pandoc doc.md -o doc.pdf \
    --resource-path=.:images:assets
```

### Variables

```bash
pandoc doc.md -o doc.pdf \
    -V documentclass=report \
    -V fontsize=12pt \
    -V geometry:margin=1in
```

## Defaults Files

Instead of long command lines, use defaults files:

**Create defaults file:**
```yaml
# defaults.yaml
from: markdown
to: pdf
pdf-engine: pdflatex
citeproc: true
number-sections: true
metadata:
  fontsize: 12pt
  geometry: margin=1in
```

**Use defaults:**
```bash
pandoc doc.md --defaults=defaults.yaml -o doc.pdf
```

## Batch Conversion

### Convert All MD Files

```bash
for file in *.md; do
    pandoc "$file" -o "${file%.md}.pdf" --pdf-engine=pdflatex
done
```

### With Validation

```bash
PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"

for file in *.md; do
    if python3 "$PLUGIN_DIR/skills/pandoc/scripts/validate.py" "$file"; then
        pandoc "$file" -o "${file%.md}.pdf"
    fi
done
```

## Format Detection

Pandoc auto-detects formats from extensions:

| Extension | Format |
|-----------|--------|
| `.md`, `.markdown` | Markdown |
| `.pdf` | PDF |
| `.html`, `.htm` | HTML |
| `.docx` | DOCX |
| `.tex` | LaTeX |
| `.epub` | EPUB |
| `.rst` | reStructuredText |
| `.org` | Org-mode |

Override with `--from` and `--to`:
```bash
pandoc input.txt --from markdown --to html -o output.html
```

## Common Patterns

### Academic Paper

```bash
pandoc paper.md -o paper.pdf \
    --pdf-engine=pdflatex \
    --citeproc \
    --number-sections \
    --toc \
    --toc-depth=3
```

### Web Article

```bash
pandoc article.md -o article.html \
    --standalone \
    --self-contained \
    --toc \
    --css=style.css \
    --highlight-style=tango
```

### Presentation

```bash
pandoc slides.md -o slides.html \
    --to revealjs \
    --standalone \
    -V theme=black \
    -V transition=slide
```

### Book/Thesis

```bash
pandoc thesis.md -o thesis.pdf \
    --pdf-engine=xelatex \
    --citeproc \
    --number-sections \
    --toc \
    --toc-depth=4 \
    -V documentclass=book \
    -V fontsize=12pt \
    -V geometry:margin=1in
```

## Performance Tips

1. **Use pdflatex for speed** - Switch to xelatex only if needed
2. **Cache intermediate files** - Use `--standalone` wisely
3. **Batch similar conversions** - Reuse pandoc process
4. **Optimize images** - Compress before embedding
5. **Use defaults files** - Faster than parsing long command lines
