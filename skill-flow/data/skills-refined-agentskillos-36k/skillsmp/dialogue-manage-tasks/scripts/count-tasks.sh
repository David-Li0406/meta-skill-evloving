#!/usr/bin/env bash
# count-tasks.sh — Count tasks with optional grouping
# Part of the Dialogue Framework
# Usage: count-tasks.sh [options]
#   --by <FIELD>      Group by field: status, type, priority, prefix [default: none]
#   --status <STATUS> Filter by status before counting
#   --type <TYPE>     Filter by type before counting
#   --prefix <PREFIX> Filter by prefix before counting
#   --format <FMT>    Output format: table, json [default: table]

set -euo pipefail

PROJECT_ROOT="${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR must be set}"
TASKS_DIR="${PROJECT_ROOT}/.dialogue/tasks"

# Defaults
GROUP_BY=""
FILTER_STATUS=""
FILTER_TYPE=""
FILTER_PREFIX=""
OUTPUT_FORMAT="table"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --by)
            GROUP_BY="$2"
            shift 2
            ;;
        --status)
            FILTER_STATUS="$2"
            shift 2
            ;;
        --type)
            FILTER_TYPE="$2"
            shift 2
            ;;
        --prefix)
            FILTER_PREFIX="$2"
            shift 2
            ;;
        --format)
            OUTPUT_FORMAT="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: count-tasks.sh [options]"
            echo ""
            echo "Options:"
            echo "  --by <FIELD>      Group by: status, type, priority, prefix [default: total only]"
            echo "  --status <STATUS> Filter by status before counting"
            echo "  --type <TYPE>     Filter by type before counting"
            echo "  --prefix <PREFIX> Filter by prefix before counting"
            echo "  --format <FMT>    Output format: table, json [default: table]"
            echo ""
            echo "Examples:"
            echo "  count-tasks.sh                    # Total count"
            echo "  count-tasks.sh --by status        # Count by status"
            echo "  count-tasks.sh --by type          # Count by type"
            echo "  count-tasks.sh --by priority      # Count by priority"
            echo "  count-tasks.sh --by prefix        # Count by ID prefix"
            echo "  count-tasks.sh --status READY     # Count READY tasks only"
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

# Use temp file for portable counting (avoids bash 4+ associative arrays)
TEMP_FILE=$(mktemp)
trap 'rm -f "$TEMP_FILE"' EXIT

total=0

for file in "$TASKS_DIR"/*.yaml; do
    [[ -f "$file" ]] || continue

    id=$(extract_field "$file" "id")
    status=$(extract_field "$file" "status")
    type=$(extract_field "$file" "type")
    priority=$(extract_field "$file" "priority")

    # Apply filters
    if [[ -n "$FILTER_STATUS" && "$status" != "$FILTER_STATUS" ]]; then
        continue
    fi

    if [[ -n "$FILTER_TYPE" && "$type" != "$FILTER_TYPE" ]]; then
        continue
    fi

    if [[ -n "$FILTER_PREFIX" ]]; then
        prefix="${id%%-*}"
        if [[ "$prefix" != "$FILTER_PREFIX" ]]; then
            continue
        fi
    fi

    # Count total
    ((total++))

    # Record group key if grouping
    if [[ -n "$GROUP_BY" ]]; then
        case "$GROUP_BY" in
            status)
                key="${status:-UNKNOWN}"
                ;;
            type)
                key="${type:-UNKNOWN}"
                ;;
            priority)
                key="${priority:-MEDIUM}"
                ;;
            prefix)
                key="${id%%-*}"
                ;;
            *)
                echo "Unknown group-by field: $GROUP_BY" >&2
                exit 1
                ;;
        esac
        echo "$key" >> "$TEMP_FILE"
    fi
done

# Output results
case "$OUTPUT_FORMAT" in
    table)
        if [[ -z "$GROUP_BY" ]]; then
            echo "Total: $total"
        else
            printf "%-15s %s\n" "$(echo "$GROUP_BY" | tr '[:lower:]' '[:upper:]')" "COUNT"
            printf "%-15s %s\n" "---------------" "-----"

            # Count occurrences and sort
            if [[ -s "$TEMP_FILE" ]]; then
                sort "$TEMP_FILE" | uniq -c | while read -r count key; do
                    printf "%-15s %d\n" "$key" "$count"
                done
            fi
            echo "---------------"
            printf "%-15s %d\n" "TOTAL" "$total"
        fi
        ;;

    json)
        if [[ -z "$GROUP_BY" ]]; then
            echo "{\"total\": $total}"
        else
            echo "{"
            echo "  \"group_by\": \"$GROUP_BY\","
            echo "  \"counts\": {"
            first=true
            if [[ -s "$TEMP_FILE" ]]; then
                sort "$TEMP_FILE" | uniq -c | while read -r count key; do
                    if [[ "$first" == "true" ]]; then
                        first=false
                    else
                        printf ',\n'
                    fi
                    printf '    "%s": %d' "$key" "$count"
                done
            fi
            echo ""
            echo "  },"
            echo "  \"total\": $total"
            echo "}"
        fi
        ;;
esac
