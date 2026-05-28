#!/bin/bash
# =============================================================================
# commit-and-push.sh
# =============================================================================
# Stages all changes, commits with conventional commit format, and pushes.
#
# Usage:
#   TICKET_ID="ENG-123" TITLE="Fix bug" BRANCH_NAME="kevin/eng-123" ./commit-and-push.sh
#
# Required environment variables:
#   TICKET_ID   - The Linear ticket ID (e.g., "ENG-123")
#   TITLE       - Short description for commit message
#   BRANCH_NAME - Git branch name to push to
#
# Optional environment variables:
#   COMMIT_TYPE - Conventional commit type (default: "fix")
#                 Common values: fix, feat, chore, refactor, docs, test
#
# Commit format:
#   <COMMIT_TYPE>(TICKET_ID): TITLE
#
# Exit codes:
#   0 - Success (committed and pushed)
#   1 - Missing env vars, nothing to commit, or push failed
#
# Examples:
#   TICKET_ID="ENG-123" TITLE="Fix login bug" BRANCH_NAME="kevin/eng-123" ./commit-and-push.sh
#   # Commits: "fix(ENG-123): Fix login bug"
#
#   COMMIT_TYPE="feat" TICKET_ID="ENG-456" TITLE="Add dashboard" BRANCH_NAME="kevin/eng-456" ./commit-and-push.sh
#   # Commits: "feat(ENG-456): Add dashboard"
# =============================================================================

if [ -z "$TICKET_ID" ] || [ -z "$TITLE" ] || [ -z "$BRANCH_NAME" ]; then
  echo "Error: TICKET_ID, TITLE, and BRANCH_NAME must be set" >&2
  exit 1
fi

# Default commit type to "fix" if not specified
COMMIT_TYPE="${COMMIT_TYPE:-fix}"

# Stage all changes
git add -A

# Generate commit message
COMMIT_MSG="$COMMIT_TYPE($TICKET_ID): $TITLE"

# Commit
if ! git commit -m "$COMMIT_MSG"; then
  echo "Error: Nothing to commit or commit failed"
  exit 1
fi

# Push to origin
echo "📤 Pushing to origin/$BRANCH_NAME"
git push -u origin "$BRANCH_NAME"
