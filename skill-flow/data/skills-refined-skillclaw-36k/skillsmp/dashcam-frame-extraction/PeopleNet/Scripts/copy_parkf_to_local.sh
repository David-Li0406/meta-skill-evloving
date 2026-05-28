#!/usr/bin/env bash
set -euo pipefail
SRC_LIST="/workspace/Outputs/Park_F_GPU/batch_videos.txt"
DEST_DIR="/workspace/local_videos/Park_F"
SRC_MOUNT="/data/Park_F"
mkdir -p "$DEST_DIR"
while IFS= read -r src; do
  [ -z "$src" ] && continue
  base="$(basename "$src")"
  src_in_container="$SRC_MOUNT/$base"
  dest="$DEST_DIR/$base"
  if [ -f "$dest" ]; then
    continue
  fi
  if [ -f "$src_in_container" ]; then
    cp -n "$src_in_container" "$dest" 2>/dev/null || true
    echo "$dest"
  fi
done < "$SRC_LIST"
