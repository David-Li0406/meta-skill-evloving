#!/bin/bash
#
# send-notification.sh - Send MacOS notification for freshness check
#
# Usage: ./tools/freshness/send-notification.sh [--message "custom message"]

set -euo pipefail

MESSAGE="Monthly Design Ops freshness check ready. Run /design freshness in Claude Code."
TITLE="Design Ops"
SUBTITLE="Freshness Check"
SOUND="Glass"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --message)
            MESSAGE="$2"
            shift 2
            ;;
        --title)
            TITLE="$2"
            shift 2
            ;;
        --subtitle)
            SUBTITLE="$2"
            shift 2
            ;;
        --sound)
            SOUND="$2"
            shift 2
            ;;
        --silent)
            SOUND=""
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [--message \"msg\"] [--title \"title\"] [--sound \"sound\"]"
            exit 0
            ;;
        *)
            shift
            ;;
    esac
done

# Check if running on MacOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo "Warning: MacOS notifications only work on MacOS"
    echo "Message: $MESSAGE"
    exit 0
fi

# Build osascript command
if [[ -n "$SOUND" ]]; then
    osascript -e "display notification \"$MESSAGE\" with title \"$TITLE\" subtitle \"$SUBTITLE\" sound name \"$SOUND\""
else
    osascript -e "display notification \"$MESSAGE\" with title \"$TITLE\" subtitle \"$SUBTITLE\""
fi

echo "Notification sent: $MESSAGE"
