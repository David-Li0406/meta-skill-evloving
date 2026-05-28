#!/bin/bash
#
# Debug script for Dify plugins
#
# This script kills any previously running debug process before starting a new one.
# It identifies debug processes by the "python -m main" command pattern within the
# current plugin directory.
#
# Usage:
#   ./debug.sh              # Run from plugin directory
#   ./debug.sh --kill-only  # Only kill existing process, don't start new one
#   ./debug.sh --status     # Show status of running debug processes
#
# The script automatically:
#   1. Finds and kills any existing debug process for this plugin
#   2. Starts a new debug process using `uv run python -m main`
#

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

info() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }
debug_msg() { echo -e "${CYAN}[DEBUG]${NC} $1"; }

# Get the absolute path of the current directory
PLUGIN_DIR=$(pwd)

# PID file location (in plugin directory)
PID_FILE="${PLUGIN_DIR}/.debug.pid"

# Check if we're in a plugin directory
check_plugin_dir() {
    if [[ ! -f "${PLUGIN_DIR}/manifest.yaml" ]]; then
        error "Not a plugin directory (manifest.yaml not found). Please run from your plugin root."
    fi
    if [[ ! -f "${PLUGIN_DIR}/main.py" ]]; then
        error "main.py not found. Please ensure your plugin has a main.py entry point."
    fi
}

# Find running debug processes for this plugin
find_debug_processes() {
    local pids=""

    # Method 1: Check PID file
    if [[ -f "$PID_FILE" ]]; then
        local saved_pid
        saved_pid=$(cat "$PID_FILE" 2>/dev/null)
        if [[ -n "$saved_pid" ]] && kill -0 "$saved_pid" 2>/dev/null; then
            pids="$saved_pid"
        fi
    fi

    # Method 2: Search for processes by pattern (as backup)
    # Look for python processes running main in this directory
    local found_pids
    found_pids=$(pgrep -f "python.*-m main" 2>/dev/null || true)

    for pid in $found_pids; do
        # Verify this process is running from our plugin directory
        local proc_cwd
        proc_cwd=$(lsof -p "$pid" 2>/dev/null | grep cwd | awk '{print $NF}' || true)
        if [[ "$proc_cwd" == "$PLUGIN_DIR" ]]; then
            if [[ -z "$pids" ]]; then
                pids="$pid"
            elif [[ ! "$pids" =~ $pid ]]; then
                pids="$pids $pid"
            fi
        fi
    done

    echo "$pids"
}

# Kill existing debug processes
kill_debug_processes() {
    local pids
    pids=$(find_debug_processes)

    if [[ -z "$pids" ]]; then
        info "No existing debug process found"
        return 0
    fi

    for pid in $pids; do
        info "Killing debug process (PID: $pid)..."
        kill "$pid" 2>/dev/null || true

        # Wait for graceful shutdown
        local count=0
        while kill -0 "$pid" 2>/dev/null && [[ $count -lt 10 ]]; do
            sleep 0.5
            ((count++))
        done

        # Force kill if still running
        if kill -0 "$pid" 2>/dev/null; then
            warn "Process didn't exit gracefully, force killing..."
            kill -9 "$pid" 2>/dev/null || true
        fi

        info "Process $pid terminated"
    done

    # Clean up PID file
    rm -f "$PID_FILE"
}

# Start new debug process
start_debug_process() {
    info "Starting debug process..."

    # Check if .env exists
    if [[ ! -f "${PLUGIN_DIR}/.env" ]]; then
        warn ".env file not found. You may need to run: python scripts/get_debug_key.py --output-env > .env"
    fi

    # Start the process in foreground (so Ctrl+C works)
    # Save PID for future cleanup
    uv run python -m main &
    local pid=$!

    echo "$pid" > "$PID_FILE"
    info "Debug process started (PID: $pid)"

    # Wait for the process
    wait "$pid" 2>/dev/null || true

    # Clean up PID file when process exits
    rm -f "$PID_FILE"
}

# Show status of debug processes
show_status() {
    local pids
    pids=$(find_debug_processes)

    if [[ -z "$pids" ]]; then
        info "No debug process running for this plugin"
    else
        for pid in $pids; do
            info "Debug process running (PID: $pid)"
            ps -p "$pid" -o pid,ppid,stat,time,command 2>/dev/null || true
        done
    fi
}

# Cleanup handler for Ctrl+C
cleanup() {
    echo ""
    info "Caught interrupt signal, cleaning up..."
    rm -f "$PID_FILE"
    exit 0
}

# Main
main() {
    trap cleanup SIGINT SIGTERM

    case "${1:-}" in
        --kill-only|-k)
            check_plugin_dir
            kill_debug_processes
            ;;
        --status|-s)
            check_plugin_dir
            show_status
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Debug script for Dify plugins. Automatically kills existing debug"
            echo "processes before starting a new one."
            echo ""
            echo "Options:"
            echo "  --kill-only, -k    Only kill existing process, don't start new one"
            echo "  --status, -s       Show status of running debug processes"
            echo "  --help, -h         Show this help message"
            echo ""
            echo "Run from your plugin directory (where manifest.yaml is located)."
            ;;
        "")
            check_plugin_dir
            kill_debug_processes
            start_debug_process
            ;;
        *)
            error "Unknown option: $1. Use --help for usage."
            ;;
    esac
}

main "$@"
