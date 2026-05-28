#!/bin/bash
# Ralph Planner - Recursive planning loop
# Runs iterations until bd plan fully covers input requirements
# Auto-detects session name from git repo, supports multiple concurrent planners

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Auto-detect session name from git repo, allow override
detect_session_name() {
  if [ -n "$RALPH_ID" ]; then
    echo "${RALPH_ID}-plan"
  elif git rev-parse --show-toplevel &>/dev/null; then
    echo "$(basename "$(git rev-parse --show-toplevel)")-plan"
  else
    echo "$(basename "$PWD")-plan"
  fi
}

MAX_ITERATIONS=${2:-3}
REQUIREMENTS_FILE="${1:-}"
COMPLETION_MARKER="/tmp/planner-complete-$$"

# Usage check
if [[ -z "$REQUIREMENTS_FILE" && -t 0 ]]; then
  echo "Usage: planner.sh <requirements-file> [max_iterations]"
  echo "   or: echo 'requirements' | planner.sh - [max_iterations]"
  echo ""
  echo "Examples:"
  echo "  ./planner.sh requirements.md"
  echo "  ./planner.sh requirements.md 10"
  echo "  cat feature-spec.md | ./planner.sh - 5"
  echo ""
  echo "Environment variables:"
  echo "  RALPH_ID - Override auto-detected session name prefix"
  echo ""
  echo "Session name is auto-detected from git repo (e.g., myproject-plan)"
  exit 1
fi

# Read requirements from file or stdin
if [[ -n "$REQUIREMENTS_FILE" && "$REQUIREMENTS_FILE" != "-" ]]; then
  if [[ ! -f "$REQUIREMENTS_FILE" ]]; then
    echo "Error: File not found: $REQUIREMENTS_FILE"
    exit 1
  fi
  REQUIREMENTS=$(cat "$REQUIREMENTS_FILE")
  PLAN_PATH=$(realpath "$REQUIREMENTS_FILE")
else
  REQUIREMENTS=$(cat)
  # Save stdin to temp file so agent can re-read it
  PLAN_PATH=$(mktemp --suffix=.md)
  echo "$REQUIREMENTS" > "$PLAN_PATH"
  echo "Saved stdin to: $PLAN_PATH"
fi

if [[ -z "$REQUIREMENTS" ]]; then
  echo "Error: No requirements provided"
  exit 1
fi

SESSION=$(detect_session_name)

# Check if session already exists
if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "⚠ Session '$SESSION' already running."
  echo ""
  echo "Options:"
  echo "  tmux attach -t $SESSION        # Attach to existing"
  echo "  tmux kill-session -t $SESSION  # Kill and restart"
  echo "  RALPH_ID=other ./planner.sh    # Use different name"
  exit 1
fi

# Clean up any previous state
rm -f "$COMPLETION_MARKER"

# Create session
tmux new-session -d -s "$SESSION" -n "parent"

echo "Planning loop started: $SESSION"
echo "   Attach: tmux attach -t $SESSION"
echo "   Max iterations: $MAX_ITERATIONS"
echo "   Plan file: $PLAN_PATH"
echo ""

# Build command that syncs and marks complete on exit
CLAUDE_CMD="cd '$(dirname "$PLAN_PATH")' 2>/dev/null || true; MAX_ITERATIONS=$MAX_ITERATIONS PLAN_PATH='$PLAN_PATH' cat '$SCRIPT_DIR/planner-prompt.md' | claude --dangerously-skip-permissions; EXIT_CODE=\$?; echo ''; echo 'Agent exited. Syncing...'; bd sync 2>/dev/null || echo 'bd sync skipped'; touch '$COMPLETION_MARKER'; exit \$EXIT_CODE"

# Launch planner agent
tmux send-keys -t "$SESSION:parent" "$CLAUDE_CMD" Enter

echo "Planner loop launched. Monitoring for completion..."
echo "(Ctrl+C to detach - planner will continue in background)"
echo ""

# Monitor for completion (check every 10 seconds, timeout after 30 minutes)
TIMEOUT=1800
ELAPSED=0
INTERVAL=10

while [ $ELAPSED -lt $TIMEOUT ]; do
  sleep $INTERVAL
  ELAPSED=$((ELAPSED + INTERVAL))

  # Check if completion marker exists
  if [ -f "$COMPLETION_MARKER" ]; then
    rm -f "$COMPLETION_MARKER"
    echo ""
    echo "✓ Planner completed (${ELAPSED}s)"

    # Capture final output
    echo ""
    echo "=== Final Summary ==="
    tmux capture-pane -t "$SESSION:parent" -p -S -50 2>/dev/null | grep -A 100 "Plan Complete\|Coverage Verification\|Total Stories" | head -40 || true
    echo "===================="

    # Clean up session
    tmux kill-session -t "$SESSION" 2>/dev/null || true

    # Show next steps
    echo ""
    echo "Next steps:"
    echo "  bd ready              # See available work"
    echo "  ./ralph.sh 25         # Start implementation loop"
    exit 0
  fi

  # Check if session still exists
  if ! tmux has-session -t "$SESSION" 2>/dev/null; then
    echo ""
    echo "⚠ Session ended unexpectedly"
    rm -f "$COMPLETION_MARKER"
    exit 1
  fi

  # Progress indicator (every minute show elapsed time)
  if [ $((ELAPSED % 60)) -eq 0 ]; then
    echo " ${ELAPSED}s..."
  else
    printf "."
  fi
done

# Timeout reached
echo ""
echo "⚠ Timeout reached (${TIMEOUT}s). Session still running."
echo "   Attach to check: tmux attach -t $SESSION"
echo "   Kill if stuck:   tmux kill-session -t $SESSION"
rm -f "$COMPLETION_MARKER"
exit 1
