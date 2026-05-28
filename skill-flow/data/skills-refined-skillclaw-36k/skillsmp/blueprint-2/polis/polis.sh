#!/bin/bash
# Polis - Agent Registry Viewer
# View available Agents and their descriptions
#
# Usage:
#   polis --list                     List all agents with descriptions
#   polis <agent>                    Show agent instruction

set -e

# Source common functions
source "$(dirname "$0")/../_common.sh"

# Note: Agents are global (not per-project), no initialization check needed
AGENTS_DIR="$HOME/.claude/agents"

# Check if agents directory exists
if [ ! -d "$AGENTS_DIR" ]; then
  error "Agents directory not found: $AGENTS_DIR"
  exit 1
fi

# --list: Show all agents with descriptions
if [ "$1" = "--list" ] || [ "$1" = "-l" ]; then
  found=0
  echo "Available Agents:"
  echo ""
  for file in "$AGENTS_DIR"/*.md; do
    if [ -f "$file" ]; then
      name=$(basename "$file" .md)
      if [ "$name" != "README" ]; then
        desc=$(get_description "$file")
        printf "  %-15s %s\n" "$name" "$desc"
        found=1
      fi
    fi
  done

  if [ "$found" -eq 0 ]; then
    echo "  (no agents found)"
  fi
  exit 0
fi

# No argument: show usage
if [ -z "$1" ]; then
  echo "Polis - Agent Registry Viewer"
  echo ""
  echo "Usage:"
  echo "  polis --list               List all agents with descriptions"
  echo "  polis <agent>              Show agent instruction"
  echo ""
  echo "Examples:"
  echo "  blueprint.sh polis --list"
  echo "  blueprint.sh polis reviewer"
  exit 1
fi

AGENT="$1"
AGENT_FILE="$AGENTS_DIR/$AGENT.md"

# Check if agent exists
if [ ! -f "$AGENT_FILE" ]; then
  error "Agent not found: $AGENT"
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

# Show agent instruction
cat "$AGENT_FILE"
