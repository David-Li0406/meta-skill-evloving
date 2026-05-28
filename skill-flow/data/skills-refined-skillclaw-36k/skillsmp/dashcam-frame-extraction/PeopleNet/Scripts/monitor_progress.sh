#!/usr/bin/env bash
set -euo pipefail

# Monitor PeopleNet Pipeline Progress

BATCH_NAME="${1:-Park_F_Batch1}"
OUTPUT_DIR="/home/yousuf/PROJECTS/PeopleNet/Outputs/${BATCH_NAME}"
STAGING_DIR="/home/yousuf/PROJECTS/PeopleNet/Staging/${BATCH_NAME}"

echo "═══════════════════════════════════════════════════════"
echo "PeopleNet Pipeline Monitor - ${BATCH_NAME}"
echo "═══════════════════════════════════════════════════════"
echo ""

# Check if output directory exists
if [ ! -d "${OUTPUT_DIR}" ]; then
    echo "ERROR: Output directory not found: ${OUTPUT_DIR}"
    exit 1
fi

# Count processed videos
if [ -f "${OUTPUT_DIR}/processed_videos.txt" ]; then
    PROCESSED_COUNT=$(wc -l < "${OUTPUT_DIR}/processed_videos.txt")
else
    PROCESSED_COUNT=0
fi

# Count staging videos
STAGING_COUNT=$(find "${STAGING_DIR}" -name "*.MP4" 2>/dev/null | wc -l)

# Count output clips
OUTPUT_CLIPS=$(find "${OUTPUT_DIR}" -name "*.mp4" 2>/dev/null | wc -l)

# Calculate output size
OUTPUT_SIZE=$(du -sh "${OUTPUT_DIR}" 2>/dev/null | awk '{print $1}')

# Calculate staging size
STAGING_SIZE=$(du -sh "${STAGING_DIR}" 2>/dev/null | awk '{print $1}')

# Calculate detection rate
if [ "${PROCESSED_COUNT}" -gt 0 ]; then
    DETECTION_RATE=$(awk "BEGIN {printf \"%.1f\", (${OUTPUT_CLIPS}/${PROCESSED_COUNT})*100}")
else
    DETECTION_RATE="0.0"
fi

echo "Progress Summary:"
echo "  Videos Processed:  ${PROCESSED_COUNT}"
echo "  Videos in Staging: ${STAGING_COUNT}"
echo "  Clips Extracted:   ${OUTPUT_CLIPS}"
echo "  Detection Rate:    ${DETECTION_RATE}%"
echo ""
echo "Storage:"
echo "  Staging Size:      ${STAGING_SIZE}"
echo "  Output Size:       ${OUTPUT_SIZE}"
echo ""

# Show recent worker activity
echo "Recent Worker Activity:"
for worker_log in "${OUTPUT_DIR}"/worker_*_log.txt; do
    if [ -f "${worker_log}" ]; then
        worker_name=$(basename "${worker_log}" .txt)
        last_line=$(tail -1 "${worker_log}" 2>/dev/null || echo "No activity")
        echo "  ${worker_name}: ${last_line}"
    fi
done

echo ""
echo "═══════════════════════════════════════════════════════"
