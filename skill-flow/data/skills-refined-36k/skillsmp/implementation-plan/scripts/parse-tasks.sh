#!/usr/bin/env bash
# Parse and display task status from IMPLEMENTATION_PLAN.md

PLAN_FILE="${1:-IMPLEMENTATION_PLAN.md}"

if [ ! -f "$PLAN_FILE" ]; then
    echo "Error: $PLAN_FILE not found"
    exit 1
fi

echo "Task Status for $PLAN_FILE"
echo "================================"

# Count tasks
INCOMPLETE=$(grep -c '^\- \[ \]' "$PLAN_FILE" 2>/dev/null || echo 0)
COMPLETE=$(grep -c '^\- \[x\]' "$PLAN_FILE" 2>/dev/null || echo 0)
TOTAL=$((INCOMPLETE + COMPLETE))

echo "Total Tasks: $TOTAL"
echo "Completed:   $COMPLETE"
echo "Remaining:   $INCOMPLETE"
echo ""

if [ "$INCOMPLETE" -gt 0 ]; then
    echo "Next Tasks:"
    grep '^\- \[ \]' "$PLAN_FILE" | head -5
fi
