#!/usr/bin/env bash
# Save a new idea
# Usage: echo "content" | save.sh <title> [tags...]

set -euo pipefail

DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/idea-storage/ideas"
TITLE="${1:-Untitled}"
shift || true
TAGS=("$@")

# Create data directory if needed
mkdir -p "$DATA_DIR"

# Generate metadata
DATE=$(date +%Y-%m-%d)
DATETIME=$(date +%Y-%m-%dT%H-%M-%S)
ISO8601=$(date -u +%Y-%m-%dT%H:%M:%SZ)
UUID=$(uuidgen 2>/dev/null || cat /proc/sys/kernel/random/uuid 2>/dev/null || echo "$(date +%s)-$$")
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//' | cut -c1-50)

# Create date directory
mkdir -p "$DATA_DIR/$DATE"

# Build tags YAML array
TAGS_YAML="[]"
if [[ ${#TAGS[@]} -gt 0 ]]; then
  TAGS_YAML="["
  for i in "${!TAGS[@]}"; do
    [[ $i -gt 0 ]] && TAGS_YAML+=", "
    TAGS_YAML+="\"${TAGS[$i]}\""
  done
  TAGS_YAML+="]"
fi

# Read content from stdin
CONTENT=$(cat)

# Write idea file
FILEPATH="$DATA_DIR/$DATE/${DATETIME}-${SLUG}.md"
cat > "$FILEPATH" << EOF
---
id: $UUID
title: $TITLE
created: $ISO8601
updated: $ISO8601
tags: $TAGS_YAML
status: draft
---

$CONTENT
EOF

echo "Saved: $FILEPATH"
echo "ID: $UUID"
