#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   scripts/review-diff.sh main..HEAD
RANGE="${1:-}"
if [ -z "$RANGE" ]; then
  echo "Provide a git range, e.g. main..HEAD"
  exit 2
fi

git diff --unified=0 "$RANGE"
