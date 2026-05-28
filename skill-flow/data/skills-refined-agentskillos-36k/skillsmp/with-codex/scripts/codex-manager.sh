#!/bin/bash
#
# codex-manager.sh - Manages tmux pane with Codex CLI
# For use with Claude Code "with-codex" skill on Windows/WSL
#
# This script splits the CURRENT tmux pane to create a Codex pane
# (instead of creating a separate detached session)
#

set -e

# Configuration
CODEX_PANE_TITLE="codex"
CODEX_BG_COLOR="colour233" # Dark background for Codex pane

# File to store Codex pane ID
PANE_ID_FILE="/tmp/codex-pane-id"

# Utility functions
log_info() {
  echo "[INFO] $1" >&2
}

log_error() {
  echo "[ERROR] $1" >&2
}

# Check if codex CLI is available
check_codex() {
  if ! command -v codex &>/dev/null; then
    log_error "Codex CLI not found. Please install it first: npm install -g @openai/codex"
    exit 1
  fi
}

# Check if we're inside a tmux session
check_tmux() {
  if [ -z "$TMUX" ]; then
    log_error "Not running inside tmux. Please start Claude Code inside a tmux session."
    log_error "Run: tmux new-session -s claude"
    log_error "Then start Claude Code inside that session."
    exit 1
  fi
}

# Get the stored Codex pane ID
get_codex_pane() {
  if [ -f "$PANE_ID_FILE" ]; then
    local pane_id=$(cat "$PANE_ID_FILE")
    # Verify pane still exists
    if tmux list-panes -F '#{pane_id}' | grep -q "^${pane_id}$"; then
      echo "$pane_id"
      return 0
    fi
  fi
  echo ""
}

# Check if Codex pane exists
codex_pane_exists() {
  local pane_id=$(get_codex_pane)
  [ -n "$pane_id" ]
}

# Setup: Split current pane and start Codex
cmd_setup() {
  log_info "Setting up Codex pane in current tmux session..."

  check_codex
  check_tmux

  # Check if Codex pane already exists
  if codex_pane_exists; then
    local existing_pane=$(get_codex_pane)
    log_info "Codex pane already exists: $existing_pane"
    echo "PANE_EXISTS:$existing_pane"
    return 0
  fi

  # Get current pane ID (Claude's pane)
  local claude_pane=$(tmux display-message -p '#{pane_id}')

  # Split the current pane horizontally (creates pane on the right)
  tmux split-window -h -d

  # Get the new pane ID (the one we just created)
  local codex_pane=$(tmux list-panes -F '#{pane_id}' | tail -1)

  # Save the Codex pane ID for later use
  echo "$codex_pane" >"$PANE_ID_FILE"

  # Set pane title for identification
  tmux select-pane -t "$codex_pane" -T "$CODEX_PANE_TITLE"

  # Set distinctive background color for Codex pane
  tmux select-pane -t "$codex_pane" -P "bg=$CODEX_BG_COLOR"

  # Start Codex in the right pane (interactive mode)
  tmux send-keys -t "$codex_pane" "codex" Enter

  # Wait for Codex to initialize (needs more time to fully start)
  sleep 5

  # Focus stays on Claude's pane (left side)
  tmux select-pane -t "$claude_pane"

  log_info "Codex pane created: $codex_pane"
  echo "PANE_CREATED:$codex_pane"
}

# Send a prompt to the Codex pane
cmd_send() {
  local prompt="$1"

  if [ -z "$prompt" ]; then
    log_error "No prompt provided. Usage: $0 send \"your prompt\""
    exit 1
  fi

  check_tmux

  if ! codex_pane_exists; then
    log_error "Codex pane does not exist. Run 'setup' first."
    exit 1
  fi

  local codex_pane=$(get_codex_pane)

  log_info "Sending prompt to Codex pane: $codex_pane"

  # Clear any existing input
  tmux send-keys -t "$codex_pane" C-u

  # Use -l (literal) flag to send text without interpreting special characters
  # This handles Japanese text, spaces, and special characters correctly
  tmux send-keys -t "$codex_pane" -l "$prompt"

  # Small delay before pressing Enter
  sleep 0.5

  # Send Enter key separately
  tmux send-keys -t "$codex_pane" Enter

  echo "PROMPT_SENT:$codex_pane"
}

# Capture output from the Codex pane
cmd_capture() {
  local lines="${1:-100}" # Default to last 100 lines

  check_tmux

  if ! codex_pane_exists; then
    log_error "Codex pane does not exist."
    exit 1
  fi

  local codex_pane=$(get_codex_pane)

  # Capture pane content
  # -p: print to stdout
  # -S: start line (negative = from end of history)
  # -J: join wrapped lines
  tmux capture-pane -t "$codex_pane" -p -S "-$lines" -J
}

# Wait for Codex response (polls until output stabilizes)
cmd_wait() {
  local timeout="${1:-60}" # Default 60 second timeout
  local poll_interval=2
  local elapsed=0
  local prev_content=""
  local stable_count=0
  local required_stable=3 # Need 3 consecutive stable reads

  check_tmux

  if ! codex_pane_exists; then
    log_error "Codex pane does not exist."
    exit 1
  fi

  log_info "Waiting for Codex response (timeout: ${timeout}s)..."

  while [ $elapsed -lt $timeout ]; do
    local current_content=$(cmd_capture 50)

    if [ "$current_content" = "$prev_content" ]; then
      ((stable_count++)) || true
      if [ $stable_count -ge $required_stable ]; then
        log_info "Response stabilized after ${elapsed}s"
        echo "RESPONSE_READY"
        return 0
      fi
    else
      stable_count=0
      prev_content="$current_content"
    fi

    sleep $poll_interval
    ((elapsed += poll_interval)) || true
  done

  log_error "Timeout waiting for response"
  echo "TIMEOUT"
  return 1
}

# Cleanup: Close the Codex pane
cmd_cleanup() {
  check_tmux

  if codex_pane_exists; then
    local codex_pane=$(get_codex_pane)
    log_info "Closing Codex pane: $codex_pane"

    # Send exit command to Codex first
    tmux send-keys -t "$codex_pane" "/exit" Enter 2>/dev/null || true
    sleep 1

    # Kill the pane
    tmux kill-pane -t "$codex_pane" 2>/dev/null || true

    # Remove the pane ID file
    rm -f "$PANE_ID_FILE"

    echo "PANE_CLOSED"
  else
    log_info "Codex pane does not exist."
    echo "NO_PANE"
  fi
}

# Status: Check pane status
cmd_status() {
  check_tmux

  if codex_pane_exists; then
    local codex_pane=$(get_codex_pane)
    echo "PANE_EXISTS:$codex_pane"
    tmux list-panes -F 'Pane #{pane_index}: #{pane_id} (#{pane_width}x#{pane_height}) Title: #{pane_title}'
  else
    echo "NO_PANE"
  fi
}

# Focus: Switch focus to Codex pane
cmd_focus() {
  check_tmux

  if codex_pane_exists; then
    local codex_pane=$(get_codex_pane)
    tmux select-pane -t "$codex_pane"
    echo "FOCUSED:$codex_pane"
  else
    log_error "Codex pane does not exist."
    exit 1
  fi
}

# Main command dispatcher
case "${1:-}" in
setup)
  cmd_setup
  ;;
send)
  cmd_send "$2"
  ;;
capture)
  cmd_capture "${2:-100}"
  ;;
wait)
  cmd_wait "${2:-60}"
  ;;
cleanup)
  cmd_cleanup
  ;;
status)
  cmd_status
  ;;
focus)
  cmd_focus
  ;;
*)
  echo "Usage: $0 {setup|send|capture|wait|cleanup|status|focus}"
  echo ""
  echo "Commands:"
  echo "  setup              Split current pane and start Codex on the right"
  echo "  send \"prompt\"      Send a prompt to the Codex pane"
  echo "  capture [lines]    Capture output from Codex pane (default: 100 lines)"
  echo "  wait [timeout]     Wait for Codex response to stabilize (default: 60s)"
  echo "  cleanup            Close the Codex pane"
  echo "  status             Show pane status"
  echo "  focus              Switch focus to Codex pane"
  echo ""
  echo "IMPORTANT: Must be run inside a tmux session!"
  echo "Start Claude Code inside tmux: tmux new-session -s claude"
  exit 1
  ;;
esac
