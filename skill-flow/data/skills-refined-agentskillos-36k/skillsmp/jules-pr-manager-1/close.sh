#!/bin/bash
PR_ID=$1
shift
MSG="$*"
if [ -z "$PR_ID" ]; then echo "Usage: $0 <pr-id> [message]"; exit 1; fi
if [ -z "$MSG" ]; then
  gh pr close "$PR_ID"
else
  gh pr close "$PR_ID" --comment "$MSG"
fi
