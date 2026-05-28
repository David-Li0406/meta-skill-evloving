#!/usr/bin/env bash
# Full-text search ideas
# Usage: search.sh <query>

set -euo pipefail

DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/idea-storage/ideas"
QUERY="${1:-}"

if [[ -z "$QUERY" ]]; then
  echo "Usage: search.sh <query>" >&2
  exit 1
fi

if [[ ! -d "$DATA_DIR" ]]; then
  echo "No ideas found. Data directory does not exist: $DATA_DIR"
  exit 0
fi

# Use grep for simple search, with context
grep -ril "$QUERY" "$DATA_DIR" 2>/dev/null | while read -r file; do
  TITLE=$(sed -n 's/^title: //p' "$file" | head -1)
  CREATED=$(sed -n 's/^created: //p' "$file" | head -1)
  STATUS=$(sed -n 's/^status: //p' "$file" | head -1)

  echo "---"
  echo "File: $file"
  echo "Title: $TITLE"
  echo "Created: ${CREATED:0:10}"
  echo "Status: $STATUS"
  echo ""
  # Show matching lines with context
  grep -i -C 2 "$QUERY" "$file" 2>/dev/null | head -10
  echo ""
done
