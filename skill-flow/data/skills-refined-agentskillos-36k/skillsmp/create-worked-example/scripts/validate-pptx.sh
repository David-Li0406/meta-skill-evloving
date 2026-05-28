#!/bin/bash
#
# Validate PPTX Output
#
# Converts PPTX to PDF and then to images for visual validation.
# This is a required step per pptx.md section 16.
#
# Prerequisites:
#   - LibreOffice (for PDF conversion)
#   - Poppler (for image conversion): brew install poppler
#
# Usage:
#   ./validate-pptx.sh <pptx-file> [output-dir]
#
# Example:
#   ./validate-pptx.sh output.pptx ./validation-images
#

set -e

# Check arguments
if [ $# -lt 1 ]; then
    echo "Usage: $0 <pptx-file> [output-dir]"
    echo ""
    echo "Arguments:"
    echo "  pptx-file   Path to the PPTX file to validate"
    echo "  output-dir  Optional output directory for images (default: same as pptx)"
    exit 1
fi

PPTX_FILE="$1"
OUTPUT_DIR="${2:-$(dirname "$PPTX_FILE")}"

# Check if file exists
if [ ! -f "$PPTX_FILE" ]; then
    echo "Error: File not found: $PPTX_FILE"
    exit 1
fi

# Get base name without extension
BASENAME=$(basename "$PPTX_FILE" .pptx)
PDF_FILE="$OUTPUT_DIR/$BASENAME.pdf"

echo "=== PPTX Validation ==="
echo ""
echo "Input:  $PPTX_FILE"
echo "Output: $OUTPUT_DIR"
echo ""

# Step 1: Convert PPTX to PDF using LibreOffice
echo "Step 1: Converting PPTX to PDF..."
if command -v soffice &> /dev/null; then
    soffice --headless --convert-to pdf --outdir "$OUTPUT_DIR" "$PPTX_FILE"
    echo "  Created: $PDF_FILE"
else
    echo "Error: LibreOffice (soffice) not found."
    echo "Install with: brew install --cask libreoffice"
    exit 1
fi
echo ""

# Step 2: Convert PDF to images using pdftoppm
echo "Step 2: Converting PDF to images..."
if command -v pdftoppm &> /dev/null; then
    pdftoppm -jpeg -r 150 "$PDF_FILE" "$OUTPUT_DIR/slide"
    echo "  Created slide images in $OUTPUT_DIR/"
else
    echo "Error: pdftoppm not found."
    echo "Install with: brew install poppler"
    exit 1
fi
echo ""

# Step 3: List generated images
echo "Step 3: Generated images:"
ls -la "$OUTPUT_DIR"/slide-*.jpg 2>/dev/null || echo "  No images found"
echo ""

# Step 4: Print validation checklist
echo "=== Visual Validation Checklist ==="
echo ""
echo "Open the generated images and check for:"
echo ""
echo "  [ ] Text cutoff - Text being cut off by shapes or slide edges"
echo "  [ ] Text overlap - Text overlapping with other text or shapes"
echo "  [ ] Positioning issues - Content too close to boundaries"
echo "  [ ] Contrast issues - Insufficient contrast between text and backgrounds"
echo "  [ ] Alignment problems - Elements not properly aligned"
echo "  [ ] Visual hierarchy - Important content properly emphasized"
echo ""
echo "If issues found, fix in order:"
echo "  1. Increase margins/padding"
echo "  2. Adjust font sizes"
echo "  3. Rethink layout"
echo ""

echo "Done!"
