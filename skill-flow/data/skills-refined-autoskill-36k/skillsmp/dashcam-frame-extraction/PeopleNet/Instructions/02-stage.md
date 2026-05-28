# 02 - Stage with Disk Guard (≥20GB free)

Variables:
```bash
PEOPLENET_ROOT="/home/yousuf/PROJECTS/PeopleNet"
STAGE="$PEOPLENET_ROOT/staging/videos"
PENDING="$PEOPLENET_ROOT/state/pending_videos.txt"
MIN_FREE_GB=20
mkdir -p "$STAGE" "$PEOPLENET_ROOT/logs"
```

Check space:
```bash
df -h "$PEOPLENET_ROOT" | sed -n '1,2p'
```

Stage a small batch (e.g., 3 videos) while keeping ≥$MIN_FREE_GB free:
```bash
FREE_GB=$(df -BG --output=avail "$PEOPLENET_ROOT" | tail -1 | tr -dc '0-9')
if [ "$FREE_GB" -lt "$MIN_FREE_GB" ]; then
  echo "Low space: ${FREE_GB}GB < ${MIN_FREE_GB}GB"; exit 1
fi
head -n 3 "$PENDING" | while read -r src; do
  [ -f "$src" ] || continue
  rsync -a --info=progress2 --human-readable "$src" "$STAGE/"
done
ls -lh "$STAGE" | sed -n '1,10p'
```

Checkpoint (return):
- df -h output (first 2 lines) before staging
- ls -lh of `staging/videos/` (first ~10 lines) after staging


