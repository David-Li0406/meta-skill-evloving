#!/bin/bash
#
# codex-exec.sh - Simple wrapper for non-interactive Codex queries
# Preferred method for quick queries without visual split-pane
#

set -e

PROMPT="$1"

if [ -z "$PROMPT" ]; then
  echo "Usage: $0 \"your prompt here\"" >&2
  echo "" >&2
  echo "Examples:" >&2
  echo "  $0 \"What is the time complexity of quicksort?\"" >&2
  echo "  $0 \"Review this code for bugs: function add(a,b) { return a + b }\"" >&2
  exit 1
fi

# Check if codex is available
if ! command -v codex &>/dev/null; then
  echo "[ERROR] Codex CLI not found. Please install it:" >&2
  echo "  npm install -g @openai/codex" >&2
  exit 1
fi

# Execute codex in non-interactive mode
# stderr is redirected to /dev/null to show only the final response
codex exec "$PROMPT" 2>/dev/null

# Exit with codex's exit code
exit $?
