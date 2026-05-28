#!/bin/bash
# Remove worktree with submodule handling
# Usage: wt-remove.sh <branch-name> [base-dir]
#
# Arguments:
#   branch-name: Name of the branch/worktree to remove
#   base-dir: Optional repo root (defaults to git root)

set -e

BRANCH="${1:?Usage: wt-remove.sh <branch-name> [base-dir]}"
BASE_DIR="${2:-$(git rev-parse --show-toplevel)}"
WT_BASE="${BASE_DIR}-wt"
WORKTREE_PATH="$WT_BASE/$BRANCH"

echo "Removing worktree: $BRANCH"
echo "  Path: $WORKTREE_PATH"

# Clean up any stale lock files first
echo "  Cleaning lock files..."
find "$BASE_DIR/.git/modules" -name "*.lock" -delete 2>/dev/null || true
find "$BASE_DIR/.git" -maxdepth 1 -name "*.lock" -delete 2>/dev/null || true

# Check if worktree exists in git
if git -C "$BASE_DIR" worktree list | grep -q "$WORKTREE_PATH"; then
    echo "  Removing worktree (force mode for submodules)..."
    git -C "$BASE_DIR" worktree remove --force "$WORKTREE_PATH" 2>/dev/null || {
        echo "  Git remove failed, cleaning manually..."
        rm -rf "$WORKTREE_PATH"
    }
else
    echo "  Worktree not in git list"
    if [ -d "$WORKTREE_PATH" ]; then
        echo "  Directory exists, removing..."
        rm -rf "$WORKTREE_PATH"
    fi
fi

# Prune worktree references
git -C "$BASE_DIR" worktree prune

# Remove branch if it exists
if git -C "$BASE_DIR" show-ref --verify --quiet "refs/heads/$BRANCH"; then
    echo "  Deleting branch..."
    git -C "$BASE_DIR" branch -D "$BRANCH" 2>/dev/null || echo "  Branch deletion skipped"
fi

echo ""
echo "✅ Worktree $BRANCH removed"
echo ""
echo "Remaining worktrees:"
git -C "$BASE_DIR" worktree list
