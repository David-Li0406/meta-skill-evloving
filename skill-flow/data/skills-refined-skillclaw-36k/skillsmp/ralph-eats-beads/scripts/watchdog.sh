#!/bin/bash
# Ralph Watchdog - active health monitor that unblocks stuck agents
# Usage: ./watchdog.sh <session-name> [check-interval-seconds]
#
# Runs a Claude agent that monitors the ralph session and takes action
# on stuck subagents. Runs in a separate tmux window within the session.

set -e

RALPH_ID="${1:-ralph}"
CHECK_INTERVAL="${2:-60}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPT_FILE="$SCRIPT_DIR/watchdog-prompt.md"

# Detect project directory from session
PROJECT_DIR=$(tmux display-message -t "$RALPH_ID:parent" -p '#{pane_current_path}' 2>/dev/null || pwd)

if ! tmux has-session -t "$RALPH_ID" 2>/dev/null; then
  echo "Error: Session '$RALPH_ID' does not exist"
  exit 1
fi

if [ ! -f "$PROMPT_FILE" ]; then
  echo "Error: Prompt file not found: $PROMPT_FILE"
  exit 1
fi

echo "Starting watchdog for session: $RALPH_ID"
echo "  Check interval: ${CHECK_INTERVAL}s"
echo "  Project dir: $PROJECT_DIR"
echo "  Prompt: $PROMPT_FILE"

# Check if watchdog window already exists
if tmux list-windows -t "$RALPH_ID" -F '#{window_name}' 2>/dev/null | grep -q '^watchdog$'; then
  echo "Watchdog window already exists. Attaching..."
  tmux select-window -t "$RALPH_ID:watchdog"
  exit 0
fi

# Create watchdog window with Claude agent
tmux new-window -t "$RALPH_ID" -n "watchdog" "
export RALPH_ID='$RALPH_ID'
export CHECK_INTERVAL='$CHECK_INTERVAL'
export PROJECT_DIR='$PROJECT_DIR'

cd '$PROJECT_DIR'

cat << 'PROMPT_EOF' | claude --dangerously-skip-permissions
$(cat "$PROMPT_FILE")

## Current Environment
- RALPH_ID=$RALPH_ID
- CHECK_INTERVAL=$CHECK_INTERVAL
- PROJECT_DIR=$PROJECT_DIR

Begin your monitoring loop now.
PROMPT_EOF

echo 'Watchdog exited. Press any key to close.'
read -n 1
"

echo "Watchdog started in window 'watchdog'"
echo "  Attach: tmux select-window -t $RALPH_ID:watchdog"
