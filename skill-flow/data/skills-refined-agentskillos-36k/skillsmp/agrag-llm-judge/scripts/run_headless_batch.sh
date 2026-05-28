#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 3 ]; then
  echo "Usage: run_headless_batch.sh <thread_id> <prompts_file> <output_file> [output_format]"
  exit 1
fi

thread_id="$1"
prompts_file="$2"
output_file="$3"
output_format="${4:-json}"

if [ ! -f "$prompts_file" ]; then
  echo "Prompts file not found: $prompts_file"
  exit 1
fi

: > "$output_file"

while IFS= read -r line || [ -n "$line" ]; do
  prompt="$line"
  if [ -z "$prompt" ]; then
    continue
  fi
  case "$prompt" in
    \#*) continue ;;
  esac

  python - <<'PY' "$prompt" >> "$output_file"
import json
import sys
print(json.dumps({"type": "prompt", "content": sys.argv[1]}))
PY

  poetry run agrag -p "$prompt" --thread-id "$thread_id" --output-format "$output_format" >> "$output_file"
  printf '\n' >> "$output_file"
done < "$prompts_file"
