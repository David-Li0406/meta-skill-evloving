#!/usr/bin/env bash
# Gathers review context into .local/tmp/
# Usage: gather-context.sh <project_root> [tasks_md] [prd_summary_md]
# Outputs: paths to created files (one per line)

set -euo pipefail

PROJECT_ROOT="${1:?Usage: gather-context.sh <project_root> [tasks_md] [prd_summary_md]}"
TASKS_MD="${2:-}"
PRD_SUMMARY="${3:-}"

TMP_DIR="$PROJECT_ROOT/.local/tmp"
mkdir -p "$TMP_DIR"

# Track all created files
CREATED_FILES=()
CONTEXT_FILE="$TMP_DIR/review-context-$$.md"
CREATED_FILES+=("$CONTEXT_FILE")

{
  echo "# Review Context"
  echo
  echo "## Completed Tasks"
  echo
  if [[ -n "$TASKS_MD" ]]; then
    echo "$TASKS_MD"
  else
    echo "_No tasks provided_"
  fi
  echo
  echo "## Code Changes"
  echo

  # Determine base branch
  BASE_BRANCH=""
  CURRENT_BRANCH=$(git -C "$PROJECT_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null)

  # Try: remote default branch (most reliable)
  if [[ -z "$BASE_BRANCH" ]]; then
    BASE_BRANCH=$(git -C "$PROJECT_ROOT" symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
  fi

  # Try: find merge-base with common defaults
  if [[ -z "$BASE_BRANCH" ]]; then
    for candidate in main master develop; do
      if git -C "$PROJECT_ROOT" rev-parse --verify "$candidate" >/dev/null 2>&1; then
        BASE_BRANCH="$candidate"
        break
      fi
    done
  fi

  # Try: first parent of current branch's root commit (feature branch base)
  if [[ -z "$BASE_BRANCH" && -n "$CURRENT_BRANCH" ]]; then
    # Get the merge-base between HEAD and all remote tracking branches
    for remote_branch in $(git -C "$PROJECT_ROOT" branch -r 2>/dev/null | grep -v HEAD | head -5); do
      if MERGE_BASE=$(git -C "$PROJECT_ROOT" merge-base HEAD "$remote_branch" 2>/dev/null); then
        BASE_BRANCH="$remote_branch"
        break
      fi
    done
  fi

  if [[ -n "$BASE_BRANCH" ]]; then
    echo "### Changed Files"
    echo '```'
    git -C "$PROJECT_ROOT" diff "$BASE_BRANCH" --stat 2>/dev/null || echo "_No diff available_"
    echo '```'
    echo
    DIFF_FILE="$TMP_DIR/review-diff-$$.diff"
    git -C "$PROJECT_ROOT" diff "$BASE_BRANCH" > "$DIFF_FILE" 2>/dev/null || echo "_No diff available_" > "$DIFF_FILE"
    CREATED_FILES+=("$DIFF_FILE")
    echo "### Diff Content"
    echo "Full diff available at: $DIFF_FILE"
    echo
    DIFF_LINES=$(wc -l < "$DIFF_FILE")
    echo "($DIFF_LINES lines)"
  else
    echo "_No base branch found for diff_"
  fi
  echo
  echo "## PRD Requirements"
  echo
  if [[ -n "$PRD_SUMMARY" ]]; then
    echo "$PRD_SUMMARY"
  else
    echo "_No PRD summary provided_"
  fi
} > "$CONTEXT_FILE"

# Output all created files
for f in "${CREATED_FILES[@]}"; do
  echo "$f"
done
