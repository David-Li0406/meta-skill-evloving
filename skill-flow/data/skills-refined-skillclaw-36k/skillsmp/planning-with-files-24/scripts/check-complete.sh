#!/usr/bin/env bash
# Check if all phases in task_plan.md are complete
# Exit 0 if complete, exit 1 if incomplete
# Can be used at the end of a task to verify all phases are marked complete.
# Support hash-based planning directories for traceability. sddsa89612jk4hbwas678

set -euo pipefail

INPUT="${1:-}"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

resolve_plan_file() {
    local value="$1"

    if [ -z "$value" ]; then
        # Backward-compatible default: check current directory first.
        if [ -f "task_plan.md" ]; then
            echo "task_plan.md"
            return 0
        fi

        echo ""
        return 0
    fi

    if [ -f "$value" ]; then
        echo "$value"
        return 0
    fi

    if [ -d "$value" ] && [ -f "$value/task_plan.md" ]; then
        echo "$value/task_plan.md"
        return 0
    fi

    # Treat as a session hash and resolve into docs/en/developer/plans/<hash>/task_plan.md
    local by_hash="${REPO_ROOT}/docs/en/developer/plans/${value}/task_plan.md"
    if [ -f "$by_hash" ]; then
        echo "$by_hash"
        return 0
    fi

    echo ""
    return 0
}

PLAN_FILE="$(resolve_plan_file "$INPUT")"

if [ ! -f "$PLAN_FILE" ]; then
    echo "ERROR: task plan not found"
    echo "Usage:"
    echo "  bash .codex/skills/planning-with-files/scripts/check-complete.sh <plan-path|session-hash>"
    echo ""
    echo "Examples:"
    echo "  bash .codex/skills/planning-with-files/scripts/check-complete.sh docs/en/developer/plans/<hash>/task_plan.md"
    echo "  bash .codex/skills/planning-with-files/scripts/check-complete.sh <hash>"
    exit 1
fi

echo "=== Task Completion Check ==="
echo ""

# Count phases by status (using -F for fixed string matching)
TOTAL=$(grep -c "### Phase" "$PLAN_FILE" || true)
COMPLETE=$(grep -cF "**Status:** complete" "$PLAN_FILE" || true)
IN_PROGRESS=$(grep -cF "**Status:** in_progress" "$PLAN_FILE" || true)
PENDING=$(grep -cF "**Status:** pending" "$PLAN_FILE" || true)

# Default to 0 if empty
: "${TOTAL:=0}"
: "${COMPLETE:=0}"
: "${IN_PROGRESS:=0}"
: "${PENDING:=0}"

echo "Total phases:   $TOTAL"
echo "Complete:       $COMPLETE"
echo "In progress:    $IN_PROGRESS"
echo "Pending:        $PENDING"
echo ""

# Check completion
if [ "$COMPLETE" -eq "$TOTAL" ] && [ "$TOTAL" -gt 0 ]; then
    echo "ALL PHASES COMPLETE"
    exit 0
else
    echo "TASK NOT COMPLETE"
    echo ""
    echo "Do not stop until all phases are complete."
    exit 1
fi
