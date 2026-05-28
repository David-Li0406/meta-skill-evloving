# Pandoc Templates Guide

How to use and customize Pandoc document templates.

## Available Templates

### 1. academic-paper.yaml
**Purpose:** Academic papers with citations
**Features:**
- Bibliography support
- Citation style (CSL)
- Standard academic formatting
- Table of contents

**Best for:** Research papers, essays, academic assignments

### 2. thesis-report.yaml
**Purpose:** Thesis and long-form reports
**Features:**
- Custom title page
- Supervisor/institution fields
- List of figures/tables
- Chapter-based structure
- Declaration section

**Best for:** Final year projects, dissertations, technical reports

### 3. presentation-beamer.yaml
**Purpose:** PDF presentations via LaTeX Beamer
**Features:**
- Slide themes
- Code highlighting
- Incremental reveals
- Speaker notes

**Best for:** Academic presentations, lectures, conferences

### 4. presentation-revealjs.yaml
**Purpose:** Web-based presentations
**Features:**
- Modern web slides
- Transitions and animations
- Two-column layouts
- Background images
- Fragment animations

**Best for:** Web presentations, online seminars, interactive slides

### 5. article-simple.yaml
**Purpose:** Quick, minimal documents
**Features:**
- Basic metadata only
- Fast compilation
- Minimal configuration

**Best for:** Quick notes, simple documents, drafts

### 6. defaults-pdf.yaml
**Purpose:** Reusable defaults file
**Features:**
- Consistent settings across documents
- Project-wide configuration
- Override-able options

**Best for:** Multi-document projects, team collaboration

### 7. references.bib
**Purpose:** BibTeX bibliography template
**Features:**
- Example entries for all common types
- Field reference guide
- Formatting instructions

**Best for:** Citation management, bibliography creation

## Using Templates

### Method 1: Copy to New File

```bash
PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
cp "$PLUGIN_DIR/skills/pandoc/assets/templates/academic-paper.yaml" paper.md
```

### Method 2: User Command

```bash
/pandoc:template academic-paper paper.md
```

### Method 3: View Then Create

```bash
# View template first
/pandoc:template academic-paper

# Then create when ready
/pandoc:template academic-paper paper.md
```

## Customizing Templates

### 1. Edit Metadata Fields

Replace placeholder values:
```yaml
title: "Your Paper Title"        # Change this
author: "Your Name"              # Change this
date: "November 2024"            # Change this
```

### 2. Add Custom Fields

```yaml
# Add to existing frontmatter
student-id: "C21348423"
module: "COMP4060"
supervisor: "Dr. Smith"
```

### 3. Modify Formatting

```yaml
# Change document appearance
fontsize: 11pt              # Was 12pt
geometry: margin=1.5in      # Was 1in
linestretch: 2.0            # Was 1.5 (now double-spaced)
```

### 4. Bibliography Settings

```yaml
# Change citation style
csl: apa.csl                # Was harvard.csl

# Add multiple bibliography files
bibliography:
  - references.bib
  - additional.bib
```

### 5. LaTeX Customization

```yaml
header-includes: |
  \usepackage{graphicx}
  \usepackage{custom-package}
  \newcommand{\mycommand}{text}
```

## Creating Custom Templates

### Step 1: Start from Existing

```bash
PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"

# Copy closest match
cp "$PLUGIN_DIR/skills/pandoc/assets/templates/academic-paper.yaml" my-template.yaml
```

### Step 2: Customize Frontmatter

Edit `my-template.yaml`:
```yaml
---
# Your custom fields
title: "Template Title"
custom-field: "Custom Value"

# Your formatting preferences
documentclass: report
fontsize: 12pt
geometry: "left=1.5in, right=1in"
linestretch: 1.5

# Your packages
header-includes: |
  \usepackage{custom}
---

# Template Content

Your template content here.
```

### Step 3: Save for Reuse

```bash
# Save in project
mkdir -p .pandoc/templates/
mv my-template.yaml .pandoc/templates/

# Use it
cp .pandoc/templates/my-template.yaml new-document.md
```

## Template Inheritance

### Using Defaults Files

Create base configuration:

**.pandoc/base.yaml:**
```yaml
from: markdown
to: pdf
pdf-engine: pdflatex

metadata:
  lang: en-GB
  fontsize: 12pt
  geometry: margin=1in
```

**Use in document:**
```bash
pandoc document.md --defaults=.pandoc/base.yaml -o output.pdf
```

### Layered Defaults

**Base settings:**
```yaml
# .pandoc/base.yaml
metadata:
  fontsize: 12pt
  lang: en-GB
```

**Citation settings:**
```yaml
# .pandoc/citations.yaml
citeproc: true
metadata:
  link-citations: true
```

**Combine:**
```bash
pandoc doc.md \
    --defaults=.pandoc/base.yaml \
    --defaults=.pandoc/citations.yaml \
    -o output.pdf
```

## Project Templates

### Academic Project Structure

```
project/
├── .pandoc/
│   ├── defaults.yaml         # Project-wide settings
│   ├── templates/
│   │   ├── chapter.yaml      # Chapter template
│   │   └── appendix.yaml     # Appendix template
│   └── filters/
│       └── custom.lua        # Custom filters
├── chapters/
│   ├── chapter1.md
│   ├── chapter2.md
│   └── chapter3.md
├── references.bib
├── harvard.csl
└── Makefile
```

### Makefile for Project

```makefile
# Variables
PANDOC = pandoc
DEFAULTS = .pandoc/defaults.yaml
CHAPTERS = chapters/*.md
OUTPUT = thesis.pdf

# Main targets
all: $(OUTPUT)

$(OUTPUT): $(CHAPTERS) references.bib
	$(PANDOC) $(CHAPTERS) \
		--defaults=$(DEFAULTS) \
		-o $(OUTPUT)

# Individual chapters
chapter%.pdf: chapters/chapter%.md
	$(PANDOC) $< \
		--defaults=$(DEFAULTS) \
		-o $@

# Clean
clean:
	rm -f *.pdf

# Help
help:
	@echo "Available targets:"
	@echo "  all           - Build complete thesis"
	@echo "  chapter%.pdf  - Build individual chapter"
	@echo "  clean         - Remove generated PDFs"

.PHONY: all clean help
```

**Usage:**
```bash
make                # Build thesis
make chapter1.pdf   # Build chapter 1 only
make clean          # Remove PDFs
```

## Template Best Practices

### 1. Use Placeholders

```yaml
title: "Document Title"          # Clear what to change
author: "Author Name"            # Not "TODO" or "FILL IN"
date: "Date"                     # Simple placeholder
```

### 2. Include Comments

```yaml
documentclass: report  # Options: article, report, book
fontsize: 12pt        # Options: 10pt, 11pt, 12pt
geometry: margin=1in  # Or: margin=2cm, left=1.5in
```

### 3. Provide Examples

```yaml
# Single author
author: "Author Name"

# Multiple authors
# author:
#   - "First Author"
#   - "Second Author"
```

### 4. Set Sensible Defaults

```yaml
lang: en-GB               # British English
fontsize: 12pt           # Standard academic
geometry: margin=1in     # Standard margins
linestretch: 1.5         # Standard spacing
```

### 5. Document Requirements

```yaml
# Required files for this template:
# - references.bib (bibliography)
# - harvard.csl (citation style)
# - logo.png (if using custom title page)
```

## Troubleshooting Templates

### Template Won't Convert

**Check:**
1. YAML syntax (spaces not tabs)
2. Required files exist
3. Field names spelled correctly
4. Values properly quoted

**Validate:**
```bash
PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
python3 "$PLUGIN_DIR/skills/pandoc/scripts/validate.py" template.md
```

### Custom Fields Not Working

Some fields are LaTeX-specific:
```yaml
# Works in PDF
geometry: margin=1in

# Doesn't work in HTML/DOCX
# Use CSS for HTML instead
```

### Bibliography Issues

**Ensure:**
```yaml
bibliography: references.bib  # File exists
csl: harvard.csl             # File exists
```

**Then convert with:**
```bash
pandoc doc.md -o doc.pdf --citeproc
```

## Advanced Customization

### Custom LaTeX Template

**Create template.tex:**
```latex
\documentclass{$documentclass$}

% Packages
$for(header-includes)$
$header-includes$
$endfor$

\title{$title$}
\author{$author$}
\date{$date$}

\begin{document}
\maketitle

$body$

\end{document}
```

**Use template:**
```bash
pandoc doc.md -o doc.pdf --template=template.tex
```

### Conditional Content

```yaml
# In frontmatter
draft: true
```

```markdown
<!-- In document -->
$if(draft)$
**DRAFT VERSION**
$endif$
```

### Variables in Content

**Frontmatter:**
```yaml
institution: "University Name"
```

**Content:**
```markdown
This research was conducted at $institution$.
```

## Resources

- **Pandoc Templates:** https://pandoc.org/MANUAL.html#templates
- **Template Variables:** https://pandoc.org/MANUAL.html#variables
- **LaTeX Templates:** https://www.latextemplates.com/
- **CSL Styles:** https://github.com/citation-style-language/styles
