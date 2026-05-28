# Pandoc Quick Reference Snippets

Copy-paste ready commands for common Pandoc operations.

## Validation

```bash
# Validate document
PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
python3 "$PLUGIN_DIR/skills/pandoc/scripts/validate.py" document.md
```

## Basic Conversions

```bash
# Markdown to PDF
pandoc document.md -o document.pdf

# Markdown to HTML
pandoc document.md -o document.html --standalone

# Markdown to DOCX
pandoc document.md -o document.docx
```

## PDF with Options

```bash
# Academic paper
pandoc paper.md -o paper.pdf \
    --pdf-engine=pdflatex \
    --citeproc \
    --number-sections \
    --toc

# With XeLaTeX (Unicode support)
pandoc paper.md -o paper.pdf \
    --pdf-engine=xelatex \
    --citeproc \
    --number-sections

# Custom margins
pandoc doc.md -o doc.pdf \
    -V geometry:margin=1.5in
```

## HTML with Options

```bash
# Standalone HTML with TOC
pandoc doc.md -o doc.html \
    --standalone \
    --toc \
    --toc-depth=3

# Self-contained (embed resources)
pandoc doc.md -o doc.html \
    --standalone \
    --self-contained

# With custom CSS
pandoc doc.md -o doc.html \
    --standalone \
    --css=style.css

# With syntax highlighting
pandoc doc.md -o doc.html \
    --standalone \
    --highlight-style=tango
```

## Presentations

```bash
# Beamer PDF slides
pandoc slides.md -o slides.pdf --to beamer

# reveal.js web slides
pandoc slides.md -o slides.html \
    --to revealjs \
    --standalone \
    -V theme=black

# With custom theme
pandoc slides.md -o slides.pdf \
    --to beamer \
    -V theme=Madrid \
    -V colortheme=dolphin
```

## Using Templates

```bash
# Copy template
PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
cp "$PLUGIN_DIR/skills/pandoc/assets/templates/academic-paper.yaml" paper.md

# Copy bibliography template
cp "$PLUGIN_DIR/skills/pandoc/assets/templates/references.bib" references.bib

# Copy Makefile
cp "$PLUGIN_DIR/skills/pandoc/assets/templates/Makefile" Makefile
```

## Using Defaults Files

```bash
# Create defaults file
PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
cp "$PLUGIN_DIR/skills/pandoc/assets/templates/defaults-pdf.yaml" defaults.yaml

# Use defaults
pandoc document.md --defaults=defaults.yaml -o output.pdf

# Override output
pandoc document.md --defaults=defaults.yaml -o custom-name.pdf
```

## Project Setup

```bash
# Create project structure
mkdir -p project/{images,.pandoc}
cd project

# Copy templates
PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
cp "$PLUGIN_DIR/skills/pandoc/assets/templates/academic-paper.yaml" paper.md
cp "$PLUGIN_DIR/skills/pandoc/assets/templates/references.bib" references.bib
cp "$PLUGIN_DIR/skills/pandoc/assets/templates/defaults-pdf.yaml" .pandoc/defaults.yaml
cp "$PLUGIN_DIR/skills/pandoc/assets/templates/Makefile" Makefile

# Setup local scripts
make setup

# Build
make
```

## Batch Conversion

```bash
# Convert all MD files to PDF
for file in *.md; do
    pandoc "$file" -o "${file%.md}.pdf" --pdf-engine=pdflatex
done

# With validation
PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
for file in *.md; do
    if python3 "$PLUGIN_DIR/skills/pandoc/scripts/validate.py" "$file"; then
        pandoc "$file" -o "${file%.md}.pdf"
    fi
done
```

## Download Citation Styles

```bash
# Harvard
curl -o harvard.csl https://raw.githubusercontent.com/citation-style-language/styles/master/harvard-cite-them-right.csl

# APA
curl -o apa.csl https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl

# IEEE
curl -o ieee.csl https://raw.githubusercontent.com/citation-style-language/styles/master/ieee.csl

# Chicago
curl -o chicago.csl https://raw.githubusercontent.com/citation-style-language/styles/master/chicago-author-date.csl
```

## Debugging

```bash
# Check Pandoc version
pandoc --version

# Generate LaTeX to inspect
pandoc doc.md -o doc.tex
cat doc.tex

# Minimal test
echo "# Test" > test.md
pandoc test.md -o test.pdf

# Verbose output
pandoc doc.md -o doc.pdf --verbose
```

## Environment Variables

```bash
# Set plugin directory
export PANDOC_PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"

# Use in commands
python3 "$PANDOC_PLUGIN_DIR/skills/pandoc/scripts/validate.py" document.md
```

## Shell Functions

```bash
# Add to ~/.bashrc or ~/.zshrc

# Validate and convert
pandoc-convert() {
    PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
    python3 "$PLUGIN_DIR/skills/pandoc/scripts/validate.py" "$1" && \
    pandoc "$1" -o "$2" --pdf-engine=pdflatex --citeproc --number-sections
}

# Usage: pandoc-convert paper.md paper.pdf

# Quick validate
pandoc-validate() {
    PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
    python3 "$PLUGIN_DIR/skills/pandoc/scripts/validate.py" "$1"
}

# Usage: pandoc-validate document.md
```

## Git Integration

```bash
# .gitignore for Pandoc projects
cat > .gitignore << 'EOF'
# Generated files
*.pdf
*.html
*.docx
*.tex

# LaTeX auxiliary files
*.aux
*.log
*.out
*.toc

# Keep source files
!*.md
!*.bib
!*.csl
!*.yaml
EOF
```

## CI/CD (GitHub Actions)

```yaml
# .github/workflows/build.yml
name: Build Document

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install Pandoc
        run: |
          sudo apt-get update
          sudo apt-get install -y pandoc texlive-latex-base

      - name: Build PDF
        run: |
          pandoc document.md -o document.pdf \
            --pdf-engine=pdflatex \
            --citeproc

      - name: Upload artifact
        uses: actions/upload-artifact@v2
        with:
          name: document
          path: document.pdf
```

## Common Patterns

```bash
# Academic paper workflow
PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
cp "$PLUGIN_DIR/skills/pandoc/assets/templates/academic-paper.yaml" paper.md
# Edit paper.md
python3 "$PLUGIN_DIR/skills/pandoc/scripts/validate.py" paper.md
pandoc paper.md -o paper.pdf --pdf-engine=pdflatex --citeproc --number-sections

# Web article workflow
pandoc article.md -o article.html --standalone --toc --css=style.css

# Presentation workflow
cp "$PLUGIN_DIR/skills/pandoc/assets/templates/presentation-revealjs.yaml" slides.md
# Edit slides.md
pandoc slides.md -o slides.html --to revealjs --standalone
```
