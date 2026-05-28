#!/bin/bash
# find-tasks.sh - Find tasks in Obsidian vault with status filtering
# Usage: find-tasks.sh [status_filter] [vault_path]
#   status_filter: all | incomplete | x | f | / | b | ?
#   vault_path: defaults to current directory

set -euo pipefail

# Parse arguments
STATUS_FILTER="${1:-all}"
VAULT_PATH="${2:-.}"

# Validate vault path exists
if [[ ! -d "$VAULT_PATH" ]]; then
    echo "Error: Vault path '$VAULT_PATH' does not exist" >&2
    exit 1
fi

# Define search directories (PARA structure)
SEARCH_DIRS=(
    "$VAULT_PATH/00_Inbox"
    "$VAULT_PATH/01_Projects"
    "$VAULT_PATH/02_Areas"
)

# Build grep pattern based on status filter
case "$STATUS_FILTER" in
    all)
        PATTERN='\- \[.\]'
        ;;
    incomplete)
        PATTERN='\- \[[^x]\]'
        ;;
    x|f|/|b|\?)
        PATTERN="\- \[${STATUS_FILTER}\]"
        ;;
    *)
        echo "Error: Invalid status filter '$STATUS_FILTER'" >&2
        echo "Valid options: all, incomplete, x, f, /, b, ?" >&2
        exit 1
        ;;
esac

# Function to categorize file path
categorize_path() {
    local path="$1"
    if [[ "$path" == *"/00_Inbox/"* ]]; then
        echo "inbox"
    elif [[ "$path" == *"/01_Projects/"* ]]; then
        echo "projects"
    elif [[ "$path" == *"/02_Areas/"* ]]; then
        echo "areas"
    else
        echo "other"
    fi
}

# Find and format tasks
for dir in "${SEARCH_DIRS[@]}"; do
    if [[ ! -d "$dir" ]]; then
        continue
    fi

    # Use grep to find tasks with line numbers
    # -n: show line numbers
    # -r: recursive
    # -H: show filename
    # --include: only .md files
    grep -nrH --include="*.md" "$PATTERN" "$dir" 2>/dev/null | while IFS=: read -r filepath linenum content; do
        # Make path relative to vault
        rel_path="${filepath#$VAULT_PATH/}"
        category=$(categorize_path "$filepath")

        # Extract status character
        status=$(echo "$content" | sed -n 's/.*\[\(.\)\].*/\1/p')

        # Clean up task content (remove checkbox)
        task_text=$(echo "$content" | sed 's/\- \[.\] //')

        # Output format: category|status|file|line|task
        echo "${category}|${status}|${rel_path}|${linenum}|${task_text}"
    done
done | sort -t'|' -k1,1 -k2,2 -k3,3
