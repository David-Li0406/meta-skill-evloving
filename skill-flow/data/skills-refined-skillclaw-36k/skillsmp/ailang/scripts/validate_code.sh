#!/usr/bin/env bash
# Validate AILANG code syntax

set -euo pipefail

if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <file.ail>" >&2
    echo "Validate AILANG code syntax using 'ailang check'" >&2
    exit 1
fi

FILE="$1"

if [[ ! -f "$FILE" ]]; then
    echo "File not found: $FILE" >&2
    exit 1
fi

echo "Validating $FILE..."

if ailang check "$FILE" 2>&1; then
    echo "Type check passed"
else
    echo "Type check failed"
    exit 1
fi
