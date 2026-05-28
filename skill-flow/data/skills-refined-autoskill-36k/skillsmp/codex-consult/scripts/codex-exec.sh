#!/bin/bash
# Codex CLI wrapper script for codex-consult skill
#
# Usage: codex-exec.sh [OPTIONS] <TASK_DESCRIPTION>
# Options:
#   --model=<model>   Model to use (default: gpt-5.2-codex)
#   --mode=plan|patch Execution mode (default: plan)
#   --scope=<path>    Target directory (default: current)
#   --no-web          Disable web search (enabled by default)
#   --output=<file>   Output file path

set -euo pipefail

# Default values
MODEL="${CODEX_MODEL:-gpt-5.2-codex}"
MODE="plan"
SCOPE="${PWD}"
WEB_SEARCH="-c search=true"
OUTPUT_FILE="/tmp/codex-consult.last.md"
LOG_FILE="/tmp/codex-consult.run.log"
TASK=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --model=*)
            MODEL="${1#*=}"
            shift
            ;;
        --mode=*)
            MODE="${1#*=}"
            shift
            ;;
        --scope=*)
            SCOPE="${1#*=}"
            shift
            ;;
        --no-web)
            WEB_SEARCH=""
            shift
            ;;
        --output=*)
            OUTPUT_FILE="${1#*=}"
            shift
            ;;
        -*)
            echo "Error: Unknown option $1" >&2
            exit 1
            ;;
        *)
            TASK="$1"
            shift
            ;;
    esac
done

# Validate required arguments
if [[ -z "${TASK}" ]]; then
    echo "Error: Task description is required" >&2
    echo "Usage: codex-exec.sh [OPTIONS] <TASK_DESCRIPTION>" >&2
    exit 1
fi

# Validate mode
if [[ "$MODE" != "plan" && "$MODE" != "patch" ]]; then
    echo "Error: Invalid mode '$MODE'. Must be 'plan' or 'patch'" >&2
    exit 1
fi

# Build prompt based on mode
if [[ "$MODE" == "patch" ]]; then
    PROMPT="Analyze and propose changes for: ${TASK}

Please provide:
1. Summary of the proposed changes (what to change, assumptions, impact)
2. Unified diff format patches for each file that needs modification
3. Verification steps (test commands, manual verification, edge cases to check)

Format the diff sections as:
\`\`\`diff
--- a/path/to/file
+++ b/path/to/file
@@ -line,count +line,count @@
 context
-removed
+added
\`\`\`"
else
    PROMPT="Analyze and provide implementation plan for: ${TASK}

Please provide:
1. Summary (what to change, assumptions, prerequisites)
2. Implementation approach (step-by-step strategy, files to modify/create)
3. Verification steps (test commands, validation points, edge cases)

Be thorough in your analysis and consider:
- Existing code patterns and conventions
- Potential edge cases and error handling
- Testing strategy
- Performance implications if relevant"
fi

# Log the execution
echo "=== Codex Consult Execution ===" > "$LOG_FILE"
echo "Timestamp: $(date -Iseconds)" >> "$LOG_FILE"
echo "Model: $MODEL" >> "$LOG_FILE"
echo "Mode: $MODE" >> "$LOG_FILE"
echo "Scope: $SCOPE" >> "$LOG_FILE"
if [[ -n "$WEB_SEARCH" ]]; then
    echo "Web Search: enabled" >> "$LOG_FILE"
else
    echo "Web Search: disabled" >> "$LOG_FILE"
fi
echo "Task: $TASK" >> "$LOG_FILE"
echo "===" >> "$LOG_FILE"

# Execute Codex with read-only sandbox
codex exec \
    -m "$MODEL" \
    -s read-only \
    -C "$SCOPE" \
    $WEB_SEARCH \
    -o "$OUTPUT_FILE" \
    -c hide_agent_reasoning=true \
    "$PROMPT" >> "$LOG_FILE" 2>&1

EXIT_CODE=$?

# Check execution result
if [[ $EXIT_CODE -eq 0 ]] && [[ -s "$OUTPUT_FILE" ]]; then
    echo "=== Codex Output ===" >> "$LOG_FILE"
    cat "$OUTPUT_FILE" >> "$LOG_FILE"
    cat "$OUTPUT_FILE"
else
    echo "Error: Codex execution failed (exit code: $EXIT_CODE)" >&2
    echo "Check $LOG_FILE for details." >&2
    echo "" >&2
    echo "=== Log Contents ===" >&2
    cat "$LOG_FILE" >&2
    exit 1
fi
