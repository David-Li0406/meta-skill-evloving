#!/bin/bash
# =============================================================================
# create-git-worktree.sh
# =============================================================================
# Creates a git worktree for working on a Linear ticket in isolation.
#
# Usage:
#   ./create-git-worktree.sh ENG-123
#   TICKET_ID="ENG-123" ./create-git-worktree.sh
#   TICKET_ID="ENG-123" TICKET_URL="https://linear.app/team/issue/ENG-123/fix-the-bug" ./create-git-worktree.sh
#
# Arguments:
#   TICKET_ID  - The Linear ticket ID (e.g., "ENG-123")
#                Can be passed as first argument or environment variable
#   TICKET_URL - (Optional) The Linear ticket URL. If provided, the path after
#                /issue/ is used for the branch name (e.g., "eng-123/fix-the-bug")
#
# Outputs (to stdout, one per line):
#   BRANCH_NAME=<branch>       - Branch name in format "[username]/[ticket-path]"
#   WORKTREE_PATH=<path>       - Absolute path to created worktree
#   DEFAULT_BRANCH=<branch>    - The repository's default branch (e.g., "main")
#
# Exit codes:
#   0 - Success (worktree created)
#   1 - Failed to create worktree
#
# Note: Caller must cd to WORKTREE_PATH after running this script
#
# Example:
#   TICKET_ID="ENG-123" TICKET_URL="https://linear.app/team/issue/ENG-123/fix-bug" ./create-git-worktree.sh
#   # Creates worktree, outputs:
#   # BRANCH_NAME=kevin/eng-123/fix-bug
#   # WORKTREE_PATH=/path/to/repo/.worktrees/eng-123
#   # DEFAULT_BRANCH=main
# =============================================================================

# Accept TICKET_ID from env var or first positional argument
TICKET_ID="${TICKET_ID:-$1}"

if [[ -z "$TICKET_ID" ]]; then
  echo "Error: TICKET_ID is required (as env var or first argument)" >&2
  exit 1
fi

# Generate branch name: [username]/[ticket-path-lowercase]
OS_USER=$(whoami)
TICKET_LOWER=$(echo "$TICKET_ID" | tr '[:upper:]' '[:lower:]')

# If TICKET_URL is provided, extract path after /issue/ for branch name
if [[ -n "$TICKET_URL" ]]; then
  # Extract everything after /issue/ and convert to lowercase
  BRANCH_SUFFIX=$(echo "$TICKET_URL" | sed -n 's|.*/issue/||p' | tr '[:upper:]' '[:lower:]')
  # Fallback if URL doesn't contain /issue/ pattern
  if [[ -z "$BRANCH_SUFFIX" ]]; then
    BRANCH_SUFFIX="$TICKET_LOWER"
  fi
else
  BRANCH_SUFFIX="$TICKET_LOWER"
fi

BRANCH_NAME="${OS_USER}/${BRANCH_SUFFIX}"
WORKTREE_PATH="$(pwd)/.worktrees/$TICKET_LOWER"

# Get the default branch name
DEFAULT_BRANCH=$(git remote show origin | grep 'HEAD branch' | cut -d' ' -f5)

# Create worktree
echo "🌳 Creating worktree at $WORKTREE_PATH" >&2
if ! git worktree add -b "$BRANCH_NAME" "$WORKTREE_PATH" "origin/$DEFAULT_BRANCH" >&2; then
  echo "Error: Failed to create worktree" >&2
  exit 1
fi

echo "✅ Worktree created at $WORKTREE_PATH" >&2
echo "" >&2
echo "📦 Remember to install dependencies in the new worktree:" >&2
echo "   cd $WORKTREE_PATH && <package-manager> install" >&2
echo "   (e.g., pnpm install, npm install, yarn, bun install, etc.)" >&2

# Output variables for caller to capture
echo "BRANCH_NAME=$BRANCH_NAME"
echo "WORKTREE_PATH=$WORKTREE_PATH"
echo "DEFAULT_BRANCH=$DEFAULT_BRANCH"
