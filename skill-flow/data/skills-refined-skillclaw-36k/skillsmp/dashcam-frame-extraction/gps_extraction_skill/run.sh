#!/bin/bash
################################################################################
# GPS Extraction Skill - Main Entry Point
#
# Usage: ./run.sh /path/to/crop/directory [options]
#
# This is the main entry point for the GPS extraction skill package.
################################################################################

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

################################################################################
# PARSE ARGUMENTS
################################################################################

CROP_DIR=""
PYTHON_BIN=""
OUTPUT_FILE=""
WORKERS=""
SHOW_HELP=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            SHOW_HELP=true
            shift
            ;;
        --python)
            PYTHON_BIN="$2"
            shift 2
            ;;
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --workers)
            WORKERS="$2"
            shift 2
            ;;
        *)
            if [ -z "$CROP_DIR" ]; then
                CROP_DIR="$1"
            else
                echo "Error: Unknown argument '$1'"
                exit 1
            fi
            shift
            ;;
    esac
done

if [ "$SHOW_HELP" = true ] || [ -z "$CROP_DIR" ]; then
    cat << 'EOF'
GPS Extraction Skill - One-Shot Optimized

Usage: ./run.sh <crop_directory> [options]

Arguments:
  crop_directory          Directory containing crop image files (.jpg)

Options:
  --python PATH          Path to Python 3.11 executable with PaddleOCR
  --output PATH          Output Excel file path
  --workers N            Number of GPU workers (default: 4)
  -h, --help            Show this help message

Examples:
  ./run.sh /path/to/crops
  ./run.sh /path/to/crops --workers 2
  ./run.sh /path/to/crops --output results.xlsx
  ./run.sh /path/to/crops --python /opt/conda/envs/paddle/bin/python3

Expected Results:
  - Success rate: 85-90%
  - Processing time: 40-60 minutes for ~28k images
  - Output: Excel file with GPS coordinates

For more information, see README.md or docs/AGENT_SPEC.md
EOF
    exit 0
fi

################################################################################
# LOAD CONFIGURATION
################################################################################

if [ -f "config/extraction.conf" ]; then
    source config/extraction.conf
fi

# Override with command-line arguments
[ -n "$PYTHON_BIN" ] || PYTHON_BIN="${PYTHON_BIN:-auto}"
[ -n "$OUTPUT_FILE" ] || OUTPUT_FILE="output/gps_extraction_$(date +%Y%m%d_%H%M%S).xlsx"
[ -n "$WORKERS" ] || WORKERS="${WORKERS:-4}"

################################################################################
# VALIDATE INPUTS
################################################################################

echo "======================================================================="
echo "GPS EXTRACTION SKILL - ONE-SHOT OPTIMIZED"
echo "======================================================================="
echo ""

if [ ! -d "$CROP_DIR" ]; then
    echo "❌ Error: Crop directory not found: $CROP_DIR"
    exit 1
fi

CROP_COUNT=$(find "$CROP_DIR" -type f -name "*.jpg" 2>/dev/null | wc -l)
if [ "$CROP_COUNT" -eq 0 ]; then
    echo "❌ Error: No .jpg files found in $CROP_DIR"
    exit 1
fi

echo "📂 Input: $CROP_DIR ($CROP_COUNT files)"
echo "📄 Output: $OUTPUT_FILE"
echo "⚙️  Workers: $WORKERS"
echo ""

################################################################################
# RUN EXTRACTION
################################################################################

mkdir -p output logs

echo "Starting GPS extraction..."
echo ""

# Run the optimized extraction script
bash scripts/extract_gps_optimized.sh \
    --source "$CROP_DIR" \
    --output "$OUTPUT_FILE" \
    --workers "$WORKERS" \
    --python "$PYTHON_BIN"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "======================================================================="
    echo "✅ GPS EXTRACTION COMPLETED SUCCESSFULLY"
    echo "======================================================================="
    echo ""
    echo "Output file: $OUTPUT_FILE"
    echo ""

    # Run analysis
    if [ -f "$OUTPUT_FILE" ]; then
        python3 scripts/analyze_results.py "$OUTPUT_FILE"
    fi

    exit 0
else
    echo ""
    echo "======================================================================="
    echo "❌ GPS EXTRACTION FAILED"
    echo "======================================================================="
    echo ""
    echo "Check logs/extraction.log for details"
    echo "See docs/TROUBLESHOOTING.md for common issues"
    echo ""
    exit 1
fi
