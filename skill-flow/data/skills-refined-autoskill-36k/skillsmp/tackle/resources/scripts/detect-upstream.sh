#!/usr/bin/env bash
# detect-upstream.sh - Detect git remote and extract org/repo
#
# Usage: source detect-upstream.sh
#
# Inputs: None (reads from git remotes)
#
# Outputs (exported variables):
#   UPSTREAM_REMOTE - Git remote name (upstream, fork-source, or origin)
#   UPSTREAM_URL    - The remote URL
#   ORG_REPO        - The org/repo format (e.g., "steveyegge/beads")
#   DEFAULT_BRANCH  - The default branch name (e.g., "main")
#   UPSTREAM_REF    - The full ref (e.g., "upstream/main")
#
# Errors: Exits 1 if no valid remote found or URL cannot be parsed

set -euo pipefail

# Detect remote (prefer upstream, then fork-source, then origin)
UPSTREAM_REMOTE="upstream"
UPSTREAM_URL=$(git remote -v | grep -E '^upstream\s' | head -1 | awk '{print $2}')
if [ -z "$UPSTREAM_URL" ]; then
  UPSTREAM_REMOTE="fork-source"
  UPSTREAM_URL=$(git remote -v | grep -E '^fork-source\s' | head -1 | awk '{print $2}')
fi
if [ -z "$UPSTREAM_URL" ]; then
  UPSTREAM_REMOTE="origin"
  UPSTREAM_URL=$(git remote -v | grep -E '^origin\s' | head -1 | awk '{print $2}')
fi

# Error if no remote found
if [ -z "$UPSTREAM_URL" ]; then
  echo "ERROR: No git remote found. Expected 'upstream', 'fork-source', or 'origin'."
  echo "Add a remote with: git remote add origin <url>"
  exit 1
fi

# Extract org/repo, strip .git suffix if present
ORG_REPO=$(echo "$UPSTREAM_URL" | sed -E 's#.*github.com[:/]##' | sed 's/\.git$//')

# Verify we got a valid org/repo
if [ -z "$ORG_REPO" ] || [ "$ORG_REPO" = "$UPSTREAM_URL" ]; then
  echo "ERROR: Could not parse org/repo from URL: $UPSTREAM_URL"
  echo "Expected GitHub URL format (https or ssh)"
  exit 1
fi

# If we fell back to origin, check if it's a fork and use parent instead
if [ "$UPSTREAM_REMOTE" = "origin" ]; then
  PARENT_REPO=$(gh api repos/$ORG_REPO --jq '.parent.full_name // empty' 2>/dev/null || true)
  if [ -n "$PARENT_REPO" ]; then
    echo "Detected fork: $ORG_REPO is a fork of $PARENT_REPO"
    echo "Using upstream: $PARENT_REPO"
    ORG_REPO="$PARENT_REPO"
    # Add the upstream remote for future use
    git remote add upstream "https://github.com/$PARENT_REPO.git" 2>/dev/null || true
    git fetch upstream 2>/dev/null || true
    UPSTREAM_REMOTE="upstream"
    UPSTREAM_URL="https://github.com/$PARENT_REPO.git"
  fi
fi

# Detect default branch
DEFAULT_BRANCH=$(gh api repos/$ORG_REPO --jq '.default_branch')
UPSTREAM_REF="$UPSTREAM_REMOTE/$DEFAULT_BRANCH"

# Export variables for use by calling script
export UPSTREAM_REMOTE UPSTREAM_URL ORG_REPO DEFAULT_BRANCH UPSTREAM_REF
