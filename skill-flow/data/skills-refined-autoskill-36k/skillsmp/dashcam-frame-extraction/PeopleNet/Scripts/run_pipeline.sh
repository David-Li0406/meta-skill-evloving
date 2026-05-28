#!/usr/bin/env bash
set -euo pipefail

# PeopleNet Processing Pipeline Orchestrator
# Handles Docker container setup with log rotation and multi-worker GPU processing

# Configuration
BATCH_NAME="${1:-Park_F_Batch1}"
NUM_WORKERS="${2:-3}"
CONTAINER_NAME="peoplenet-${BATCH_NAME,,}"
IMAGE="nvcr.io/nvidia/tensorrt:24.08-py3"
PROJECT_DIR="/home/yousuf/PROJECTS/PeopleNet"
STAGING_DIR="${PROJECT_DIR}/Staging/${BATCH_NAME}"
OUTPUT_DIR="${PROJECT_DIR}/Outputs/${BATCH_NAME}"

# Docker log configuration - CRITICAL to prevent log bloat
LOG_MAX_SIZE="50m"  # Max 50MB per log file
LOG_MAX_FILE="3"    # Keep only 3 rotated files (150MB total max)

echo "═══════════════════════════════════════════════════════"
echo "PeopleNet Processing Pipeline"
echo "═══════════════════════════════════════════════════════"
echo "Batch: ${BATCH_NAME}"
echo "Workers: ${NUM_WORKERS}"
echo "Container: ${CONTAINER_NAME}"
echo "Staging: ${STAGING_DIR}"
echo "Output: ${OUTPUT_DIR}"
echo "Docker Log Limit: ${LOG_MAX_SIZE} × ${LOG_MAX_FILE} files"
echo "═══════════════════════════════════════════════════════"

# Create necessary directories
mkdir -p "${STAGING_DIR}" "${OUTPUT_DIR}" "${PROJECT_DIR}/logs"

# Check if container already exists
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Container '${CONTAINER_NAME}' already exists. Removing..."
    docker rm -f "${CONTAINER_NAME}" 2>/dev/null || true
fi

# Start container with log rotation configured
echo "Starting Docker container with log rotation..."
docker run -d \
    --name "${CONTAINER_NAME}" \
    --gpus all \
    --runtime=nvidia \
    --log-driver json-file \
    --log-opt max-size="${LOG_MAX_SIZE}" \
    --log-opt max-file="${LOG_MAX_FILE}" \
    -v "${PROJECT_DIR}:/workspace" \
    "${IMAGE}" \
    sleep infinity

# Install ffmpeg (critical dependency for clip extraction)
echo "Installing ffmpeg in container..."
docker exec "${CONTAINER_NAME}" bash -c "apt-get update -qq && apt-get install -y -qq ffmpeg" || {
    echo "ERROR: Failed to install ffmpeg"
    exit 1
}

# Verify GPU access
echo "Verifying GPU access..."
docker exec "${CONTAINER_NAME}" nvidia-smi --query-gpu=name --format=csv,noheader || {
    echo "ERROR: GPU not accessible in container"
    exit 1
}

# Start GPU workers
echo "Starting ${NUM_WORKERS} GPU workers..."
for worker_id in $(seq 1 "${NUM_WORKERS}"); do
    docker exec -d "${CONTAINER_NAME}" \
        bash -c "cd /workspace && BATCH_NAME=${BATCH_NAME} python3 worker.py ${worker_id}"
    echo "  Worker ${worker_id} started"
done

echo ""
echo "═══════════════════════════════════════════════════════"
echo "Pipeline Started Successfully!"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Monitor with:"
echo "  docker logs -f ${CONTAINER_NAME}           # Live stdout"
echo "  tail -f ${OUTPUT_DIR}/worker_*.txt         # Worker logs"
echo "  wc -l ${OUTPUT_DIR}/processed_videos.txt   # Progress count"
echo "  du -sh ${OUTPUT_DIR}                       # Output size"
echo ""
echo "Copy videos to staging to process:"
echo "  cp /path/to/videos/*.MP4 ${STAGING_DIR}/"
echo ""
echo "Stop pipeline:"
echo "  docker stop ${CONTAINER_NAME}"
echo "═══════════════════════════════════════════════════════"
