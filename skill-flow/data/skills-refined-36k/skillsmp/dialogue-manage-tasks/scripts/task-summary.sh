#!/usr/bin/env bash
# task-summary.sh — Present a task status summary
# Part of the Dialogue Framework
# Usage: task-summary.sh [--format table|json]

set -euo pipefail

PROJECT_ROOT="${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR must be set}"
TASKS_DIR="${PROJECT_ROOT}/.dialogue/tasks"

OUTPUT_FORMAT="table"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --format)
            OUTPUT_FORMAT="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: task-summary.sh [--format table|json]"
            echo ""
            echo "Presents a summary of task status including:"
            echo "  - Counts by status"
            echo "  - In-progress tasks with titles"
            echo "  - High-priority ready tasks"
            echo "  - Blocked tasks"
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Check tasks directory exists
if [[ ! -d "$TASKS_DIR" ]]; then
    echo "No tasks directory found at $TASKS_DIR" >&2
    exit 1
fi

# Helper: Extract field from YAML file
extract_field() {
    local file="$1"
    local field="$2"
    grep "^${field}:" "$file" 2>/dev/null | sed "s/^${field}:[[:space:]]*//" | tr -d '"' || echo ""
}

# Collect data
declare -a IN_PROGRESS_TASKS=()
declare -a HIGH_PRIORITY_READY=()
declare -a BLOCKED_TASKS=()

count_backlog=0
count_ready=0
count_in_progress=0
count_blocked=0
count_completed=0
count_cancelled=0
total=0

for file in "$TASKS_DIR"/*.yaml; do
    [[ -f "$file" ]] || continue

    id=$(extract_field "$file" "id")
    status=$(extract_field "$file" "status")
    priority=$(extract_field "$file" "priority")
    title=$(extract_field "$file" "title")

    ((total++))

    case "$status" in
        BACKLOG)
            ((count_backlog++))
            ;;
        READY)
            ((count_ready++))
            if [[ "$priority" == "HIGH" || "$priority" == "CRITICAL" ]]; then
                HIGH_PRIORITY_READY+=("$id|$title|$priority")
            fi
            ;;
        IN_PROGRESS)
            ((count_in_progress++))
            IN_PROGRESS_TASKS+=("$id|$title|$priority")
            ;;
        BLOCKED)
            ((count_blocked++))
            BLOCKED_TASKS+=("$id|$title")
            ;;
        COMPLETED)
            ((count_completed++))
            ;;
        CANCELLED)
            ((count_cancelled++))
            ;;
    esac
done

# Calculate active (non-terminal) count
active=$((count_backlog + count_ready + count_in_progress + count_blocked))

# Output
case "$OUTPUT_FORMAT" in
    table)
        echo "=== Task Status Summary ==="
        echo ""
        printf "%-15s %5d\n" "In Progress:" "$count_in_progress"
        printf "%-15s %5d\n" "Ready:" "$count_ready"
        printf "%-15s %5d\n" "Blocked:" "$count_blocked"
        printf "%-15s %5d\n" "Backlog:" "$count_backlog"
        printf "%-15s %5d\n" "Completed:" "$count_completed"
        printf "%-15s %5d\n" "Cancelled:" "$count_cancelled"
        echo "------------------------"
        printf "%-15s %5d\n" "Active:" "$active"
        printf "%-15s %5d\n" "Total:" "$total"

        if [[ ${#IN_PROGRESS_TASKS[@]} -gt 0 ]]; then
            echo ""
            echo "=== In Progress ==="
            for task in "${IN_PROGRESS_TASKS[@]}"; do
                IFS='|' read -r id title priority <<< "$task"
                printf "  %-10s %s" "$id" "$title"
                if [[ "$priority" == "HIGH" || "$priority" == "CRITICAL" ]]; then
                    printf " [%s]" "$priority"
                fi
                echo ""
            done
        fi

        if [[ ${#HIGH_PRIORITY_READY[@]} -gt 0 ]]; then
            echo ""
            echo "=== High Priority Ready ==="
            for task in "${HIGH_PRIORITY_READY[@]}"; do
                IFS='|' read -r id title priority <<< "$task"
                printf "  %-10s %s [%s]\n" "$id" "$title" "$priority"
            done
        fi

        if [[ ${#BLOCKED_TASKS[@]} -gt 0 ]]; then
            echo ""
            echo "=== Blocked ==="
            for task in "${BLOCKED_TASKS[@]}"; do
                IFS='|' read -r id title <<< "$task"
                printf "  %-10s %s\n" "$id" "$title"
            done
        fi
        ;;

    json)
        # Build JSON arrays for task lists
        in_progress_json="["
        first=true
        for task in "${IN_PROGRESS_TASKS[@]:-}"; do
            [[ -z "$task" ]] && continue
            IFS='|' read -r id title priority <<< "$task"
            if [[ "$first" == "true" ]]; then
                first=false
            else
                in_progress_json+=","
            fi
            in_progress_json+="{\"id\":\"$id\",\"title\":\"$title\",\"priority\":\"$priority\"}"
        done
        in_progress_json+="]"

        high_priority_json="["
        first=true
        for task in "${HIGH_PRIORITY_READY[@]:-}"; do
            [[ -z "$task" ]] && continue
            IFS='|' read -r id title priority <<< "$task"
            if [[ "$first" == "true" ]]; then
                first=false
            else
                high_priority_json+=","
            fi
            high_priority_json+="{\"id\":\"$id\",\"title\":\"$title\",\"priority\":\"$priority\"}"
        done
        high_priority_json+="]"

        blocked_json="["
        first=true
        for task in "${BLOCKED_TASKS[@]:-}"; do
            [[ -z "$task" ]] && continue
            IFS='|' read -r id title <<< "$task"
            if [[ "$first" == "true" ]]; then
                first=false
            else
                blocked_json+=","
            fi
            blocked_json+="{\"id\":\"$id\",\"title\":\"$title\"}"
        done
        blocked_json+="]"

        cat <<EOF
{
  "counts": {
    "in_progress": $count_in_progress,
    "ready": $count_ready,
    "blocked": $count_blocked,
    "backlog": $count_backlog,
    "completed": $count_completed,
    "cancelled": $count_cancelled,
    "active": $active,
    "total": $total
  },
  "in_progress": $in_progress_json,
  "high_priority_ready": $high_priority_json,
  "blocked": $blocked_json
}
EOF
        ;;
esac
