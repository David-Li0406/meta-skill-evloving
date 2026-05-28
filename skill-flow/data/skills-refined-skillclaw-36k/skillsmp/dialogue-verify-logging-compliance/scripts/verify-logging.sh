#!/bin/bash
# verify-logging.sh — Verify logging compliance for a process execution
# Part of the Dialogue Framework
# Usage: verify-logging.sh <process-identifier> <min-decisions> <min-observations>

set -euo pipefail

# Use Claude's project directory environment variable
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR must be set}"

# Per-file log directories (current structure)
DECISIONS_DIR="${PROJECT_ROOT}/.dialogue/logs/decisions"
OBSERVATIONS_DIR="${PROJECT_ROOT}/.dialogue/logs/observations"

if [[ $# -lt 3 ]]; then
    echo "Usage: verify-logging.sh <process-identifier> <min-decisions> <min-observations>" >&2
    echo "  process-identifier: String to search for in log files" >&2
    echo "  min-decisions: Minimum number of decision entries expected" >&2
    echo "  min-observations: Minimum number of observation entries expected" >&2
    exit 1
fi

PROCESS_ID="$1"
MIN_DECISIONS="$2"
MIN_OBSERVATIONS="$3"

echo "Verifying logging compliance for: $PROCESS_ID"
echo "---"

# Count decisions matching the process identifier (per-file structure)
DECISION_COUNT=0
if [[ -d "$DECISIONS_DIR" ]]; then
    DECISION_COUNT=$(grep -l "$PROCESS_ID" "$DECISIONS_DIR"/*.yaml 2>/dev/null | wc -l | tr -d ' ')
fi

# Count observations matching the process identifier (per-file structure)
OBSERVATION_COUNT=0
if [[ -d "$OBSERVATIONS_DIR" ]]; then
    OBSERVATION_COUNT=$(grep -l "$PROCESS_ID" "$OBSERVATIONS_DIR"/*.yaml 2>/dev/null | wc -l | tr -d ' ')
fi

# Check decisions
if [[ "$DECISION_COUNT" -ge "$MIN_DECISIONS" ]]; then
    echo "Decisions found: $DECISION_COUNT (minimum: $MIN_DECISIONS) ✓"
    DECISIONS_PASS=true
else
    echo "Decisions found: $DECISION_COUNT (minimum: $MIN_DECISIONS) ✗"
    DECISIONS_PASS=false
fi

# Check observations
if [[ "$OBSERVATION_COUNT" -ge "$MIN_OBSERVATIONS" ]]; then
    echo "Observations found: $OBSERVATION_COUNT (minimum: $MIN_OBSERVATIONS) ✓"
    OBSERVATIONS_PASS=true
else
    echo "Observations found: $OBSERVATION_COUNT (minimum: $MIN_OBSERVATIONS) ✗"
    OBSERVATIONS_PASS=false
fi

echo "---"

# Overall result
if [[ "$DECISIONS_PASS" == "true" && "$OBSERVATIONS_PASS" == "true" ]]; then
    echo "PASS: Logging compliance verified"
    exit 0
else
    echo "FAIL: Logging compliance not met"
    if [[ "$DECISIONS_PASS" != "true" ]]; then
        echo "  - Need $((MIN_DECISIONS - DECISION_COUNT)) more decision entries"
    fi
    if [[ "$OBSERVATIONS_PASS" != "true" ]]; then
        echo "  - Need $((MIN_OBSERVATIONS - OBSERVATION_COUNT)) more observation entries"
    fi
    exit 1
fi
