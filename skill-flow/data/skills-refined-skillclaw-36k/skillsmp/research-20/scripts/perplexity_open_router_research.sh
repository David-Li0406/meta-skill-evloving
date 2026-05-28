#! /bin/zsh

set -euo pipefail

# Absolute directory of this script, even when sourced or symlinked
SCRIPT_DIR="${0:A:h}"

exec "${SCRIPT_DIR}/perplexity_open_router_research.py" "$@"
