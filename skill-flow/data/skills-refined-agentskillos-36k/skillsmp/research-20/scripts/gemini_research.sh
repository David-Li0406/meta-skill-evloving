#! /bin/zsh

set -euo pipefail

# Absolute directory of this script, even when sourced or symlinked
SCRIPT_DIR="${0:A:h}"

exec "${SCRIPT_DIR}/gemini_research.py" "$@"
