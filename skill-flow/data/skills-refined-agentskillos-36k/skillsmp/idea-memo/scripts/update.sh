#!/usr/bin/env bash
# Update idea metadata
# Usage: update.sh <id> [--status S] [--tags T1,T2]

set -euo pipefail

DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/idea-storage/ideas"
ID=""
NEW_STATUS=""
NEW_TAGS=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --status) NEW_STATUS="$2"; shift 2 ;;
    --tags) NEW_TAGS="$2"; shift 2 ;;
    -*) echo "Unknown option: $1" >&2; exit 1 ;;
    *) ID="$1"; shift ;;
  esac
done

if [[ -z "$ID" ]]; then
  echo "Usage: update.sh <id> [--status S] [--tags T1,T2]" >&2
  exit 1
fi

if [[ ! -d "$DATA_DIR" ]]; then
  echo "No ideas found. Data directory does not exist: $DATA_DIR"
  exit 1
fi

# Find file by ID
FOUND=""
while IFS= read -r -d '' file; do
  if grep -q "^id: .*$ID" "$file" 2>/dev/null; then
    FOUND="$file"
    break
  fi
  if [[ "$(basename "$file")" == *"$ID"* ]]; then
    FOUND="$file"
    break
  fi
done < <(find "$DATA_DIR" -name "*.md" -type f -print0 2>/dev/null)

if [[ -z "$FOUND" ]]; then
  echo "Idea not found: $ID" >&2
  exit 1
fi

# Update metadata
ISO8601=$(date -u +%Y-%m-%dT%H:%M:%SZ)

if [[ -n "$NEW_STATUS" ]]; then
  sed -i.bak "s/^status: .*/status: $NEW_STATUS/" "$FOUND"
  rm -f "${FOUND}.bak"
fi

if [[ -n "$NEW_TAGS" ]]; then
  # Convert comma-separated to YAML array
  TAGS_YAML="[$(echo "$NEW_TAGS" | sed 's/,/", "/g' | sed 's/^/"/;s/$/"/' )]"
  sed -i.bak "s/^tags: .*/tags: $TAGS_YAML/" "$FOUND"
  rm -f "${FOUND}.bak"
fi

# Update timestamp
sed -i.bak "s/^updated: .*/updated: $ISO8601/" "$FOUND"
rm -f "${FOUND}.bak"

echo "Updated: $FOUND"
