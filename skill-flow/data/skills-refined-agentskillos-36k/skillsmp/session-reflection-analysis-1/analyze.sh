#!/usr/bin/env bash
set -euo pipefail

# Find project directory
PROJ_PATH=$(pwd | sed 's|^/||; s|/|-|g')
PROJECT_DIR="$HOME/.claude/projects/-${PROJ_PATH}"
OUTPUT="/tmp/session-summary.jsonl"

if [ ! -d "$PROJECT_DIR" ]; then
  echo "ERROR: No session folder found at $PROJECT_DIR"
  echo "Available projects:"
  ls ~/.claude/projects/
  exit 1
fi

# Check jq
if ! command -v jq &> /dev/null; then
  echo "ERROR: jq is required but not installed"
  echo "Install with: brew install jq (macOS) or apt install jq (Linux)"
  exit 1
fi

# Generate summary
echo "Processing sessions from: $PROJECT_DIR"
cat "$PROJECT_DIR"/*.jsonl 2>/dev/null | jq -c 'select(.type == "user" or .type == "assistant") | {type, ts: .timestamp, content: (if .message.content | type == "string" then .message.content[0:300] elif .message.content | type == "array" then [.message.content[] | if .type == "text" then {t: "text", v: .text[0:300]} elif .type == "tool_use" then {t: "tool", v: .name} elif .type == "tool_result" then {t: "result", len: (.content | length)} elif .type == "thinking" then empty else {t: .type} end] else null end)}' > "$OUTPUT" 2>/dev/null

echo "Summary generated: $(wc -l < "$OUTPUT") messages, $(wc -c < "$OUTPUT" | xargs) bytes"
echo "Summary saved to: $OUTPUT"
