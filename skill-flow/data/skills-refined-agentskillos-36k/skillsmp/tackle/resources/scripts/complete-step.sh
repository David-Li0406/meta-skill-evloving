#!/usr/bin/env bash
# complete-step.sh - Complete current step and claim next
#
# Usage: source complete-step.sh
#
# Inputs (required):
#   STEP_ID - The step ID to close
#   MOL_ID  - The molecule ID to find next step in
#
# Outputs (exported variables):
#   NEXT_STEP - The next step ID (or empty if none available)
#
# Notes:
#   - Closes STEP_ID with --continue flag
#   - Claims next step via gt hook (primary) or bd dep list (fallback)
#   - The assignee update is required because bd mol current filters by assignee

set -euo pipefail

# Verify required variables are set
if [ -z "${STEP_ID:-}" ]; then
  echo "ERROR: STEP_ID must be set before sourcing complete-step.sh"
  exit 1
fi
if [ -z "${MOL_ID:-}" ]; then
  echo "ERROR: MOL_ID must be set before sourcing complete-step.sh"
  exit 1
fi

# Close the current step
bd close "$STEP_ID" --continue

# CRITICAL: Claim next step so bd mol current can find you
# Use gt hook --json first (more reliable due to routing issues with bd commands)
HOOK_JSON=$(gt hook --json 2>/dev/null || echo '{}')
NEXT_STEP=$(echo "$HOOK_JSON" | jq -r '.progress.ready_steps[0] // empty')

# Fallback: Find steps via parent-child deps (steps are children of molecule)
# Filter for open steps that aren't the one we just closed
if [ -z "$NEXT_STEP" ]; then
  NEXT_STEP=$(bd dep list "$MOL_ID" --direction=up --type=parent-child --json 2>/dev/null | \
    jq -r --arg closed "$STEP_ID" '[.[] | select(.id != $closed and .status == "open")][0].id // empty' || echo "")
fi

if [ -n "$NEXT_STEP" ]; then
  bd update "$NEXT_STEP" --status=in_progress --assignee="${BD_ACTOR:-}"
fi

# Export variable for use by calling script
export NEXT_STEP
