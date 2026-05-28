#!/usr/bin/env bash
# Check for unread messages in AILANG messaging system

set -euo pipefail

INBOX="${1:-}"

if ! command -v ailang &> /dev/null; then
    echo "AILANG is not installed" >&2
    echo "Run: ./skills/ailang/scripts/install.sh" >&2
    exit 1
fi

if [[ -n "$INBOX" ]]; then
    echo "Checking inbox: $INBOX"
    ailang messages list --inbox "$INBOX" --unread
else
    echo "Checking all unread messages"
    ailang messages list --unread
fi
