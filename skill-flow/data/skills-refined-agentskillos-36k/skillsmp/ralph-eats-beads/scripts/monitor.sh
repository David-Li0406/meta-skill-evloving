#!/bin/bash
# Ralph monitor - background watchdog for all ralph sessions
# Usage: ./monitor.sh [interval_minutes]
#   interval_minutes: check interval (default: 20)

set -e

INTERVAL_MIN=${1:-20}
INTERVAL_SEC=$((INTERVAL_MIN * 60))
LOG="/tmp/ralph-monitor.log"

echo "$(date): Ralph monitor started" > "$LOG"
echo "  Interval: ${INTERVAL_MIN}m" >> "$LOG"
echo "  Monitoring all ralph-* sessions" >> "$LOG"

# Track consecutive stuck checks per session
declare -A STUCK_COUNT

check_session() {
  local SESSION="$1"
  local PROJECT_DIR="$2"

  echo "" >> "$LOG"
  echo "--- $SESSION ---" >> "$LOG"

  # Count windows (1 = only parent)
  WINDOWS=$(tmux list-windows -t "$SESSION" 2>/dev/null | wc -l)
  WINDOW_NAMES=$(tmux list-windows -t "$SESSION" -F '#{window_name}' 2>/dev/null | tr '\n' ' ')
  echo "Windows ($WINDOWS): $WINDOW_NAMES" >> "$LOG"

  # Try to get bd stats from the session's working directory
  if [ -n "$PROJECT_DIR" ] && [ -d "$PROJECT_DIR/.beads" ]; then
    cd "$PROJECT_DIR" 2>/dev/null || true
    CLOSED=$(bd list --status=closed 2>/dev/null | grep -c "^[0-9]\|^\[" || echo "?")
    READY=$(bd ready 2>/dev/null | grep -c "^[0-9]\|^\[" || echo "?")
    IN_PROGRESS=$(bd list --status=in_progress 2>/dev/null | grep -c "^[0-9]\|^\[" || echo "?")
    echo "Closed: $CLOSED | In Progress: $IN_PROGRESS | Ready: $READY" >> "$LOG"
  else
    READY="?"
  fi

  # Check if done (no ready work and only parent window)
  if [ "$READY" = "0" ] && [ "$WINDOWS" -eq 1 ]; then
    echo "Status: COMPLETE" >> "$LOG"
    return 0
  fi

  # Check for stuck state (only parent window, but work remains)
  if [ "$WINDOWS" -eq 1 ] && [ "$READY" != "?" ] && [ "$READY" -gt 0 ]; then
    STUCK_COUNT[$SESSION]=$((${STUCK_COUNT[$SESSION]:-0} + 1))
    echo "Warning: Only parent but $READY tasks ready (stuck: ${STUCK_COUNT[$SESSION]})" >> "$LOG"

    if [ "${STUCK_COUNT[$SESSION]}" -ge 2 ]; then
      echo "Status: STUCK" >> "$LOG"
    fi
  else
    STUCK_COUNT[$SESSION]=0
    if [ "$WINDOWS" -gt 1 ]; then
      echo "Status: RUNNING ($((WINDOWS - 1)) agents)" >> "$LOG"
    else
      echo "Status: IDLE" >> "$LOG"
    fi
  fi

  # Capture recent parent output
  echo "--- Parent tail ---" >> "$LOG"
  tmux capture-pane -t "$SESSION:parent" -p -S -5 2>/dev/null | tail -3 >> "$LOG" || true
}

while true; do
  sleep "$INTERVAL_SEC"

  echo "" >> "$LOG"
  echo "=== $(date) ===" >> "$LOG"

  # Find all ralph sessions
  SESSIONS=$(tmux list-sessions -F '#{session_name}' 2>/dev/null | grep -E '^ralph-' || true)

  if [ -z "$SESSIONS" ]; then
    echo "No ralph sessions found" >> "$LOG"
    continue
  fi

  for SESSION in $SESSIONS; do
    # Try to detect project directory from session
    # Look at the parent pane's current directory
    PROJECT_DIR=$(tmux display-message -t "$SESSION:parent" -p '#{pane_current_path}' 2>/dev/null || echo "")
    check_session "$SESSION" "$PROJECT_DIR"
  done

  # Also check for planner sessions
  PLAN_SESSIONS=$(tmux list-sessions -F '#{session_name}' 2>/dev/null | grep -E 'plan$' || true)
  for SESSION in $PLAN_SESSIONS; do
    echo "" >> "$LOG"
    echo "--- $SESSION (planner) ---" >> "$LOG"
    WINDOWS=$(tmux list-windows -t "$SESSION" 2>/dev/null | wc -l)
    echo "Windows: $WINDOWS" >> "$LOG"
    echo "--- Output tail ---" >> "$LOG"
    tmux capture-pane -t "$SESSION:parent" -p -S -5 2>/dev/null | tail -3 >> "$LOG" || true
  done
done
