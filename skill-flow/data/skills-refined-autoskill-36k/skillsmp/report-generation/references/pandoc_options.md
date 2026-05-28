# Pandoc Configuration Reference

Advanced Pandoc options for report generation.

## Basic Command Structure

```bash
pandoc input.md -o output.pdf [options]
```

## Output Formats

| Format | Extension | Engine Required |
|--------|-----------|-----------------|
| PDF | `.pdf` | LaTeX (xelatex, pdflatex) |
| Word | `.docx` | None |
| HTML | `.html` | None |
| EPUB | `.epub` | None |

## Common Options

### Table of Contents
```bash
--toc                    # Enable TOC
--toc-depth=3            # Heading depth (1-6)
```

### Section Numbering
```bash
--number-sections        # Add section numbers
--number-offset=1        # Start from different number
```

### PDF Engine
```bash
--pdf-engine=xelatex     # Better Unicode (recommended)
--pdf-engine=pdflatex    # Standard LaTeX
--pdf-engine=lualatex    # Lua-based LaTeX
```

### Page Layout
```bash
-V geometry:margin=1in   # Set margins
-V geometry:a4paper      # Paper size
-V fontsize=11pt         # Font size (10pt, 11pt, 12pt)
```

### Colors
```bash
-V colorlinks=true       # Enable colored links
-V linkcolor=blue        # Internal links
-V urlcolor=blue         # External URLs
-V citecolor=blue        # Citations
```

## Citation Processing

### Using CSL
```bash
--citeproc               # Enable citation processing
--bibliography=refs.bib  # BibTeX file
--csl=ieee.csl           # Citation style
```

### Citation Formats Supported
- BibTeX (`.bib`)
- CSL JSON (`.json`)
- CSL YAML (`.yaml`)

### Example with Citations
```bash
pandoc report.md -o report.pdf \
  --citeproc \
  --bibliography=references.bib \
  --csl=ieee.csl \
  --toc \
  --pdf-engine=xelatex
```

## Templates

### Using Custom Template
```bash
--template=mytemplate.tex
```

### Template Variables
```bash
-V title="Report Title"
-V author="Author Name"
-V date="January 2024"
-V subtitle="Subtitle"
```

### Default Template Location
```bash
pandoc --print-default-template=latex > template.tex
```

## Metadata (YAML Frontmatter)

Include in markdown file:
```yaml
---
title: "Project Report"
subtitle: "Technical Specification"
author: "Project Team"
date: "January 2024"
abstract: |
  This report provides a comprehensive overview...
toc: true
toc-depth: 3
numbersections: true
geometry: margin=1in
fontsize: 11pt
---
```

## Code Highlighting

### Enable Syntax Highlighting
```bash
--highlight-style=tango
```

### Available Styles
- `pygments` (default)
- `tango`
- `espresso`
- `zenburn`
- `kate`
- `monochrome`
- `breezedark`
- `haddock`

### Disable Highlighting
```bash
--no-highlight
```

## Images

### Image Settings
```bash
-V graphics=true         # Enable graphics
```

### In Markdown
```markdown
![Caption](image.png){width=80%}
```

## Filters

### Lua Filters
```bash
--lua-filter=filter.lua
```

### Common Filters
- `pagebreak.lua` - Handle page breaks
- `diagram.lua` - Generate diagrams

## Complete Example

### Professional PDF Report
```bash
pandoc report.md -o report.pdf \
  --toc \
  --toc-depth=3 \
  --number-sections \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V colorlinks=true \
  -V linkcolor=blue \
  -V urlcolor=blue \
  --highlight-style=tango \
  --citeproc \
  --bibliography=references.bib \
  --csl=ieee.csl
```

### Word Document
```bash
pandoc report.md -o report.docx \
  --toc \
  --toc-depth=3 \
  --number-sections \
  --reference-doc=template.docx
```

### Standalone HTML
```bash
pandoc report.md -o report.html \
  --standalone \
  --toc \
  --self-contained \
  --css=style.css
```

## Troubleshooting

### Common Errors

| Error | Solution |
|-------|----------|
| "xelatex not found" | Install LaTeX: `brew install --cask mactex` |
| "Missing Unicode char" | Use `--pdf-engine=xelatex` |
| "Image not found" | Use absolute paths or set resource-path |
| "CSL file not found" | Provide full path to CSL file |

### Debug Mode
```bash
pandoc input.md -o output.pdf --verbose
```

### Check Version
```bash
pandoc --version
```

## Dependencies Installation

### macOS
```bash
brew install pandoc
brew install --cask mactex  # For PDF output
```

### Ubuntu/Debian
```bash
apt-get install pandoc
apt-get install texlive-xetex  # For PDF output
```

### Check All Dependencies
```bash
# Check pandoc
pandoc --version

# Check LaTeX
xelatex --version

# Check available PDF engines
which xelatex pdflatex lualatex
```
