#!/usr/bin/env bash
# Read AI diary entry
# Usage: read.sh <date-or-slug>

set -euo pipefail

DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/idea-storage/ai-diary"
QUERY="${1:-}"

if [[ -z "$QUERY" ]]; then
  echo "Usage: read.sh <date-or-slug>" >&2
  exit 1
fi

if [[ ! -d "$DATA_DIR" ]]; then
  echo "No diary entries found. Data directory does not exist: $DATA_DIR"
  exit 1
fi

# Try to find matching file
FOUND=""

# If query looks like a date (YYYY-MM-DD), list entries for that date
if [[ "$QUERY" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  if [[ -d "$DATA_DIR/$QUERY" ]]; then
    echo "Entries for $QUERY:"
    ls -1 "$DATA_DIR/$QUERY"/*.md 2>/dev/null | while read -r f; do
      echo "  $(basename "$f")"
    done
    exit 0
  fi
fi

# Search by filename/slug
while IFS= read -r -d '' file; do
  if [[ "$(basename "$file")" == *"$QUERY"* ]]; then
    FOUND="$file"
    break
  fi
done < <(find "$DATA_DIR" -name "*.md" -type f -print0 2>/dev/null)

if [[ -n "$FOUND" ]]; then
  cat "$FOUND"
else
  echo "Entry not found: $QUERY" >&2
  exit 1
fi
