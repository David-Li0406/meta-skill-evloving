#!/usr/bin/env bash
set -euo pipefail

# Smart Feed - Replenishes staging at a rate slower than processing
# Measured processing rate: 13 videos/min
# Feed rate: 10 videos/min (safety margin)

VIDEO_LIST="/home/yousuf/PROJECTS/PeopleNet/park_f_net_new_oct13_onwards.txt"
STAGING_DIR="/home/yousuf/PROJECTS/PeopleNet/Staging/Park_F_Batch1"
PROCESSED_LIST="/home/yousuf/PROJECTS/PeopleNet/Outputs/Park_F_Batch1/processed_videos.txt"
OUTPUT_DIR="/home/yousuf/PROJECTS/PeopleNet/Outputs/Park_F_Batch1"

# Feed rate: 10 videos per minute = 1 video every 6 seconds
FEED_BATCH=10
BATCH_INTERVAL=60  # Copy 10 videos every 60 seconds = 10/min

# Safety limits
MIN_STAGING=15      # Trigger refill when below this
MAX_STAGING=30      # Never exceed this
MIN_FREE_GB=10      # Minimum free disk space

total_videos=$(wc -l < "$VIDEO_LIST")
line_num=0

echo "Smart Feed Starting..."
echo "Processing Rate: 13 videos/min (measured)"
echo "Feed Rate: 10 videos/min (safety margin)"
echo "Batch Size: $FEED_BATCH videos every ${BATCH_INTERVAL}s"
echo ""

while IFS= read -r video_path; do
    ((line_num++))

    # Skip if source doesn't exist
    [ ! -f "$video_path" ] && continue

    video_name=$(basename "$video_path")

    # Skip if already processed
    if [ -f "$PROCESSED_LIST" ] && grep -q "^${video_name}$" "$PROCESSED_LIST" 2>/dev/null; then
        continue
    fi

    # Skip if already in staging
    [ -f "${STAGING_DIR}/${video_name}" ] && continue

    # Check staging count
    staging_count=$(find "$STAGING_DIR" -name "*.MP4" 2>/dev/null | wc -l)

    # Wait if staging is full
    while [ "$staging_count" -ge "$MAX_STAGING" ]; do
        echo "Staging full ($staging_count/$MAX_STAGING). Waiting 10s..."
        sleep 10
        staging_count=$(find "$STAGING_DIR" -name "*.MP4" 2>/dev/null | wc -l)
    done

    # Check disk space
    available_gb=$(df /home/yousuf/PROJECTS | tail -1 | awk '{print int($4/1024/1024)}')
    if [ "$available_gb" -lt "$MIN_FREE_GB" ]; then
        echo "WARNING: Low disk space (${available_gb}GB). Pausing..."
        sleep 30
        continue
    fi

    # Copy video
    if cp "$video_path" "${STAGING_DIR}/" 2>/dev/null; then
        echo "[${line_num}/${total_videos}] Copied: $video_name (staging: $staging_count)"

        # Pause after each batch to maintain feed rate
        if [ $((line_num % FEED_BATCH)) -eq 0 ]; then
            processed_count=$(wc -l < "$PROCESSED_LIST" 2>/dev/null || echo 0)
            clips_count=$(find "$OUTPUT_DIR" -name "*.mp4" 2>/dev/null | wc -l)
            echo "Batch done. Processed: $processed_count, Clips: $clips_count. Pausing ${BATCH_INTERVAL}s..."
            sleep "$BATCH_INTERVAL"
        fi
    fi

done < "$VIDEO_LIST"

echo ""
echo "Smart feed complete!"
