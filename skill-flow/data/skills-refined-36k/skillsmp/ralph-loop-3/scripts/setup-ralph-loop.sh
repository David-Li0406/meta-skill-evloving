#!/bin/bash

# Ralph Loop Setup Script
# Creates state file for in-session Ralph loop
# Supports multiple concurrent loops via --task-id

set -euo pipefail

# Parse arguments
PROMPT_PARTS=()
MAX_ITERATIONS=0
COMPLETION_PROMISE="null"
TASK_ID="default"
MODE="yolo"  # yolo = autonomous, review = ask questions at milestones

# Parse options and positional arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      cat << 'HELP_EOF'
Ralph Loop - Interactive self-referential development loop

USAGE:
  /ralph-loop [PROMPT...] [OPTIONS]

ARGUMENTS:
  PROMPT...    Initial prompt to start the loop (can be multiple words without quotes)

OPTIONS:
  --task-id <id>                 Unique identifier for this loop (default: "default")
                                 Use different IDs to run multiple Ralphs concurrently!
  --max-iterations <n>           Maximum iterations before auto-stop (default: unlimited)
  --completion-promise '<text>'  Promise phrase (USE QUOTES for multi-word)
  --mode <yolo|review>           yolo = autonomous (default), review = ask questions
  -h, --help                     Show this help message

DESCRIPTION:
  Starts a Ralph Loop in your CURRENT session. The stop hook prevents
  exit and feeds your output back as input until completion or iteration limit.

  To signal completion, you must output: <promise>YOUR_PHRASE</promise>

  Use this for:
  - Interactive iteration where you want to see progress
  - Tasks requiring self-correction and refinement
  - Learning how Ralph works

CONCURRENT LOOPS:
  Run multiple Ralphs by using different --task-id values:

    # Terminal 1: Trading system
    /ralph-loop --task-id trading Build trading system --max-iterations 50

    # Terminal 2: Zone completion
    /ralph-loop --task-id zones Complete zone design --max-iterations 50

  Each loop runs independently in its own session!

EXAMPLES:
  /ralph-loop Build a todo API --completion-promise 'DONE' --max-iterations 20
  /ralph-loop --task-id api-work Fix the auth bug --max-iterations 10
  /ralph-loop --task-id refactor Refactor cache layer
  /ralph-loop --completion-promise 'TASK COMPLETE' Create a REST API

REVIEW MODE:
  Use --mode review to ask user questions at decision points.

  To ask a question:
    1. Write to .claude/ralph-steering-{task-id}.md with status: pending
    2. On next iteration, use AskUserQuestion tool to wait for response
    3. Update file with status: answered and the response
    4. Continue with user's decision

STOPPING:
  Only by reaching --max-iterations or detecting --completion-promise
  No manual stop - Ralph runs infinitely by default!

  To manually cancel a specific loop:
    rm .claude/ralph-loop-{task-id}.local.md

MONITORING:
  # View specific loop iteration:
  grep '^iteration:' .claude/ralph-loop-{task-id}.local.md

  # List all active loops:
  ls .claude/ralph-loop-*.local.md 2>/dev/null

  # View full state:
  head -15 .claude/ralph-loop-{task-id}.local.md
HELP_EOF
      exit 0
      ;;
    --task-id)
      if [[ -z "${2:-}" ]]; then
        echo "❌ Error: --task-id requires an identifier" >&2
        echo "" >&2
        echo "   Valid examples:" >&2
        echo "     --task-id trading" >&2
        echo "     --task-id zone-completion" >&2
        echo "     --task-id my-feature" >&2
        echo "" >&2
        echo "   Use different IDs to run multiple Ralphs concurrently!" >&2
        exit 1
      fi
      # Sanitize task ID (alphanumeric and hyphens only)
      TASK_ID=$(echo "$2" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g')
      shift 2
      ;;
    --max-iterations)
      if [[ -z "${2:-}" ]]; then
        echo "❌ Error: --max-iterations requires a number argument" >&2
        echo "" >&2
        echo "   Valid examples:" >&2
        echo "     --max-iterations 10" >&2
        echo "     --max-iterations 50" >&2
        echo "     --max-iterations 0  (unlimited)" >&2
        echo "" >&2
        echo "   You provided: --max-iterations (with no number)" >&2
        exit 1
      fi
      if ! [[ "$2" =~ ^[0-9]+$ ]]; then
        echo "❌ Error: --max-iterations must be a positive integer or 0, got: $2" >&2
        echo "" >&2
        echo "   Valid examples:" >&2
        echo "     --max-iterations 10" >&2
        echo "     --max-iterations 50" >&2
        echo "     --max-iterations 0  (unlimited)" >&2
        echo "" >&2
        echo "   Invalid: decimals (10.5), negative numbers (-5), text" >&2
        exit 1
      fi
      MAX_ITERATIONS="$2"
      shift 2
      ;;
    --completion-promise)
      if [[ -z "${2:-}" ]]; then
        echo "❌ Error: --completion-promise requires a text argument" >&2
        echo "" >&2
        echo "   Valid examples:" >&2
        echo "     --completion-promise 'DONE'" >&2
        echo "     --completion-promise 'TASK COMPLETE'" >&2
        echo "     --completion-promise 'All tests passing'" >&2
        echo "" >&2
        echo "   You provided: --completion-promise (with no text)" >&2
        echo "" >&2
        echo "   Note: Multi-word promises must be quoted!" >&2
        exit 1
      fi
      COMPLETION_PROMISE="$2"
      shift 2
      ;;
    --mode)
      if [[ -z "${2:-}" ]]; then
        echo "❌ Error: --mode requires 'yolo' or 'review'" >&2
        exit 1
      fi
      if [[ "$2" != "yolo" ]] && [[ "$2" != "review" ]]; then
        echo "❌ Error: --mode must be 'yolo' or 'review', got: $2" >&2
        echo "" >&2
        echo "   yolo   = autonomous, no questions (default)" >&2
        echo "   review = ask questions at milestones" >&2
        exit 1
      fi
      MODE="$2"
      shift 2
      ;;
    *)
      # Non-option argument - collect all as prompt parts
      PROMPT_PARTS+=("$1")
      shift
      ;;
  esac
done

# Join all prompt parts with spaces
PROMPT="${PROMPT_PARTS[*]}"

# Validate prompt is non-empty
if [[ -z "$PROMPT" ]]; then
  echo "❌ Error: No prompt provided" >&2
  echo "" >&2
  echo "   Ralph needs a task description to work on." >&2
  echo "" >&2
  echo "   Examples:" >&2
  echo "     /ralph-loop Build a REST API for todos" >&2
  echo "     /ralph-loop --task-id api Fix the auth bug --max-iterations 20" >&2
  echo "     /ralph-loop --completion-promise 'DONE' Refactor code" >&2
  echo "" >&2
  echo "   For all options: /ralph-loop --help" >&2
  exit 1
fi

# Create state file for stop hook (markdown with YAML frontmatter)
mkdir -p .claude

# Auto-generate unique task-id if "default" is used
if [[ "$TASK_ID" == "default" ]]; then
  # Generate unique ID: short hash of prompt + timestamp
  HASH=$(echo "$PROMPT" | md5sum | cut -c1-6)
  TASK_ID="task-${HASH}"
  echo "ℹ️  Auto-generated task-id: $TASK_ID" >&2
fi

# Determine state file path based on task ID
RALPH_STATE_FILE=".claude/ralph-loop-${TASK_ID}.local.md"

# Check if this loop already exists - auto-append suffix to avoid collision
if [[ -f "$RALPH_STATE_FILE" ]]; then
  # Check if existing loop is for THIS session (same transcript) - allow restart
  EXISTING_SESSION=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$RALPH_STATE_FILE" | grep '^session_transcript:' | sed 's/session_transcript: *//' | sed 's/^"\(.*\)"$/\1/')

  # If unclaimed or different session, generate unique suffix
  if [[ "$EXISTING_SESSION" == "null" ]] || [[ -z "$EXISTING_SESSION" ]]; then
    SUFFIX=$(date +%s | tail -c 5)
    TASK_ID="${TASK_ID}-${SUFFIX}"
    RALPH_STATE_FILE=".claude/ralph-loop-${TASK_ID}.local.md"
    echo "⚠️  Task-id collision detected. Using unique id: $TASK_ID" >&2
  fi
fi

# Final check - if still exists after suffix, something is wrong
if [[ -f "$RALPH_STATE_FILE" ]]; then
  echo "⚠️  Warning: Loop '$TASK_ID' already exists!" >&2
  echo "   File: $RALPH_STATE_FILE" >&2
  echo "" >&2
  echo "   Options:" >&2
  echo "     • Cancel existing: rm $RALPH_STATE_FILE" >&2
  echo "     • Use different ID: --task-id another-name" >&2
  echo "" >&2
  read -p "   Overwrite existing loop? [y/N] " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "   Aborted."
    exit 1
  fi
fi

# Quote completion promise for YAML if it contains special chars or is not null
if [[ -n "$COMPLETION_PROMISE" ]] && [[ "$COMPLETION_PROMISE" != "null" ]]; then
  COMPLETION_PROMISE_YAML="\"$COMPLETION_PROMISE\""
else
  COMPLETION_PROMISE_YAML="null"
fi

cat > "$RALPH_STATE_FILE" <<EOF
---
active: true
task_id: "$TASK_ID"
iteration: 1
max_iterations: $MAX_ITERATIONS
completion_promise: $COMPLETION_PROMISE_YAML
mode: "$MODE"
session_transcript: null
started_at: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
---

$PROMPT
EOF

# Output setup message
cat <<EOF
🔄 Ralph loop '$TASK_ID' activated!

Task ID: $TASK_ID
State file: $RALPH_STATE_FILE
Iteration: 1
Max iterations: $(if [[ $MAX_ITERATIONS -gt 0 ]]; then echo $MAX_ITERATIONS; else echo "unlimited"; fi)
Mode: $(if [[ "$MODE" == "review" ]]; then echo "review (will ask questions)"; else echo "yolo (autonomous)"; fi)
Completion promise: $(if [[ "$COMPLETION_PROMISE" != "null" ]]; then echo "${COMPLETION_PROMISE//\"/} (ONLY output when TRUE - do not lie!)"; else echo "none (runs forever)"; fi)

The stop hook is now active. When you try to exit, the SAME PROMPT will be
fed back to you. You'll see your previous work in files, creating a
self-referential loop where you iteratively improve on the same task.

To monitor: head -15 $RALPH_STATE_FILE
To cancel:  rm $RALPH_STATE_FILE

EOF

# Show other active loops if any
OTHER_LOOPS=$(ls .claude/ralph-loop*.local.md 2>/dev/null | grep -v "^${RALPH_STATE_FILE}$" || true)
if [[ -n "$OTHER_LOOPS" ]]; then
  echo "📋 Other active loops:"
  for loop in $OTHER_LOOPS; do
    loop_id=$(grep '^task_id:' "$loop" 2>/dev/null | sed 's/task_id: *"//' | sed 's/"$//' || echo "unknown")
    loop_iter=$(grep '^iteration:' "$loop" 2>/dev/null | sed 's/iteration: *//' || echo "?")
    echo "   • $loop_id (iteration $loop_iter) - $loop"
  done
  echo ""
fi

cat <<EOF
⚠️  WARNING: This loop cannot be stopped manually! It will run infinitely
    unless you set --max-iterations or --completion-promise.

🔄
EOF

# Output the initial prompt if provided
if [[ -n "$PROMPT" ]]; then
  echo ""
  echo "$PROMPT"
fi

# Display completion promise requirements if set
if [[ "$COMPLETION_PROMISE" != "null" ]]; then
  echo ""
  echo "═══════════════════════════════════════════════════════════"
  echo "CRITICAL - Ralph Loop Completion Promise"
  echo "═══════════════════════════════════════════════════════════"
  echo ""
  echo "To complete this loop, output this EXACT text:"
  echo "  <promise>$COMPLETION_PROMISE</promise>"
  echo ""
  echo "STRICT REQUIREMENTS (DO NOT VIOLATE):"
  echo "  ✓ Use <promise> XML tags EXACTLY as shown above"
  echo "  ✓ The statement MUST be completely and unequivocally TRUE"
  echo "  ✓ Do NOT output false statements to exit the loop"
  echo "  ✓ Do NOT lie even if you think you should exit"
  echo ""
  echo "IMPORTANT - Do not circumvent the loop:"
  echo "  Even if you believe you're stuck, the task is impossible,"
  echo "  or you've been running too long - you MUST NOT output a"
  echo "  false promise statement. The loop is designed to continue"
  echo "  until the promise is GENUINELY TRUE. Trust the process."
  echo ""
  echo "  If the loop should stop, the promise statement will become"
  echo "  true naturally. Do not force it by lying."
  echo "═══════════════════════════════════════════════════════════"
fi
