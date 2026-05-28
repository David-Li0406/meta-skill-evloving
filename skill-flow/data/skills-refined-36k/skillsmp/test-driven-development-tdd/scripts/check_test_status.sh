#!/usr/bin/env bash
# Check test status to determine red/green state
# Usage: ./check_test_status.sh [category]

CATEGORY="${1:-all}"
TIMEOUT_SECONDS="${2:-30}"

# Store output in temp file to preserve exit code and filter output
TEMP_OUTPUT=$(mktemp)
trap "rm -f $TEMP_OUTPUT" EXIT

timeout "$TIMEOUT_SECONDS" lake test > "$TEMP_OUTPUT" 2>&1
EXIT_CODE=$?

if [ "$CATEGORY" = "all" ]; then
    cat "$TEMP_OUTPUT"
else
    # Filter to specific category section
    # Use awk for robust section extraction
    awk -v cat="$CATEGORY" '
        /^=== .* tests ===/ { in_section = ($0 ~ "=== " cat " tests ===") }
        in_section { print }
        /^$/ && in_section && seen_content { in_section = 0 }
        in_section && /^  / { seen_content = 1 }
    ' "$TEMP_OUTPUT"
fi

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "🟢 GREEN: All tests passing"
    exit 0
elif [ $EXIT_CODE -eq 124 ]; then
    echo "⏱️  TIMEOUT: Tests took longer than $TIMEOUT_SECONDS seconds"
    exit 2
else
    echo "🔴 RED: Tests failing"
    exit 1
fi
