#!/usr/bin/env bash
set -euo pipefail

# Auto Next Batch - Monitors Park_F completion and auto-starts Park_R

PROJECT_DIR="/home/yousuf/PROJECTS/PeopleNet"
PARK_F_TOTAL=698
PARK_R_LIST="${PROJECT_DIR}/park_r_net_new_oct13_onwards.txt"
LOG_FILE="${PROJECT_DIR}/logs/auto_next_batch.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "Auto-Next-Batch: Monitoring started"
log "Waiting for Park_F to complete (698 videos)..."

# Monitor Park_F completion
while true; do
    processed=$(wc -l < "${PROJECT_DIR}/Outputs/Park_F_Batch1/processed_videos.txt" 2>/dev/null || echo 0)

    if [ "$processed" -ge "$PARK_F_TOTAL" ]; then
        log "✓ Park_F COMPLETE! ($processed/$PARK_F_TOTAL videos)"
        break
    fi

    # Log progress every 10 minutes
    if [ $(($(date +%s) % 600)) -lt 60 ]; then
        log "Park_F progress: $processed/$PARK_F_TOTAL videos"
    fi

    sleep 60  # Check every minute
done

log "Waiting 30 seconds for final cleanup..."
sleep 30

# Stop Park_F processing
log "Stopping Park_F container and workers..."
docker stop peoplenet-park_f_batch1 2>&1 | tee -a "$LOG_FILE"
pkill -f "controlled_feed.sh" 2>&1 | tee -a "$LOG_FILE" || true
pkill -f "auto_fix_ownership.sh" 2>&1 | tee -a "$LOG_FILE" || true

log "Cleaning up Park_F staging..."
rm -f "${PROJECT_DIR}/Staging/Park_F_Batch1/"*.MP4 2>&1 | tee -a "$LOG_FILE" || true

log "════════════════════════════════════════════════════════"
log "Starting Park_R Batch1 Processing..."
log "════════════════════════════════════════════════════════"

# Prepare Park_R
mkdir -p "${PROJECT_DIR}/Staging/Park_R_Batch1"
mkdir -p "${PROJECT_DIR}/Outputs/Park_R_Batch1"

# Check if Park_R list exists
if [ ! -f "$PARK_R_LIST" ]; then
    log "ERROR: Park_R list not found: $PARK_R_LIST"
    log "Creating Park_R list from source..."
    find /media/yousuf/C67813AB7813996F1/Users/yousu/Desktop/CARDV/Park_R/ -name "*.MP4" | \
        grep -E "202510(1[3-9]|[2-3][0-9])|20251[1-2]" | sort > "$PARK_R_LIST"
fi

park_r_count=$(wc -l < "$PARK_R_LIST")
log "Park_R videos to process: $park_r_count"

# Start Park_R container (reuse existing or create new)
log "Starting Docker container for Park_R..."
if docker ps -a --format '{{.Names}}' | grep -q "^peoplenet-park_r_batch1$"; then
    docker start peoplenet-park_r_batch1 2>&1 | tee -a "$LOG_FILE"
else
    docker run -d \
        --name peoplenet-park_r_batch1 \
        --gpus all \
        --runtime=nvidia \
        --log-driver json-file \
        --log-opt max-size=50m \
        --log-opt max-file=3 \
        -v "${PROJECT_DIR}:/workspace" \
        nvcr.io/nvidia/tensorrt:24.08-py3 \
        sleep infinity 2>&1 | tee -a "$LOG_FILE"

    log "Installing dependencies in container..."
    docker exec peoplenet-park_r_batch1 bash -c \
        "apt-get update -qq && apt-get install -y -qq ffmpeg && pip install -q opencv-python-headless onnxruntime-gpu numpy" \
        2>&1 | tee -a "$LOG_FILE"
fi

# Start Park_R workers
log "Starting 3 GPU workers for Park_R..."
for worker_id in 1 2 3; do
    docker exec -d peoplenet-park_r_batch1 bash -c \
        "cd /workspace && BATCH_NAME=Park_R_Batch1 python3 worker.py ${worker_id}" \
        2>&1 | tee -a "$LOG_FILE"
    log "  Worker ${worker_id} started"
done

# Copy initial videos
log "Copying initial 30 videos to Park_R staging..."
head -30 "$PARK_R_LIST" | xargs -I {} cp {} "${PROJECT_DIR}/Staging/Park_R_Batch1/" 2>&1 | tee -a "$LOG_FILE"

# Start controlled feed for Park_R
log "Starting controlled feed for Park_R..."
sed "s|Park_F_Batch1|Park_R_Batch1|g; s|park_f_net_new|park_r_net_new|g" \
    "${PROJECT_DIR}/Scripts/controlled_feed.sh" > /tmp/controlled_feed_park_r.sh
chmod +x /tmp/controlled_feed_park_r.sh
nohup /tmp/controlled_feed_park_r.sh > "${PROJECT_DIR}/logs/controlled_feed_park_r.log" 2>&1 &
log "Controlled feed started (PID: $!)"

# Start auto-ownership fixer for Park_R
sed "s|Park_F_Batch1|Park_R_Batch1|g" \
    "${PROJECT_DIR}/Scripts/auto_fix_ownership.sh" > /tmp/auto_fix_ownership_park_r.sh
chmod +x /tmp/auto_fix_ownership_park_r.sh
nohup /tmp/auto_fix_ownership_park_r.sh > /dev/null 2>&1 &
log "Auto-ownership fixer started (PID: $!)"

log "════════════════════════════════════════════════════════"
log "✓ Park_R Batch1 Started Successfully!"
log "════════════════════════════════════════════════════════"
log "Output: ${PROJECT_DIR}/Outputs/Park_R_Batch1/"
log "Monitor: ./Scripts/monitor_progress.sh Park_R_Batch1"
log "════════════════════════════════════════════════════════"
