#!/bin/bash
# create-task.sh — Create a new task file
# Part of the Dialogue Framework
# Usage: create-task.sh <PREFIX> <TITLE> [options]
#
# Required:
#   PREFIX              Task ID prefix (SH, CD, FW, DOC, VAL)
#   TITLE               Task title (brief description)
#
# Options:
#   --status <STATUS>   Initial status [default: BACKLOG]
#   --type <TYPE>       Task type (CAPABILITY, SCHEMA, DOCUMENT, RESEARCH, DEBT, DECISION)
#   --priority <PRIO>   Priority (CRITICAL, HIGH, MEDIUM, LOW) [default: MEDIUM]
#   --phase <N>         SDLC phase (1-7)
#   --description <D>   Full description
#   --objective <O>     Success criteria
#   --rationale <R>     Why this is needed
#   --blocked-by <IDS>  Comma-separated IDs of blocking tasks
#   --blocks <IDS>      Comma-separated IDs this blocks
#   --notes <N>         Initial notes
#   --id <ID>           Use specific ID instead of auto-generating

set -euo pipefail

PROJECT_ROOT="${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR must be set}"
TASKS_DIR="${PROJECT_ROOT}/.dialogue/tasks"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Validate minimum arguments
if [[ $# -lt 2 ]]; then
    echo "Usage: create-task.sh <PREFIX> <TITLE> [options]" >&2
    echo "" >&2
    echo "Required:" >&2
    echo "  PREFIX              Task ID prefix (SH, CD, FW, DOC, VAL)" >&2
    echo "  TITLE               Task title" >&2
    echo "" >&2
    echo "Options:" >&2
    echo "  --status <STATUS>   Initial status [default: BACKLOG]" >&2
    echo "  --type <TYPE>       Task type (CAPABILITY, SCHEMA, etc.)" >&2
    echo "  --priority <PRIO>   Priority [default: MEDIUM]" >&2
    echo "  --phase <N>         SDLC phase (1-7)" >&2
    echo "  --description <D>   Full description" >&2
    echo "  --objective <O>     Success criteria" >&2
    echo "  --rationale <R>     Why needed" >&2
    echo "  --blocked-by <IDS>  Comma-separated blocking task IDs" >&2
    echo "  --blocks <IDS>      Comma-separated IDs this blocks" >&2
    echo "  --notes <N>         Initial notes" >&2
    echo "  --id <ID>           Use specific ID (skip auto-generation)" >&2
    exit 1
fi

PREFIX="$1"
TITLE="$2"
shift 2

# Defaults
STATUS="BACKLOG"
TYPE=""
PRIORITY="MEDIUM"
PHASE=""
DESCRIPTION=""
OBJECTIVE=""
RATIONALE=""
BLOCKED_BY=""
BLOCKS=""
NOTES=""
EXPLICIT_ID=""

# Parse options
while [[ $# -gt 0 ]]; do
    case "$1" in
        --status)
            STATUS="$2"
            shift 2
            ;;
        --type)
            TYPE="$2"
            shift 2
            ;;
        --priority)
            PRIORITY="$2"
            shift 2
            ;;
        --phase)
            PHASE="$2"
            shift 2
            ;;
        --description)
            DESCRIPTION="$2"
            shift 2
            ;;
        --objective)
            OBJECTIVE="$2"
            shift 2
            ;;
        --rationale)
            RATIONALE="$2"
            shift 2
            ;;
        --blocked-by)
            BLOCKED_BY="$2"
            shift 2
            ;;
        --blocks)
            BLOCKS="$2"
            shift 2
            ;;
        --notes)
            NOTES="$2"
            shift 2
            ;;
        --id)
            EXPLICIT_ID="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Validate status
case "$STATUS" in
    BACKLOG|READY|IN_PROGRESS|BLOCKED|COMPLETED|CANCELLED) ;;
    *)
        echo "Error: Invalid status '$STATUS'" >&2
        echo "Valid: BACKLOG, READY, IN_PROGRESS, BLOCKED, COMPLETED, CANCELLED" >&2
        exit 1
        ;;
esac

# Validate type if provided
if [[ -n "$TYPE" ]]; then
    case "$TYPE" in
        CAPABILITY|SCHEMA|DOCUMENT|RESEARCH|DEBT|DECISION) ;;
        *)
            echo "Error: Invalid type '$TYPE'" >&2
            echo "Valid: CAPABILITY, SCHEMA, DOCUMENT, RESEARCH, DEBT, DECISION" >&2
            exit 1
            ;;
    esac
fi

# Validate priority
case "$PRIORITY" in
    CRITICAL|HIGH|MEDIUM|LOW) ;;
    *)
        echo "Error: Invalid priority '$PRIORITY'" >&2
        echo "Valid: CRITICAL, HIGH, MEDIUM, LOW" >&2
        exit 1
        ;;
esac

# Validate phase if provided
if [[ -n "$PHASE" ]]; then
    if [[ ! "$PHASE" =~ ^[1-7]$ ]]; then
        echo "Error: Phase must be 1-7" >&2
        exit 1
    fi
fi

# Ensure tasks directory exists
mkdir -p "$TASKS_DIR"

# Generate or use explicit ID
if [[ -n "$EXPLICIT_ID" ]]; then
    TASK_ID="$EXPLICIT_ID"
    # Validate explicit ID format
    if [[ ! "$TASK_ID" =~ ^[A-Z]{2,4}-[0-9]{3}$ ]]; then
        echo "Error: ID must match pattern PREFIX-NNN (e.g., FW-001)" >&2
        exit 1
    fi
else
    TASK_ID=$("$SCRIPT_DIR/next-id.sh" "$PREFIX")
fi

# Check ID doesn't already exist
TASK_FILE="$TASKS_DIR/${TASK_ID}.yaml"
if [[ -f "$TASK_FILE" ]]; then
    echo "Error: Task $TASK_ID already exists" >&2
    exit 1
fi

# Generate timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Helper: Convert comma-separated IDs to YAML array
to_yaml_array() {
    local input="$1"
    if [[ -z "$input" ]]; then
        echo "[]"
        return
    fi
    # Split by comma and format as YAML array
    local result="["
    local first=true
    IFS=',' read -ra items <<< "$input"
    for item in "${items[@]}"; do
        item=$(echo "$item" | xargs)  # trim whitespace
        if [[ "$first" == "true" ]]; then
            first=false
        else
            result+=", "
        fi
        result+="\"$item\""
    done
    result+="]"
    echo "$result"
}

# Build YAML content
{
    echo "id: \"$TASK_ID\""
    echo "title: \"$TITLE\""
    echo "status: $STATUS"
    echo "created: \"$TIMESTAMP\""
    echo "updated: \"$TIMESTAMP\""

    if [[ -n "$TYPE" ]]; then
        echo "type: $TYPE"
    fi

    if [[ -n "$PHASE" ]]; then
        echo "phase: $PHASE"
    fi

    echo "priority: $PRIORITY"

    if [[ -n "$DESCRIPTION" ]]; then
        echo "description: |"
        # Indent each line of description
        echo "$DESCRIPTION" | sed 's/^/  /'
    fi

    if [[ -n "$OBJECTIVE" ]]; then
        echo "objective: \"$OBJECTIVE\""
    fi

    if [[ -n "$RATIONALE" ]]; then
        echo "rationale: |"
        echo "$RATIONALE" | sed 's/^/  /'
    fi

    echo "blocked_by: $(to_yaml_array "$BLOCKED_BY")"
    echo "blocks: $(to_yaml_array "$BLOCKS")"

    if [[ -n "$NOTES" ]]; then
        echo "notes: |"
        echo "$NOTES" | sed 's/^/  /'
    else
        # Add default creation note
        created_date=$(date -u +"%d %B %Y")
        echo "notes: |"
        echo "  Created $created_date."
    fi
} > "$TASK_FILE"

echo "$TASK_ID"
