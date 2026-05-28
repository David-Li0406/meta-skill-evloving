#!/usr/bin/env bash

set -euo pipefail

title=""
body=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --title)
      title="$2"
      shift 2
      ;;
    --body)
      body="$2"
      shift 2
      ;;
    *)
      echo "Error: Unknown argument $1" >&2
      exit 1
      ;;
  esac
done

# Check if title is provided
if [[ -z "$title" ]]; then
  echo "Error: --title is required" >&2
  exit 1
fi

# Check title length
if [[ ${#title} -gt 72 ]]; then
  echo "Error: Title is ${#title} characters (max 72)" >&2
  exit 1
fi

# Print title
echo "$title"

# Format and print body if present
if [[ -n "$body" ]]; then
  echo
  echo "$body" | npx prettier --parser markdown --prose-wrap always --print-width 72
fi
