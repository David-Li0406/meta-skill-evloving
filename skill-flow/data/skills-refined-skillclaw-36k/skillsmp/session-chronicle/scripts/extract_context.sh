#!/usr/bin/env bash
# extract_context.sh - Extract and compress session context around a target
# Usage: ./extract_context.sh <session_file> <line_number> <output_file> [context_before] [context_after]
#
# Extracts lines around target and compresses to .jsonl.gz

set -euo pipefail

SESSION_FILE="${1:-}"
LINE_NUMBER="${2:-}"
OUTPUT_FILE="${3:-}"
CONTEXT_BEFORE="${4:-100}"
CONTEXT_AFTER="${5:-10}"

if [[ -z "$SESSION_FILE" || -z "$LINE_NUMBER" || -z "$OUTPUT_FILE" ]]; then
  echo "Usage: $0 <session_file> <line_number> <output_file> [context_before] [context_after]" >&2
  exit 1
fi

if [[ ! -f "$SESSION_FILE" ]]; then
  echo "ERROR: Session file not found: $SESSION_FILE" >&2
  exit 1
fi

TOTAL_LINES=$(wc -l < "$SESSION_FILE" | tr -d ' ')
START_LINE=$((LINE_NUMBER - CONTEXT_BEFORE))
END_LINE=$((LINE_NUMBER + CONTEXT_AFTER))

# Clamp to valid range
[[ $START_LINE -lt 1 ]] && START_LINE=1
[[ $END_LINE -gt $TOTAL_LINES ]] && END_LINE=$TOTAL_LINES

EXTRACT_COUNT=$((END_LINE - START_LINE + 1))

# Create output directory if needed
mkdir -p "$(dirname "$OUTPUT_FILE")"

# Extract context
sed -n "${START_LINE},${END_LINE}p" "$SESSION_FILE" > "${OUTPUT_FILE%.gz}"

# Compress
gzip -f "${OUTPUT_FILE%.gz}"

echo "Extracted $EXTRACT_COUNT lines (${START_LINE}-${END_LINE}) to ${OUTPUT_FILE}"
echo "Target line: $LINE_NUMBER"
echo "File size: $(stat -f%z "${OUTPUT_FILE}" 2>/dev/null || stat -c%s "${OUTPUT_FILE}" 2>/dev/null) bytes"
