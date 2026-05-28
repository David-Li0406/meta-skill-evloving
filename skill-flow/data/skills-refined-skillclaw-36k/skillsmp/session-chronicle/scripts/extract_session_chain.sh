#!/usr/bin/env bash
# extract_session_chain.sh - Extract and archive FULL session chain for provenance
# Usage: ./extract_session_chain.sh <uuid_chain_file> <output_dir> [project_path]
#
# Archives ALL sessions in the UUID chain, not just a fixed window.
# Each session is compressed individually with a manifest.
# ADR: /docs/adr/2026-01-02-session-chronicle-s3-sharing.md (Brotli compression)

set -euo pipefail

CHAIN_FILE="${1:-}"
OUTPUT_DIR="${2:-}"
PROJECT_PATH="${3:-$(pwd)}"

if [[ -z "$CHAIN_FILE" || -z "$OUTPUT_DIR" ]]; then
  echo "Usage: $0 <uuid_chain_file> <output_dir> [project_path]" >&2
  echo "" >&2
  echo "Arguments:" >&2
  echo "  uuid_chain_file  NDJSON file from uuid_tracer.sh" >&2
  echo "  output_dir       Directory to store archived sessions" >&2
  echo "  project_path     Project path (default: current dir)" >&2
  exit 1
fi

if [[ ! -f "$CHAIN_FILE" ]]; then
  echo "ERROR: Chain file not found: $CHAIN_FILE" >&2
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

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Get unique session IDs from chain
SESSION_IDS=$(jq -r '.session_id' "$CHAIN_FILE" 2>/dev/null | sort -u)

if [[ -z "$SESSION_IDS" ]]; then
  echo "ERROR: No session IDs found in chain file" >&2
  exit 1
fi

echo "Extracting full session chain..."
echo "Chain file: $CHAIN_FILE"
echo "Output dir: $OUTPUT_DIR"
echo ""

TOTAL_SESSIONS=0
TOTAL_LINES=0
TOTAL_BYTES=0

# Archive each session in the chain
for session_id in $SESSION_IDS; do
  SESSION_PATH="$PROJECT_SESSIONS/${session_id}.jsonl"

  if [[ -f "$SESSION_PATH" ]]; then
    # Get session stats
    LINE_COUNT=$(wc -l < "$SESSION_PATH" | tr -d ' ')
    FILE_SIZE=$(stat -f%z "$SESSION_PATH" 2>/dev/null || stat -c%s "$SESSION_PATH" 2>/dev/null)

    # Compress full session with Brotli (level 9 for best compression)
    brotli -9 -o "$OUTPUT_DIR/${session_id}.jsonl.br" "$SESSION_PATH"
    COMPRESSED_SIZE=$(stat -f%z "$OUTPUT_DIR/${session_id}.jsonl.br" 2>/dev/null || stat -c%s "$OUTPUT_DIR/${session_id}.jsonl.br" 2>/dev/null)

    echo "  Archived: $session_id"
    echo "    Lines: $LINE_COUNT"
    echo "    Original: $(numfmt --to=iec $FILE_SIZE 2>/dev/null || echo "${FILE_SIZE}B")"
    echo "    Compressed: $(numfmt --to=iec $COMPRESSED_SIZE 2>/dev/null || echo "${COMPRESSED_SIZE}B")"

    ((TOTAL_SESSIONS++))
    ((TOTAL_LINES += LINE_COUNT))
    ((TOTAL_BYTES += COMPRESSED_SIZE))
  else
    echo "  WARNING: Session not found: $session_id" >&2
  fi
done

# Copy the chain file
cp "$CHAIN_FILE" "$OUTPUT_DIR/uuid_chain.jsonl"

# Get chain metadata
CHAIN_DEPTH=$(wc -l < "$CHAIN_FILE" | tr -d ' ')
FIRST_TS=$(head -1 "$CHAIN_FILE" | jq -r '.timestamp // "unknown"')
LAST_TS=$(tail -1 "$CHAIN_FILE" | jq -r '.timestamp // "unknown"')

# Create manifest
jq -n \
  --argjson total_sessions "$TOTAL_SESSIONS" \
  --argjson total_lines "$TOTAL_LINES" \
  --argjson total_bytes "$TOTAL_BYTES" \
  --argjson chain_depth "$CHAIN_DEPTH" \
  --arg first_timestamp "$FIRST_TS" \
  --arg last_timestamp "$LAST_TS" \
  --arg project_path "$PROJECT_PATH" \
  --arg created_at "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
  '{
    total_sessions: $total_sessions,
    total_lines: $total_lines,
    total_bytes_compressed: $total_bytes,
    chain_depth: $chain_depth,
    first_timestamp: $first_timestamp,
    last_timestamp: $last_timestamp,
    project_path: $project_path,
    created_at: $created_at,
    note: "Full session chain - not limited to fixed entry count",
    compression: "brotli-9"
  }' > "$OUTPUT_DIR/manifest.json"

echo ""
echo "Session chain archived:"
echo "  Sessions: $TOTAL_SESSIONS"
echo "  Total lines: $TOTAL_LINES"
echo "  Chain depth: $CHAIN_DEPTH UUIDs"
echo "  Compressed size: $(numfmt --to=iec $TOTAL_BYTES 2>/dev/null || echo "${TOTAL_BYTES}B")"
echo "  Output: $OUTPUT_DIR"
