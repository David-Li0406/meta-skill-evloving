#!/usr/bin/env bash
set -euo pipefail

# Smart Feed for Park_F Oct 24-27 (154 videos)
# Processing rate: ~13 videos/min
# Feed rate: 10 videos/min (safety margin)

VIDEO_LIST="/home/yousuf/PROJECTS/PeopleNet/park_f_oct24_27.txt"
STAGING_DIR="/home/yousuf/PROJECTS/PeopleNet/Staging/Park_F_Oct24_27"
PROCESSED_LIST="/home/yousuf/PROJECTS/PeopleNet/Outputs/Park_F_Oct24_27/processed_videos.txt"
OUTPUT_DIR="/home/yousuf/PROJECTS/PeopleNet/Outputs/Park_F_Oct24_27"

# Feed rate: 10 videos per minute = batch of 10 every 60 seconds
FEED_BATCH=10
BATCH_INTERVAL=60  # seconds

# Safety limits
MIN_STAGING=15      # Trigger refill when below this
MAX_STAGING=30      # Never exceed this
MIN_FREE_GB=10      # Minimum free disk space

# Create processed list if doesn't exist
touch "$PROCESSED_LIST"

total_videos=$(wc -l < "$VIDEO_LIST")
line_num=0

echo "========================================"
echo "Smart Feed - Park_F Oct 24-27"
echo "========================================"
echo "Total videos: $total_videos"
echo "Processing Rate: 13 videos/min (measured)"
echo "Feed Rate: 10 videos/min (safety margin)"
echo "Batch Size: $FEED_BATCH videos every ${BATCH_INTERVAL}s"
echo "Staging: ${MIN_STAGING}-${MAX_STAGING} videos"
echo ""

while IFS= read -r video_path; do
    ((line_num++))

    # Skip if source doesn't exist
    if [ ! -f "$video_path" ]; then
        echo "WARN: Source not found: $video_path"
        continue
    fi

    video_name=$(basename "$video_path")

    # Skip if already processed
    if grep -q "^${video_name}$" "$PROCESSED_LIST" 2>/dev/null; then
        continue
    fi

    # Skip if already in staging
    [ -f "${STAGING_DIR}/${video_name}" ] && continue

    # Check staging count
    staging_count=$(find "$STAGING_DIR" -name "*.MP4" 2>/dev/null | wc -l)

    # Wait if staging is full
    while [ "$staging_count" -ge "$MAX_STAGING" ]; do
        echo "$(date +%H:%M:%S) Staging full ($staging_count/$MAX_STAGING). Waiting 10s..."
        sleep 10
        staging_count=$(find "$STAGING_DIR" -name "*.MP4" 2>/dev/null | wc -l)
    done

    # Check disk space
    available_gb=$(df /home/yousuf/PROJECTS | tail -1 | awk '{print int($4/1024/1024)}')
    if [ "$available_gb" -lt "$MIN_FREE_GB" ]; then
        echo "$(date +%H:%M:%S) WARNING: Low disk space (${available_gb}GB). Pausing..."
        sleep 30
        continue
    fi

    # Copy video
    if cp "$video_path" "${STAGING_DIR}/" 2>/dev/null; then
        echo "$(date +%H:%M:%S) [${line_num}/${total_videos}] Copied: $video_name (staging: $staging_count)"

        # Pause after each batch to maintain feed rate
        if [ $((line_num % FEED_BATCH)) -eq 0 ]; then
            processed_count=$(wc -l < "$PROCESSED_LIST" 2>/dev/null || echo 0)
            clips_count=$(find "$OUTPUT_DIR" -name "*.mp4" 2>/dev/null | wc -l)
            echo "$(date +%H:%M:%S) Batch $((line_num / FEED_BATCH)). Processed: $processed_count, Clips: $clips_count. Pausing ${BATCH_INTERVAL}s..."
            sleep "$BATCH_INTERVAL"
        fi
    else
        echo "$(date +%H:%M:%S) ERROR: Failed to copy $video_name"
    fi

done < "$VIDEO_LIST"

echo ""
echo "$(date +%H:%M:%S) Smart feed complete for Park_F Oct 24-27!"
echo "$(date +%H:%M:%S) Final stats:"
echo "  Processed: $(wc -l < "$PROCESSED_LIST")"
echo "  Clips: $(find "$OUTPUT_DIR" -name "*.mp4" | wc -l)"
