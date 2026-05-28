#!/bin/bash
# Get all comments on an issue
# Usage: get-issue-comments.sh <number>

NUMBER=$1

if [ -z "$NUMBER" ]; then
  echo "Usage: get-issue-comments.sh <number>" >&2
  exit 1
fi

OWNER=$(gh repo view --json owner -q '.owner.login')
REPO=$(gh repo view --json name -q '.name')

gh api "repos/$OWNER/$REPO/issues/$NUMBER/comments" --jq '.[] | {author: .user.login, created_at, body}'
