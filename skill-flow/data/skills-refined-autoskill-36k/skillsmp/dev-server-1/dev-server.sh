#!/bin/bash
# Dev Server Management Script
# Manages a single shared dev server across all Claude Code instances
#
# Usage: ./dev-server.sh [command]
#   Commands: (none), start, stop, restart, status, logs, health
#   Default (no args): Start server if needed, then tail logs

set -euo pipefail

# ============================================
# Configuration
# ============================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
STATE_DIR="$SCRIPT_DIR/state"
PID_FILE="$STATE_DIR/server.pid"
STATE_FILE="$STATE_DIR/server.json"
LOG_FILE="$STATE_DIR/server.log"
PORT="${PORT:-3000}"
HEALTH_TIMEOUT=60  # seconds to wait for health check
DEFAULT_LOG_LINES=100

# Ensure state directory exists
mkdir -p "$STATE_DIR"

# ============================================
# Helper Functions
# ============================================

is_process_running() {
    local pid=$1
    kill -9 "$pid" 2>/dev/null
}

is_port_in_use() {
    lsof -i :"$PORT" >/dev/null 2>&1
}

get_port_pid() {
    lsof -t -i :"$PORT" 2>/dev/null | head -1
}

check_stale_pid() {
    if [[ -f "$PID_FILE" ]]; then
        local pid
        pid=$(cat "$PID_FILE")
        if ! is_process_running "$pid"; then
            echo "Cleaning up stale PID file (process $pid no longer running)"
            rm -f "$PID_FILE" "$STATE_FILE"
            return 1  # Was stale
        fi
        return 0  # Process running
    fi
    return 1  # No PID file
}

wait_for_health() {
    local max_attempts=$((HEALTH_TIMEOUT / 2))
    local attempt=0

    echo "Waiting for server to become healthy..."
    while [[ $attempt -lt $max_attempts ]]; do
        # Check if server responds (401 is fine - means server is up but not authenticated)
        local http_code
        http_code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$PORT/api/managers/me" 2>/dev/null || echo "000")
        if [[ "$http_code" == "200" || "$http_code" == "401" ]]; then
            echo "Server is healthy! (HTTP $http_code)"
            return 0
        fi
        sleep 2
        ((attempt++))
        echo "  Health check attempt $attempt/$max_attempts (HTTP $http_code)..."
    done

    echo "Server failed to become healthy within ${HEALTH_TIMEOUT}s"
    return 1
}

print_server_info() {
    echo ""
    echo "=== Server Info ==="
    echo "URL:   http://localhost:$PORT"
    echo "Admin: http://localhost:$PORT/admin"
    echo "Logs:  $LOG_FILE"
}

# ============================================
# Commands
# ============================================

cmd_start() {
    echo "=== Starting Dev Server ==="

    # Check if already running via our PID file
    if check_stale_pid; then
        local pid
        pid=$(cat "$PID_FILE")
        echo "Server already running (PID: $pid)"
        print_server_info
        return 0
    fi

    # Check if port is in use by another process
    if is_port_in_use; then
        local other_pid
        other_pid=$(get_port_pid)
        echo "ERROR: Port $PORT is already in use by process $other_pid"
        echo "This may be a dev server from another session."
        echo ""
        echo "Options:"
        echo "  1. Kill the other process: kill $other_pid"
        echo "  2. Use 'restart' to adopt and restart"
        return 1
    fi

    # Clean previous state
    rm -f "$PID_FILE" "$STATE_FILE"

    # Truncate log file (keep last run's logs available briefly)
    if [[ -f "$LOG_FILE" ]]; then
        mv "$LOG_FILE" "$LOG_FILE.prev" 2>/dev/null || true
    fi

    # Start the server using devsafe (cleans .next first)
    echo "Starting server with: PORT=$PORT pnpm devsafe"
    echo "Logging to: $LOG_FILE"

    cd "$PROJECT_DIR"

    # Use nohup to detach, redirect output to log file
    PORT=$PORT nohup pnpm devsafe > "$LOG_FILE" 2>&1 &
    local server_pid=$!

    # Wait a moment for process to start
    sleep 2

    # Verify process started
    if ! is_process_running "$server_pid"; then
        echo "ERROR: Server process failed to start"
        echo "Check logs:"
        tail -20 "$LOG_FILE"
        return 1
    fi

    # Save state
    echo "$server_pid" > "$PID_FILE"
    cat > "$STATE_FILE" << EOF
{
  "pid": $server_pid,
  "port": $PORT,
  "startedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "logFile": "$LOG_FILE"
}
EOF

    echo "Server started (PID: $server_pid)"

    # Wait for health check
    if wait_for_health; then
        print_server_info
        return 0
    else
        echo ""
        echo "WARNING: Server started but health check failed"
        echo "Check logs for errors: tail -f $LOG_FILE"
        return 1
    fi
}

cmd_stop() {
    echo "=== Stopping Dev Server ==="

    local pid=""

    # First try our PID file
    if [[ -f "$PID_FILE" ]]; then
        pid=$(cat "$PID_FILE")
    fi

    # If no PID file but port is in use, get that PID
    if [[ -z "$pid" ]] && is_port_in_use; then
        pid=$(get_port_pid)
        echo "No PID file, but found process $pid using port $PORT"
    fi

    if [[ -z "$pid" ]]; then
        echo "No server to stop"
        return 0
    fi

    if is_process_running "$pid"; then
        echo "Stopping server (PID: $pid)..."
        kill "$pid" 2>/dev/null || true

        # Wait for graceful shutdown
        local attempts=0
        while is_process_running "$pid" && [[ $attempts -lt 10 ]]; do
            sleep 1
            ((attempts++))
            echo "  Waiting for shutdown... ($attempts/10)"
        done

        # Force kill if still running
        if is_process_running "$pid"; then
            echo "Force killing..."
            kill -9 "$pid" 2>/dev/null || true
            sleep 1
        fi

        echo "Server stopped"
    else
        echo "Server process $pid is not running"
    fi

    # Clean up state files
    rm -f "$PID_FILE" "$STATE_FILE"
}

cmd_restart() {
    echo "=== Restarting Dev Server ==="
    cmd_stop
    echo ""
    sleep 1
    cmd_start
}

cmd_status() {
    echo "=== Dev Server Status ==="

    if [[ ! -f "$PID_FILE" ]]; then
        echo "Status: NOT RUNNING (no PID file)"

        if is_port_in_use; then
            local pid
            pid=$(get_port_pid)
            echo ""
            echo "WARNING: Port $PORT is in use by untracked process $pid"
            echo "Run 'restart' to adopt this process"
        fi
        return 1
    fi

    local pid
    pid=$(cat "$PID_FILE")

    if ! is_process_running "$pid"; then
        echo "Status: STALE (PID file exists but process not running)"
        rm -f "$PID_FILE" "$STATE_FILE"
        return 1
    fi

    echo "Status: RUNNING"
    echo "PID:    $pid"

    # Read state
    if [[ -f "$STATE_FILE" ]]; then
        local started_at
        started_at=$(grep -o '"startedAt": "[^"]*"' "$STATE_FILE" | cut -d'"' -f4)
        echo "Started: $started_at"
    fi

    # Health check
    local http_code
    http_code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$PORT/api/managers/me" 2>/dev/null || echo "000")
    if [[ "$http_code" == "200" || "$http_code" == "401" ]]; then
        echo "Health: HEALTHY (HTTP $http_code)"
    else
        echo "Health: UNHEALTHY (HTTP $http_code)"
    fi

    print_server_info
}

cmd_logs() {
    local lines=${1:-$DEFAULT_LOG_LINES}

    if [[ ! -f "$LOG_FILE" ]]; then
        echo "No log file found at $LOG_FILE"
        echo "Start the server first with: $0 start"
        return 1
    fi

    echo "=== Dev Server Logs (last $lines lines) ==="
    echo ""
    tail -n "$lines" "$LOG_FILE"

    echo ""
    echo "=== Tailing logs (Ctrl+C to stop) ==="
    echo ""
    tail -f "$LOG_FILE"
}

cmd_health() {
    local http_code
    http_code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$PORT/api/managers/me" 2>/dev/null || echo "000")

    if [[ "$http_code" == "200" || "$http_code" == "401" ]]; then
        echo "HEALTHY (HTTP $http_code)"
        echo "Server responding at http://localhost:$PORT"
        return 0
    else
        echo "UNHEALTHY (HTTP $http_code)"
        echo "Server not responding at http://localhost:$PORT"
        return 1
    fi
}

cmd_default() {
    # Default: Start if needed, then tail logs

    # Check if server is running
    if check_stale_pid; then
        local pid
        pid=$(cat "$PID_FILE")
        echo "Server already running (PID: $pid)"
        print_server_info
        echo ""
    else
        cmd_start
        echo ""
    fi

    # Tail logs
    cmd_logs "$DEFAULT_LOG_LINES"
}

show_help() {
    echo "Dev Server Management Script"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  (none)     Default: Start if needed, show last 100 lines + tail logs"
    echo "  start      Start the dev server (uses pnpm devsafe)"
    echo "  stop       Stop the dev server"
    echo "  restart    Stop and start the dev server"
    echo "  status     Show server status and health"
    echo "  logs [N]   Show last N lines (default 100) and tail logs"
    echo "  health     Quick health check"
    echo "  help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                 # Start + tail logs (most common)"
    echo "  $0 start           # Start without tailing"
    echo "  $0 restart         # Restart after config changes"
    echo "  $0 logs 50         # Show last 50 lines + tail"
}

# ============================================
# Main
# ============================================

main() {
    local cmd="${1:-}"
    shift || true

    case "$cmd" in
        "")
            cmd_default
            ;;
        start)
            cmd_start
            ;;
        stop)
            cmd_stop
            ;;
        restart)
            cmd_restart
            ;;
        status)
            cmd_status
            ;;
        logs)
            cmd_logs "${1:-$DEFAULT_LOG_LINES}"
            ;;
        health)
            cmd_health
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo "Unknown command: $cmd"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

main "$@"
