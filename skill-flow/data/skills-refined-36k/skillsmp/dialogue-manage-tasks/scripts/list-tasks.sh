#!/bin/bash
# list-tasks.sh — List tasks with optional filtering
# Part of the Dialogue Framework
# Usage: list-tasks.sh [options]
#   --status <STATUS>    Filter by status (BACKLOG, READY, IN_PROGRESS, BLOCKED, COMPLETED, CANCELLED)
#   --type <TYPE>        Filter by type (CAPABILITY, SCHEMA, DOCUMENT, RESEARCH, DEBT, DECISION)
#   --priority <PRIO>    Filter by priority (CRITICAL, HIGH, MEDIUM, LOW)
#   --prefix <PREFIX>    Filter by ID prefix (SH, CD, FW, DOC, VAL)
#   --sort <FIELD>       Sort by field (id, created, updated, priority, status) [default: id]
#   --format <FORMAT>    Output format: table, brief, json [default: table]
#   --active             Shortcut for --status IN_PROGRESS
#   --ready              Shortcut for --status READY
#   --all                Include all statuses (default excludes COMPLETED, CANCELLED)

set -euo pipefail

PROJECT_ROOT="${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR must be set}"
TASKS_DIR="${PROJECT_ROOT}/.dialogue/tasks"

# Defaults
FILTER_STATUS=""
FILTER_TYPE=""
FILTER_PRIORITY=""
FILTER_PREFIX=""
SORT_FIELD="id"
OUTPUT_FORMAT="table"
INCLUDE_ALL=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --status)
            FILTER_STATUS="$2"
            shift 2
            ;;
        --type)
            FILTER_TYPE="$2"
            shift 2
            ;;
        --priority)
            FILTER_PRIORITY="$2"
            shift 2
            ;;
        --prefix)
            FILTER_PREFIX="$2"
            shift 2
            ;;
        --sort)
            SORT_FIELD="$2"
            shift 2
            ;;
        --format)
            OUTPUT_FORMAT="$2"
            shift 2
            ;;
        --active)
            FILTER_STATUS="IN_PROGRESS"
            shift
            ;;
        --ready)
            FILTER_STATUS="READY"
            shift
            ;;
        --all)
            INCLUDE_ALL=true
            shift
            ;;
        -h|--help)
            echo "Usage: list-tasks.sh [options]"
            echo ""
            echo "Options:"
            echo "  --status <STATUS>    Filter by status (BACKLOG, READY, IN_PROGRESS, BLOCKED, COMPLETED, CANCELLED)"
            echo "  --type <TYPE>        Filter by type (CAPABILITY, SCHEMA, DOCUMENT, RESEARCH, DEBT, DECISION)"
            echo "  --priority <PRIO>    Filter by priority (CRITICAL, HIGH, MEDIUM, LOW)"
            echo "  --prefix <PREFIX>    Filter by ID prefix (SH, CD, FW, DOC, VAL)"
            echo "  --sort <FIELD>       Sort by field: id, created, updated, priority, status [default: id]"
            echo "  --format <FORMAT>    Output format: table, brief, json [default: table]"
            echo "  --active             Shortcut for --status IN_PROGRESS"
            echo "  --ready              Shortcut for --status READY"
            echo "  --all                Include COMPLETED and CANCELLED (excluded by default)"
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

# Helper: Priority to number for sorting
priority_to_num() {
    case "$1" in
        CRITICAL) echo "1" ;;
        HIGH)     echo "2" ;;
        MEDIUM)   echo "3" ;;
        LOW)      echo "4" ;;
        *)        echo "5" ;;
    esac
}

# Helper: Status to number for sorting
status_to_num() {
    case "$1" in
        IN_PROGRESS) echo "1" ;;
        BLOCKED)     echo "2" ;;
        READY)       echo "3" ;;
        BACKLOG)     echo "4" ;;
        COMPLETED)   echo "5" ;;
        CANCELLED)   echo "6" ;;
        *)           echo "7" ;;
    esac
}

# Collect task data
declare -a TASKS=()

for file in "$TASKS_DIR"/*.yaml; do
    [[ -f "$file" ]] || continue

    id=$(extract_field "$file" "id")
    status=$(extract_field "$file" "status")
    type=$(extract_field "$file" "type")
    priority=$(extract_field "$file" "priority")
    title=$(extract_field "$file" "title")
    created=$(extract_field "$file" "created")
    updated=$(extract_field "$file" "updated")

    # Apply filters
    if [[ -n "$FILTER_STATUS" && "$status" != "$FILTER_STATUS" ]]; then
        continue
    fi

    if [[ -n "$FILTER_TYPE" && "$type" != "$FILTER_TYPE" ]]; then
        continue
    fi

    if [[ -n "$FILTER_PRIORITY" && "$priority" != "$FILTER_PRIORITY" ]]; then
        continue
    fi

    if [[ -n "$FILTER_PREFIX" ]]; then
        prefix="${id%%-*}"
        if [[ "$prefix" != "$FILTER_PREFIX" ]]; then
            continue
        fi
    fi

    # Exclude completed/cancelled unless --all
    if [[ "$INCLUDE_ALL" == "false" && -z "$FILTER_STATUS" ]]; then
        if [[ "$status" == "COMPLETED" || "$status" == "CANCELLED" ]]; then
            continue
        fi
    fi

    # Calculate sort key
    case "$SORT_FIELD" in
        id)       sort_key="$id" ;;
        created)  sort_key="$created" ;;
        updated)  sort_key="${updated:-$created}" ;;
        priority) sort_key="$(priority_to_num "$priority")" ;;
        status)   sort_key="$(status_to_num "$status")" ;;
        *)        sort_key="$id" ;;
    esac

    # Store as tab-separated record: sort_key, id, status, type, priority, title, created, updated
    TASKS+=("${sort_key}	${id}	${status}	${type:-}	${priority:-MEDIUM}	${title}	${created}	${updated:-}")
done

# Sort tasks
IFS=$'\n' SORTED=($(sort -t$'\t' -k1 <<<"${TASKS[*]:-}"))
unset IFS

# Output based on format
case "$OUTPUT_FORMAT" in
    table)
        # Print header
        printf "%-10s %-12s %-10s %-8s %s\n" "ID" "STATUS" "TYPE" "PRIORITY" "TITLE"
        printf "%-10s %-12s %-10s %-8s %s\n" "----------" "------------" "----------" "--------" "-----"

        for task in "${SORTED[@]:-}"; do
            [[ -z "$task" ]] && continue
            IFS=$'\t' read -r _ id status type priority title _ _ <<< "$task"
            printf "%-10s %-12s %-10s %-8s %s\n" "$id" "$status" "${type:-}" "${priority:-}" "$title"
        done
        ;;

    brief)
        for task in "${SORTED[@]:-}"; do
            [[ -z "$task" ]] && continue
            IFS=$'\t' read -r _ id status type priority title _ _ <<< "$task"
            echo "$id: $title [$status]"
        done
        ;;

    json)
        echo "["
        first=true
        for task in "${SORTED[@]:-}"; do
            [[ -z "$task" ]] && continue
            IFS=$'\t' read -r _ id status type priority title created updated <<< "$task"

            if [[ "$first" == "true" ]]; then
                first=false
            else
                echo ","
            fi

            cat <<EOF
  {
    "id": "$id",
    "status": "$status",
    "type": "${type:-null}",
    "priority": "${priority:-MEDIUM}",
    "title": "$title",
    "created": "$created",
    "updated": "${updated:-null}"
  }
EOF
        done
        echo ""
        echo "]"
        ;;
esac
