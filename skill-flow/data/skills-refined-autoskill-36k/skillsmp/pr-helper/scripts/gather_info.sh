#!/bin/bash
# Gather git information for PR creation

echo "PR CONTEXT"
echo "=========================================="

# Current branch
BRANCH=$(git branch --show-current 2>/dev/null)
echo "Branch: $BRANCH"

# Check if on main
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
    echo ""
    echo "ERROR: Cannot create PR from $BRANCH branch"
    echo "Create a feature branch first"
    exit 1
fi

# Check if branch is pushed
if ! git rev-parse --verify "origin/$BRANCH" >/dev/null 2>&1; then
    echo "Status: NOT PUSHED"
    echo ""
    echo "Push first: git push -u origin $BRANCH"
    exit 1
fi
echo "Status: Pushed to origin"

# Commit count
COMMIT_COUNT=$(git log origin/main..HEAD --oneline 2>/dev/null | wc -l)
echo "Commits: $COMMIT_COUNT"

# Files changed
echo ""
echo "FILES CHANGED"
echo "----------------------------------------"
git diff origin/main..HEAD --stat 2>/dev/null | tail -20

# Recent commits
echo ""
echo "RECENT COMMITS"
echo "----------------------------------------"
git log origin/main..HEAD --oneline 2>/dev/null | head -10

# Detect change type from commits
echo ""
echo "SUGGESTED TYPE"
echo "----------------------------------------"
COMMITS=$(git log origin/main..HEAD --oneline 2>/dev/null)
if echo "$COMMITS" | grep -qi "^[a-f0-9]* feat"; then
    echo "feat (new feature detected)"
elif echo "$COMMITS" | grep -qi "^[a-f0-9]* fix"; then
    echo "fix (bug fix detected)"
elif echo "$COMMITS" | grep -qi "^[a-f0-9]* docs"; then
    echo "docs (documentation detected)"
elif echo "$COMMITS" | grep -qi "^[a-f0-9]* refactor"; then
    echo "refactor (refactoring detected)"
else
    echo "chore (default)"
fi

echo ""
echo "=========================================="
echo "Ready for PR creation"
