#!/bin/bash
# show-tasks.sh - Friendly wrapper for find-tasks.sh with formatted output
# Usage: show-tasks.sh [status_filter] [vault_path]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIND_TASKS="$SCRIPT_DIR/find-tasks.sh"

# Run find-tasks and format output
"$FIND_TASKS" "$@" | awk -F'|' '
BEGIN {
    current_category = ""
    count = 0
}
{
    category = $1
    status = $2
    file = $3
    line = $4
    task = $5

    # Print category header when it changes
    if (category != current_category) {
        if (current_category != "") print ""
        print toupper(substr(category, 1, 1)) substr(category, 2) ":"
        current_category = category
    }

    # Print task with status marker if present
    status_display = (status == " " || status == "") ? "[ ]" : "[" status "]"
    printf "  %s %s\n", status_display, task
    printf "    File: %s (line %s)\n", file, line
    count++
}
END {
    if (count > 0) {
        print ""
        print "Total tasks: " count
    } else {
        print "No tasks found."
    }
}
'
