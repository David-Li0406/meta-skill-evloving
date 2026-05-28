#!/usr/bin/env bash
# validate-prerequisites.sh - Check required tool installation
# ADR: /docs/adr/2026-01-02-session-chronicle-s3-sharing.md

set -euo pipefail

echo "=== Prerequisites Validation ==="

# Check brotli
if command -v brotli &>/dev/null; then
  BROTLI_VERSION=$(brotli --version 2>&1 | head -1)
  echo "✓ brotli: $BROTLI_VERSION"
else
  echo "✗ brotli: NOT INSTALLED"
  exit 1
fi

# Check aws
if command -v aws &>/dev/null; then
  AWS_VERSION=$(aws --version 2>&1)
  echo "✓ aws: $AWS_VERSION"
else
  echo "✗ aws: NOT INSTALLED"
  exit 1
fi

# Check op (1Password CLI)
if command -v op &>/dev/null; then
  OP_VERSION=$(op --version 2>&1)
  echo "✓ op: $OP_VERSION"
else
  echo "✗ op: NOT INSTALLED"
  exit 1
fi

# Check jq
if command -v jq &>/dev/null; then
  JQ_VERSION=$(jq --version 2>&1)
  echo "✓ jq: $JQ_VERSION"
else
  echo "✗ jq: NOT INSTALLED"
  exit 1
fi

echo ""
echo "All prerequisites satisfied"
