#!/usr/bin/env bash
# List user diary entries
# Usage: list.sh [-n N] [-y year]

set -euo pipefail

DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/idea-storage/user-diary"
LIMIT=10
YEAR_FILTER=""

while getopts "n:y:" opt; do
  case $opt in
    n) LIMIT="$OPTARG" ;;
    y) YEAR_FILTER="$OPTARG" ;;
    *) echo "Usage: list.sh [-n N] [-y year]" >&2; exit 1 ;;
  esac
done

if [[ ! -d "$DATA_DIR" ]]; then
  echo "No diary entries found. Data directory does not exist: $DATA_DIR"
  exit 0
fi

SEARCH_DIR="$DATA_DIR"
[[ -n "$YEAR_FILTER" ]] && SEARCH_DIR="$DATA_DIR/$YEAR_FILTER"

if [[ ! -d "$SEARCH_DIR" ]]; then
  echo "No entries for year: $YEAR_FILTER"
  exit 0
fi

# Find and list entries (sorted by date descending)
find "$SEARCH_DIR" -name "*.md" -type f 2>/dev/null | \
  sort -r | \
  head -n "$LIMIT" | \
while read -r file; do
  DATE=$(basename "$file" .md)
  SESSION_COUNT=$(sed -n 's/^session_count: //p' "$file" | head -1)
  printf "%s | %s sessions\n" "$DATE" "${SESSION_COUNT:-0}"
done
