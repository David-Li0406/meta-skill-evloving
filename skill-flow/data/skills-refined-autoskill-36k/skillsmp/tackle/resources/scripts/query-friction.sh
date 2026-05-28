#!/usr/bin/env bash
# query-friction.sh - Query closed tackle molecules for friction patterns
#
# Usage: source query-friction.sh
#        or: bash query-friction.sh
#
# Inputs: None
#
# Outputs:
#   Prints JSON of closed tackle molecules that had friction, showing:
#   - id: molecule ID
#   - close_reason: why it was closed (contains friction notes)
#   - notes: additional notes
#
# Use this to detect recurring issues before proposing skill fixes.
# Rule: 2+ occurrences = propose fix, 3+ = definitely fix

set -euo pipefail

# Find closed tackle molecules that had friction (excludes clean runs)
bd list --all --label "formula:tackle" --label "tackle:friction" --json 2>/dev/null | jq '
  .[] | select(.status == "closed") |
  {id, close_reason, notes}
'
