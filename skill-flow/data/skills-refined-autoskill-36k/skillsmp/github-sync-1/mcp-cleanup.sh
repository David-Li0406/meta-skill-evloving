#!/bin/bash
# MCP Process Cleanup - kills orphan MCP server processes
# Part of Claude Code Sync system
#
# Usage:
#   mcp-cleanup.sh              # Kill orphans not from current session
#   mcp-cleanup.sh 0 true       # Kill all orphans, quiet mode (for hooks)
#   mcp-cleanup.sh --list       # Just list orphans, don't kill
#
# Integrated with:
#   - SessionEnd hook (automatic cleanup when session ends)
#   - git-sync-check.sh (daily orphan detection)

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Get current TTY to avoid killing current session's processes
CURRENT_TTY=$(tty 2>/dev/null | sed 's/\/dev\///' || echo "none")

# Arguments
MODE="${1:-kill}"  # kill, --list, or age in hours
QUIET="${2:-false}"

# MCP process patterns to look for
MCP_PATTERNS="mcp-remote|firebase.*mcp|xero-mcp|things-mcp|playwright.*mcp|@playwright/mcp|SuperThings"

log() {
    [[ "$QUIET" == "true" ]] && return
    echo -e "$1"
}

# List all MCP processes
list_mcp_processes() {
    ps aux | grep -E "$MCP_PATTERNS" | grep -v grep | grep -v "mcp-cleanup" || true
}

# Count orphan processes (not from current TTY)
count_orphans() {
    local count=0
    while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        local tty=$(echo "$line" | awk '{print $7}')
        [[ "$tty" != "$CURRENT_TTY" ]] && ((count++))
    done < <(list_mcp_processes)
    echo "$count"
}

# Kill orphan processes
kill_orphans() {
    local killed=0
    local skipped=0

    while IFS= read -r line; do
        [[ -z "$line" ]] && continue

        local pid=$(echo "$line" | awk '{print $2}')
        local tty=$(echo "$line" | awk '{print $7}')
        local cmd=$(echo "$line" | awk '{for(i=11;i<=NF;i++) printf "%s ", $i; print ""}' | head -c 60)

        # Skip current session's processes
        if [[ "$tty" == "$CURRENT_TTY" ]]; then
            ((skipped++))
            continue
        fi

        # Kill the process
        if kill "$pid" 2>/dev/null; then
            ((killed++))
            log "  ${GREEN}Killed${NC} PID $pid ($tty): $cmd"
        fi
    done < <(list_mcp_processes)

    echo "$killed"
}

# Main
case "$MODE" in
    --list|-l)
        log "${YELLOW}MCP Processes:${NC}"
        log "Current TTY: $CURRENT_TTY"
        log ""
        list_mcp_processes | while read -r line; do
            tty=$(echo "$line" | awk '{print $7}')
            if [[ "$tty" == "$CURRENT_TTY" ]]; then
                echo -e "${GREEN}[current]${NC} $line"
            else
                echo -e "${RED}[orphan]${NC} $line"
            fi
        done
        log ""
        log "Orphan count: $(count_orphans)"
        ;;
    --help|-h)
        echo "MCP Process Cleanup"
        echo ""
        echo "Usage:"
        echo "  mcp-cleanup.sh              Kill orphan MCP processes"
        echo "  mcp-cleanup.sh 0 true       Kill all, quiet mode (for hooks)"
        echo "  mcp-cleanup.sh --list       List all MCP processes"
        echo "  mcp-cleanup.sh --help       Show this help"
        echo ""
        echo "Patterns matched: $MCP_PATTERNS"
        ;;
    *)
        # Kill mode
        orphan_count=$(count_orphans)

        if [[ $orphan_count -eq 0 ]]; then
            log "${GREEN}No orphan MCP processes found${NC}"
            exit 0
        fi

        log "${YELLOW}Found $orphan_count orphan MCP process(es)${NC}"
        killed=$(kill_orphans)

        if [[ $killed -gt 0 ]]; then
            log "${GREEN}Cleaned up $killed orphan MCP process(es)${NC}"
        fi
        ;;
esac

exit 0
