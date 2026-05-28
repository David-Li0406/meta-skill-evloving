#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: search.sh <cached_file> <query...>" >&2
  exit 2
fi

file="$1"
shift
query="$*"

if [[ ! -f "$file" ]]; then
  echo "error: file not found: $file" >&2
  exit 2
fi

if command -v rg >/dev/null 2>&1; then
  rg -n --context 3 --no-heading --smart-case "$query" "$file" | head -n 80
else
  grep -n -C 3 -i -- "$query" "$file" | head -n 80
fi

