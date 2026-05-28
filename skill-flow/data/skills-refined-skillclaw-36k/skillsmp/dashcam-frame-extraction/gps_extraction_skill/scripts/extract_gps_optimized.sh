#!/bin/bash
################################################################################
# GPS Extraction - Optimized Script
#
# This script implements the battle-tested optimal parameters for GPS extraction
# from dashcam frame crops using GPU-accelerated PaddleOCR.
################################################################################

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"
cd "$SCRIPT_DIR"

################################################################################
# PARSE ARGUMENTS
################################################################################

SOURCE_DIR=""
OUTPUT_FILE=""
WORKERS=4
PYTHON_BIN="auto"

while [[ $# -gt 0 ]]; do
    case $1 in
        --source)
            SOURCE_DIR="$2"
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
        --python)
            PYTHON_BIN="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

################################################################################
# AUTO-DETECT PYTHON IF NOT SPECIFIED
################################################################################

if [ "$PYTHON_BIN" = "auto" ]; then
    # Try to find PaddleOCR-enabled Python
    CANDIDATES=(
        "/home/yousuf/PROJECTS/ExtractedGPS/.mambaforge/envs/paddle311/bin/python3"
        "$HOME/.mambaforge/envs/paddle311/bin/python3"
        "$HOME/miniconda3/envs/paddle/bin/python3"
        "$(which python3)"
    )

    for candidate in "${CANDIDATES[@]}"; do
        if [ -f "$candidate" ]; then
            if "$candidate" -c "import paddleocr" 2>/dev/null; then
                PYTHON_BIN="$candidate"
                echo "✅ Auto-detected Python with PaddleOCR: $PYTHON_BIN"
                break
            fi
        fi
    done

    if [ "$PYTHON_BIN" = "auto" ]; then
        echo "❌ Error: Could not find Python with PaddleOCR installed"
        echo "   Please specify with --python /path/to/python3"
        exit 1
    fi
fi

################################################################################
# CONFIGURATION - CRITICAL SUCCESS PARAMETERS
################################################################################

# CRITICAL: These parameters are battle-tested and non-negotiable
CROP_WIDTH_PCT=0.70   # Minimum 70% - DO NOT REDUCE
CROP_HEIGHT_PCT=0.22  # Minimum 22% - tested optimal
UTIL_THRESHOLD=90.0
MEM_THRESHOLD=85.0
OCR_BACKEND="paddle"

# Set CUDA library paths
ENV_DIR="$(dirname "$(dirname "$PYTHON_BIN")")"
export CUDNN_LIB="${ENV_DIR}/lib/python3.11/site-packages/nvidia/cudnn/lib"
export CUBLAS_LIB="${ENV_DIR}/lib/python3.11/site-packages/nvidia/cublas/lib"
export LD_LIBRARY_PATH="${CUDNN_LIB}:${CUBLAS_LIB}:$LD_LIBRARY_PATH"

################################################################################
# PRE-FLIGHT CHECKS
################################################################################

echo "======================================================================="
echo "GPS EXTRACTION - OPTIMIZED (Pre-flight Checks)"
echo "======================================================================="
echo ""

echo "[1/6] Checking disk space..."
DISK_USAGE=$(df "$SCRIPT_DIR" | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 85 ]; then
    echo "  ⚠️  WARNING: Disk usage at ${DISK_USAGE}%"
else
    echo "  ✅ Disk usage OK (${DISK_USAGE}%)"
fi

echo "[2/6] Checking GPU availability..."
if nvidia-smi > /dev/null 2>&1; then
    GPU_MEM=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)
    echo "  ✅ GPU available with ${GPU_MEM} MB free memory"
else
    echo "  ⚠️  WARNING: GPU not detected - will run slower on CPU"
fi

echo "[3/6] Verifying Python environment..."
PADDLE_OK=$($PYTHON_BIN -c "import paddleocr; print('OK')" 2>/dev/null || echo "FAIL")
if [ "$PADDLE_OK" = "OK" ]; then
    echo "  ✅ PaddleOCR available"
else
    echo "  ❌ ERROR: PaddleOCR not found in Python environment"
    exit 1
fi

echo "[4/6] Checking source directory..."
if [ ! -d "$SOURCE_DIR" ]; then
    echo "  ❌ ERROR: Source directory not found: $SOURCE_DIR"
    exit 1
fi
CROP_COUNT=$(find "$SOURCE_DIR" -type f -name "*.jpg" 2>/dev/null | wc -l)
echo "  ✅ Found ${CROP_COUNT} crop files"

echo "[5/6] Checking for run_multi.py..."
# Try to find run_multi.py
RUN_MULTI=""
SEARCH_PATHS=(
    "/home/yousuf/PROJECTS/ExtractedGPS/src/run_multi.py"
    "$SCRIPT_DIR/../ExtractedGPS/src/run_multi.py"
    "$SCRIPT_DIR/src/run_multi.py"
)

for path in "${SEARCH_PATHS[@]}"; do
    if [ -f "$path" ]; then
        RUN_MULTI="$path"
        break
    fi
done

if [ -z "$RUN_MULTI" ]; then
    echo "  ⚠️  WARNING: run_multi.py not found, will use single-threaded mode"
    USE_MULTI=false
else
    echo "  ✅ Multi-worker script found: $RUN_MULTI"
    USE_MULTI=true
fi

echo "[6/6] Creating output directories..."
OUTPUT_DIR="$(dirname "$OUTPUT_FILE")"
mkdir -p "$OUTPUT_DIR" logs
echo "  ✅ Output directories ready"

echo ""
echo "======================================================================="
echo "PRE-FLIGHT CHECKS COMPLETE ✅"
echo "======================================================================="
echo ""
echo "Configuration:"
echo "  Source: $SOURCE_DIR ($CROP_COUNT files)"
echo "  Output: $OUTPUT_FILE"
echo "  Crop: ${CROP_WIDTH_PCT} width, ${CROP_HEIGHT_PCT} height"
echo "  Workers: $WORKERS (GPU-accelerated)"
echo "  Python: $PYTHON_BIN"
echo ""
echo "Expected: 85-90% success in 30-45 minutes"
echo ""

################################################################################
# RUN EXTRACTION
################################################################################

echo "Starting extraction..."
START_TIME=$(date +%s)

if [ "$USE_MULTI" = true ]; then
    # Use multi-worker extraction
    $PYTHON_BIN "$RUN_MULTI" \
        --python-bin "$PYTHON_BIN" \
        --workers $WORKERS \
        --util-threshold $UTIL_THRESHOLD \
        --mem-threshold $MEM_THRESHOLD \
        --source "$SOURCE_DIR" \
        --output-final "$OUTPUT_FILE" \
        --missing-final "${OUTPUT_FILE%.xlsx}_missing.csv" \
        --crop-width-pct $CROP_WIDTH_PCT \
        --crop-height-pct $CROP_HEIGHT_PCT \
        --ocr-backend $OCR_BACKEND \
        --aggregate-log "logs/extraction.log"
else
    # Fallback: Single-threaded extraction
    echo "⚠️  Running in single-threaded mode (slower)"
    $PYTHON_BIN scripts/extract_single.py \
        --source "$SOURCE_DIR" \
        --output "$OUTPUT_FILE" \
        --crop-width $CROP_WIDTH_PCT \
        --crop-height $CROP_HEIGHT_PCT
fi

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
MINUTES=$((ELAPSED / 60))
SECONDS=$((ELAPSED % 60))

echo ""
echo "======================================================================="
echo "EXTRACTION COMPLETE"
echo "======================================================================="
echo "Elapsed time: ${MINUTES}m ${SECONDS}s"
echo "Output: $OUTPUT_FILE"
echo ""
