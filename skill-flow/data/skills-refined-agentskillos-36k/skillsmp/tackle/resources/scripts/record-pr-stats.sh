#!/usr/bin/env bash
# record-pr-stats.sh - Calculate diff stats and update issue with PR info
#
# Usage: source record-pr-stats.sh
#
# Inputs (required):
#   ISSUE_ID     - The local issue bead ID to update
#   PR_URL       - The PR URL
#   UPSTREAM_REF - The upstream ref to diff against (e.g., "upstream/main")
#
# Outputs (exported variables):
#   FILES_CHANGED - Number of files changed
#   LINES_CHANGED - Total lines changed (insertions + deletions)
#
# Side effects:
#   - Adds pr-submitted label to issue
#   - Sets issue status to deferred
#   - Updates issue notes with PR info

set -euo pipefail

# Verify required variables are set
if [ -z "${ISSUE_ID:-}" ]; then
  echo "ERROR: ISSUE_ID must be set before sourcing record-pr-stats.sh"
  exit 1
fi
if [ -z "${PR_URL:-}" ]; then
  echo "ERROR: PR_URL must be set before sourcing record-pr-stats.sh"
  exit 1
fi
if [ -z "${UPSTREAM_REF:-}" ]; then
  echo "ERROR: UPSTREAM_REF must be set before sourcing record-pr-stats.sh"
  exit 1
fi

# Count changed files and lines
DIFF_STAT=$(git diff --stat "$UPSTREAM_REF" | tail -1)
FILES_CHANGED=$(echo "$DIFF_STAT" | grep -oE '[0-9]+ file' | grep -oE '[0-9]+' || echo "0")

# Sum insertions and deletions using shell arithmetic (avoids bc/paste dependency)
INSERTIONS=$(echo "$DIFF_STAT" | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+' || echo "0")
DELETIONS=$(echo "$DIFF_STAT" | grep -oE '[0-9]+ deletion' | grep -oE '[0-9]+' || echo "0")
LINES_CHANGED=$((${INSERTIONS:-0} + ${DELETIONS:-0}))

# Update issue with PR info
bd update "$ISSUE_ID" \
  --add-label pr-submitted \
  --status=deferred \
  --notes="PR: $PR_URL
files: $FILES_CHANGED
lines: ~$LINES_CHANGED
submitted: $(date -Iseconds)"

echo "Updated $ISSUE_ID: $FILES_CHANGED files, ~$LINES_CHANGED lines"

# Export variables for use by calling script
export FILES_CHANGED LINES_CHANGED
