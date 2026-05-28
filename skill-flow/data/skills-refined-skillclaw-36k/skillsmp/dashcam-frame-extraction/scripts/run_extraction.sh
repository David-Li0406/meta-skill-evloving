#!/bin/bash
#############################################################################
# AUTO FRAME EXTRACTION - Movie_F Videos ONLY
#############################################################################
# Purpose: Automated frame extraction when new videos are placed in Desktop CARDV
# Usage: ./run_extraction.sh
#
# This script is specifically for Movie_F category only
#############################################################################

set -euo pipefail

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Configuration - Movie_F ONLY
CATEGORY="Movie_F"
DESKTOP_SOURCE="/mnt/sdcard/CARDV/Movie_F"
FRAMES_OUTPUT="/home/yousuf/GoogleDrive/PROJECTS/INVESTIGATION/DASHCAM/FRAMES_CLIPS/Movie_F&R_MotionSamples"
WORK_DIR="/home/yousuf/PROJECTS/PeopleNet/FrameExtraction"
STAGING_DIR="/home/yousuf/PROJECTS/PeopleNet/Staging/${CATEGORY}_Batch"
NUM_WORKERS=4
BATCH_SIZE=50
MIN_FREE_GB=25

echo "═══════════════════════════════════════════════════════════════"
echo "  AUTO FRAME EXTRACTION - ${CATEGORY}"
echo "═══════════════════════════════════════════════════════════════"
echo ""

#############################################################################
# Pre-flight Checks
#############################################################################
echo "[1/7] Running pre-flight checks..."

# Check GPU availability
if ! nvidia-smi &>/dev/null; then
    echo "❌ ERROR: NVIDIA GPU not detected or drivers not installed"
    exit 1
fi
echo "  ✓ GPU detected: $(nvidia-smi --query-gpu=name --format=csv,noheader)"

# Check CUDA availability
if ! command -v ffmpeg &>/dev/null; then
    echo "❌ ERROR: ffmpeg not found"
    exit 1
fi
echo "  ✓ ffmpeg available"

# Check Python
if ! python3 --version &>/dev/null; then
    echo "❌ ERROR: Python3 not found"
    exit 1
fi
echo "  ✓ Python available"

# Check required scripts
if [ ! -f "$SCRIPT_DIR/extract_frames_worker.py" ]; then
    echo "❌ ERROR: extract_frames_worker.py not found"
    exit 1
fi
if [ ! -f "$SCRIPT_DIR/coordinator.sh" ]; then
    echo "❌ ERROR: coordinator.sh not found"
    exit 1
fi
echo "  ✓ Required scripts present"

# Check disk space
FREE_GB=$(df -BG "$WORK_DIR" | awk 'NR==2 {print $4}' | sed 's/G//')
if [ "$FREE_GB" -lt "$MIN_FREE_GB" ]; then
    echo "❌ ERROR: Insufficient disk space. Need ${MIN_FREE_GB}GB, have ${FREE_GB}GB"
    exit 1
fi
echo "  ✓ Disk space: ${FREE_GB}GB available"

# Check source directory
if [ ! -d "$DESKTOP_SOURCE" ]; then
    echo "❌ ERROR: Source directory not found: $DESKTOP_SOURCE"
    exit 1
fi
VIDEO_COUNT=$(find "$DESKTOP_SOURCE" -name "*.MP4" -type f | wc -l)
echo "  ✓ Source directory: $VIDEO_COUNT videos found"

# Check output directory
mkdir -p "$FRAMES_OUTPUT"
echo "  ✓ Output directory ready"

echo ""

#############################################################################
# Identify New Videos (Gap Analysis)
#############################################################################
echo "[2/7] Identifying videos needing frame extraction..."

# Get list of all videos in source
find "$DESKTOP_SOURCE" -name "*.MP4" -type f -exec basename {} .MP4 \; | sort > /tmp/all_source_videos.txt

# Get list of videos already processed (from existing frames)
find "$FRAMES_OUTPUT" -name "*.jpg" -type f | \
    sed -E 's/_BEGIN_.*|_MIDDLE_.*|_END_.*//' | \
    xargs -n1 basename | \
    sort -u > /tmp/processed_videos.txt

# Find net-new videos (handle 'A' suffix variations)
comm -23 /tmp/all_source_videos.txt /tmp/processed_videos.txt > /tmp/net_new_base.txt

# Add variations with A suffix
cat /tmp/net_new_base.txt | while read video; do
    # Check if video exists as-is or with A suffix
    if [ -f "$DESKTOP_SOURCE/${video}.MP4" ]; then
        echo "${video}.MP4"
    elif [ -f "$DESKTOP_SOURCE/${video}A.MP4" ]; then
        echo "${video}A.MP4"
    elif [ -f "$DESKTOP_SOURCE/${video}_A.MP4" ]; then
        echo "${video}_A.MP4"
    fi
done > /tmp/net_new_videos.txt

NET_NEW_COUNT=$(wc -l < /tmp/net_new_videos.txt)

if [ "$NET_NEW_COUNT" -eq 0 ]; then
    echo "  ℹ️  No new videos to process. All videos already have frames extracted."
    exit 0
fi

echo "  ✓ Found $NET_NEW_COUNT new videos requiring frame extraction"
cp /tmp/net_new_videos.txt "$WORK_DIR/${CATEGORY}_NET_NEW_${NET_NEW_COUNT}_videos.txt"
echo ""

#############################################################################
# Create Batch Files
#############################################################################
echo "[3/7] Creating batch files ($BATCH_SIZE videos per batch)..."

mkdir -p "$WORK_DIR/batches" "$WORK_DIR/logs" "$WORK_DIR/completed"
rm -rf "$WORK_DIR/batches"/*
rm -rf "$WORK_DIR/completed"/*

split -l "$BATCH_SIZE" -d -a 3 \
    "$WORK_DIR/${CATEGORY}_NET_NEW_${NET_NEW_COUNT}_videos.txt" \
    "$WORK_DIR/batches/batch_"

BATCH_COUNT=$(ls "$WORK_DIR/batches"/ | wc -l)
echo "  ✓ Created $BATCH_COUNT batch files"
echo ""

#############################################################################
# Launch Parallel Processing
#############################################################################
echo "[4/7] Launching parallel extraction ($NUM_WORKERS workers)..."

# Launch coordinator in background
"$SCRIPT_DIR/coordinator.sh" > "$WORK_DIR/logs/coordinator.log" 2>&1 &
COORDINATOR_PID=$!

echo "  ✓ Coordinator launched (PID: $COORDINATOR_PID)"
echo "  ✓ Processing $NET_NEW_COUNT videos across $BATCH_COUNT batches"
echo ""

#############################################################################
# Setup Monitoring
#############################################################################
echo "[5/7] Setting up progress monitoring..."

# Get baseline frame count
BASELINE=$(find "$FRAMES_OUTPUT" -name "*.jpg" -type f 2>/dev/null | wc -l)

# Launch monitor in background
"$SCRIPT_DIR/monitor.sh" "$BASELINE" "$NET_NEW_COUNT" "$BATCH_COUNT" &
MONITOR_PID=$!

echo "  ✓ Progress monitor started (PID: $MONITOR_PID)"
echo ""

#############################################################################
# Summary
#############################################################################
echo "[6/7] Extraction in progress!"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  SUMMARY"
echo "═══════════════════════════════════════════════════════════════"
echo "Source:        $DESKTOP_SOURCE"
echo "Output:        $FRAMES_OUTPUT"
echo "Videos:        $NET_NEW_COUNT to process"
echo "Batches:       $BATCH_COUNT batches"
echo "Workers:       $NUM_WORKERS parallel workers"
echo "GPU:           $(nvidia-smi --query-gpu=name --format=csv,noheader)"
echo ""
echo "Monitor PID:   $MONITOR_PID (updates every 30s)"
echo "Coordinator:   $COORDINATOR_PID"
echo "Logs:          $WORK_DIR/logs/"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Progress updates will appear every 30 seconds above."
echo "To monitor manually: tail -f $WORK_DIR/logs/coordinator.log"
echo ""
