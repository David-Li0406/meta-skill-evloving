# 01 - Discovery (Build Net-New List)

Set variables (adjust paths as needed):

```bash
PEOPLENET_ROOT="/home/yousuf/PROJECTS/PeopleNet"
SRC_PARK_F="/mnt/windows/Users/.../CARDV/Park_F"
SRC_PARK_R="/mnt/windows/Users/.../CARDV/Park_R"
mkdir -p "$PEOPLENET_ROOT/state"
```

List source MP4s and counts:
```bash
find "$SRC_PARK_F" -type f -iname '*.mp4' | sort > "$PEOPLENET_ROOT/state/src_park_f.txt"
find "$SRC_PARK_R" -type f -iname '*.mp4' | sort > "$PEOPLENET_ROOT/state/src_park_r.txt"
wc -l "$PEOPLENET_ROOT/state/src_park_f.txt" "$PEOPLENET_ROOT/state/src_park_r.txt"
```

Prepare processed manifest (create if missing):
```bash
PROC="$PEOPLENET_ROOT/state/processed_videos.txt"
[ -f "$PROC" ] || : > "$PROC"
```

Build pending list (net‑new only):
```bash
cat "$PEOPLENET_ROOT/state/src_park_f.txt" "$PEOPLENET_ROOT/state/src_park_r.txt" | sort \
  | grep -vxF -f "$PROC" > "$PEOPLENET_ROOT/state/pending_videos.txt"
wc -l "$PEOPLENET_ROOT/state/pending_videos.txt"
head -n 10 "$PEOPLENET_ROOT/state/pending_videos.txt"
```

Checkpoint (return):
- Lines and counts for `src_park_f.txt`, `src_park_r.txt`
- Line count for `pending_videos.txt` and the first 5–10 entries


