#!/bin/bash
# Script to commit, set bookmark, and push using Jujutsu
# Usage: ./commit-and-push.sh "commit message" "bookmark-name"

set -e

if [ -z "$1" ]; then
  echo "Error: Please provide a commit message" >&2
  echo "Usage: $0 \"commit message\" \"bookmark-name\"" >&2
  exit 1
fi

if [ -z "$2" ]; then
  echo "Error: Please provide a bookmark name" >&2
  echo "Usage: $0 \"commit message\" \"bookmark-name\"" >&2
  exit 1
fi

commit_message="$1"
bookmark="$2"

jj commit -m "$commit_message"
jj bookmark set "$bookmark" -r @-

echo ""
echo "Bookmark set to: $bookmark"
read -p "Push to remote? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Push cancelled"
  exit 0
fi

jj git push --bookmark "$bookmark"
