#!/usr/bin/env bash
# Generic tmux session creation template
# This demonstrates the pattern for creating multi-window, multi-pane sessions

set -euo pipefail

SESSION_NAME="${1:-dev-session}"
WORK_DIR="${2:-.}"

# Check if session already exists
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "Session '$SESSION_NAME' already exists, attaching..."
    tmux attach-session -t "$SESSION_NAME"
    exit 0
fi

echo "Creating session: $SESSION_NAME"

# Create first window
tmux new-session -d -s "$SESSION_NAME" -n main -c "$WORK_DIR"

# Split the window horizontally (side-by-side)
tmux split-window -h -t "$SESSION_NAME:main" -c "$WORK_DIR"

# Create second window
tmux new-window -t "$SESSION_NAME" -n secondary -c "$WORK_DIR"

# Split second window vertically (stacked)
tmux split-window -v -t "$SESSION_NAME:secondary" -c "$WORK_DIR"

# Optional: Send commands to specific panes
# tmux send-keys -t "$SESSION_NAME:main.1" "nvim" C-m
# tmux send-keys -t "$SESSION_NAME:secondary.1" "npm run dev" C-m

# Select first window
tmux select-window -t "$SESSION_NAME:main"

# Attach to the session
tmux attach-session -t "$SESSION_NAME"
