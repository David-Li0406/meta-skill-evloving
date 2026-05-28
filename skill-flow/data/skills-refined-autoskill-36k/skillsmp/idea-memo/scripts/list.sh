#!/usr/bin/env bash
# List ideas with filters
# Usage: list.sh [-n N] [-t tag] [-s status]

set -euo pipefail

DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/idea-storage/ideas"
LIMIT=10
TAG_FILTER=""
STATUS_FILTER=""

while getopts "n:t:s:" opt; do
  case $opt in
    n) LIMIT="$OPTARG" ;;
    t) TAG_FILTER="$OPTARG" ;;
    s) STATUS_FILTER="$OPTARG" ;;
    *) echo "Usage: list.sh [-n N] [-t tag] [-s status]" >&2; exit 1 ;;
  esac
done

if [[ ! -d "$DATA_DIR" ]]; then
  echo "No ideas found. Data directory does not exist: $DATA_DIR"
  exit 0
fi

# Find all idea files, sorted by modification time (newest first)
find "$DATA_DIR" -name "*.md" -type f -print0 2>/dev/null | \
  xargs -0 ls -t 2>/dev/null | \
  head -n "$LIMIT" | \
while read -r file; do
  # Extract frontmatter
  TITLE=$(sed -n 's/^title: //p' "$file" | head -1)
  STATUS=$(sed -n 's/^status: //p' "$file" | head -1)
  TAGS=$(sed -n 's/^tags: //p' "$file" | head -1)
  CREATED=$(sed -n 's/^created: //p' "$file" | head -1)

  # Apply filters
  if [[ -n "$STATUS_FILTER" && "$STATUS" != "$STATUS_FILTER" ]]; then
    continue
  fi

  if [[ -n "$TAG_FILTER" && "$TAGS" != *"$TAG_FILTER"* ]]; then
    continue
  fi

  # Output
  BASENAME=$(basename "$file" .md)
  printf "%-20s | %-8s | %s\n" "${CREATED:0:10}" "$STATUS" "$TITLE"
done
