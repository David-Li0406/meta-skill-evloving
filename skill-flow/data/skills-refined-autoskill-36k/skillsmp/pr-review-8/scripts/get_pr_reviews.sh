#!/bin/bash
# Script to find PR for current or parent jj bookmark and display review comments

set -e

# Find the bookmark associated with current or parent revisions
find_bookmark() {
    # Try current revision first
    local bookmark=$(jj log -r @ -T 'bookmarks' --no-graph 2>/dev/null | grep -v '^$' | grep -v '^~$')

    if [ -n "$bookmark" ]; then
        echo "$bookmark"
        return 0
    fi

    # Try parent revisions
    bookmark=$(jj log -r '@-' -T 'bookmarks' --no-graph 2>/dev/null | grep -v '^$' | grep -v '^~$')

    if [ -n "$bookmark" ]; then
        echo "$bookmark"
        return 0
    fi

    # Try grandparent
    bookmark=$(jj log -r '@--' -T 'bookmarks' --no-graph 2>/dev/null | grep -v '^$' | grep -v '^~$')

    if [ -n "$bookmark" ]; then
        echo "$bookmark"
        return 0
    fi

    return 1
}

# Main execution
bookmark=$(find_bookmark)

if [ -z "$bookmark" ]; then
    echo "Error: Could not find a bookmark on current or parent revisions" >&2
    echo "Run 'jj bookmark list' to see available bookmarks" >&2
    exit 1
fi

echo "Found bookmark: $bookmark" >&2
echo "" >&2

# Try to find PR by branch name
pr_number=$(gh pr list --state all --json number,headRefName --jq ".[] | select(.headRefName == \"$bookmark\") | .number" | head -1)

if [ -z "$pr_number" ]; then
    echo "Error: No PR found for branch '$bookmark'" >&2
    exit 1
fi

echo "Found PR #$pr_number" >&2
echo "==================" >&2
echo "" >&2

# Display PR details with review comments
gh pr view "$pr_number"
