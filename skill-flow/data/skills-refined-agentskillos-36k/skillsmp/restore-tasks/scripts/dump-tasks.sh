#!/bin/bash
# Dump all tasks from a session as JSON array

set -e

SESSION_ID="$1"
TASKS_DIR="$HOME/.claude/tasks/$SESSION_ID"

if [[ -z "$SESSION_ID" ]]; then
    echo "Usage: dump-tasks.sh <session-id>" >&2
    exit 1
fi

if [[ ! -d "$TASKS_DIR" ]]; then
    echo "No tasks found for session: $SESSION_ID" >&2
    exit 1
fi

# Output JSON array of all tasks
echo "["
first=1
for task_file in "$TASKS_DIR"/*.json; do
    [[ -f "$task_file" ]] || continue
    [[ $first -eq 0 ]] && echo ","
    first=0
    cat "$task_file"
done
echo "]"
