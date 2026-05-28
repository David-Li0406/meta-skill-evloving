#!/usr/bin/env bash
# sling-tackle.sh - Sling tackle formula onto issue and set up molecule
#
# Usage: source sling-tackle.sh
#
# Inputs (required):
#   ISSUE_ID  - The issue bead ID to tackle
#   ORG_REPO  - The upstream org/repo (e.g., "steveyegge/beads")
#
# Outputs (exported variables):
#   MOL_ID     - The created molecule ID
#   FIRST_STEP - The first ready step ID (may be empty)
#
# Side effects:
#   - Updates issue with upstream context
#   - Slings tackle formula (creates molecule, hooks issue)
#   - Claims first step with current actor
#
# Note: Steps are linked to molecule via parent-child deps.
#   Use gt hook --json or bd dep list --type=parent-child to find steps.
#
# Errors: Exits 1 with guidance if sling fails or BD_ACTOR not set

set -euo pipefail

# Verify required variables
if [ -z "${ISSUE_ID:-}" ]; then
  echo "ERROR: ISSUE_ID must be set before sourcing sling-tackle.sh"
  exit 1
fi
if [ -z "${ORG_REPO:-}" ]; then
  echo "ERROR: ORG_REPO must be set before sourcing sling-tackle.sh"
  exit 1
fi

# Store upstream context in the issue bead (bead carries its own context)
# This is needed because gt sling --on doesn't support --var
bd update "$ISSUE_ID" --notes "upstream: $ORG_REPO"

# Sling the issue with tackle formula
# This creates the molecule wisp, bonds it to the issue, hooks issue to self,
# and stores attached_molecule in the issue bead's description
gt sling tackle --on "$ISSUE_ID"

# Verify hook is set
if ! gt hook --json 2>/dev/null | jq -e '.attached_molecule' > /dev/null; then
  echo "ERROR: Sling failed - no molecule attached"
  echo "Check gt sling output above for errors"
  echo ">>> Mail the mayor (see 'When Things Go Wrong' above) - do NOT try to fix this yourself <<<"
  exit 1
fi

# Get molecule ID and first step from hook (avoids bd routing issues)
HOOK_JSON=$(gt hook --json)
MOL_ID=$(echo "$HOOK_JSON" | jq -r '.attached_molecule')
echo "Tackle started: $MOL_ID"

# Add formula label for pattern detection in reflect phase
bd update "$MOL_ID" --add-label "formula:tackle"

# CRITICAL: Claim first step with assignee so bd mol current works
# Use gt hook data directly (more reliable than bd ready --parent)
FIRST_STEP=$(echo "$HOOK_JSON" | jq -r '.progress.ready_steps[0] // empty')
if [ -n "$FIRST_STEP" ]; then
  if [ -z "${BD_ACTOR:-}" ]; then
    echo "ERROR: BD_ACTOR not set. Run env-check.sh first, or report to mayor."
    exit 1
  fi
  bd update "$FIRST_STEP" --status=in_progress --assignee "$BD_ACTOR"
fi

# Export for use by calling context
export MOL_ID FIRST_STEP
