#!/usr/bin/env bash
# Generate user diary from history.json
# Usage: generate.sh [date]

set -euo pipefail

DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/idea-storage/user-diary"
HISTORY_FILE="${HOME}/.claude/history.json"
TARGET_DATE="${1:-$(date -v-1d +%Y-%m-%d 2>/dev/null || date -d 'yesterday' +%Y-%m-%d)}"
YEAR="${TARGET_DATE:0:4}"

# Validate date format
if [[ ! "$TARGET_DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "Invalid date format. Use YYYY-MM-DD" >&2
  exit 1
fi

# Check history file exists
if [[ ! -f "$HISTORY_FILE" ]]; then
  echo "History file not found: $HISTORY_FILE" >&2
  exit 1
fi

# Create output directory
mkdir -p "$DATA_DIR/$YEAR"

OUTPUT_FILE="$DATA_DIR/$YEAR/${TARGET_DATE}.md"
ISO8601=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Get day of week
DOW=$(date -j -f "%Y-%m-%d" "$TARGET_DATE" "+%A" 2>/dev/null || date -d "$TARGET_DATE" "+%A")

# Extract sessions for target date using jq
# history.json format: array of { id, timestamp, summary, project, ... }
SESSIONS=$(jq -r --arg date "$TARGET_DATE" '
  [.[] | select(.timestamp | startswith($date))] |
  sort_by(.timestamp) |
  .[] |
  "### \(.timestamp | split("T")[1] | split(".")[0]) - \(.project // "unknown")\n- \(.summary // "No summary")\n"
' "$HISTORY_FILE" 2>/dev/null || echo "")

SESSION_COUNT=$(jq -r --arg date "$TARGET_DATE" '
  [.[] | select(.timestamp | startswith($date))] | length
' "$HISTORY_FILE" 2>/dev/null || echo "0")

PROJECTS=$(jq -r --arg date "$TARGET_DATE" '
  [.[] | select(.timestamp | startswith($date)) | .project] | unique | join(", ")
' "$HISTORY_FILE" 2>/dev/null || echo "")

# Write diary entry
cat > "$OUTPUT_FILE" << EOF
---
date: $TARGET_DATE
generated: $ISO8601
session_count: $SESSION_COUNT
---

# $TARGET_DATE ($DOW)

## Sessions

$SESSIONS

## Summary

- Total sessions: $SESSION_COUNT
- Projects worked on: $PROJECTS

## Notable Events

(Auto-generated from history.json - edit manually to add notes)
EOF

echo "Generated: $OUTPUT_FILE"
echo "Sessions found: $SESSION_COUNT"
