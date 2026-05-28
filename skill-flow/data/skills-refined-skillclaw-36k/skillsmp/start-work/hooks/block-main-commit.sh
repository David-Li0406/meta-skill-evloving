#!/bin/bash
set -euo pipefail

# Read hook input from stdin
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command // empty')

# Check if this is a git commit/push command
if echo "$command" | grep -qE 'git\s+(commit|push)'; then
  # Get current branch
  current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")

  if [[ "$current_branch" == "main" || "$current_branch" == "master" ]]; then
    echo "Error: Commits to $current_branch branch are prohibited. Create a feature branch first." >&2
    exit 2  # Exit code 2 blocks the tool call
  fi
fi

exit 0
