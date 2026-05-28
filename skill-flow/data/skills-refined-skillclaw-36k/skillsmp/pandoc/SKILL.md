---
name: pandoc
description: Automatically assist with Pandoc document conversions when user mentions converting markdown to PDF/DOCX/HTML or other formats. Validate YAML frontmatter, check dependencies (bibliography, images), and provide format-specific conversion guidance. Use when user asks about citations, academic papers, presentations, or document generation from markdown.
allowed-tools: Bash, Read, Write
---

# Pandoc Document Conversion

## Overview

Provide expert assistance for converting markdown documents to PDF, DOCX, HTML, and presentations using Pandoc. Handle YAML frontmatter validation, bibliography setup, template generation, and format-specific conversion guidance.

## When to Use This Skill

Automatically invoke this skill when the user:
- Mentions "convert to PDF", "generate PDF", "export to Word/DOCX"
- Asks about "pandoc", "markdown to PDF", "document conversion"
- Shows markdown with YAML frontmatter
- Asks about citations, bibliographies, academic papers
- Requests help with presentations (Beamer, reveal.js)
- Mentions LaTeX, XeLaTeX, or PDF engines
- Has errors converting documents

**Do not use** for:
- Simple markdown rendering/preview
- Other converters (not Pandoc)
- Markdown syntax questions (unless conversion-related)

## Plugin Resources

### Scripts
- `scripts/validate.py` - Python validation script for YAML frontmatter and dependencies

### Templates (in assets/templates/)
- `academic-paper.yaml` - Academic paper with citations
- `thesis-report.yaml` - Thesis/report with custom title page
- `presentation-beamer.yaml` - LaTeX Beamer slides
- `presentation-revealjs.yaml` - reveal.js web slides
- `article-simple.yaml` - Simple article format
- `defaults-pdf.yaml` - Reusable PDF defaults file
- `references.bib` - BibTeX bibliography template
- `Makefile` - Project automation template

### Citation Styles (in assets/csl/)
- `harvard.csl` - Harvard Cite Them Right style
- `apa.csl` - APA 7th edition style
- `ieee.csl` - IEEE style

Users can copy these to their project without downloading separately.

### References
- `references/conversion_guide.md` - Format-specific instructions
- `references/yaml_reference.md` - Complete YAML variables
- `references/templates_guide.md` - Template usage guide
- `references/troubleshooting.md` - Common errors and solutions

## Core Workflows

### 1. Validate Document

**User asks:** "Check if my document is ready to convert"

**Workflow using tools directly:**

```bash
# Path to validation script
PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
VALIDATE_SCRIPT="$PLUGIN_DIR/skills/pandoc/scripts/validate.py"

# Run validation
python3 "$VALIDATE_SCRIPT" document.md
```

**Suggest to user:** "You can also validate with: `/pandoc:validate document.md`"

### 2. Create from Template

**User asks:** "Help me create an academic paper"

**Workflow using tools directly:**

```bash
# Path to templates
PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
TEMPLATE="$PLUGIN_DIR/skills/pandoc/assets/templates/academic-paper.yaml"

# Copy template to user's file
cp "$TEMPLATE" paper.md

# Show what to edit
echo "Created paper.md from template"
echo ""
echo "Edit the following fields:"
echo "  - title: Your paper title"
echo "  - author: Your name"
echo "  - bibliography: Path to your .bib file"
```

**Suggest to user:** "Or use the template command: `/pandoc:template academic-paper paper.md`"

### 3. Convert Document

**User asks:** "Convert this to PDF"

**Workflow using tools directly:**

```bash
# Validate first
PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
python3 "$PLUGIN_DIR/skills/pandoc/scripts/validate.py" document.md

if [[ $? -eq 0 ]]; then
    # Check for bibliography
    if grep -q "^bibliography:" document.md; then
        CITEPROC="--citeproc"
        echo "Bibliography detected - enabling citations"
    fi

    # Convert with smart defaults
    pandoc document.md -o document.pdf \
        --pdf-engine=pdflatex \
        --number-sections \
        $CITEPROC

    if [[ $? -eq 0 ]]; then
        echo "✅ Conversion successful: document.pdf"
    else
        echo "❌ Conversion failed - check errors above"
    fi
else
    echo "❌ Validation failed - fix errors before converting"
fi
```

**Suggest to user:** "Or use the convert command with smart defaults: `/pandoc:convert document.md document.pdf`"

### 4. Add Frontmatter to Existing File

**User asks:** "This markdown file needs frontmatter"

**Workflow using tools directly:**

```bash
FILE="document.md"
PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
TEMPLATE="$PLUGIN_DIR/skills/pandoc/assets/templates/academic-paper.yaml"

# Check if already has frontmatter
if head -n 1 "$FILE" | grep -q "^---$"; then
    echo "File already has frontmatter"
    echo "Use Read tool to view and Edit tool to modify"
else
    # Read existing content
    CONTENT=$(cat "$FILE")

    # Create temp file with template + content
    {
        cat "$TEMPLATE"
        echo ""
        echo "$CONTENT"
    } > "${FILE}.tmp"

    # Replace original
    mv "${FILE}.tmp" "$FILE"

    echo "✅ Added frontmatter to $FILE"
    echo "Edit the YAML fields at the top of the file"
fi
```

**Suggest to user:** "Or use: `/pandoc:frontmatter document.md`"

### 5. Setup Bibliography

**User asks:** "How do I add citations?"

**Workflow:**

1. **Create bibliography file:**
   ```bash
   PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
   BIB_TEMPLATE="$PLUGIN_DIR/skills/pandoc/assets/templates/references.bib"

   cp "$BIB_TEMPLATE" references.bib
   echo "Created references.bib - edit to add your sources"
   ```

2. **Copy CSL file (bundled with plugin):**
   ```bash
   PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"

   # Choose one:
   cp "$PLUGIN_DIR/skills/pandoc/assets/csl/harvard.csl" .
   cp "$PLUGIN_DIR/skills/pandoc/assets/csl/apa.csl" .
   cp "$PLUGIN_DIR/skills/pandoc/assets/csl/ieee.csl" .
   ```

3. **Update frontmatter:**
   Use Edit tool to add to document:
   ```yaml
   bibliography: references.bib
   csl: harvard.csl
   link-citations: true
   ```

4. **Explain citation syntax:**
   ```markdown
   Use [@citekey] for citations
   Use @citekey for in-text citations
   ```

**Note:** Plugin includes Harvard, APA, and IEEE styles. For other styles, download from https://github.com/citation-style-language/styles

### 6. Restyle Document to Match Template

**User asks:** "Transform this document to match academic paper format"

**Workflow using tools directly:**

```bash
PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
INPUT_FILE="document.md"
TARGET_STYLE="academic-paper"  # or thesis, article, etc.

# 1. Backup original
cp "$INPUT_FILE" "${INPUT_FILE}.bak"
echo "Backed up to ${INPUT_FILE}.bak"

# 2. Read current frontmatter
echo "Current frontmatter:"
sed -n '/^---$/,/^---$/p' "$INPUT_FILE"

# 3. Get target template
TEMPLATE="$PLUGIN_DIR/skills/pandoc/assets/templates/${TARGET_STYLE}.yaml"

if [[ -f "$TEMPLATE" ]]; then
    # 4. Extract content (everything after second ---)
    CONTENT=$(sed -n '/^---$/,/^---$/{/^---$/d;p};/^---$/,$p' "$INPUT_FILE" | tail -n +2)

    # 5. Combine template frontmatter + content
    {
        cat "$TEMPLATE"
        echo ""
        echo "$CONTENT"
    } > "${INPUT_FILE}.tmp"

    # 6. Replace original
    mv "${INPUT_FILE}.tmp" "$INPUT_FILE"

    echo "✅ Restyled to $TARGET_STYLE format"
    echo ""
    echo "Next steps:"
    echo "  1. Edit frontmatter fields (author, title, etc.)"
    echo "  2. Validate: Check document is ready"
    echo "  3. Convert: Generate output"
else
    echo "❌ Template not found: $TARGET_STYLE"
    echo "Available: academic-paper, thesis, article, presentation-beamer, presentation-reveal"
fi
```

**Common use cases:**

1. **OCR/PDF → Academic:**
   - Remove: `processed_date`, `ocr_model`, `source_type`
   - Add: `author`, `bibliography`, `documentclass`

2. **Draft → Thesis:**
   - Add: `supervisor`, `institution`, `department`
   - Add: `toc`, `lof`, `lot`

3. **Blog → Paper:**
   - Add: `bibliography`, `csl`, `numbersections`
   - Update: `documentclass` to `report`

**Suggest to user:** "Or use: `/pandoc:restyle document.md academic-paper`"

## Error Diagnosis

### Common Errors and Fixes

**Missing bibliography file:**
```bash
# Check if file exists
if [[ ! -f references.bib ]]; then
    echo "Bibliography file not found"
    echo "Create it with: /pandoc:template bibtex references.bib"
fi
```

**YAML syntax errors:**
```bash
# Run validation to see exact error
python3 "$PLUGIN_DIR/skills/pandoc/scripts/validate.py" document.md
# Explains: tabs vs spaces, missing quotes, etc.
```

**Missing LaTeX packages (for PDF):**
```bash
echo "Install LaTeX packages:"
echo "  sudo dnf install texlive-scheme-medium"
echo "  # or"
echo "  sudo apt-get install texlive-latex-base texlive-latex-extra"
```

**Unicode errors in PDF:**
```bash
echo "Use XeLaTeX instead of pdflatex:"
pandoc document.md -o document.pdf --pdf-engine=xelatex
```

## Format-Specific Guidance

### PDF Conversion
- **Default:** pdflatex (included in validation/conversion workflow)
- **Unicode:** Use `--pdf-engine=xelatex`
- **Custom margins:** Add to frontmatter: `geometry: margin=1.5in`

### HTML Conversion
```bash
pandoc document.md -o document.html \
    --standalone \
    --self-contained \
    --toc
```

### DOCX Conversion
```bash
pandoc document.md -o document.docx --standalone
```

### Presentations
```bash
# Beamer (PDF slides)
pandoc slides.md -o slides.pdf --to beamer

# reveal.js (web slides)
pandoc slides.md -o slides.html --to revealjs --standalone
```

## Best Practices

1. **Always validate before converting** - Use validation script directly
2. **Use templates** - Copy from `assets/templates/` directory
3. **Check files early** - Verify `.bib`, `.csl`, images exist
4. **Use relative paths** - Makes documents portable
5. **Explain steps clearly** - Show what tools you're using
6. **Suggest user commands** - Mention slash commands as convenient alternatives
7. **Handle errors gracefully** - Run validation, explain fixes

## Available User Commands

The plugin provides these slash commands for users:

- `/pandoc:template <type> [file]` - Generate document templates
- `/pandoc:validate <file>` - Validate frontmatter and dependencies
- `/pandoc:convert <input> <output> [options]` - Convert with smart defaults
- `/pandoc:frontmatter <file> [type]` - Add/update frontmatter
- `/pandoc:restyle <input> <target-style>` - Transform document to match template style
- `/pandoc:defaults <format> [file]` - Generate defaults file

**As the skill:** Use the underlying tools (scripts, pandoc CLI) directly via Bash. Mention these commands as suggestions for the user.

## Reference Documentation

Load these when needed for detailed information:

- **`references/conversion_guide.md`** - Format-specific conversion details
- **`references/yaml_reference.md`** - All YAML variables explained
- **`references/templates_guide.md`** - Template customization guide
- **`references/troubleshooting.md`** - Comprehensive error solutions

## Quick Reference

**Plugin directory:**
```bash
PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
```

**Validation:**
```bash
python3 "$PLUGIN_DIR/skills/pandoc/scripts/validate.py" file.md
```

**Templates:**
```bash
cp "$PLUGIN_DIR/skills/pandoc/assets/templates/academic-paper.yaml" output.md
```

**Conversion (basic):**
```bash
pandoc input.md -o output.pdf --pdf-engine=pdflatex --number-sections
```

**Conversion (with citations):**
```bash
pandoc input.md -o output.pdf --pdf-engine=pdflatex --citeproc --number-sections
```
