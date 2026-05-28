#!/usr/bin/env bash
# validate-commit-format.sh - Git commit message format check
# ADR: /docs/adr/2026-01-02-session-chronicle-s3-sharing.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Git Commit Message Format Validation ==="

# Check if generate script exists
GEN_SCRIPT="$SCRIPT_DIR/../../scripts/generate_commit_message.sh"
if [[ ! -f "$GEN_SCRIPT" ]]; then
  echo "✗ generate_commit_message.sh: NOT FOUND"
  exit 1
fi
echo "✓ generate_commit_message.sh: Found"

# Generate commit message with mock data
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Create mock manifest
cat > "$TEMP_DIR/manifest.json" << 'MANIFEST'
{
  "total_sessions": 2,
  "total_lines": 1500,
  "total_bytes_compressed": 50000,
  "chain_depth": 12,
  "first_timestamp": "2026-01-01T00:00:00Z",
  "last_timestamp": "2026-01-02T00:00:00Z",
  "project_path": "/test/project",
  "created_at": "2026-01-02T12:00:00Z",
  "s3_location": "s3://eonlabs-findings/sessions/test-123"
}
MANIFEST

# Run generate script
COMMIT_MSG=$(bash "$GEN_SCRIPT" "$TEMP_DIR" "Test provenance finding" 2>&1 || true)

# Validate required elements
VALIDATIONS=(
  "Session-Chronicle Provenance"
  "s3://eonlabs-findings"
  "sessions"
  "op read"
  "aws s3"
  "Session-Chronicle-S3:"
)

PASSED=0
FAILED=0

for pattern in "${VALIDATIONS[@]}"; do
  if echo "$COMMIT_MSG" | grep -q "$pattern"; then
    echo "✓ Contains: $pattern"
    ((PASSED++)) || true
  else
    echo "✗ Missing: $pattern"
    ((FAILED++)) || true
  fi
done

# Validate NO presigned URLs
if echo "$COMMIT_MSG" | grep -qi "presigned\|expires"; then
  echo "✗ Contains presigned URL reference (should not)"
  ((FAILED++)) || true
else
  echo "✓ No presigned URL references"
  ((PASSED++)) || true
fi

# Validate retrieval command is embedded
if echo "$COMMIT_MSG" | grep -q "op://Claude Automation"; then
  echo "✓ Contains 1Password retrieval pattern"
  ((PASSED++)) || true
else
  echo "✗ Missing 1Password retrieval pattern"
  ((FAILED++)) || true
fi

echo ""
if [[ $FAILED -eq 0 ]]; then
  echo "Git commit message format validation PASSED ($PASSED checks)"
else
  echo "Git commit message format validation FAILED ($FAILED failures, $PASSED passed)"
  exit 1
fi
