#!/usr/bin/env bash
# verify-pr-ready.sh - Verify PR is no longer in draft state
#
# Usage: source verify-pr-ready.sh
#
# Inputs (required):
#   PR_NUMBER - The PR number to check
#   ORG_REPO  - The upstream org/repo (e.g., "steveyegge/beads")
#
# Outputs (exported variables):
#   IS_DRAFT  - "true" if still draft, "false" if ready
#   PR_STATE  - The PR state (OPEN, CLOSED, MERGED)
#   PR_URL    - The PR URL
#
# Errors: Exits 1 if PR is still in draft state

set -euo pipefail

# Verify required variables are set
if [ -z "${PR_NUMBER:-}" ]; then
  echo "ERROR: PR_NUMBER must be set before sourcing verify-pr-ready.sh"
  exit 1
fi
if [ -z "${ORG_REPO:-}" ]; then
  echo "ERROR: ORG_REPO must be set before sourcing verify-pr-ready.sh"
  exit 1
fi

# Check draft status
IS_DRAFT=$(gh pr view "$PR_NUMBER" --repo "$ORG_REPO" --json isDraft --jq '.isDraft')
if [ "$IS_DRAFT" = "true" ]; then
  echo "ERROR: PR #$PR_NUMBER still in draft - gh pr ready may have failed"
  exit 1
fi

# Get state and URL
PR_STATE=$(gh pr view "$PR_NUMBER" --repo "$ORG_REPO" --json state --jq '.state')
PR_URL=$(gh pr view "$PR_NUMBER" --repo "$ORG_REPO" --json url --jq '.url')

echo "PR #$PR_NUMBER is $PR_STATE and ready for review"

# Export variables for use by calling script
export IS_DRAFT PR_STATE PR_URL
