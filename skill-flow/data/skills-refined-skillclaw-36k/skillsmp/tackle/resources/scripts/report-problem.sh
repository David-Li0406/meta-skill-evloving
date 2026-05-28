#!/usr/bin/env bash
# report-problem.sh - Report a tackle problem to the mayor
#
# Usage: source report-problem.sh
#
# Inputs (required):
#   SKILL_DIR   - Path to the tackle skill directory
#   STEP        - Current tackle step (e.g., "gate-submit", "validate")
#   ERROR_DESC  - Description of the problem
#
# Inputs (optional):
#   ERROR_MSG   - Exact error message (if applicable)
#
# Side effects:
#   - Sends mail to mayor with problem details and investigation instructions
#   - Exits 0 on success, 1 on missing required variables

set -euo pipefail

# Verify required variables
if [ -z "${SKILL_DIR:-}" ]; then
  echo "ERROR: SKILL_DIR must be set before sourcing report-problem.sh"
  exit 1
fi
if [ -z "${STEP:-}" ]; then
  echo "ERROR: STEP must be set before sourcing report-problem.sh"
  exit 1
fi
if [ -z "${ERROR_DESC:-}" ]; then
  echo "ERROR: ERROR_DESC must be set before sourcing report-problem.sh"
  exit 1
fi

# Capture state
HOOK_STATE=$(gt hook --json 2>/dev/null || echo "no hook")
MOL_STATE=$(bd --no-daemon mol current 2>/dev/null || echo "no molecule")

# Build error context
ERROR_CONTEXT="- Step: ${STEP}"
if [ -n "${ERROR_MSG:-}" ]; then
  ERROR_CONTEXT="${ERROR_CONTEXT}
- Error: ${ERROR_MSG}"
fi
ERROR_CONTEXT="${ERROR_CONTEXT}
- Skill: ${SKILL_DIR}"

# Send mail to mayor
gt mail send mayor/ -s "tackle: ${STEP} failure" --body "$(cat <<EOF
## Problem
${ERROR_DESC}

## Context
${ERROR_CONTEXT}

## State
${HOOK_STATE}

${MOL_STATE}

## Instructions for Mayor
1. Do NOT start working immediately - queue this for later if busy
2. Read the skill files first: ${SKILL_DIR}/SKILL.md and relevant resources/
3. Check the script that failed (if applicable)
4. Reproduce if possible, then fix the skill (not just the symptom)
EOF
)"

echo "Problem reported to mayor: ${STEP} failure"
