#!/usr/bin/env bash
# Write AI diary entry
# Usage: echo "content" | write.sh <trigger> [mood]

set -euo pipefail

DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/idea-storage/ai-diary"
TRIGGER="${1:-manual}"
MOOD="${2:-reflective}"

# Create data directory if needed
mkdir -p "$DATA_DIR"

# Generate metadata
DATE=$(date +%Y-%m-%d)
DATETIME=$(date +%Y-%m-%dT%H-%M-%S)
ISO8601=$(date -u +%Y-%m-%dT%H:%M:%SZ)
SESSION_ID="${CLAUDE_SESSION_ID:-$(date +%s)-$$}"

# Create date directory
mkdir -p "$DATA_DIR/$DATE"

# Read content from stdin
CONTENT=$(cat)

# Generate slug from first line of content (usually the title)
TITLE=$(echo "$CONTENT" | head -1 | sed 's/^#* *//')
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//' | cut -c1-50)
[[ -z "$SLUG" ]] && SLUG="session"

# Write diary file
FILEPATH="$DATA_DIR/$DATE/${DATETIME}-${SLUG}.md"
cat > "$FILEPATH" << EOF
---
session_id: $SESSION_ID
created: $ISO8601
trigger: $TRIGGER
mood: $MOOD
---

$CONTENT
EOF

echo "Saved: $FILEPATH"
