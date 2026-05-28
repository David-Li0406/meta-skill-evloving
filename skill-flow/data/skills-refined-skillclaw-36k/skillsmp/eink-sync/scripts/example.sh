#!/usr/bin/env bash
set -euo pipefail

# Example helper for workflow skills. Replace with commands you run every time.
# Usage: ./example.sh <context>

if [ "${1-}" = "" ]; then
  echo "Usage: $(basename "$0") <context>" >&2
  exit 1
fi

context="$1"
echo "[workflow] running standard checks for: $context"

echo "- TODO: add commands (lint, tests, deployments)"
# e.g., npm run lint && npm run test
