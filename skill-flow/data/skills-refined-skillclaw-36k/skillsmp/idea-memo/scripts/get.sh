#!/usr/bin/env bash
# Get idea by ID or slug
# Usage: get.sh <id-or-slug>

set -euo pipefail

DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/idea-storage/ideas"
QUERY="${1:-}"

if [[ -z "$QUERY" ]]; then
  echo "Usage: get.sh <id-or-slug>" >&2
  exit 1
fi

if [[ ! -d "$DATA_DIR" ]]; then
  echo "No ideas found. Data directory does not exist: $DATA_DIR"
  exit 1
fi

# Search by ID in frontmatter or by filename (slug)
FOUND=""
while IFS= read -r -d '' file; do
  # Check if ID matches
  if grep -q "^id: .*$QUERY" "$file" 2>/dev/null; then
    FOUND="$file"
    break
  fi
  # Check if filename contains slug
  if [[ "$(basename "$file")" == *"$QUERY"* ]]; then
    FOUND="$file"
    break
  fi
done < <(find "$DATA_DIR" -name "*.md" -type f -print0 2>/dev/null)

if [[ -n "$FOUND" ]]; then
  cat "$FOUND"
else
  echo "Idea not found: $QUERY" >&2
  exit 1
fi
