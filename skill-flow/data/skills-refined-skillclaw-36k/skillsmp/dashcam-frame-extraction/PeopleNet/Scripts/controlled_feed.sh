#!/usr/bin/env bash
# Controlled Feed - Maintains 10-20 videos in staging, respecting space

VIDEO_LIST="/home/yousuf/PROJECTS/PeopleNet/park_f_net_new_oct13_onwards.txt"
STAGING_DIR="/home/yousuf/PROJECTS/PeopleNet/Staging/Park_F_Batch1"
PROCESSED_LIST="/home/yousuf/PROJECTS/PeopleNet/Outputs/Park_F_Batch1/processed_videos.txt"

MIN_STAGING=10  # Refill when below this
MAX_STAGING=20  # Stop when reaching this

while true; do
    # Check current staging count
    staging_count=$(find "$STAGING_DIR" -name "*.MP4" 2>/dev/null | wc -l)

    # If staging is below minimum, add videos
    if [ "$staging_count" -lt "$MIN_STAGING" ]; then
        needed=$((MAX_STAGING - staging_count))
        echo "$(date +%H:%M:%S) Staging low ($staging_count). Adding $needed videos..."

        # Find videos to copy (not already processed or in staging)
        copied=0
        while IFS= read -r video_path && [ "$copied" -lt "$needed" ]; do
            [ ! -f "$video_path" ] && continue

            video_name=$(basename "$video_path")

            # Skip if already processed
            [ -f "$PROCESSED_LIST" ] && grep -q "^${video_name}$" "$PROCESSED_LIST" 2>/dev/null && continue

            # Skip if already in staging
            [ -f "${STAGING_DIR}/${video_name}" ] && continue

            # Copy video
            if cp "$video_path" "$STAGING_DIR/" 2>/dev/null; then
                ((copied++))
            fi
        done < "$VIDEO_LIST"

        echo "$(date +%H:%M:%S) Added $copied videos. Staging now: $((staging_count + copied))"
    fi

    # Check every 10 seconds
    sleep 10
done
