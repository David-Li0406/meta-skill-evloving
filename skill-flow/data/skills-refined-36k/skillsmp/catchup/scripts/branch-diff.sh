#!/bin/bash
# Branch diff: show changes since fork from base branch

set -e

# Get current branch
CURRENT=$(git branch --show-current)

if [ -z "$CURRENT" ]; then
    echo "ERROR: Detached HEAD state"
    echo "Current commit: $(git rev-parse --short HEAD)"
    exit 1
fi

# Check if on base branch
if [ "$CURRENT" = "main" ] || [ "$CURRENT" = "master" ]; then
    echo "ERROR: Already on base branch ($CURRENT)"
    echo "Nothing to compare - checkout a feature branch first"
    exit 1
fi

# Detect base branch
if git rev-parse --verify origin/main >/dev/null 2>&1; then
    BASE="origin/main"
elif git rev-parse --verify origin/master >/dev/null 2>&1; then
    BASE="origin/master"
elif git rev-parse --verify main >/dev/null 2>&1; then
    BASE="main"
elif git rev-parse --verify master >/dev/null 2>&1; then
    BASE="master"
else
    echo "ERROR: Cannot find main or master branch"
    exit 1
fi

# Fetch latest
echo "Fetching latest from ${BASE}..."
git fetch origin "${BASE#origin/}" 2>/dev/null || true

# Find fork point
FORK_POINT=$(git merge-base "$BASE" HEAD)

echo ""
echo "=== Branch Info ==="
echo "Current branch: $CURRENT"
echo "Base branch:    $BASE"
echo "Fork point:     ${FORK_POINT:0:8}"
echo ""

echo "=== Changed Files ==="
git diff "$FORK_POINT"..HEAD --name-only
echo ""

echo "=== Diff Stats ==="
git diff "$FORK_POINT"..HEAD --stat
echo ""

echo "=== Commit History ==="
git log "$FORK_POINT"..HEAD --oneline
