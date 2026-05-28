#!/bin/bash

# Fresh Context Ralph Loop Utility
# Launches Ralph loops that use a fresh Claude session for every iteration.
# This prevents context accumulation and history-based confusion.

set -euo pipefail

# Parse arguments
PROMPT_PARTS=()
MAX_ITERATIONS=0
COMPLETION_PROMISE=""
TASK_ID="fresh-task"
MODE="yolo"

while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      cat << 'HELP_EOF'
Ralph Fresh Loop - Autonomous loop with fresh context per iteration

USAGE:
  /ralph-fresh [PROMPT...] [OPTIONS]

ARGUMENTS:
  PROMPT...    Task description to work on

OPTIONS:
  --task-id <id>                 Unique identifier (default: "fresh-task")
  --max-iterations <n>           Safety limit (default: 0 = unlimited)
  --completion-promise '<text>'  Phrase to stop the loop
  --mode <yolo|review>           yolo (default) or review (asks questions)

DESCRIPTION:
  Unlike the standard /ralph-loop which runs in one persistent session,
  /ralph-fresh starts a NEW Claude session for every iteration.
  
  This is useful when you want to avoid history-based hallucinations
  or when the task benefits from a "clean slate" at each step.
HELP_EOF
      exit 0
      ;;
    --task-id)
      TASK_ID="$2"
      shift 2
      ;;
    --max-iterations)
      MAX_ITERATIONS="$2"
      shift 2
      ;;
    --completion-promise)
      COMPLETION_PROMISE="$2"
      shift 2
      ;;
    --mode)
      MODE="$2"
      shift 2
      ;;
    *)
      PROMPT_PARTS+=("$1")
      shift
      ;;
  esac
done

PROMPT="${PROMPT_PARTS[*]}"

if [[ -z "$PROMPT" ]]; then
  echo "❌ Error: No prompt provided" >&2
  exit 1
fi

# We build the loop command
# We use a tracking file for iterations
ITERATION_FILE="/tmp/ralph-fresh-$(id -u)-${TASK_ID}-iter"
echo "1" > "$ITERATION_FILE"

echo "🔄 Starting Fresh Context Ralph Loop: $TASK_ID"
echo "   Mode: $MODE"
echo "   Safety Limit: $MAX_ITERATIONS"

# Clean up on exit
trap "rm -f $ITERATION_FILE; exit" SIGINT SIGTERM

while true; do
  ITER=$(cat "$ITERATION_FILE")
  
  if [[ $MAX_ITERATIONS -gt 0 ]] && [[ $ITER -gt $MAX_ITERATIONS ]]; then
    echo "🛑 Max iterations ($MAX_ITERATIONS) reached."
    break
  fi

  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🚀 ITERATION $ITER | $TASK_ID"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  # Construct the message for Claude
  # We include the iteration count and promise info in the prompt
  SYSTEM_CTX="You are Ralph (iteration $ITER). Work on the task below.

AT THE END of each iteration, update .claude/ralph-progress-${TASK_ID}.md with:
- What you completed this iteration
- Files changed
- Next steps
- Any blockers"

  if [[ -n "$COMPLETION_PROMISE" ]]; then
    SYSTEM_CTX="$SYSTEM_CTX

Output <promise>$COMPLETION_PROMISE</promise> ONLY when work is complete."
  fi

  # Run Claude with the prompt in non-interactive print mode
  # Use -p (print mode) for non-interactive execution
  # Use --dangerously-skip-permissions to ensure autonomy
  # Export RALPH_FRESH_MODE=1 so the stop hook allows clean exit (new Claude per iteration)
  export RALPH_FRESH_MODE=1
  FULL_PROMPT="$SYSTEM_CTX

TASK:
$PROMPT"
  claude -p --dangerously-skip-permissions "$FULL_PROMPT" > /tmp/ralph-fresh-last-output 2>&1 || {
    echo "⚠️ Claude session exited with error. Retrying next iteration..."
  }

  # Show output to user (streamed/tail)
  cat /tmp/ralph-fresh-last-output

  # Check for completion promise in the output
  if [[ -n "$COMPLETION_PROMISE" ]] && grep -q "<promise>$COMPLETION_PROMISE</promise>" /tmp/ralph-fresh-last-output; then
    echo "✅ Ralph loop $TASK_ID complete: Detected completion promise."
    break
  fi

  # Increment iteration
  echo $((ITER + 1)) > "$ITERATION_FILE"
  
  # Slight delay to allow user to break if needed
  sleep 2
done

rm -f "$ITERATION_FILE" /tmp/ralph-fresh-last-output
echo "✅ Fresh loop finished."
