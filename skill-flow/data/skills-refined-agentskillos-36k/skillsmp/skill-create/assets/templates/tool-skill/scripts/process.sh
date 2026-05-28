#!/usr/bin/env bash
set -euo pipefail

# Example deterministic helper for tool skills.
# Usage: ./process.sh <input> <output>

if [ $# -lt 2 ]; then
  echo "Usage: $(basename "$0") <input> <output>" >&2
  exit 1
fi

input="$1"
output="$2"

echo "[tool] processing $input -> $output"

# TODO: replace with real processing commands
# cat "$input" > "$output"
