#!/bin/bash
# Script to find the bookmark associated with current or parent jj revisions

set -e

# Try current revision first
bookmark=$(jj log -r @ -T 'bookmarks' --no-graph 2>/dev/null | grep -v '^$' | grep -v '^~$' || true)

if [ -n "$bookmark" ]; then
    echo "$bookmark"
    exit 0
fi

# Try parent revision
bookmark=$(jj log -r '@-' -T 'bookmarks' --no-graph 2>/dev/null | grep -v '^$' | grep -v '^~$' || true)

if [ -n "$bookmark" ]; then
    echo "$bookmark"
    exit 0
fi

# Try grandparent
bookmark=$(jj log -r '@--' -T 'bookmarks' --no-graph 2>/dev/null | grep -v '^$' | grep -v '^~$' || true)

if [ -n "$bookmark" ]; then
    echo "$bookmark"
    exit 0
fi

echo "Error: Could not find a bookmark on current or parent revisions" >&2
exit 1
