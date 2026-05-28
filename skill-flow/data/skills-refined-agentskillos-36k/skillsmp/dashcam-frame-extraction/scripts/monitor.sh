#!/bin/bash
# Progress monitor for frame extraction
# Prints periodic updates without clearing screen

if [ $# -ne 3 ]; then
    echo "Usage: $0 <baseline_frames> <target_videos> <batch_count>"
    exit 1
fi

BASELINE=$1
TARGET=$2
BATCH_COUNT=$3
START_TIME=$(date +%s)

FRAMES_OUTPUT="/home/yousuf/GoogleDrive/PROJECTS/INVESTIGATION/DASHCAM/FRAMES_CLIPS/Movie_F&R_MotionSamples"
WORK_DIR="/home/yousuf/PROJECTS/PeopleNet/FrameExtraction"

while true; do
    sleep 30

    CURRENT=$(find "$FRAMES_OUTPUT" -name "*.jpg" -type f 2>/dev/null | wc -l)
    NEW_FRAMES=$((CURRENT - BASELINE))
    NEW_VIDEOS=$((NEW_FRAMES / 3))
    ELAPSED=$(($(date +%s) - START_TIME))

    COMPLETED=$(ls "$WORK_DIR/completed/" 2>/dev/null | wc -l)
    WORKERS=$(ps aux | grep extract_frames_worker | grep -v grep | wc -l)
    GPU=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits 2>/dev/null)

    if [ $ELAPSED -gt 0 ] && [ $NEW_VIDEOS -gt 0 ]; then
        VIDS_PER_MIN=$(echo "scale=1; ($NEW_VIDEOS * 60) / $ELAPSED" | bc 2>/dev/null || echo "0")
        FRAMES_PER_SEC=$(echo "scale=2; $NEW_FRAMES / $ELAPSED" | bc 2>/dev/null || echo "0")
        REMAINING=$((TARGET - NEW_VIDEOS))

        if [ $(echo "$VIDS_PER_MIN > 0.1" | bc 2>/dev/null || echo "0") -eq 1 ]; then
            ETA_MIN=$(echo "scale=0; ($REMAINING * 60) / $VIDS_PER_MIN" | bc 2>/dev/null || echo "0")
            ETA_HR=$(echo "scale=1; $ETA_MIN / 60" | bc 2>/dev/null || echo "0")
        else
            ETA_HR="calculating"
        fi
    else
        VIDS_PER_MIN="0.0"
        FRAMES_PER_SEC="0.00"
        ETA_HR="calculating"
    fi

    PCT=$((NEW_VIDEOS * 100 / TARGET))

    echo ""
    echo "════════════════════════════════════════════════════════════════"
    echo "📊 EXTRACTION PROGRESS - $(date '+%I:%M:%S %p')"
    echo "Videos: $NEW_VIDEOS/$TARGET (${PCT}%) | Batches: $COMPLETED/$BATCH_COUNT | Workers: $WORKERS"
    echo "Speed: $VIDS_PER_MIN vids/min | $FRAMES_PER_SEC fps | ETA: ${ETA_HR}h | GPU: ${GPU}%"
    echo "════════════════════════════════════════════════════════════════"
    echo ""

    # Exit when all workers done
    if [ "$WORKERS" -eq 0 ] && [ "$COMPLETED" -eq "$BATCH_COUNT" ]; then
        echo "✅ Extraction complete!"
        break
    fi
done
