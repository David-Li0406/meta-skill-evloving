#!/usr/bin/env bash
# uuid_tracer.sh - Trace UUID chain across Claude Code sessions
# Usage: ./uuid_tracer.sh <starting_uuid> [session_file] [project_path]
#
# Traces parentUuid links backwards to find origin, crossing session boundaries

set -euo pipefail

STARTING_UUID="${1:-}"
SESSION_FILE="${2:-}"
PROJECT_PATH="${3:-$(pwd)}"

if [[ -z "$STARTING_UUID" ]]; then
  echo "Usage: $0 <uuid> [session_file] [project_path]" >&2
  exit 1
fi

# Claude Code encodes paths: remove leading /, replace /. with -, prepend -
ENCODED_PATH=$(echo "$PROJECT_PATH" | sed 's|^/||' | tr '/.' '--')
ENCODED_PATH="-$ENCODED_PATH"
PROJECT_SESSIONS="$HOME/.claude/projects/$ENCODED_PATH"

# Output chain as NDJSON
trace_chain() {
  local uuid="$1"
  local current_session="${2:-}"
  local depth=0
  local max_depth=200
  local chain_file=$(mktemp)

  while [[ -n "$uuid" && "$uuid" != "null" && $depth -lt $max_depth ]]; do
    local found=false
    local entry=""

    # Try current session first
    if [[ -n "$current_session" && -f "$current_session" ]]; then
      entry=$(grep "\"uuid\":\"$uuid\"" "$current_session" 2>/dev/null | head -1 || true)
      if [[ -n "$entry" ]]; then
        found=true
      fi
    fi

    # Search other sessions if not found
    if [[ "$found" == "false" ]]; then
      for session in "$PROJECT_SESSIONS"/*.jsonl; do
        [[ -f "$session" ]] || continue
        [[ "$session" == "$current_session" ]] && continue

        entry=$(grep "\"uuid\":\"$uuid\"" "$session" 2>/dev/null | head -1 || true)
        if [[ -n "$entry" ]]; then
          current_session="$session"
          found=true
          break
        fi
      done
    fi

    if [[ "$found" == "false" ]]; then
      echo "Chain broken at UUID: $uuid (not found in any session)" >&2
      break
    fi

    # Extract metadata
    local parent_uuid=$(echo "$entry" | jq -r '.parentUuid // empty')
    local timestamp=$(echo "$entry" | jq -r '.timestamp // empty')
    local type=$(echo "$entry" | jq -r '.type // empty')
    local session_id=$(basename "$current_session" .jsonl)

    # Determine if this is a tool_use
    local tool_name=""
    tool_name=$(echo "$entry" | jq -r '.message.content[0].name // empty' 2>/dev/null || true)

    # Output chain entry
    jq -n --compact-output \
      --argjson depth "$depth" \
      --arg uuid "$uuid" \
      --arg parent_uuid "$parent_uuid" \
      --arg timestamp "$timestamp" \
      --arg type "$type" \
      --arg session_id "$session_id" \
      --arg tool_name "$tool_name" \
      '{
        depth: $depth,
        uuid: $uuid,
        parent_uuid: $parent_uuid,
        timestamp: $timestamp,
        type: $type,
        session_id: $session_id,
        tool_name: (if $tool_name == "" then null else $tool_name end)
      }' >> "$chain_file"

    uuid="$parent_uuid"
    ((depth++))
  done

  # Output complete chain
  cat "$chain_file"
  rm -f "$chain_file"

  echo "Chain depth: $depth" >&2
}

trace_chain "$STARTING_UUID" "$SESSION_FILE"
