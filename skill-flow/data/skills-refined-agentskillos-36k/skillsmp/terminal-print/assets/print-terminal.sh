#!/bin/bash
# Terminal Print - Print iTerm2 output to HP printer
# Based on cc-skills pandoc-pdf-generation pattern
#
# Usage: ./print-terminal.sh [OPTIONS]
#
# Options:
#   --file FILE    Read from file instead of clipboard
#   --no-preview   Skip preview, print directly
#   --no-print     Generate PDF only, don't print
#   -h, --help     Show help
#
# ADR: /docs/adr/2025-12-28-terminal-print-skill.md (if created)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMPDIR="${TMPDIR:-/tmp}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PRINTER="HP_LaserJet_Pro_MFP_3101_3108__A02E22__20250803224332"

# Defaults
INPUT_FILE=""
NO_PREVIEW=""
NO_PRINT=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --file)
            INPUT_FILE="$2"
            shift 2
            ;;
        --no-preview)
            NO_PREVIEW="yes"
            shift
            ;;
        --no-print)
            NO_PRINT="yes"
            shift
            ;;
        -h|--help)
            echo "Terminal Print - Print iTerm2 output to HP printer"
            echo ""
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --file FILE    Read from file instead of clipboard"
            echo "  --no-preview   Skip preview, print directly"
            echo "  --no-print     Generate PDF only, don't print"
            echo "  -h, --help     Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            echo "Use -h for help" >&2
            exit 1
            ;;
    esac
done

# Pre-flight checks
preflight_check() {
    local missing=()

    command -v pandoc &>/dev/null || missing+=("pandoc (brew install pandoc)")
    command -v xelatex &>/dev/null || missing+=("xelatex (brew install --cask mactex)")

    if ! lpstat -p &>/dev/null; then
        missing+=("printer (none configured)")
    fi

    if [[ ${#missing[@]} -gt 0 ]]; then
        echo "❌ Missing prerequisites:"
        for item in "${missing[@]}"; do
            echo "   - $item"
        done
        exit 1
    fi
}

preflight_check

# 1. Get input
if [[ -n "$INPUT_FILE" ]]; then
    if [[ ! -f "$INPUT_FILE" ]]; then
        echo "❌ File not found: $INPUT_FILE"
        exit 1
    fi
    content=$(cat "$INPUT_FILE")
    echo "📋 Reading from file: $INPUT_FILE"
else
    content=$(pbpaste)
    echo "📋 Reading from clipboard"
fi

# 2. Check for empty input
if [[ -z "$content" ]]; then
    echo "❌ No text in clipboard."
    echo "   Copy terminal output first (Cmd+C in iTerm2)."
    exit 1
fi

# 3. Strip ANSI escape codes
# Handles: colors, cursor movement, and other escape sequences
clean_content=$(echo "$content" | sed 's/\x1b\[[0-9;]*[a-zA-Z]//g')

echo "📝 Stripped ANSI codes, preparing markdown..."

# 4. Create markdown with code block
MD_FILE="$TMPDIR/terminal-$TIMESTAMP.md"
cat > "$MD_FILE" << 'MARKDOWN_HEADER'
# Terminal Output

```text
MARKDOWN_HEADER

echo "$clean_content" >> "$MD_FILE"
echo '```' >> "$MD_FILE"

# 5. Generate PDF with pandoc (landscape, monospace)
OUTPUT_PDF="$TMPDIR/terminal-output-$TIMESTAMP.pdf"

echo "🔧 Generating PDF with pandoc + xelatex..."

pandoc "$MD_FILE" \
  -o "$OUTPUT_PDF" \
  --pdf-engine=xelatex \
  -V geometry:letterpaper,landscape \
  -V geometry:margin=0.5in \
  -V mainfont="DejaVu Sans Mono" \
  -V monofont="DejaVu Sans Mono" \
  -V fontsize=9pt

echo "📄 PDF generated: $OUTPUT_PDF"

# 6. Preview (unless --no-preview)
if [[ -z "$NO_PREVIEW" ]]; then
    open "$OUTPUT_PDF"
    echo ""
    echo "👀 Preview opened. Press Enter to print, or Ctrl+C to cancel."
    read -r
fi

# 7. Print (unless --no-print)
if [[ -z "$NO_PRINT" ]]; then
    lpr -P "$PRINTER" -o sides=one-sided "$OUTPUT_PDF"
    echo "✅ Sent to printer: $PRINTER"
else
    echo "ℹ️  --no-print specified, skipping print"
fi

echo "📁 PDF saved: $OUTPUT_PDF"
