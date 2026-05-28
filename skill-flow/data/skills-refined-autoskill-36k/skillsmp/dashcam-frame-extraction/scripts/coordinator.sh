#!/bin/bash
# Coordinator for parallel batch processing - Movie_F ONLY
# Exits on error - all batches must succeed

set -euo pipefail

WORK_DIR="/home/yousuf/PROJECTS/PeopleNet/FrameExtraction"
NUM_WORKERS=4
MIN_FREE_GB=25
CATEGORY="Movie_F"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

check_space() {
    df -BG "$WORK_DIR" | awk 'NR==2 {print $4}' | sed 's/G//'
}

process_batch() {
    local batch_file="$1"
    local worker_id="$2"
    local batch_name=$(basename "$batch_file")

    echo "[Worker $worker_id] Processing $batch_name..."

    python3 \
        "$SCRIPT_DIR/extract_frames_worker.py" \
        "$batch_file" \
        "$CATEGORY" \
        "$worker_id" \
        > "$WORK_DIR/logs/${batch_name}_worker${worker_id}.log" 2>&1

    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        echo "[Worker $worker_id] ERROR: Batch $batch_name failed with exit code $exit_code"
        exit $exit_code
    fi

    # Move to completed only on success
    mv "$batch_file" "$WORK_DIR/completed/"
    echo "[Worker $worker_id] Completed $batch_name"
}

export -f process_batch
export -f check_space
export WORK_DIR NUM_WORKERS MIN_FREE_GB CATEGORY SCRIPT_DIR

worker_id=0
ACTIVE_WORKERS=0

# Process all batches
for batch_file in "$WORK_DIR/batches"/*; do
    [ -f "$batch_file" ] || continue

    # Wait if at max workers
    while [ $ACTIVE_WORKERS -ge $NUM_WORKERS ]; do
        sleep 5
        ACTIVE_WORKERS=$(pgrep -f "extract_frames_worker.py" | wc -l)
    done

    # Check available space
    FREE_GB=$(check_space)
    if [ "$FREE_GB" -lt "$MIN_FREE_GB" ]; then
        echo "[Coordinator] ⚠️  Low disk space ($FREE_GB GB). Waiting..."
        while [ "$(check_space)" -lt "$MIN_FREE_GB" ]; do
            sleep 10
        done
    fi

    # Launch worker in background
    worker_id=$((worker_id + 1))
    process_batch "$batch_file" "$worker_id" &
    ACTIVE_WORKERS=$((ACTIVE_WORKERS + 1))

    sleep 2
done

# Wait for all workers to complete
wait
echo "[Coordinator] All batches completed!"
