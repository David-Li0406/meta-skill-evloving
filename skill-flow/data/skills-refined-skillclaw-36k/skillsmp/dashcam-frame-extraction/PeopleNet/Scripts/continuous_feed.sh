#!/usr/bin/env bash
set -euo pipefail

# Continuous Feed Script - Keeps feeding videos to staging as workers process them

VIDEO_LIST="${1:-/home/yousuf/PROJECTS/PeopleNet/park_f_process_list_fullpaths.txt}"
STAGING_DIR="/home/yousuf/PROJECTS/PeopleNet/Staging/Park_F_Batch1"
PROCESSED_LIST="/home/yousuf/PROJECTS/PeopleNet/Outputs/Park_F_Batch1/processed_videos.txt"
BATCH_SIZE=10
MIN_FREE_GB=15
STAGING_MAX_COUNT=15

echo "Continuous Feed Starting..."
echo "Video List: $VIDEO_LIST"
echo "Staging: $STAGING_DIR"
echo "Batch Size: $BATCH_SIZE"
echo ""

total_videos=$(wc -l < "$VIDEO_LIST")
copied_total=0

while IFS= read -r video_path; do
    # Skip if source doesn't exist
    [ ! -f "$video_path" ] && continue

    video_name=$(basename "$video_path")

    # Skip if already processed
    if [ -f "$PROCESSED_LIST" ] && grep -q "^${video_name}$" "$PROCESSED_LIST"; then
        continue
    fi

    # Check disk space
    available_gb=$(df /home/yousuf/PROJECTS | tail -1 | awk '{print int($4/1024/1024)}')
    if [ "$available_gb" -lt "$MIN_FREE_GB" ]; then
        echo "WARNING: Low disk space (${available_gb}GB). Waiting..."
        sleep 30
        continue
    fi

    # Check staging count - don't overflow
    staging_count=$(find "$STAGING_DIR" -name "*.MP4" 2>/dev/null | wc -l)
    if [ "$staging_count" -ge "$STAGING_MAX_COUNT" ]; then
        echo "Staging full ($staging_count videos). Waiting for workers..."
        sleep 10
        continue
    fi

    # Copy video
    if cp "$video_path" "${STAGING_DIR}/" 2>/dev/null; then
        ((copied_total++))
        echo "[${copied_total}/${total_videos}] Copied: $video_name (staging: $staging_count)"

        # Brief pause every batch
        if [ $((copied_total % BATCH_SIZE)) -eq 0 ]; then
            echo "Batch complete. Pausing 5s..."
            sleep 5
        fi
    fi

done < "$VIDEO_LIST"

echo ""
echo "Feed complete! Total copied: $copied_total"
