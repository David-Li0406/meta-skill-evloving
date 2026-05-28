#!/bin/bash
# config.json構文検証スクリプト

CONFIG_FILE="scripts/generate/config.json"

echo "Validating config.json..."

# JSON構文チェック
if ! jq empty "$CONFIG_FILE" 2>/dev/null; then
  echo "ERROR: Invalid JSON syntax in $CONFIG_FILE"
  exit 1
fi

echo "✓ config.json is valid"
exit 0
