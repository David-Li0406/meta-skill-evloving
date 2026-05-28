#!/bin/bash
# Quick wrapper for calling a Foundry agent
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Use venv if it exists, otherwise system python
if [ -f "$SKILL_DIR/.venv/bin/python" ]; then
    PYTHON="$SKILL_DIR/.venv/bin/python"
else
    PYTHON="python3"
fi

exec "$PYTHON" "$SCRIPT_DIR/call_agent.py" --quiet "$@"
