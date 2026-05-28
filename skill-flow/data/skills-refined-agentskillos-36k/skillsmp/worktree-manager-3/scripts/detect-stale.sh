#!/usr/bin/env bash
# Detect stale (merged) worktrees in alpha-forge
# ADR: /docs/adr/2025-12-14-alpha-forge-worktree-management.md
#
# Usage: detect-stale.sh
# Output: List of stale worktrees (branch merged to main)

set -euo pipefail

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

# Validate alpha-forge repo exists
if [[ ! -d "$AF_ROOT/.git" ]]; then
    echo "Error: alpha-forge repo not found at $AF_ROOT" >&2
    exit 1
fi

cd "$AF_ROOT"

# Get branches merged to main (excluding main itself and current branch)
MERGED=$(git branch --merged main 2>/dev/null | grep -v '^\*' | grep -v 'main' | tr -d ' ' || true)

if [[ -z "$MERGED" ]]; then
    echo "No merged branches found."
    exit 0
fi

# Get worktree information
WORKTREES=$(git worktree list --porcelain 2>/dev/null || true)

if [[ -z "$WORKTREES" ]]; then
    echo "No worktrees found."
    exit 0
fi

# Track if we found any stale worktrees
FOUND_STALE=0

# Check each worktree
while IFS= read -r line; do
    if [[ "$line" =~ ^worktree\ (.+)$ ]]; then
        CURRENT_PATH="${BASH_REMATCH[1]}"
    elif [[ "$line" =~ ^branch\ refs/heads/(.+)$ ]]; then
        BRANCH_NAME="${BASH_REMATCH[1]}"

        # Skip if this is the main worktree
        if [[ "$CURRENT_PATH" == "$AF_ROOT" ]]; then
            continue
        fi

        # Check if branch is in merged list
        if echo "$MERGED" | grep -q "^${BRANCH_NAME}$"; then
            if [[ $FOUND_STALE -eq 0 ]]; then
                echo "Stale worktrees (branch merged to main):"
                echo ""
                FOUND_STALE=1
            fi

            # Extract slug and generate tab name for context
            SLUG=$(basename "$CURRENT_PATH" | sed 's/alpha-forge\.worktree-[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}-//')
            ACRONYM=$(echo "$SLUG" | tr '-' '\n' | cut -c1 | tr -d '\n' | tr '[:upper:]' '[:lower:]')

            echo "  STALE: $BRANCH_NAME"
            echo "    Path: $CURRENT_PATH"
            echo "    Tab:  AF-${ACRONYM}"
            echo ""
        fi
    fi
done <<< "$WORKTREES"

if [[ $FOUND_STALE -eq 0 ]]; then
    echo "No stale worktrees found. All worktree branches are unmerged."
fi
