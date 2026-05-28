#!/bin/bash
# .gemini/skills/jules-pr-manager/merge.sh
PR_ID=$1
shift
MSG="$*"
if [ -z "$PR_ID" ]; then echo "Usage: $0 <pr-id> [approval-message]"; exit 1; fi

# Default message
if [ -z "$MSG" ]; then MSG="Approved. Merging changes."; fi

# Ensure @jules is in the message for the review record
if [[ ! "$MSG" == *"@jules"* ]]; then
  MSG="@jules $MSG"
fi

echo "Posting approval review for #$PR_ID..."
gh pr review "$PR_ID" --approve --body "$MSG"

echo "Merging #$PR_ID..."
gh pr merge "$PR_ID" --squash --delete-branch --auto
