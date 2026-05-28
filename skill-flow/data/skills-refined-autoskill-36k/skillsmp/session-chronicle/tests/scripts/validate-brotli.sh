#!/usr/bin/env bash
# validate-brotli.sh - Brotli compression round-trip test
# ADR: /docs/adr/2026-01-02-session-chronicle-s3-sharing.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FIXTURE_DIR="$SCRIPT_DIR/../fixtures"
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

echo "=== Brotli Compression Validation ==="

# Create test data
echo '{"uuid":"test-1","type":"user","message":"Hello"}' > "$TEMP_DIR/test.jsonl"
echo '{"uuid":"test-2","type":"assistant","message":"World"}' >> "$TEMP_DIR/test.jsonl"

# Compress with brotli level 9
brotli -9 -o "$TEMP_DIR/test.jsonl.br" "$TEMP_DIR/test.jsonl"

# Verify compression ratio
ORIG_SIZE=$(stat -f%z "$TEMP_DIR/test.jsonl" 2>/dev/null || stat -c%s "$TEMP_DIR/test.jsonl")
COMP_SIZE=$(stat -f%z "$TEMP_DIR/test.jsonl.br" 2>/dev/null || stat -c%s "$TEMP_DIR/test.jsonl.br")
RATIO=$(echo "scale=2; $ORIG_SIZE / $COMP_SIZE" | bc 2>/dev/null || echo "N/A")
echo "✓ Compression ratio: ${RATIO}x ($ORIG_SIZE → $COMP_SIZE bytes)"

# Decompress and verify integrity
brotli -d -o "$TEMP_DIR/test-restored.jsonl" "$TEMP_DIR/test.jsonl.br"
if diff -q "$TEMP_DIR/test.jsonl" "$TEMP_DIR/test-restored.jsonl" >/dev/null; then
  echo "✓ Round-trip integrity verified"
else
  echo "✗ Round-trip integrity FAILED"
  exit 1
fi

# Test with mock session fixture
if [[ -f "$FIXTURE_DIR/mock-session.jsonl" ]]; then
  brotli -9 -o "$TEMP_DIR/mock-session.jsonl.br" "$FIXTURE_DIR/mock-session.jsonl"
  brotli -d -o "$TEMP_DIR/mock-session-restored.jsonl" "$TEMP_DIR/mock-session.jsonl.br"
  if diff -q "$FIXTURE_DIR/mock-session.jsonl" "$TEMP_DIR/mock-session-restored.jsonl" >/dev/null; then
    echo "✓ Mock session fixture round-trip verified"
  else
    echo "✗ Mock session fixture round-trip FAILED"
    exit 1
  fi
fi

echo ""
echo "Brotli compression validation PASSED"
