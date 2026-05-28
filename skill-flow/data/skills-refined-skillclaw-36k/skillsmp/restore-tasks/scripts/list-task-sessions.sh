#!/bin/bash
# List sessions that have persisted tasks for the current project
# Outputs JSON array sorted by modified time (most recent first)

set -e

CLAUDE_DIR="$HOME/.claude"
TASKS_DIR="$CLAUDE_DIR/tasks"
PROJECTS_DIR="$CLAUDE_DIR/projects"

# Default to 5 sessions, configurable via --limit
LIMIT=5
while [[ $# -gt 0 ]]; do
    case "$1" in
        --limit)
            LIMIT="$2"
            shift 2
            ;;
        --limit=*)
            LIMIT="${1#*=}"
            shift
            ;;
        --all)
            LIMIT=999999
            shift
            ;;
        *)
            PROJECT_PATH="$1"
            shift
            ;;
    esac
done

# Encode current path: /Users/bob/github.com/foo -> -Users-bob-github-com-foo
encode_path() {
    echo "$1" | sed 's|^/|-|' | tr '/.' '-'
}

# Get current project path
PROJECT_PATH="${PROJECT_PATH:-$(pwd)}"
ENCODED_PATH=$(encode_path "$PROJECT_PATH")
PROJECT_DIR="$PROJECTS_DIR/$ENCODED_PATH"
INDEX_FILE="$PROJECT_DIR/sessions-index.json"

if [[ ! -d "$PROJECT_DIR" ]]; then
    echo '{"error": "no_project_data", "message": "No Claude project data found"}'
    exit 1
fi

if [[ ! -d "$TASKS_DIR" ]]; then
    echo '{"error": "no_tasks_dir", "message": "No tasks directory found"}'
    exit 1
fi

if [[ ! -f "$INDEX_FILE" ]]; then
    echo '{"error": "no_index", "message": "No sessions index found"}'
    exit 1
fi

# Build JSON array of sessions with tasks
# Uses jq to parse sessions-index.json and filter/enrich with task data
jq -r --arg tasks_dir "$TASKS_DIR" --argjson limit "$LIMIT" '
    .entries
    | map(
        . as $session |
        ($tasks_dir + "/" + .sessionId) as $task_dir |
        # Check if task directory exists and count tasks
        (try ([$task_dir + "/*.json" | @sh | "ls -1 " + . + " 2>/dev/null | wc -l"] | .[0]) catch "0") as $count_cmd |
        {
            sessionId: .sessionId,
            summary: (.summary // "No summary"),
            modified: .modified,
            taskCount: null  # Will be filled by shell
        }
    )
    | sort_by(.modified)
    | reverse
' "$INDEX_FILE" | jq -c '.[]' | while read -r session; do
    session_id=$(echo "$session" | jq -r '.sessionId')
    task_dir="$TASKS_DIR/$session_id"

    # Only include sessions that have task files
    if [[ -d "$task_dir" ]]; then
        task_count=$(ls -1 "$task_dir"/*.json 2>/dev/null | wc -l | tr -d ' ')
        if [[ "$task_count" -gt 0 ]]; then
            echo "$session" | jq -c --argjson count "$task_count" '.taskCount = $count'
        fi
    fi
done | jq -s --argjson limit "$LIMIT" '
    . as $all |
    {
        sessions: .[:$limit],
        total: ($all | length),
        showing: ([($all | length), $limit] | min),
        hasMore: (($all | length) > $limit)
    }
'
