#!/bin/bash
# team-progress.sh - Query progress from all remote branches
# Usage: ./team-progress.sh [--detail]

set -e

DETAIL=false
if [ "$1" = "--detail" ]; then
  DETAIL=true
fi

# Fetch all remote branches
git fetch --all --quiet 2>/dev/null

echo "# Team Progress Summary ($(date +%Y-%m-%d))"
echo ""

if [ "$DETAIL" = true ]; then
  # Detailed view: show full progress log for each branch
  for branch in $(git branch -r | grep -v HEAD | grep -v '/main$' | grep -v '/master$'); do
    progress=$(git show "$branch:BRANCH_PROGRESS.md" 2>/dev/null || true)
    if [ -n "$progress" ]; then
      echo "---"
      echo "## $branch"
      echo ""
      echo "$progress"
      echo ""
    fi
  done
else
  # Summary table view
  echo "| Branch | Task | Owner | Status |"
  echo "|--------|------|-------|--------|"

  for branch in $(git branch -r | grep -v HEAD | grep -v '/main$' | grep -v '/master$'); do
    progress=$(git show "$branch:BRANCH_PROGRESS.md" 2>/dev/null || true)
    if [ -n "$progress" ]; then
      task=$(echo "$progress" | grep -E "^\*\*Task ID\*\*:" | cut -d: -f2 | xargs || echo "-")
      owner=$(echo "$progress" | grep -E "^\*\*Owner\*\*:" | cut -d: -f2 | xargs || echo "-")
      status=$(echo "$progress" | grep -E "^\*\*Status\*\*:" | cut -d: -f2 | xargs || echo "-")
      branch_short=$(echo "$branch" | sed 's|origin/||')
      echo "| $branch_short | $task | $owner | $status |"
    fi
  done
fi

echo ""
echo "_Generated at $(date '+%Y-%m-%d %H:%M:%S')_"
