#!/bin/bash
# cleanup-test-pr.sh - Tears down test PR and branch
# Usage: ./cleanup-test-pr.sh --pr=<number> --branch=<branch>

set -e

PR_NUMBER=""
BRANCH=""

for arg in "$@"; do
  case $arg in
    --pr=*) PR_NUMBER="${arg#*=}" ;;
    --branch=*) BRANCH="${arg#*=}" ;;
  esac
done

if [ -z "$PR_NUMBER" ] || [ -z "$BRANCH" ]; then
  echo "Usage: ./cleanup-test-pr.sh --pr=<number> --branch=<branch>" >&2
  exit 1
fi

echo "Closing PR #$PR_NUMBER..." >&2
gh pr close "$PR_NUMBER" --delete-branch 2>/dev/null || true

echo "Switching to main..." >&2
git checkout main 2>/dev/null || git checkout master

echo "Deleting local branch..." >&2
git branch -D "$BRANCH" 2>/dev/null || true

echo "Removing test fixture file if present..." >&2
rm -f test-fixture-file.ts

echo "Removing temp guide file..." >&2
rm -f .claude/tmp/test-resolve-review-guide.md
rmdir .claude/tmp 2>/dev/null || true

echo "Cleanup complete." >&2
