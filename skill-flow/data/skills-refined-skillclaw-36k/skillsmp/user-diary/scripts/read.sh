#!/usr/bin/env bash
# Read user diary entry
# Usage: read.sh <date>

set -euo pipefail

DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/idea-storage/user-diary"
DATE="${1:-}"

if [[ -z "$DATE" ]]; then
  echo "Usage: read.sh <date>" >&2
  exit 1
fi

# Normalize date format
if [[ ! "$DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "Invalid date format. Use YYYY-MM-DD" >&2
  exit 1
fi

YEAR="${DATE:0:4}"
FILEPATH="$DATA_DIR/$YEAR/${DATE}.md"

if [[ -f "$FILEPATH" ]]; then
  cat "$FILEPATH"
else
  echo "Diary entry not found: $DATE" >&2
  echo "Try generating with: generate.sh $DATE"
  exit 1
fi
