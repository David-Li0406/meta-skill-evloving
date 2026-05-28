#!/usr/bin/env bash
# session_indexer.sh - Index all Claude Code sessions for a project
# Usage: ./session_indexer.sh [project_path]
#
# Output: NDJSON index to stdout with session metadata

set -euo pipefail

PROJECT_PATH="${1:-$(pwd)}"
# Claude Code encodes paths by:
# 1. Removing leading /
# 2. Replacing / with -
# 3. Replacing . with -
# 4. Prepending -
# The path /Users/terryli/foo.bar becomes -Users-terryli-foo-bar
ENCODED_PATH=$(echo "$PROJECT_PATH" | sed 's|^/||' | tr '/.' '--')
ENCODED_PATH="-$ENCODED_PATH"
PROJECT_SESSIONS="$HOME/.claude/projects/$ENCODED_PATH"

if [[ ! -d "$PROJECT_SESSIONS" ]]; then
  echo "ERROR: No sessions found at $PROJECT_SESSIONS" >&2
  exit 1
fi

# Index each session file
for session in "$PROJECT_SESSIONS"/*.jsonl; do
  [[ -f "$session" ]] || continue

  SESSION_ID=$(basename "$session" .jsonl)
  LINE_COUNT=$(wc -l < "$session" | tr -d ' ')
  FILE_SIZE=$(stat -f%z "$session" 2>/dev/null || stat -c%s "$session" 2>/dev/null)

  # Extract first and last timestamps
  FIRST_TS=$(head -1 "$session" | jq -r '.timestamp // "unknown"' 2>/dev/null || echo "unknown")
  LAST_TS=$(tail -1 "$session" | jq -r '.timestamp // "unknown"' 2>/dev/null || echo "unknown")

  # Count message types
  ASSISTANT_COUNT=$(grep -c '"type":"assistant"' "$session" 2>/dev/null || echo 0)
  USER_COUNT=$(grep -c '"type":"user"' "$session" 2>/dev/null || echo 0)
  TOOL_USE_COUNT=$(grep -c '"tool_use"' "$session" 2>/dev/null || echo 0)

  # Output NDJSON record
  jq -n --compact-output \
    --arg id "$SESSION_ID" \
    --arg path "$session" \
    --argjson lines "$LINE_COUNT" \
    --argjson size "$FILE_SIZE" \
    --arg first_ts "$FIRST_TS" \
    --arg last_ts "$LAST_TS" \
    --argjson assistant "$ASSISTANT_COUNT" \
    --argjson user "$USER_COUNT" \
    --argjson tool_use "$TOOL_USE_COUNT" \
    '{
      session_id: $id,
      path: $path,
      lines: $lines,
      size_bytes: $size,
      first_timestamp: $first_ts,
      last_timestamp: $last_ts,
      counts: {
        assistant: $assistant,
        user: $user,
        tool_use: $tool_use
      }
    }'
done
