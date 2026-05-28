#!/usr/bin/env bash
# context-recovery.sh - Recover tackle context after session restart
#
# Usage: source context-recovery.sh
#
# Inputs: None (reads from gt hook and bd)
#
# Outputs (exported variables):
#   ISSUE_ID - The issue bead ID from the hook
#   MOL_ID   - The molecule ID attached to the hook
#   ORG_REPO - The upstream org/repo from issue notes
#
# Errors: Exits 1 if upstream not found in issue notes or git remotes
#
# Notes:
#   - Run this after session restart (compaction, handoff, new terminal)
#   - Also shows current step via bd --no-daemon mol current

set -euo pipefail

# Get IDs from hook (bead_id = issue, attached_molecule = tackle wisp)
HOOK_JSON=$(gt hook --json 2>/dev/null || echo '{}')
ISSUE_ID=$(echo "$HOOK_JSON" | jq -r '.bead_id // empty')
MOL_ID=$(echo "$HOOK_JSON" | jq -r '.attached_molecule // empty')

# Get upstream from issue bead notes (stored before slinging)
if [ -n "$ISSUE_ID" ]; then
  ORG_REPO=$(bd show "$ISSUE_ID" --json 2>/dev/null | jq -r '.[0].notes // empty' | grep -oP 'upstream: \K[^\s]+' || echo "")
else
  ORG_REPO=""
fi

# Fallback: re-detect from git remote if not in notes
if [ -z "$ORG_REPO" ]; then
  UPSTREAM_URL=$(git remote get-url upstream 2>/dev/null || git remote get-url fork-source 2>/dev/null || git remote get-url origin 2>/dev/null || echo "")
  if [ -n "$UPSTREAM_URL" ]; then
    ORG_REPO=$(echo "$UPSTREAM_URL" | sed -E 's#.*github.com[:/]##' | sed 's/\.git$//')
    echo "WARNING: ORG_REPO not in issue notes, detected from git remote: $ORG_REPO"
  fi
fi

# Still no upstream? Error
if [ -z "$ORG_REPO" ]; then
  echo "ERROR: No upstream found in issue notes or git remotes. Was this tackle started correctly?"
  if [ -n "$ISSUE_ID" ]; then
    echo "Fix: bd update $ISSUE_ID --notes 'upstream: <org/repo>'"
  fi
  exit 1
fi

# Show current step
bd --no-daemon mol current

# Export variables for use by calling script
export ISSUE_ID MOL_ID ORG_REPO
