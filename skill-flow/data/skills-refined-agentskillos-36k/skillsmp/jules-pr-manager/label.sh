#!/bin/bash
PR_ID=$1
ACTION=$2
LABEL=$3
if [ -z "$PR_ID" ] || [ -z "$ACTION" ] || [ -z "$LABEL" ]; then 
  echo "Usage: $0 <pr-id> <add|remove> <label>"
  exit 1
fi
if [ "$ACTION" == "add" ]; then
  gh pr edit "$PR_ID" --add-label "$LABEL"
elif [ "$ACTION" == "remove" ]; then
  gh pr edit "$PR_ID" --remove-label "$LABEL"
else
  echo "Action must be add or remove"
  exit 1
fi
