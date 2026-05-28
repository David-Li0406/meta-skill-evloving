#!/usr/bin/env bash
# validate-extract-chain.sh - Script modification check
# ADR: /docs/adr/2026-01-02-session-chronicle-s3-sharing.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FIXTURE_DIR="$SCRIPT_DIR/../fixtures"
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

echo "=== Extract Session Chain Validation ==="

# Check if extract script exists
EXTRACT_SCRIPT="$SCRIPT_DIR/../../scripts/extract_session_chain.sh"
if [[ ! -f "$EXTRACT_SCRIPT" ]]; then
  echo "✗ extract_session_chain.sh: NOT FOUND at $EXTRACT_SCRIPT"
  exit 1
fi
echo "✓ extract_session_chain.sh: Found"

# Check if script uses brotli (not gzip)
if grep -q "brotli" "$EXTRACT_SCRIPT"; then
  echo "✓ Compression: Uses brotli"
else
  if grep -q "gzip" "$EXTRACT_SCRIPT"; then
    echo "✗ Compression: Still uses gzip (should be brotli)"
    exit 1
  else
    echo "? Compression: Could not detect compression tool"
  fi
fi

# Check file extension in script
if grep -q "\.jsonl\.br" "$EXTRACT_SCRIPT"; then
  echo "✓ File extension: .jsonl.br"
else
  if grep -q "\.jsonl\.gz" "$EXTRACT_SCRIPT"; then
    echo "✗ File extension: Still .jsonl.gz (should be .jsonl.br)"
    exit 1
  else
    echo "? File extension: Could not detect extension"
  fi
fi

# Check for ADR reference
if grep -q "2026-01-02-session-chronicle-s3-sharing" "$EXTRACT_SCRIPT"; then
  echo "✓ ADR reference: Found in script"
else
  echo "✗ ADR reference: Missing"
  exit 1
fi

echo ""
echo "Extract session chain validation PASSED"
