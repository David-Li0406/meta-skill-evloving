#!/bin/bash
# Lexis - Constitution Viewer
# View agent-specific constitutions (base loaded via SessionStart hook)
#
# Usage:
#   lexis --list                     List all agents
#   lexis <agent>                    Show agent constitution
#   lexis --base                     Show base constitution only

set -e

# Source common functions
source "$(dirname "$0")/../_common.sh"

# Check project initialization
check_project_initialized

CONST_DIR="$BLUEPRINT_DATA_DIR/constitutions"
BASE_FILE="$CONST_DIR/base.md"
BLUEPRINT_FILE="$CONST_DIR/blueprint.md"
AGENTS_DIR="$CONST_DIR/agents"

# Check if constitutions exist
if [ ! -f "$BASE_FILE" ]; then
  error "Base constitution not found: $BASE_FILE"
  exit 1
fi

# --list: Show all agents
if [ "$1" = "--list" ] || [ "$1" = "-l" ]; then
  if [ ! -d "$AGENTS_DIR" ]; then
    error "Agents directory not found: $AGENTS_DIR"
    exit 1
  fi

  found=0
  echo "Available agents:"
  echo ""
  for file in "$AGENTS_DIR"/*.md; do
    if [ -f "$file" ]; then
      name=$(basename "$file" .md)
      if [ "$name" != "README" ]; then
        echo "  - $name"
        found=1
      fi
    fi
  done

  if [ "$found" -eq 0 ]; then
    echo "  (no agents found)"
  fi
  exit 0
fi

# --base: Show base constitution only
if [ "$1" = "--base" ] || [ "$1" = "-b" ]; then
  cat "$BASE_FILE"
  exit 0
fi

# --framework: Show framework constitution only
if [ "$1" = "--framework" ] || [ "$1" = "-f" ]; then
  if [ ! -f "$BLUEPRINT_FILE" ]; then
    error "Framework constitution not found: $BLUEPRINT_FILE"
    exit 1
  fi
  cat "$BLUEPRINT_FILE"
  exit 0
fi

# No argument: show usage
if [ -z "$1" ]; then
  echo "Lexis - Constitution Viewer"
  echo ""
  echo "Usage:"
  echo "  lexis --list               List all agents"
  echo "  lexis <agent>              Show agent constitution"
  echo "  lexis --base               Show project constitution only"
  echo "  lexis --framework          Show framework constitution only"
  echo ""
  echo "Examples:"
  echo "  blueprint.sh lexis --list"
  echo "  blueprint.sh lexis reviewer"
  echo "  blueprint.sh lexis --framework"
  exit 1
fi

AGENT="$1"
AGENT_FILE="$AGENTS_DIR/$AGENT.md"

# Check if agent exists
if [ ! -f "$AGENT_FILE" ]; then
  error "Agent constitution not found: $AGENT"
  echo ""
  echo "Available agents:"
  for file in "$AGENTS_DIR"/*.md; do
    if [ -f "$file" ]; then
      name=$(basename "$file" .md)
      if [ "$name" != "README" ]; then
        echo "  - $name"
      fi
    fi
  done
  exit 1
fi

# Show agent constitution only
# Note: Base constitution is loaded via SessionStart hook (session-init.sh)
cat "$AGENT_FILE"
