#!/usr/bin/env bash
set -euo pipefail

# cleanup-worktree.sh - Removes a git worktree and optionally its branch
# Usage: cleanup-worktree.sh <worktree-path> [--delete-branch]
#
# Arguments:
#   worktree-path: Path to the worktree to remove
#   --delete-branch: (optional) Also delete the associated branch

WORKTREE_PATH="${1:-}"
DELETE_BRANCH=false

if [[ -z "$WORKTREE_PATH" ]]; then
  echo "Error: Worktree path required" >&2
  echo "Usage: $0 <worktree-path> [--delete-branch]" >&2
  exit 1
fi

# Check for --delete-branch flag
if [[ "${2:-}" == "--delete-branch" ]]; then
  DELETE_BRANCH=true
fi

# Verify worktree exists
if ! git worktree list | grep -q "$WORKTREE_PATH"; then
  echo "Error: Worktree not found: $WORKTREE_PATH" >&2
  echo "Available worktrees:" >&2
  git worktree list >&2
  exit 1
fi

# Get the branch name associated with this worktree
BRANCH_NAME=$(git worktree list --porcelain | grep -A 2 "worktree $WORKTREE_PATH" | grep "branch" | sed 's/branch refs\/heads\///')

# Remove the worktree
echo "Removing worktree: $WORKTREE_PATH" >&2
git worktree remove "$WORKTREE_PATH"

# Delete branch if requested
if [[ "$DELETE_BRANCH" == "true" && -n "$BRANCH_NAME" ]]; then
  echo "Deleting branch: $BRANCH_NAME" >&2
  git branch -D "$BRANCH_NAME"
fi

echo "Cleanup complete" >&2
