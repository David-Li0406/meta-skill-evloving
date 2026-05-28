#!/bin/bash
# Get linked projects for current repo
# Checks for org projects first, then user projects

OWNER=$(gh repo view --json owner -q '.owner.login')
OWNER_TYPE=$(gh api users/$OWNER --jq '.type')

if [ "$OWNER_TYPE" = "Organization" ]; then
  gh project list --owner "$OWNER" --format json
else
  gh project list --format json
fi
