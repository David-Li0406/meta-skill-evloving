#!/bin/bash
# Start PR Review Polling Daemon in background
#
# Usage: ./pr-review-poll-start.sh [options]
# Options:
#   --interval N       Polling interval in seconds (default: 300)
#   --repo OWNER/REPO  Specific repo to monitor
#   --auto-respond     Auto-spawn Claude CLI to handle reviews
#   --working-dir DIR  Working directory for Claude (required with --auto-respond)
#   --include-copilot  Include Copilot reviews (default: enabled)
#   --no-copilot       Exclude Copilot reviews
#   -h, --help         Show this help message

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
POLL_SCRIPT="${SCRIPT_DIR}/pr-review-poll.sh"
PID_FILE="${HOME}/.pr-review-poll.pid"
LOG_FILE="${HOME}/.pr-review-poll.log"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

show_help() {
    cat << EOF
Start PR Review Polling Daemon

Usage: ./pr-review-poll-start.sh [options]

Options:
  --interval N         Polling interval in seconds (default: 300 = 5 minutes)
  --repo OWNER/REPO    Specific repo to monitor
  --auto-respond       Auto-spawn Claude CLI to handle reviews
  --working-dir DIR    Working directory for Claude (required with --auto-respond)
  --include-copilot    Include Copilot reviews (default: enabled)
  --no-copilot         Exclude Copilot reviews from notifications
  -h, --help           Show this help message

Files:
  PID file: $PID_FILE
  Log file: $LOG_FILE

Examples:
  # Basic polling with notifications only
  ./pr-review-poll-start.sh --interval 60

  # Auto-respond mode - Claude handles reviews automatically
  ./pr-review-poll-start.sh --auto-respond --working-dir /path/to/repo

EOF
}

# Check if already running
if [[ -f "$PID_FILE" ]]; then
    existing_pid=$(cat "$PID_FILE")
    if ps -p "$existing_pid" > /dev/null 2>&1; then
        echo -e "${YELLOW}Daemon already running (PID: $existing_pid)${NC}"
        echo "Use pr-review-poll-stop.sh to stop it first"
        exit 1
    else
        # Stale PID file
        rm -f "$PID_FILE"
    fi
fi

# Parse arguments and pass to poll script
ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            ARGS+=("$1")
            shift
            ;;
    esac
done

# Start daemon in background
echo -e "${GREEN}Starting PR Review Polling Daemon...${NC}"

nohup "$POLL_SCRIPT" "${ARGS[@]}" >> "$LOG_FILE" 2>&1 &
daemon_pid=$!

# Save PID
echo "$daemon_pid" > "$PID_FILE"

echo -e "${GREEN}✓ Daemon started (PID: $daemon_pid)${NC}"
echo ""
echo "Log file: $LOG_FILE"
echo "To view logs: tail -f $LOG_FILE"
echo "To stop: ./pr-review-poll-stop.sh"
