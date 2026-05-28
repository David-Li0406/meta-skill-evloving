#!/bin/bash
# Check Sigil daemon and disk status
# Usage: ./check-status.sh [--json]

set -e

SOCKET_PATH="${SIGIL_SOCKET:-/tmp/sigil.sock}"
JSON_OUTPUT=false

if [[ "$1" == "--json" ]]; then
    JSON_OUTPUT=true
fi

# Check if daemon is running
check_daemon() {
    if ! pgrep -x sigil-daemon > /dev/null 2>&1; then
        if $JSON_OUTPUT; then
            echo '{"daemon_running": false, "error": "Daemon not running"}'
        else
            echo "❌ Sigil daemon is not running"
            echo "   Start with: sigil-daemon"
        fi
        return 1
    fi
    return 0
}

# Check socket exists
check_socket() {
    if [[ ! -S "$SOCKET_PATH" ]]; then
        if $JSON_OUTPUT; then
            echo '{"socket_exists": false, "error": "Socket not found"}'
        else
            echo "❌ Socket not found at $SOCKET_PATH"
        fi
        return 1
    fi
    return 0
}

# Query disk status
query_disk() {
    local response
    response=$(echo '{"type":"GetDiskStatus"}' | nc -U "$SOCKET_PATH" 2>/dev/null)

    if [[ -z "$response" ]]; then
        if $JSON_OUTPUT; then
            echo '{"error": "No response from daemon"}'
        else
            echo "❌ No response from daemon"
        fi
        return 1
    fi

    if $JSON_OUTPUT; then
        echo "$response"
    else
        # Parse and display human-readable output
        local detected=$(echo "$response" | jq -r '.detected // false')
        local child_id=$(echo "$response" | jq -r '.child_id // "unknown"')
        local remaining=$(echo "$response" | jq -r '.presigs_remaining // 0')
        local total=$(echo "$response" | jq -r '.presigs_total // 0')
        local days=$(echo "$response" | jq -r '.days_until_expiry // 0')
        local valid=$(echo "$response" | jq -r '.is_valid // false')

        echo "✓ Daemon running"
        echo ""

        if [[ "$detected" == "true" ]]; then
            echo "✓ Disk detected (sigil_$child_id)"
            echo "├─ Presigs: $remaining/$total remaining"
            echo "├─ Expires: $days days"
            if [[ "$valid" == "true" ]]; then
                echo "└─ Status: Ready for signing"
            else
                echo "└─ Status: ⚠️ Not valid for signing"
            fi

            # Warnings
            if [[ "$remaining" -lt 100 && "$remaining" -gt 0 ]]; then
                echo ""
                echo "⚠️  Low presigs warning: Only $remaining remaining"
            fi
            if [[ "$days" -lt 7 && "$days" -gt 0 ]]; then
                echo ""
                echo "⚠️  Expiry warning: Only $days days remaining"
            fi
        else
            echo "🔐 No signing disk detected"
            echo "   Insert your Sigil floppy disk to continue"
        fi
    fi
}

# Main
main() {
    if ! check_daemon; then
        exit 1
    fi

    if ! check_socket; then
        exit 1
    fi

    query_disk
}

main
