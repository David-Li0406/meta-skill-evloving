#!/bin/bash
# Display extraction results summary

FRAMES_DIR="/home/yousuf/GoogleDrive/PROJECTS/INVESTIGATION/DASHCAM/FRAMES_CLIPS/Movie_F&R_MotionSamples"
BASELINE=24238
TARGET=1426

CURRENT=$(find "$FRAMES_DIR" -name "*.jpg" -type f 2>/dev/null | wc -l)
NEW_FRAMES=$((CURRENT - BASELINE))
NEW_VIDEOS=$((NEW_FRAMES / 3))
SUCCESS_PCT=$(echo "scale=1; $NEW_VIDEOS * 100 / $TARGET" | bc)
BATCHES=$(ls /home/yousuf/PROJECTS/PeopleNet/FrameExtraction/completed/ 2>/dev/null | wc -l)
WORKERS=$(ps aux | grep extract_frames_gpu | grep -v grep | wc -l)

echo "═══════════════════════════════════════════════════════════════"
echo "  FRAME EXTRACTION RESULTS - Movie_F"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Frames:"
echo "  Baseline:        24,238 frames"
echo "  Current:         $CURRENT frames"
echo "  New extracted:   $NEW_FRAMES frames"
echo ""
echo "Videos:"
echo "  Processed:       $NEW_VIDEOS videos"
echo "  Target:          1,426 videos"
echo "  Success rate:    ${SUCCESS_PCT}%"
echo ""
echo "Processing:"
echo "  Batches done:    $BATCHES/29"
echo "  Active workers:  $WORKERS"
echo ""
echo "═══════════════════════════════════════════════════════════════"
