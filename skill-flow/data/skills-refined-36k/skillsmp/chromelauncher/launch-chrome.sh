#!/usr/bin/env bash
# ChromeLauncher - Launch Chrome for Claude in Chrome extension
# Checks if Chrome is running, launches if not, waits for extension connection

set -euo pipefail

SOCKET_PATH="${TMPDIR:-/tmp}/claude-mcp-browser-bridge-${USER}"
MAX_WAIT_SECONDS=30
CHROME_CMD="${CHROME_CMD:-google-chrome-stable}"
WLRCTL_CMD="${WLRCTL_CMD:-wlrctl}"

log() {
    echo "[ChromeLauncher] $*" >&2
}

is_chrome_running() {
    # Check for user Chrome session (not headless/playwright instances)
    # Headless Chrome uses --headless flag and temp user-data-dir
    # Regular Chrome uses ~/.config/google-chrome
    local chrome_pids
    chrome_pids=$(pgrep -f "google-chrome" 2>/dev/null || true)

    if [[ -z "$chrome_pids" ]]; then
        return 1
    fi

    # Check if any chrome process is the main browser (not headless, not crashpad)
    for pid in $chrome_pids; do
        local cmdline
        cmdline=$(cat "/proc/$pid/cmdline" 2>/dev/null | tr '\0' ' ' || true)
        # Skip if empty, headless, or crashpad_handler
        if [[ -z "$cmdline" ]]; then
            continue
        fi
        if [[ "$cmdline" == *"--headless"* ]]; then
            continue
        fi
        if [[ "$cmdline" == *"crashpad_handler"* ]]; then
            continue
        fi
        if [[ "$cmdline" == *"--type="* ]]; then
            # Child process (renderer, gpu, etc) - skip
            continue
        fi
        # Found a main Chrome process that's not headless
        return 0
    done

    return 1
}

is_extension_ready() {
    [[ -S "$SOCKET_PATH" ]]
}

wake_extension() {
    # Send Alt+C to activate the Claude extension, triggering connectNative()
    if command -v "$WLRCTL_CMD" &>/dev/null; then
        log "Waking extension with Alt+C..."
        "$WLRCTL_CMD" keyboard type alt+c
        sleep 1
    else
        log "wlrctl not found - please manually click the Claude extension icon"
    fi
}

wait_for_extension() {
    local waited=0
    log "Waiting for Claude in Chrome extension (max ${MAX_WAIT_SECONDS}s)..."

    while [[ $waited -lt $MAX_WAIT_SECONDS ]]; do
        if is_extension_ready; then
            log "Extension socket ready at $SOCKET_PATH"
            return 0
        fi
        sleep 1
        ((waited++))
    done

    log "Timeout waiting for extension socket"
    return 1
}

launch_chrome() {
    log "Launching Chrome..."

    # Launch Chrome in background, detached from terminal
    nohup "$CHROME_CMD" >/dev/null 2>&1 &
    disown

    # Give Chrome a moment to start
    sleep 3

    # Wake the extension to trigger connectNative()
    wake_extension
}

main() {
    local action="${1:-ensure}"

    case "$action" in
        status)
            if is_chrome_running; then
                echo "Chrome: running"
            else
                echo "Chrome: not running"
            fi
            if is_extension_ready; then
                echo "Extension: connected (socket at $SOCKET_PATH)"
            else
                echo "Extension: not connected"
            fi
            ;;

        launch)
            if is_chrome_running; then
                log "Chrome already running"
            else
                launch_chrome
            fi
            ;;

        ensure|"")
            # Main use case: ensure Chrome is running and extension is ready
            if is_extension_ready; then
                log "Extension already connected"
                echo "ready"
                exit 0
            fi

            if ! is_chrome_running; then
                launch_chrome
            else
                log "Chrome running but extension not connected"
                wake_extension
            fi

            if wait_for_extension; then
                echo "ready"
                exit 0
            else
                echo "timeout"
                exit 1
            fi
            ;;

        wait)
            wait_for_extension
            ;;

        *)
            echo "Usage: $0 [status|launch|ensure|wait]"
            echo "  status  - Check Chrome and extension status"
            echo "  launch  - Launch Chrome if not running"
            echo "  ensure  - Launch Chrome if needed, wait for extension (default)"
            echo "  wait    - Wait for extension to connect"
            exit 1
            ;;
    esac
}

main "$@"
