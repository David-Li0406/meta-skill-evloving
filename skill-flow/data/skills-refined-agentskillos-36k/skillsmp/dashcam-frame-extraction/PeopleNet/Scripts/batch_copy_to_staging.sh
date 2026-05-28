#!/usr/bin/env bash
set -euo pipefail

# Batch Copy Videos to Staging (Space-Aware)
# Copies videos from source to staging in batches, respecting disk space limits

# Configuration
VIDEO_LIST="${1:?Usage: $0 <video_list.txt> [batch_size]}"
BATCH_SIZE="${2:-20}"
STAGING_DIR="${3:-/home/yousuf/PROJECTS/PeopleNet/Staging/Park_F_Batch1}"
MIN_FREE_GB="${4:-10}"  # Minimum free space in GB

echo "═══════════════════════════════════════════════════════"
echo "Batch Copy to Staging"
echo "═══════════════════════════════════════════════════════"
echo "Video List: ${VIDEO_LIST}"
echo "Batch Size: ${BATCH_SIZE}"
echo "Staging:    ${STAGING_DIR}"
echo "Min Free:   ${MIN_FREE_GB}GB"
echo "═══════════════════════════════════════════════════════"
echo ""

mkdir -p "${STAGING_DIR}"

# Read video list
if [ ! -f "${VIDEO_LIST}" ]; then
    echo "ERROR: Video list not found: ${VIDEO_LIST}"
    exit 1
fi

total_videos=$(wc -l < "${VIDEO_LIST}")
echo "Total videos in list: ${total_videos}"
echo ""

copied=0
skipped=0
failed=0

while IFS= read -r video_path; do
    # Skip empty lines
    [ -z "${video_path}" ] && continue

    # Check available disk space
    available_gb=$(df /home/yousuf/PROJECTS | tail -1 | awk '{print int($4/1024/1024)}')
    if [ "${available_gb}" -lt "${MIN_FREE_GB}" ]; then
        echo "WARNING: Low disk space (${available_gb}GB < ${MIN_FREE_GB}GB). Pausing..."
        echo "Delete processed videos from staging or increase disk space."
        break
    fi

    # Check if source exists
    if [ ! -f "${video_path}" ]; then
        echo "SKIP: Source not found: ${video_path}"
        ((skipped++))
        continue
    fi

    video_name=$(basename "${video_path}")
    dest_path="${STAGING_DIR}/${video_name}"

    # Skip if already in staging
    if [ -f "${dest_path}" ]; then
        ((skipped++))
        continue
    fi

    # Copy video
    if cp "${video_path}" "${dest_path}" 2>/dev/null; then
        ((copied++))
        echo "[${copied}/${total_videos}] Copied: ${video_name}"
    else
        echo "ERROR: Failed to copy: ${video_name}"
        ((failed++))
    fi

    # Pause after each batch to let workers process
    if [ $((copied % BATCH_SIZE)) -eq 0 ]; then
        staging_count=$(find "${STAGING_DIR}" -name "*.MP4" | wc -l)
        echo ""
        echo "Batch complete. Videos in staging: ${staging_count}"
        echo "Waiting 30 seconds for workers to process..."
        echo ""
        sleep 30
    fi

done < "${VIDEO_LIST}"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "Copy Complete"
echo "═══════════════════════════════════════════════════════"
echo "Copied:  ${copied}"
echo "Skipped: ${skipped}"
echo "Failed:  ${failed}"
echo "═══════════════════════════════════════════════════════"
