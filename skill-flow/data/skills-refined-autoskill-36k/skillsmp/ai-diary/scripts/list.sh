#!/usr/bin/env bash
# List AI diary entries
# Usage: list.sh [-n N] [-d date]

set -euo pipefail

DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/idea-storage/ai-diary"
LIMIT=10
DATE_FILTER=""

while getopts "n:d:" opt; do
  case $opt in
    n) LIMIT="$OPTARG" ;;
    d) DATE_FILTER="$OPTARG" ;;
    *) echo "Usage: list.sh [-n N] [-d date]" >&2; exit 1 ;;
  esac
done

if [[ ! -d "$DATA_DIR" ]]; then
  echo "No diary entries found. Data directory does not exist: $DATA_DIR"
  exit 0
fi

SEARCH_DIR="$DATA_DIR"
[[ -n "$DATE_FILTER" ]] && SEARCH_DIR="$DATA_DIR/$DATE_FILTER"

if [[ ! -d "$SEARCH_DIR" ]]; then
  echo "No entries for date: $DATE_FILTER"
  exit 0
fi

# Find and list entries
find "$SEARCH_DIR" -name "*.md" -type f -print0 2>/dev/null | \
  xargs -0 ls -t 2>/dev/null | \
  head -n "$LIMIT" | \
while read -r file; do
  MOOD=$(sed -n 's/^mood: //p' "$file" | head -1)
  TRIGGER=$(sed -n 's/^trigger: //p' "$file" | head -1)
  TITLE=$(grep -m1 "^# " "$file" | sed 's/^# //' || basename "$file" .md)
  CREATED=$(sed -n 's/^created: //p' "$file" | head -1)

  printf "%-20s | %-12s | %-10s | %s\n" "${CREATED:0:16}" "$MOOD" "$TRIGGER" "$TITLE"
done
