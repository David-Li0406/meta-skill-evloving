#!/usr/bin/env bash
# ci-status-check.sh - Check CI status and detect pre-existing failures
#
# Usage: source ci-status-check.sh
#
# Inputs (required):
#   PR_NUMBER      - The PR number to check
#   ORG_REPO       - The upstream org/repo (e.g., "steveyegge/beads")
#   DEFAULT_BRANCH - The default branch name (e.g., "main")
#
# Outputs (exported variables):
#   FAILED       - Number of failed checks
#   PRE_EXISTING - "true" if all failures are pre-existing on main, "false" otherwise
#   PENDING      - Number of pending checks (0 after polling completes)
#
# Notes:
#   - Polls CI every 30 seconds while checks are pending
#   - Compares PR failures against main branch failures
#   - Pre-existing failures are not caused by this PR

set -euo pipefail

# Verify required variables are set
if [ -z "${PR_NUMBER:-}" ]; then
  echo "ERROR: PR_NUMBER must be set before sourcing ci-status-check.sh"
  exit 1
fi
if [ -z "${ORG_REPO:-}" ]; then
  echo "ERROR: ORG_REPO must be set before sourcing ci-status-check.sh"
  exit 1
fi
if [ -z "${DEFAULT_BRANCH:-}" ]; then
  echo "ERROR: DEFAULT_BRANCH must be set before sourcing ci-status-check.sh"
  exit 1
fi

# Get CI status from PR
CHECKS=$(gh pr view "$PR_NUMBER" --repo "$ORG_REPO" --json statusCheckRollup)
PENDING=$(echo "$CHECKS" | jq '[.statusCheckRollup[] | select(.status == "COMPLETED" | not)] | length')
FAILED=$(echo "$CHECKS" | jq '[.statusCheckRollup[] | select(.conclusion == "FAILURE")] | length')

# If checks still running, wait and poll
while [ "$PENDING" -gt 0 ]; do
  echo "CI still running ($PENDING checks pending). Waiting 30s..."
  sleep 30
  CHECKS=$(gh pr view "$PR_NUMBER" --repo "$ORG_REPO" --json statusCheckRollup)
  PENDING=$(echo "$CHECKS" | jq '[.statusCheckRollup[] | select(.status == "COMPLETED" | not)] | length')
done

# Re-check for failures after completion
FAILED=$(echo "$CHECKS" | jq '[.statusCheckRollup[] | select(.conclusion == "FAILURE")] | length')

# Check if failures are pre-existing on main
PRE_EXISTING=false
if [ "$FAILED" -gt 0 ]; then
  # Get names of failed checks
  FAILED_NAMES=$(echo "$CHECKS" | jq '[.statusCheckRollup[] | select(.conclusion == "FAILURE") | .name]')

  # Get failures on main/default branch
  MAIN_FAILURES=$(gh api "repos/$ORG_REPO/commits/$DEFAULT_BRANCH/check-runs" --jq '[.check_runs[] | select(.conclusion == "failure") | .name]' 2>/dev/null || echo "[]")

  # Check if all PR failures also fail on main (pre-existing)
  PRE_EXISTING=$(jq -n --argjson pr "$FAILED_NAMES" --argjson main "$MAIN_FAILURES" '($pr - $main) | length == 0')

  if [ "$PRE_EXISTING" = "true" ]; then
    echo "CI failures are pre-existing on $DEFAULT_BRANCH (not caused by this PR)"
  fi
fi

# Export variables for use by calling script
export FAILED PRE_EXISTING PENDING
