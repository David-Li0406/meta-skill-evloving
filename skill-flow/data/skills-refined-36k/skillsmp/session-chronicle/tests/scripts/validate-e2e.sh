#!/usr/bin/env bash
# validate-e2e.sh - End-to-end integration validation
# ADR: /docs/adr/2026-01-02-session-chronicle-s3-sharing.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== End-to-End Integration Validation ==="
echo ""

VALIDATIONS=(
  "validate-prerequisites.sh"
  "validate-brotli.sh"
  "validate-credential-access.sh"
  "validate-s3-upload.sh"
  "validate-extract-chain.sh"
  "validate-commit-format.sh"
  "validate-cross-references.sh"
)

PASSED=0
FAILED=0
SKIPPED=0

for script in "${VALIDATIONS[@]}"; do
  echo "--- Running: $script ---"
  if [[ -f "$SCRIPT_DIR/$script" ]]; then
    if bash "$SCRIPT_DIR/$script"; then
      echo "PASSED"
      ((PASSED++)) || true
    else
      echo "FAILED"
      ((FAILED++)) || true
    fi
  else
    echo "SKIPPED (not found)"
    ((SKIPPED++)) || true
  fi
  echo ""
done

echo "=========================================="
echo "End-to-End Validation Summary:"
echo "  PASSED:  $PASSED"
echo "  FAILED:  $FAILED"
echo "  SKIPPED: $SKIPPED"
echo "=========================================="

if [[ $FAILED -gt 0 ]]; then
  exit 1
fi

echo ""
echo "ALL VALIDATIONS PASSED"
