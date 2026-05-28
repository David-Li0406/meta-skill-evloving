#!/bin/bash
# Parse STATE.md YAML frontmatter
# Usage: ./parse-state.sh [STATE.md path]
# Returns JSON: {"task":"...", "status":"...", "phase":"...", "context_percent":N, "last_updated":"..."}
# Exit codes: 0 = success, 1 = file not found, 2 = invalid format

STATE_FILE="${1:-STATE.md}"

if [[ ! -f "$STATE_FILE" ]]; then
    echo '{"error": "STATE.md not found", "exists": false}'
    exit 1
fi

# Check for YAML frontmatter
if ! head -1 "$STATE_FILE" | grep -q '^---$'; then
    echo '{"error": "No YAML frontmatter", "exists": true, "valid": false}'
    exit 2
fi

# Extract frontmatter (between first and second ---)
FRONTMATTER=$(awk '/^---$/{if(p)exit;p=1;next}p' "$STATE_FILE")

# Parse fields
TASK=$(echo "$FRONTMATTER" | grep '^task:' | sed 's/^task:[[:space:]]*"\?\(.*\)"\?$/\1/' | sed 's/"$//')
STATUS=$(echo "$FRONTMATTER" | grep '^status:' | awk '{print $2}')
PHASE=$(echo "$FRONTMATTER" | grep '^phase:' | awk '{print $2}')
CONTEXT_PCT=$(echo "$FRONTMATTER" | grep '^context_percent:' | awk '{print $2}')
LAST_UPDATED=$(echo "$FRONTMATTER" | grep '^last_updated:' | awk '{print $2}')

# Default values
CONTEXT_PCT=${CONTEXT_PCT:-0}

# Output JSON
cat <<EOF
{
  "exists": true,
  "valid": true,
  "task": "$TASK",
  "status": "$STATUS",
  "phase": "$PHASE",
  "context_percent": $CONTEXT_PCT,
  "last_updated": "$LAST_UPDATED"
}
EOF
