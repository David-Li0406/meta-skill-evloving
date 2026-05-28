# 06 - Orchestrate Pending Videos with Guards

Variables:
```bash
PEOPLENET_ROOT="/home/yousuf/PROJECTS/PeopleNet"
PENDING="$PEOPLENET_ROOT/state/pending_videos.txt"
PROC="$PEOPLENET_ROOT/state/processed_videos.txt"
STAGE="$PEOPLENET_ROOT/staging/videos"
OUTDIR="$PEOPLENET_ROOT/Outputs/videos"
LOGDIR="$PEOPLENET_ROOT/logs"
CONF="$PEOPLENET_ROOT/configs/peoplenet_ds_config.txt"
MIN_FREE_GB=20
GPU_MIN_FREE_MB=2000
mkdir -p "$STAGE" "$OUTDIR" "$LOGDIR"
```

Loop (pseudo‑bash) that respects disk and GPU guards:
```bash
while read -r SRC; do
  [ -f "$SRC" ] || continue
  # Disk guard
  FREE_GB=$(df -BG --output=avail "$PEOPLENET_ROOT" | tail -1 | tr -dc '0-9')
  if [ "$FREE_GB" -lt "$MIN_FREE_GB" ]; then
    echo "Waiting for free space... (have ${FREE_GB}GB)"; sleep 10; continue
  fi
  # Stage one video
  rsync -a --human-readable "$SRC" "$STAGE/"
  VID="$STAGE/$(basename "$SRC")"
  # GPU guard (free VRAM >= 2GB)
  FREE_MB=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -n1 | tr -d ' ')
  if [ -z "$FREE_MB" ] || [ "$FREE_MB" -lt "$GPU_MIN_FREE_MB" ]; then
    echo "Waiting for GPU memory (${FREE_MB}MB free)"; sleep 5
  fi
  # Run inference (choose A or B as in step 05)
  deepstream-app -c "$CONF" > "$LOGDIR/$(basename "${VID%.mp4}")_ds.log" 2>&1
  # Or: python3 run_peoplenet_ds.py --video "$VID" --config "$CONF" --output-csv "$OUTDIR/$(basename "${VID%.mp4}").csv"
  # Update manifest and cleanup
  echo "$SRC" >> "$PROC"
  rm -f "$VID"
done < "$PENDING"
```

Checkpoint (return):
- The last 20 lines of the most recent DS log
- Number of videos processed so far and remaining pending count


