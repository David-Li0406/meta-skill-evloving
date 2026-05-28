#!/bin/bash
PR_ID=$1
shift
MSG="$*"
if [ -z "$PR_ID" ] || [ -z "$MSG" ]; then echo "Usage: $0 <pr-id> <message>"; exit 1; fi
# Ensure @jules is in the message
if [[ ! "$MSG" == *"@jules"* ]]; then
  MSG="@jules $MSG"
fi
gh pr review "$PR_ID" --request-changes --body "$MSG"
