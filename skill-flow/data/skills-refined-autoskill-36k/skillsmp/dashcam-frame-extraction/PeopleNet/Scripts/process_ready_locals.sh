#!/usr/bin/env bash
set -euo pipefail
LOCAL_DIR="/workspace/local_videos/Park_F"
STATE_DIR="/workspace/Outputs/Park_F_GPU/state"
PROCESSED="$STATE_DIR/processed.txt"
LOG_DIR="/workspace/Outputs/Park_F_GPU"
MODEL="/workspace/model/resnet34_peoplenet_int8.onnx"
mkdir -p "$STATE_DIR"
: > "$STATE_DIR/last_batch.txt"
while true; do
  mapfile -t new_files < <(comm -23 <(ls -1 "$LOCAL_DIR" 2>/dev/null | sort) <(sed 's#.*/##' "$PROCESSED" | sort) | head -50)
  if [ ${#new_files[@]} -eq 0 ]; then
    sleep 5
    continue
  fi
  : > "$STATE_DIR/last_batch.txt"
  for f in "${new_files[@]}"; do
    echo "$LOCAL_DIR/$f" >> "$STATE_DIR/last_batch.txt"
  done
  python3 /workspace/Scripts/gpu_process_list.py \
    --video-list "$STATE_DIR/last_batch.txt" \
    --output-dir "$LOG_DIR" \
    --model "$MODEL" \
    --conf 0.6 \
    --sample-rate-fps 1 \
    --log-file "$LOG_DIR/processing_log_gpu_local.txt"
  while IFS= read -r p; do
    echo "$p" >> "$PROCESSED"
  done < "$STATE_DIR/last_batch.txt"
  sleep 2
done
