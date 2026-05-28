#!/usr/bin/env bash
# Silent-on-success wrapper for test commands
# Based on: https://www.hlyr.dev/blog/context-efficient-backpressure
#
# See also: lefant-claude-code-plugins/lefant/skills/test-analyzer/skill.md

set -euo pipefail

usage() {
  echo "Usage: run-silent.sh <description> <log-file> <command...>"
  echo "Example: run-silent.sh 'vitest' /artifacts/test/vitest.log pnpm run test:run"
  exit 1
}

[[ $# -lt 3 ]] && usage

DESCRIPTION="$1"
LOG_FILE="$2"
shift 2

# Ensure artifacts directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Run command, capture all output
if "$@" > "$LOG_FILE" 2>&1; then
  echo "✓ $DESCRIPTION"
  exit 0
else
  EXIT_CODE=$?
  echo "✗ $DESCRIPTION (exit: $EXIT_CODE)"
  cat "$LOG_FILE"
  exit $EXIT_CODE
fi
