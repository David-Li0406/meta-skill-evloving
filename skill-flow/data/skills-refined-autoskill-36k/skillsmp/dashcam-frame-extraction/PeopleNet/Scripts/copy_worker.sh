#!/usr/bin/env bash
set -euo pipefail
SHARD="${1:-odd}"
SRC_LIST="/workspace/Outputs/Park_F_GPU/batch_videos.txt"
DEST_DIR="/workspace/local_videos/Park_F"
SRC_MOUNT="/data/Park_F"
TMP_LIST="/workspace/Outputs/Park_F_GPU/batch_${SHARD}.txt"
mkdir -p "$DEST_DIR"
if [ "$SHARD" = "even" ]; then
  awk "NR%2==0" "$SRC_LIST" > "$TMP_LIST"
else
  awk "NR%2==1" "$SRC_LIST" > "$TMP_LIST"
fi
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
done < "$TMP_LIST"
