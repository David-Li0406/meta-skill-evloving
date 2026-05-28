#!/bin/bash
# Hermes - Handoff Form Viewer
# View Handoff forms for commands and review
#
# Usage:
#   hermes --list                    List all Handoff forms
#   hermes <form>                    Show Handoff form (after-*, request:*, response:*)

set -e

# Source common functions
source "$(dirname "$0")/../_common.sh"

# Check project initialization
check_project_initialized

FORMS_FILE="$BLUEPRINT_DATA_DIR/forms/handoff.schema.md"

# Check if forms file exists
if [ ! -f "$FORMS_FILE" ]; then
  error "Handoff forms not found: $FORMS_FILE"
  exit 1
fi

# --list: Show all available Handoff forms
if [ "$1" = "--list" ] || [ "$1" = "-l" ]; then
  echo "Available Handoff forms:"
  echo ""

  found=0
  while read -r line; do
    obj=$(echo "$line" | sed 's/OBJECTIVE\[\([^]]*\)\]/\1/')
    echo "  - $obj"
    found=1
  done < <(grep -o 'OBJECTIVE\[[^]]*\]' "$FORMS_FILE" 2>/dev/null)

  if [ "$found" -eq 0 ]; then
    echo "  (no Handoff forms found)"
  fi
  exit 0
fi

# No argument: show usage
if [ -z "$1" ]; then
  echo "Hermes - Handoff Form Viewer"
  echo ""
  echo "Usage:"
  echo "  hermes --list              List all Handoff forms"
  echo "  hermes <form>              Show Handoff form"
  echo ""
  echo "Examples:"
  echo "  blueprint.sh hermes --list"
  echo "  blueprint.sh hermes after-save"
  echo "  blueprint.sh hermes after-load:quick"
  echo "  blueprint.sh hermes after-load:standard"
  echo "  blueprint.sh hermes request:review:session-state"
  exit 1
fi

# Handoff form query
MARKER="OBJECTIVE[$1]"

# Check if Handoff form exists
if ! grep -qF "$MARKER" "$FORMS_FILE"; then
  error "Handoff form not found: $1"
  echo ""
  echo "Available Handoff forms:"
  grep -o 'OBJECTIVE\[[^]]*\]' "$FORMS_FILE" 2>/dev/null | while read -r line; do
    obj=$(echo "$line" | sed 's/OBJECTIVE\[\([^]]*\)\]/\1/')
    echo "  - $obj"
  done
  exit 1
fi

# Extract content between ---s and ---e after the Handoff marker
awk -v marker="$MARKER" '
  index($0, marker) { found=1; next }
  found && /^---s$/ { start=1; next }
  found && /^---e$/ { exit }
  start { print }
' "$FORMS_FILE"
