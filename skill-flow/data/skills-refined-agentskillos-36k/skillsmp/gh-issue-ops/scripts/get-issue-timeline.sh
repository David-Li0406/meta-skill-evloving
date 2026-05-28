#!/bin/bash
# Get timeline events for an issue
# Usage: get-issue-timeline.sh <number>

NUMBER=$1

if [ -z "$NUMBER" ]; then
  echo "Usage: get-issue-timeline.sh <number>" >&2
  exit 1
fi

OWNER=$(gh repo view --json owner -q '.owner.login')
REPO=$(gh repo view --json name -q '.name')

gh api "repos/$OWNER/$REPO/issues/$NUMBER/timeline" --jq '.[] | {event, created_at, actor: .actor.login}'
