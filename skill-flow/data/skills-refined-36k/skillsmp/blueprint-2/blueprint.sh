#!/bin/bash
# Blueprint - Unified Framework CLI
#
# Usage: blueprint.sh <submodule> [args...]
#
# Submodules:
#   aegis     Gate validation and aspects
#   forma     Document templates
#   frontis   FrontMatter search and schemas
#   hermes    Agent handoff forms
#   lexis     Constitution viewer
#   polis     Agent registry
#   project   Project alias management

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SUBMODULE="$1"

# Show help
show_help() {
  cat << 'EOF'
Blueprint - Unified Framework CLI

Usage: blueprint.sh <submodule> [args...]

Submodules:
  aegis     Gate validation and aspects
  forma     Document templates
  frontis   FrontMatter search and schemas
  hermes    Agent handoff forms
  lexis     Constitution viewer
  plan      Plan directory and listing
  polis     Agent registry
  project   Project alias management

Options:
  --help, -h    Show this help
  --list, -l    List available submodules

Examples:
  blueprint.sh aegis --list
  blueprint.sh frontis search type spec
  blueprint.sh forma show spec-lib
  blueprint.sh hermes orchestrator specifier
  blueprint.sh lexis specifier
  blueprint.sh polis --list

Run 'blueprint.sh <submodule>' without args for submodule-specific help.
EOF
}

# List submodules
list_submodules() {
  echo "Available submodules:"
  echo ""
  printf "  %-12s %s\n" "aegis" "Gate validation and aspects"
  printf "  %-12s %s\n" "forma" "Document templates"
  printf "  %-12s %s\n" "frontis" "FrontMatter search and schemas"
  printf "  %-12s %s\n" "hermes" "Agent handoff forms"
  printf "  %-12s %s\n" "lexis" "Constitution viewer"
  printf "  %-12s %s\n" "plan" "Plan directory and listing"
  printf "  %-12s %s\n" "polis" "Agent registry"
  printf "  %-12s %s\n" "project" "Project alias management"
}

# Main dispatch
case "$SUBMODULE" in
  aegis|forma|frontis|hermes|lexis|plan|polis|project)
    shift
    exec "$SCRIPT_DIR/$SUBMODULE/$SUBMODULE.sh" "$@"
    ;;
  --help|-h)
    show_help
    ;;
  --list|-l)
    list_submodules
    ;;
  "")
    show_help
    ;;
  *)
    echo "[ERROR] Unknown submodule: $SUBMODULE" >&2
    echo ""
    list_submodules
    exit 1
    ;;
esac
