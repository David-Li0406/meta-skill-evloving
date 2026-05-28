#!/usr/bin/env bash
# pr-check-idempotent.sh - Check if draft PR exists (idempotent entry to gate-submit)
#
# Usage: source pr-check-idempotent.sh
#
# Inputs (required):
#   ORG_REPO - The upstream org/repo (e.g., "steveyegge/beads")
#
# Outputs (exported variables):
#   PR_NUMBER - The PR number (if exists)
#   IS_DRAFT  - "true" if PR is draft, "false" if ready
#   PR_URL    - The PR URL
#   BRANCH    - Current git branch name
#   FORK_OWNER - The fork owner (from origin remote)
#
# Notes:
#   - Critical for session recovery at gate-submit
#   - Does NOT create PR - caller decides based on output
#   - GitHub is the source of truth for PR state

set -euo pipefail

# Verify ORG_REPO is set
if [ -z "${ORG_REPO:-}" ]; then
  echo "ERROR: ORG_REPO must be set before sourcing pr-check-idempotent.sh"
  exit 1
fi

# Get current branch
BRANCH=$(git branch --show-current)

# Get fork owner from origin remote URL (NOT gh repo view, which returns upstream owner)
ORIGIN_URL=$(git remote get-url origin 2>/dev/null || echo "")
FORK_OWNER=$(echo "$ORIGIN_URL" | sed -E 's#.*github.com[:/]([^/]+)/.*#\1#')
if [ -z "$FORK_OWNER" ]; then
  echo "ERROR: Could not determine fork owner from origin remote"
  exit 1
fi

# Check for existing PR
PR_JSON=$(gh pr list --repo "$ORG_REPO" --head "$FORK_OWNER:$BRANCH" --json number,isDraft,url --jq '.[0]' 2>/dev/null || echo "")

if [ -n "$PR_JSON" ] && [ "$PR_JSON" != "null" ]; then
  PR_NUMBER=$(echo "$PR_JSON" | jq -r '.number')
  IS_DRAFT=$(echo "$PR_JSON" | jq -r '.isDraft')
  PR_URL=$(echo "$PR_JSON" | jq -r '.url')

  if [ "$IS_DRAFT" = "false" ]; then
    # Already submitted - skip to record phase
    echo "PR #$PR_NUMBER already marked ready - continuing to record"
  else
    # Draft exists - present it for review
    echo "Found existing draft PR #$PR_NUMBER"
  fi
else
  # No PR exists
  PR_NUMBER=""
  IS_DRAFT=""
  PR_URL=""
  echo "No existing PR found for $FORK_OWNER:$BRANCH"
fi

# Export variables for use by calling script
export PR_NUMBER IS_DRAFT PR_URL BRANCH FORK_OWNER
