#!/usr/bin/env bash
set -euo pipefail

# create-worktree.sh - Creates a git worktree in .worktrees directory
# Usage: create-worktree.sh <branch-name>
#
# Arguments:
#   branch-name: Name of the branch to create/checkout

BRANCH_NAME="${1:-}"

if [[ -z "$BRANCH_NAME" ]]; then
  echo "Error: Branch name required" >&2
  echo "Usage: $0 <branch-name>" >&2
  exit 1
fi

REPO_ROOT=$(git rev-parse --show-toplevel)
WORKTREE_DIR="$REPO_ROOT/.worktrees"
WORKTREE_PATH="$WORKTREE_DIR/$BRANCH_NAME"

# Verify .worktrees is in .gitignore
if ! git check-ignore -q "$WORKTREE_DIR" 2>/dev/null; then
  echo "Warning: .worktrees is not in .gitignore" >&2
  echo "Adding .worktrees/ to .gitignore..." >&2
  echo ".worktrees/" >> "$REPO_ROOT/.gitignore"
  git add "$REPO_ROOT/.gitignore"
  git commit -m "chore: add .worktrees/ to .gitignore"
  echo "Committed .gitignore update" >&2
fi

# Check if branch exists
if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
  # Branch exists, checkout to it
  git worktree add "$WORKTREE_PATH" "$BRANCH_NAME"
else
  # Branch doesn't exist, create it
  git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME"
fi

# Output the path for the caller
echo "$WORKTREE_PATH"
