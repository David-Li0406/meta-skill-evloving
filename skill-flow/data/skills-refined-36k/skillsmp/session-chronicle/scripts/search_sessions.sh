#!/usr/bin/env bash
# search_sessions.sh - Search across all Claude Code sessions for keywords
# Usage: ./search_sessions.sh <pattern> [project_path]
#
# Searches for pattern in all session files, returns matching entries as NDJSON

set -euo pipefail

PATTERN="${1:-}"
PROJECT_PATH="${2:-$(pwd)}"

if [[ -z "$PATTERN" ]]; then
  echo "Usage: $0 <pattern> [project_path]" >&2
  exit 1
fi

# Claude Code encodes paths: remove leading /, replace /. with -, prepend -
ENCODED_PATH=$(echo "$PROJECT_PATH" | sed 's|^/||' | tr '/.' '--')
ENCODED_PATH="-$ENCODED_PATH"
PROJECT_SESSIONS="$HOME/.claude/projects/$ENCODED_PATH"

if [[ ! -d "$PROJECT_SESSIONS" ]]; then
  echo "ERROR: No sessions found at $PROJECT_SESSIONS" >&2
  exit 1
fi

# Search all session files (optimized: skip sessions without matches)
for session in "$PROJECT_SESSIONS"/*.jsonl; do
  [[ -f "$session" ]] || continue

  # Skip sessions without any matches (fast grep -q check)
  grep -q "$PATTERN" "$session" 2>/dev/null || continue

  SESSION_ID=$(basename "$session" .jsonl)

  # Find matching line numbers, then extract those lines and parse
  grep -n "$PATTERN" "$session" 2>/dev/null | cut -d: -f1 | while read -r line_num; do
    # Extract the line by number and parse with jq
    line=$(sed -n "${line_num}p" "$session")

    # Parse and output as NDJSON
    echo "$line" | jq --compact-output \
      --arg session_id "$SESSION_ID" \
      --arg session_path "$session" \
      --argjson line_num "$line_num" \
      --arg pattern "$PATTERN" \
      '{
        session_id: $session_id,
        session_path: $session_path,
        line_number: $line_num,
        uuid: (.uuid // ""),
        timestamp: (.timestamp // ""),
        type: (.type // ""),
        matched_pattern: $pattern
      }' 2>/dev/null || true
  done
done
