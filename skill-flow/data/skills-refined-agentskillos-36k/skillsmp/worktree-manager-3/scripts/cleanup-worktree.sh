#!/usr/bin/env bash
# Cleanup alpha-forge worktree and optionally delete merged branch
# ADR: /docs/adr/2025-12-14-alpha-forge-worktree-management.md
#
# Usage: cleanup-worktree.sh <worktree-path> [--delete-branch]
# Example: cleanup-worktree.sh ~/eon/alpha-forge.worktree-2025-12-14-feature-name
# Example: cleanup-worktree.sh ~/eon/alpha-forge.worktree-2025-12-14-feature-name --delete-branch

set -euo pipefail

WORKTREE_PATH="${1:-}"
DELETE_BRANCH="${2:-}"

# Dynamic worktree detection (ADR: 2025-12-29-ralph-constraint-scanning.md)
# Uses git rev-parse --git-common-dir instead of hardcoded path
detect_alpha_forge_root() {
    local git_common_dir
    git_common_dir=$(git rev-parse --git-common-dir 2>/dev/null || echo "")

    if [[ -z "$git_common_dir" ]]; then
        echo ""
        return
    fi

    if [[ "$git_common_dir" == ".git" ]]; then
        # Main worktree - we're in the repo root
        pwd
    else
        # Linked worktree - git-common-dir points to main's .git
        dirname "$git_common_dir"
    fi
}

AF_ROOT="${AF_ROOT:-$(detect_alpha_forge_root)}"

# Fallback to legacy path if detection fails
if [[ -z "$AF_ROOT" ]]; then
    AF_ROOT="$HOME/eon/alpha-forge"
fi

# Validate input
if [[ -z "$WORKTREE_PATH" ]]; then
    echo "Usage: cleanup-worktree.sh <worktree-path> [--delete-branch]" >&2
    echo "Example: cleanup-worktree.sh ~/eon/alpha-forge.worktree-2025-12-14-feature-name" >&2
    exit 1
fi

# Expand path
WORKTREE_PATH=$(eval echo "$WORKTREE_PATH")

# Validate alpha-forge repo exists
if [[ ! -d "$AF_ROOT/.git" ]]; then
    echo "Error: alpha-forge repo not found at $AF_ROOT" >&2
    exit 1
fi

cd "$AF_ROOT"

# Validate worktree exists
if ! git worktree list | grep -q "^${WORKTREE_PATH} "; then
    echo "Error: '$WORKTREE_PATH' is not a valid worktree" >&2
    echo "" >&2
    echo "Current worktrees:" >&2
    git worktree list >&2
    exit 1
fi

# Get branch name for this worktree
BRANCH=$(git worktree list | grep "^${WORKTREE_PATH} " | sed 's/.*\[\(.*\)\].*/\1/' || true)

if [[ -z "$BRANCH" ]]; then
    echo "Warning: Could not determine branch for worktree" >&2
    BRANCH="(unknown)"
fi

# Extract slug for tab name
SLUG=$(basename "$WORKTREE_PATH" | sed 's/alpha-forge\.worktree-[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}-//')
ACRONYM=$(echo "$SLUG" | tr '-' '\n' | cut -c1 | tr -d '\n' | tr '[:upper:]' '[:lower:]')

echo "Removing worktree..."
echo "  Path:   $WORKTREE_PATH"
echo "  Branch: $BRANCH"
echo "  Tab:    AF-${ACRONYM}"
echo ""

# Remove worktree
git worktree remove "$WORKTREE_PATH"

echo "✓ Worktree removed"

# Optionally delete branch
if [[ "$DELETE_BRANCH" == "--delete-branch" && "$BRANCH" != "(unknown)" ]]; then
    echo ""
    echo "Deleting branch '$BRANCH'..."

    # Check if branch is merged (safe delete with -d)
    if git branch -d "$BRANCH" 2>/dev/null; then
        echo "✓ Branch deleted (was merged)"
    else
        echo "Warning: Branch not fully merged. Use 'git branch -D $BRANCH' to force delete." >&2
    fi
fi

# Prune any orphaned worktree entries
git worktree prune 2>/dev/null || true

echo ""
echo "Done. Restart iTerm2 to update tab layout."
