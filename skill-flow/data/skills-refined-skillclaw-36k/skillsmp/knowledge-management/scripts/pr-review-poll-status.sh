#!/bin/bash
# Check PR Review Polling Daemon Status
#
# Usage: ./pr-review-poll-status.sh

set -euo pipefail

PID_FILE="${HOME}/.pr-review-poll.pid"
LOG_FILE="${HOME}/.pr-review-poll.log"
STATE_FILE="${HOME}/.pr-review-state.json"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           PR Review Polling Daemon Status                  ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check daemon status
if [[ -f "$PID_FILE" ]]; then
    daemon_pid=$(cat "$PID_FILE")
    if ps -p "$daemon_pid" > /dev/null 2>&1; then
        echo -e "Status: ${GREEN}Running${NC} (PID: $daemon_pid)"

        # Get process info
        start_time=$(ps -p "$daemon_pid" -o lstart= 2>/dev/null | xargs)
        echo -e "Started: ${GREEN}$start_time${NC}"
    else
        echo -e "Status: ${RED}Not running${NC} (stale PID file)"
    fi
else
    echo -e "Status: ${RED}Not running${NC}"
fi

echo ""

# Check state file
echo -e "${BLUE}State File:${NC} $STATE_FILE"
if [[ -f "$STATE_FILE" ]]; then
    pr_count=$(jq 'keys | length' "$STATE_FILE" 2>/dev/null || echo "0")
    echo -e "Tracked PRs: ${GREEN}$pr_count${NC}"

    if [[ "$pr_count" != "0" ]]; then
        echo ""
        echo "PR States:"
        jq -r 'to_entries[] | "  #\(.key): last checked \(.value.checked_at | strftime("%Y-%m-%d %H:%M:%S") // "unknown")"' "$STATE_FILE" 2>/dev/null || true
    fi
else
    echo -e "Tracked PRs: ${YELLOW}None (state file not found)${NC}"
fi

echo ""

# Check log file
echo -e "${BLUE}Log File:${NC} $LOG_FILE"
if [[ -f "$LOG_FILE" ]]; then
    log_size=$(du -h "$LOG_FILE" | cut -f1)
    echo -e "Size: ${GREEN}$log_size${NC}"
    echo ""
    echo "Last 5 lines:"
    tail -5 "$LOG_FILE" | sed 's/^/  /'
else
    echo -e "Size: ${YELLOW}Not found${NC}"
fi

echo ""
echo -e "${BLUE}Commands:${NC}"
echo "  Start:  ./pr-review-poll-start.sh"
echo "  Stop:   ./pr-review-poll-stop.sh"
echo "  Logs:   tail -f $LOG_FILE"
