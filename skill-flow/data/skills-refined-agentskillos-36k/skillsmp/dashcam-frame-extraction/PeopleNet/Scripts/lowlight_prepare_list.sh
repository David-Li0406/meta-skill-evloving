#!/usr/bin/env bash
set -euo pipefail

OUTDIR="${OUTDIR:-/home/yousuf/PROJECTS/PeopleNet/Outputs/Part3/LowLight_Jul24_27}"
SRC_DIR="${SRC_DIR:-/media/yousuf/C67813AB7813996F1/Users/yousu/Desktop/CARDV/Park_F}"
SUFFIX="${SUFFIX:-A}"
mkdir -p "$OUTDIR"

TMP="$OUTDIR/all_candidates.txt"
find "$SRC_DIR" -type f -name "2025072[4-7]*${SUFFIX}.MP4" | sort > "$TMP"
echo "Total candidates: $(wc -l < "$TMP")"

MORNING="$OUTDIR/morning_candidates.txt"
awk -F/ 'BEGIN{OFS="/"} {base=$NF; day=substr(base,1,8); t=substr(base,9,6); hh=substr(t,1,2)+0; if(hh<10){print $0}}' "$TMP" > "$MORNING"
echo "Morning candidates: $(wc -l < "$MORNING")"

SAMPLE="$OUTDIR/sample_videos.txt"
awk -F/ 'BEGIN{OFS="/"} {base=$NF; day=substr(base,1,8); if(cnt[day]<4){print $0; cnt[day]++}}' "$MORNING" > "$SAMPLE"
echo "Sample per day (<=4): $(wc -l < "$SAMPLE")"
sed -n '1,20p' "$SAMPLE"


