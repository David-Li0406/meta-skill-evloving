#!/bin/bash
# Skill Verification Script
# Verifies that all components of the Dashcam skill are present and functional

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ERRORS=0

echo "═══════════════════════════════════════════════════════════════"
echo "  DASHCAM SKILL VERIFICATION"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Check documentation files
echo "[1/5] Checking documentation files..."
DOCS=("AGENT_INSTRUCTIONS.md" "SKILL_README.md" "README.md" "DOCUMENTATION.md" "QUICK_REFERENCE.md" "CRITICAL_FIXES_CHECKLIST.md" "INDEX.md")
for doc in "${DOCS[@]}"; do
    if [ -f "$SKILL_DIR/$doc" ]; then
        echo "  ✓ $doc"
    else
        echo "  ✗ $doc (MISSING)"
        ((ERRORS++))
    fi
done
echo ""

# Check executable scripts
echo "[2/5] Checking executable scripts..."
SCRIPTS=("run_extraction.sh" "extract_frames_worker.py" "coordinator.sh" "monitor.sh" "show_results.sh")
for script in "${SCRIPTS[@]}"; do
    if [ -f "$SKILL_DIR/$script" ]; then
        if [ -x "$SKILL_DIR/$script" ]; then
            echo "  ✓ $script (executable)"
        else
            echo "  ⚠ $script (not executable)"
            ((ERRORS++))
        fi
    else
        echo "  ✗ $script (MISSING)"
        ((ERRORS++))
    fi
done
echo ""

# Check configuration files
echo "[3/5] Checking configuration files..."
CONFIGS=("config.json" "requirements.txt")
for config in "${CONFIGS[@]}"; do
    if [ -f "$SKILL_DIR/$config" ]; then
        echo "  ✓ $config"
    else
        echo "  ✗ $config (MISSING)"
        ((ERRORS++))
    fi
done
echo ""

# Check system requirements
echo "[4/5] Checking system requirements..."

# GPU
if nvidia-smi &>/dev/null; then
    GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader)
    echo "  ✓ GPU: $GPU_NAME"
else
    echo "  ✗ NVIDIA GPU not detected"
    ((ERRORS++))
fi

# FFmpeg
if command -v ffmpeg &>/dev/null; then
    echo "  ✓ ffmpeg installed"
    if ffmpeg -hwaccels 2>/dev/null | grep -q cuda; then
        echo "  ✓ CUDA acceleration available"
    else
        echo "  ✗ CUDA acceleration not available in ffmpeg"
        ((ERRORS++))
    fi
else
    echo "  ✗ ffmpeg not found"
    ((ERRORS++))
fi

# Python
if /home/yousuf/PROJECTS/ExtractedGPS/.venv/bin/python3 --version &>/dev/null; then
    PY_VER=$(/home/yousuf/PROJECTS/ExtractedGPS/.venv/bin/python3 --version 2>&1)
    echo "  ✓ Python: $PY_VER"
else
    echo "  ✗ Python not found at expected location"
    ((ERRORS++))
fi

# Disk space
WORK_DIR="/home/yousuf/PROJECTS/PeopleNet/FrameExtraction"
if [ -d "$WORK_DIR" ]; then
    FREE_GB=$(df -BG "$WORK_DIR" | awk 'NR==2 {print $4}' | sed 's/G//')
    if [ "$FREE_GB" -ge 25 ]; then
        echo "  ✓ Disk space: ${FREE_GB}GB available"
    else
        echo "  ⚠ Disk space: ${FREE_GB}GB (minimum 25GB recommended)"
    fi
else
    echo "  ⚠ Work directory not yet created: $WORK_DIR"
fi
echo ""

# Check paths
echo "[5/5] Checking configured paths..."

DESKTOP_SOURCE="/mnt/windows/Users/yousu/Desktop/CARDV/Movie_F"
FRAMES_OUTPUT="/home/yousuf/GoogleDrive/PROJECTS/INVESTIGATION/DASHCAM/FRAMES_CLIPS/Movie_F&R_MotionSamples"

if [ -d "$DESKTOP_SOURCE" ]; then
    VIDEO_COUNT=$(find "$DESKTOP_SOURCE" -name "*.MP4" -type f 2>/dev/null | wc -l)
    echo "  ✓ Source directory: $VIDEO_COUNT videos"
else
    echo "  ⚠ Source directory not found: $DESKTOP_SOURCE"
fi

if [ -d "$FRAMES_OUTPUT" ]; then
    FRAME_COUNT=$(find "$FRAMES_OUTPUT" -name "*.jpg" -type f 2>/dev/null | wc -l)
    echo "  ✓ Output directory: $FRAME_COUNT frames"
else
    echo "  ⚠ Output directory not found: $FRAMES_OUTPUT"
fi
echo ""

# Summary
echo "═══════════════════════════════════════════════════════════════"
if [ $ERRORS -eq 0 ]; then
    echo "  ✅ VERIFICATION PASSED - Skill is ready to use"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "To run the skill:"
    echo "  cd $SKILL_DIR"
    echo "  ./run_extraction.sh"
    echo ""
    exit 0
else
    echo "  ⚠️  VERIFICATION FAILED - $ERRORS error(s) found"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "Please fix the errors above before using the skill."
    echo ""
    exit 1
fi
