#!/bin/bash
# =============================================================================
# create-github-pr.sh
# =============================================================================
# Creates a GitHub pull request with the provided body content.
#
# Usage:
#   ./create-github-pr.sh  (with required env vars set)
#
# Required environment variables:
#   TICKET_ID      - The Linear ticket ID (e.g., "ENG-123")
#   TITLE          - Short description for PR title
#   BRANCH_NAME    - Source branch for the PR
#   DEFAULT_BRANCH - Target branch (e.g., "main")
#   PR_BODY        - The complete PR body (pre-filled by Claude)
#
# Optional environment variables:
#   COMMIT_TYPE    - Conventional commit type (default: "fix")
#   WORKTREE_PATH  - Path to worktree (for success message)
#   TICKET_URL     - Linear ticket URL (for success message)
#
# Exit codes:
#   0 - Success (PR created)
#   1 - Missing required env vars or gh pr create failed
#
# Example:
#   TICKET_ID="ENG-123" TITLE="Fix bug" BRANCH_NAME="kevin/eng-123" \
#   DEFAULT_BRANCH="main" PR_BODY="..." ./create-github-pr.sh
# =============================================================================

if [ -z "$TICKET_ID" ] || [ -z "$TITLE" ] || [ -z "$BRANCH_NAME" ] || [ -z "$DEFAULT_BRANCH" ] || [ -z "$PR_BODY" ]; then
  echo "Error: TICKET_ID, TITLE, BRANCH_NAME, DEFAULT_BRANCH, and PR_BODY must be set" >&2
  exit 1
fi

# Default commit type to "fix" if not specified
COMMIT_TYPE="${COMMIT_TYPE:-fix}"
PR_TITLE="$COMMIT_TYPE($TICKET_ID): $TITLE"

# Create PR
echo "🚀 Creating pull request"
if gh pr create --title "$PR_TITLE" --body "$PR_BODY" --base "$DEFAULT_BRANCH" --head "$BRANCH_NAME"; then
  PR_URL=$(gh pr view --json url -q .url)
  echo ""
  echo "✅ Success! PR created: $PR_URL"
  echo ""
  echo "Next steps:"
  echo "1. Review the PR: $PR_URL"
  echo "2. Update Linear ticket: ${TICKET_URL:-$TICKET_ID}"
  echo "3. Worktree location: $WORKTREE_PATH"
else
  echo "Error: Failed to create PR"
  exit 1
fi
