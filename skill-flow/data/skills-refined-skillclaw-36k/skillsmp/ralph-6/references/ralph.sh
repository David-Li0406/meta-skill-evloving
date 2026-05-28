#!/bin/bash
# Ralph Wiggum - Long-running AI Agent
# Run a coding agent with a clean slate, again and again until complete

set -e

# Configuration
MAX_ITERATIONS=${MAX_ITERATIONS:-10}
PROJECT_DIR=${PROJECT_DIR:-$(pwd)}
PRD_FILE=${PRD_FILE:-"ralph/prd.json"}
PROGRESS_FILE=${PROGRESS_FILE:-"ralph/progress.txt"}
AGENT_CMD=${AGENT_CMD:-"claude --dangerously-skip-permissions"}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Ralph Wiggum - Long-Running AI Agent${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Project: ${GREEN}$PROJECT_DIR${NC}"
echo -e "PRD File: ${GREEN}$PRD_FILE${NC}"
echo -e "Max Iterations: ${GREEN}$MAX_ITERATIONS${NC}"
echo ""

# Ensure we're in the project directory
cd "$PROJECT_DIR"

# Check if PRD file exists
if [ ! -f "$PRD_FILE" ]; then
    echo -e "${RED}Error: PRD file not found at $PRD_FILE${NC}"
    echo "Create a PRD file first with: ralph/create-prd.sh"
    exit 1
fi

# Initialize progress file if it doesn't exist
if [ ! -f "$PROGRESS_FILE" ]; then
    echo "# Ralph Progress Log" > "$PROGRESS_FILE"
    echo "# Started: $(date -u +"%Y-%m-%dT%H:%M:%SZ")" >> "$PROGRESS_FILE"
    echo "" >> "$PROGRESS_FILE"
fi

# Build the prompt
build_prompt() {
    local prd_content=$(cat "$PRD_FILE")
    local progress_content=""
    if [ -f "$PROGRESS_FILE" ]; then
        progress_content=$(cat "$PROGRESS_FILE")
    fi

    cat << EOF
You are working on a software project using the Ralph Wiggum methodology.

## Your Task
1. Read the PRD below and find the HIGHEST PRIORITY feature where "passes": false
2. Work ONLY on that single feature - do not try to do multiple features
3. Implement the feature completely
4. Run tests and type checks to ensure CI stays green
5. Commit your work with a clear commit message
6. Update the PRD file to set "passes": true for the completed feature
7. Append a progress entry to $PROGRESS_FILE with:
   - Timestamp
   - Feature completed
   - Brief summary of changes
   - Files modified

## Stop Condition
If ALL features in the PRD have "passes": true, respond with:
<promise>COMPLETE</promise>

If you complete one feature successfully, respond with:
<promise>ITERATION_DONE</promise>

## PRD (Product Requirements Document)
\`\`\`json
$prd_content
\`\`\`

## Progress So Far
\`\`\`
$progress_content
\`\`\`

## Important Rules
- Pick ONE feature only - the highest priority incomplete one
- Keep changes small and focused
- Always run tests before committing
- Always run type checks before committing
- If tests fail, fix them before moving on
- If you can't complete a feature, document why in progress.txt and move to the next one
- Use the existing code patterns in the repo

Begin working on the highest priority incomplete feature now.
EOF
}

# Main loop
for i in $(seq 1 $MAX_ITERATIONS); do
    echo -e "${YELLOW}========================================${NC}"
    echo -e "${YELLOW}  Iteration $i of $MAX_ITERATIONS${NC}"
    echo -e "${YELLOW}========================================${NC}"
    echo ""

    # Check if all tasks are complete before starting
    incomplete_count=$(jq '[.features[] | select(.passes == false)] | length' "$PRD_FILE" 2>/dev/null || echo "0")
    if [ "$incomplete_count" = "0" ]; then
        echo -e "${GREEN}All PRD features are complete!${NC}"
        break
    fi

    echo -e "Incomplete features: ${RED}$incomplete_count${NC}"
    echo ""

    # Build prompt and run agent
    PROMPT=$(build_prompt)

    # Create a temporary file for the prompt
    PROMPT_FILE=$(mktemp)
    echo "$PROMPT" > "$PROMPT_FILE"

    # Run the agent and capture output
    OUTPUT_FILE=$(mktemp)
    echo -e "${BLUE}Starting Claude Code agent...${NC}"
    echo ""

    # Run claude with the prompt (interactive mode uses Max subscription)
    if echo "$PROMPT" | $AGENT_CMD 2>&1 | tee "$OUTPUT_FILE"; then
        echo ""
    else
        echo -e "${RED}Agent exited with error${NC}"
    fi

    # Check for completion signals
    if grep -q "<promise>COMPLETE</promise>" "$OUTPUT_FILE"; then
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}  ALL FEATURES COMPLETE!${NC}"
        echo -e "${GREEN}========================================${NC}"
        rm "$PROMPT_FILE" "$OUTPUT_FILE"
        break
    fi

    if grep -q "<promise>ITERATION_DONE</promise>" "$OUTPUT_FILE"; then
        echo ""
        echo -e "${GREEN}Iteration $i completed successfully${NC}"
    fi

    # Cleanup temp files
    rm "$PROMPT_FILE" "$OUTPUT_FILE"

    # Small delay between iterations
    echo ""
    echo -e "${BLUE}Waiting 5 seconds before next iteration...${NC}"
    sleep 5
done

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Ralph Session Complete${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Progress log: $PROGRESS_FILE"
echo "PRD status: $PRD_FILE"
