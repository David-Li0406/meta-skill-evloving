#!/bin/bash
# Universal PDF Build Script for Pandoc
# Usage: ./build-pdf.sh [input.md] [output.pdf]
# If no arguments provided, looks for single .md file in current directory

set -e

# ==============================================================================
# Configuration
# ==============================================================================
SKILL_DIR="$HOME/.claude/skills/pandoc-pdf-generation/assets"
LATEX_PREAMBLE="$SKILL_DIR/table-spacing-template.tex"

# Color output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${GREEN}✓${NC} $1"; }
log_warn() { echo -e "${YELLOW}⚠${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }

# ==============================================================================
# Input Detection
# ==============================================================================

# If input file provided as argument
if [[ -n "${1:-}" ]]; then
    INPUT_FILE="$1"
# Otherwise, auto-detect single .md file in current directory
else
    MD_FILES=(*.md)
    if [[ ${#MD_FILES[@]} -eq 0 || ! -f "${MD_FILES[0]}" ]]; then
        log_error "No Markdown files found in current directory"
        echo "Usage: $0 [input.md] [output.pdf]"
        exit 1
    elif [[ ${#MD_FILES[@]} -gt 1 ]]; then
        log_error "Multiple Markdown files found. Please specify which one:"
        printf '  - %s\n' "${MD_FILES[@]}"
        echo "Usage: $0 [input.md] [output.pdf]"
        exit 1
    fi
    INPUT_FILE="${MD_FILES[0]}"
fi

# Verify input file exists
if [[ ! -f "$INPUT_FILE" ]]; then
    log_error "Input file not found: $INPUT_FILE"
    exit 1
fi

# If output file provided as argument
if [[ -n "${2:-}" ]]; then
    OUTPUT_FILE="$2"
else
    # Auto-generate output filename from input
    OUTPUT_FILE="${INPUT_FILE%.md}.pdf"
fi

log_info "Input:  $INPUT_FILE"
log_info "Output: $OUTPUT_FILE"

# ==============================================================================
# Pre-flight Checks
# ==============================================================================

# Check if Pandoc is installed
if ! command -v pandoc &> /dev/null; then
    log_error "Pandoc is not installed. Install with: brew install pandoc"
    exit 1
fi

# Check if XeLaTeX is available
if ! command -v xelatex &> /dev/null; then
    log_error "XeLaTeX not found. Install MacTeX: brew install --cask mactex"
    exit 1
fi

# Check if LaTeX preamble exists
if [[ ! -f "$LATEX_PREAMBLE" ]]; then
    log_error "LaTeX preamble not found: $LATEX_PREAMBLE"
    exit 1
fi

# ==============================================================================
# Build PDF
# ==============================================================================
log_info "Generating PDF with table of contents..."

# Check for local or global bibliography
BIBLIOGRAPHY=""
if [[ -f "references.bib" ]]; then
    BIBLIOGRAPHY="--citeproc --bibliography=references.bib"
    log_info "Using bibliography: references.bib"
fi

# Check for CSL style
CSL=""
if [[ -f "chicago-note-bibliography.csl" ]]; then
    CSL="--csl=chicago-note-bibliography.csl"
    log_info "Using citation style: chicago-note-bibliography.csl"
fi

# Build command
pandoc "$INPUT_FILE" \
  -o "$OUTPUT_FILE" \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=3 \
  --number-sections \
  -V mainfont="DejaVu Sans" \
  -V geometry:landscape \
  -V geometry:margin=1in \
  -V toc-title="Table of Contents" \
  -H "$LATEX_PREAMBLE" \
  $BIBLIOGRAPHY \
  $CSL

# ==============================================================================
# Post-build Validation
# ==============================================================================

if [[ ! -f "$OUTPUT_FILE" ]]; then
    log_error "PDF generation failed - output file not created"
    exit 1
fi

FILE_SIZE=$(ls -lh "$OUTPUT_FILE" | awk '{print $5}')
log_info "PDF generated: $OUTPUT_FILE ($FILE_SIZE)"

# Get page count if pdfinfo available
if command -v pdfinfo &> /dev/null; then
    PAGE_COUNT=$(pdfinfo "$OUTPUT_FILE" 2>/dev/null | grep "^Pages:" | awk '{print $2}')
    if [[ -n "$PAGE_COUNT" ]]; then
        log_info "Page count: $PAGE_COUNT pages"
    fi
fi

echo ""
echo "✅ Build complete!"
echo "   View: open $OUTPUT_FILE"
