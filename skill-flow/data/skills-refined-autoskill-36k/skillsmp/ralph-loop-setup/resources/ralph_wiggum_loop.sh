#!/bin/bash

# Ralph Wiggum Loop - Automated Task Implementation
# "I'm helping!" - Ralph Wiggum
#
# A simple loop that runs an AI coding assistant (claude or codex) to work through tasks.
# The AI handles all the intelligence: task selection, implementation,
# logging, and status updates.

set -u

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAX_ITERATIONS=${1:-999999}
TODO_FILE="${2:-${SCRIPT_DIR}/todolist.json}"
LOG_DIR="${SCRIPT_DIR}/logs"

# Resolve paths
TODO_FILE="$(cd "$(dirname "$TODO_FILE")" 2>/dev/null && pwd)/$(basename "$TODO_FILE")"
WORKING_DIR="$(dirname "$TODO_FILE")"
PROGRESS_FILE="${WORKING_DIR}/progress.txt"

mkdir -p "$LOG_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           Ralph Wiggum Loop - \"I'm helping!\"                   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Todo file: $TODO_FILE"
echo "Working dir: $WORKING_DIR"
echo "Max iterations: $MAX_ITERATIONS"
echo ""

# Detect AI CLI platform (codex or claude)
detect_ai_cli() {
    if command -v codex &> /dev/null; then
        echo "codex"
    elif command -v claude &> /dev/null; then
        echo "claude"
    else
        echo ""
    fi
}

AI_CLI=$(detect_ai_cli)

if [ -z "$AI_CLI" ]; then
    echo -e "${RED}Error: No AI CLI found. Install 'claude' or 'codex' CLI.${NC}"
    exit 1
fi

echo "Using AI CLI: $AI_CLI"

# Build the appropriate command based on detected CLI
run_ai_command() {
    local prompt="$1"
    local log_file="$2"

    if [ "$AI_CLI" = "codex" ]; then
        # Codex uses 'exec' subcommand with --full-auto and '-' for stdin
        echo "$prompt" | codex exec --full-auto - > "$log_file" 2>&1
    else
        # Claude Code uses --dangerously-skip-permissions and --print
        echo "$prompt" | claude --dangerously-skip-permissions --print > "$log_file" 2>&1
    fi
}

if [ ! -f "$TODO_FILE" ]; then
    echo -e "${RED}Error: Todo file not found: $TODO_FILE${NC}"
    exit 1
fi

# The prompt - this is where all the magic happens
create_prompt() {
    cat << 'EOF'
You are an AI assistant working through a project todo list.

## Your Task

1. **Read todolist.json** to see all tasks and their statuses
2. **Choose ONE task** that is:
   - Status is "pending" (not completed, failed, or in_progress)
   - Dependencies are satisfied (all tasks in "dependencies" array have status "passed")
   - Choose wisely based on priority, impact, and likelihood of success
3. **Implement the task** completely
4. **Update todolist.json** - set the task's status to "passed" or "failed"
5. **Append to progress.txt** with:
   - Timestamp and task ID
   - What you did
   - Any lessons learned for future iterations

## Important Rules

- Focus on ONE task only
- This is automated - no questions, just do the work
- Update both todolist.json and progress.txt before finishing
- If a task fails, mark it "failed" with notes explaining why
- If no eligible tasks remain, just report that and exit

## Files

- Todo list: TODOFILE_PLACEHOLDER
- Progress log: PROGRESSFILE_PLACEHOLDER
- Working directory: WORKINGDIR_PLACEHOLDER

Start now: Read the todo list, pick a task, implement it, update the files.
EOF
}

# Main loop
iteration=0

while [ $iteration -lt $MAX_ITERATIONS ]; do
    iteration=$((iteration + 1))

    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}Iteration $iteration${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"

    # Check if there are any pending tasks left
    pending_count=$(jq '[.tasks[] | select(.status == "pending")] | length' "$TODO_FILE" 2>/dev/null || echo "0")

    if [ "$pending_count" -eq 0 ]; then
        echo -e "${GREEN}All tasks completed!${NC}"
        break
    fi

    echo "Pending tasks: $pending_count"
    echo ""

    # Create prompt with actual paths
    prompt=$(create_prompt | sed \
        -e "s|TODOFILE_PLACEHOLDER|$TODO_FILE|g" \
        -e "s|PROGRESSFILE_PLACEHOLDER|$PROGRESS_FILE|g" \
        -e "s|WORKINGDIR_PLACEHOLDER|$WORKING_DIR|g")

    # Run AI CLI in the working directory
    log_file="${LOG_DIR}/iteration_${iteration}_$(date +%Y%m%d_%H%M%S).log"

    echo "Running $AI_CLI..."
    echo ""

    cd "$WORKING_DIR"
    if run_ai_command "$prompt" "$log_file"; then
        echo -e "${GREEN}Iteration $iteration completed${NC}"
    else
        exit_code=$?
        echo -e "${YELLOW}$AI_CLI exited with code $exit_code${NC}"
    fi

    echo "Log: $log_file"
    echo ""

    # Brief pause between iterations
    sleep 2
done

echo -e "${GREEN}Ralph Wiggum Loop finished after $iteration iterations${NC}"
