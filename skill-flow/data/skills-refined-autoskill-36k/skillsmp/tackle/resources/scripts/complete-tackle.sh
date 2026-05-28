#!/usr/bin/env bash
# complete-tackle.sh - Close root molecule and unhook after tackle completion
#
# Usage: source complete-tackle.sh
#
# Inputs (optional):
#   MOL_ID - The molecule ID to close (will be recovered from hook if not set)
#
# Side effects:
#   - Closes the root molecule
#   - Verifies molecule is closed
#   - Unhooks the issue (frees hook for other work)
#
# Notes:
#   - Run this AFTER closing the reflect step
#   - The issue stays in "deferred" status until PR outcome - that's correct
#   - Molecules do NOT auto-close, this explicit close is required
#
# Errors: Exits 1 if molecule ID cannot be found

set -euo pipefail

# Get MOL_ID from hook if not already set
if [ -z "${MOL_ID:-}" ]; then
  MOL_ID=$(gt hook --json 2>/dev/null | jq -r '.attached_molecule // empty')
fi

if [ -z "$MOL_ID" ]; then
  echo "ERROR: No molecule ID found. Check gt hook or context-recovery.sh output."
  exit 1
fi

# Close the root molecule
bd close "$MOL_ID" --reason "Tackle complete - PR submitted"

# Verify molecule closed
echo "Verifying molecule closure..."
bd --no-daemon mol current   # Should show "No molecules in progress"

# Unhook the issue (frees your hook for other work)
# The issue stays in "deferred" status until PR outcome - that's correct.
# But you can work on other things while waiting for maintainer review.
gt unhook --force

echo "Tackle cleanup complete: molecule closed, hook cleared"
