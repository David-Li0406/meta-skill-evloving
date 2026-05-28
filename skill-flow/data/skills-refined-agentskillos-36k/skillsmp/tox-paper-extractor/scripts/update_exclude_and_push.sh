#!/usr/bin/env bash
set -euo pipefail

# Update shared exclude list from one or more new ID files, then commit + push.
# Usage:
#   ./scripts/update_exclude_and_push.sh --exclude analysis/exclude_ids.txt --new path/to/paper_ids_part_01.txt [--new ...]
#
# Notes:
# - Lines that are blank or start with # are ignored.
# - Output is sorted and de-duplicated.

EXCLUDE=""
NEW_FILES=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --exclude)
      EXCLUDE="$2"
      shift 2
      ;;
    --new)
      NEW_FILES+=("$2")
      shift 2
      ;;
    -h|--help)
      grep '^#' "$0" | sed 's/^# //'
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      exit 1
      ;;
  esac
 done

if [[ -z "$EXCLUDE" ]]; then
  echo "--exclude is required" >&2
  exit 1
fi
if [[ ${#NEW_FILES[@]} -eq 0 ]]; then
  echo "At least one --new file is required" >&2
  exit 1
fi

if [[ ! -f "$EXCLUDE" ]]; then
  echo "Exclude file not found: $EXCLUDE" >&2
  exit 1
fi

TMP_OUT="${EXCLUDE}.tmp"

{
  cat "$EXCLUDE"
  for f in "${NEW_FILES[@]}"; do
    if [[ -f "$f" ]]; then
      cat "$f"
    else
      echo "Warning: missing new file: $f" >&2
    fi
  done
} | sed -e 's/[[:space:]]*$//' -e '/^#/d' -e '/^$/d' | sort -u > "$TMP_OUT"

mv "$TMP_OUT" "$EXCLUDE"

# Commit + push.
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

git add "$EXCLUDE"
if git diff --cached --quiet; then
  echo "No changes to commit."
  exit 0
fi

git commit -m "Update shared exclude_ids"
git push origin HEAD
