#!/bin/bash

# Usage: ./detect-base-branch.sh <repository-path>
# Returns the default branch name (main, develop, master, etc.)

REPOSITORY_PATH="$1"

if [ -z "$REPOSITORY_PATH" ]; then
    echo "Usage: $0 <repository-path>" >&2
    exit 1
fi

if [ ! -d "$REPOSITORY_PATH" ]; then
    echo "Error: Repository path does not exist: $REPOSITORY_PATH" >&2
    exit 1
fi

cd "$REPOSITORY_PATH" || exit 1

# Try to get the default branch from remote HEAD
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')

if [ -n "$DEFAULT_BRANCH" ]; then
    echo "$DEFAULT_BRANCH"
    exit 0
fi

# If that fails, try to set it and retrieve
git remote set-head origin --auto >/dev/null 2>&1
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')

if [ -n "$DEFAULT_BRANCH" ]; then
    echo "$DEFAULT_BRANCH"
    exit 0
fi

# Fallback: check common branch names in order of preference
for BRANCH in main master develop development; do
    if git show-ref --verify --quiet "refs/remotes/origin/$BRANCH"; then
        echo "$BRANCH"
        exit 0
    fi
done

# If all else fails, use the current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
if [ -n "$CURRENT_BRANCH" ] && [ "$CURRENT_BRANCH" != "HEAD" ]; then
    echo "$CURRENT_BRANCH"
    exit 0
fi

echo "Error: Could not determine base branch" >&2
exit 1
