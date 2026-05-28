#!/bin/bash
# List available feed templates
set -euo pipefail

TEMPLATES_DIR="$HOME/.claude/skills/feed-create/assets/templates"

echo "Available feed templates:"
echo ""

for template in "$TEMPLATES_DIR"/*.yaml; do
  if [ -f "$template" ]; then
    NAME=$(basename "$template" .yaml)
    DESC=$(grep "^# " "$template" | head -1 | sed 's/^# //')
    echo "  $NAME - $DESC"
  fi
done

echo ""
echo "Usage: feed-create --template <name>"
