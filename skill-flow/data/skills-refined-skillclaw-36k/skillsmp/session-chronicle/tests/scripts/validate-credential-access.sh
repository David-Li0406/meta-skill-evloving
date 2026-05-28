#!/usr/bin/env bash
# validate-credential-access.sh - 1Password credential access test
# ADR: /docs/adr/2026-01-02-session-chronicle-s3-sharing.md

set -euo pipefail

echo "=== 1Password Credential Access Validation ==="

OP_VAULT="Employee"
OP_ITEM_ID="ise47dxnkftmxopupffavsgby4"

# Check 1Password CLI is available
if ! command -v op &>/dev/null; then
  echo "✗ 1Password CLI: NOT INSTALLED"
  echo "  Run: brew install 1password-cli"
  exit 1
fi

# Check 1Password account is configured
# Note: op whoami doesn't work with biometric desktop app integration
# Use op account get instead to check account configuration
if ! op account get &>/dev/null; then
  echo "✗ 1Password: NO ACCOUNT CONFIGURED"
  echo "  Run: op account add"
  exit 1
fi
echo "✓ 1Password: Account configured"

# Check vault access with retry for biometric auth timing
# Biometric auth can have a slight delay before vault access is available
VAULT_RETRIES=3
VAULT_FOUND=false
for i in $(seq 1 $VAULT_RETRIES); do
  if op vault list 2>/dev/null | grep -q "$OP_VAULT"; then
    VAULT_FOUND=true
    break
  fi
  [[ $i -lt $VAULT_RETRIES ]] && sleep 1
done

if $VAULT_FOUND; then
  echo "✓ $OP_VAULT vault: Accessible"
else
  echo "✗ $OP_VAULT vault: NOT ACCESSIBLE"
  echo "  Ensure you have access to the $OP_VAULT vault in 1Password"
  exit 1
fi

# Check specific item access
ACCESS_KEY=$(op read "op://$OP_VAULT/$OP_ITEM_ID/access key id" 2>&1)
if [[ "$ACCESS_KEY" == AKIA* ]]; then
  echo "✓ AWS Access Key ID: Retrieved (${ACCESS_KEY:0:8}...)"
else
  echo "✗ AWS Access Key ID: FAILED"
  echo "  Error: $ACCESS_KEY"
  exit 1
fi

SECRET_KEY=$(op read "op://$OP_VAULT/$OP_ITEM_ID/secret access key" 2>&1)
if [[ ${#SECRET_KEY} -gt 20 ]]; then
  echo "✓ AWS Secret Access Key: Retrieved (${#SECRET_KEY} chars)"
else
  echo "✗ AWS Secret Access Key: FAILED"
  exit 1
fi

echo ""
echo "1Password credential access validation PASSED"
