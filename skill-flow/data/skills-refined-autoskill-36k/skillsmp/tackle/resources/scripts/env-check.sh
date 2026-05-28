#!/usr/bin/env bash
# env-check.sh - Validate required environment variables for tackle
#
# Usage: source env-check.sh
#
# Checks:
#   BD_ACTOR   - Required for claiming steps (should be set by gt/bd)
#   SKILL_DIR  - Required for sourcing tackle scripts (set by agent)
#
# Errors: Exits 1 with guidance if required vars are missing
#
# Notes:
#   - Run early in tackle session, especially after compaction
#   - BD_ACTOR is a built-in that can get lost during compaction
#   - If vars are missing, agent should report to mayor (possible compaction bug)

set -euo pipefail

MISSING=()

if [ -z "${BD_ACTOR:-}" ]; then
  MISSING+=("BD_ACTOR (built-in, should be set by gt/bd system)")
fi

if [ -z "${SKILL_DIR:-}" ]; then
  MISSING+=("SKILL_DIR (must be set by agent to tackle skill directory)")
fi

if [ ${#MISSING[@]} -gt 0 ]; then
  echo "ERROR: Missing required environment variables:"
  for var in "${MISSING[@]}"; do
    echo "  - $var"
  done
  echo ""
  echo "If BD_ACTOR is missing after compaction, this may be a compaction bug."
  echo "Report to mayor with: STEP='env-check' ERROR_DESC='BD_ACTOR not set after compaction'"
  echo "                      source \"\$SKILL_DIR/resources/scripts/report-problem.sh\""
  exit 1
fi

echo "Environment OK: BD_ACTOR=$BD_ACTOR SKILL_DIR=$SKILL_DIR"
