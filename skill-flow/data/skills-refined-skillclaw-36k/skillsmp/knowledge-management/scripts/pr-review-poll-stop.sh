#!/bin/bash
# Stop PR Review Polling Daemon
#
# Usage: ./pr-review-poll-stop.sh

set -euo pipefail

PID_FILE="${HOME}/.pr-review-poll.pid"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [[ ! -f "$PID_FILE" ]]; then
    echo -e "${YELLOW}Daemon is not running (no PID file found)${NC}"
    exit 0
fi

daemon_pid=$(cat "$PID_FILE")

if ps -p "$daemon_pid" > /dev/null 2>&1; then
    echo -e "${YELLOW}Stopping daemon (PID: $daemon_pid)...${NC}"
    kill "$daemon_pid"

    # Wait for process to terminate
    for i in {1..10}; do
        if ! ps -p "$daemon_pid" > /dev/null 2>&1; then
            break
        fi
        sleep 0.5
    done

    # Force kill if still running
    if ps -p "$daemon_pid" > /dev/null 2>&1; then
        echo -e "${RED}Force killing...${NC}"
        kill -9 "$daemon_pid" 2>/dev/null || true
    fi

    rm -f "$PID_FILE"
    echo -e "${GREEN}✓ Daemon stopped${NC}"
else
    echo -e "${YELLOW}Daemon not running (stale PID file removed)${NC}"
    rm -f "$PID_FILE"
fi
