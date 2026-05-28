#!/bin/bash

# Backlog Stop Hook
# Generic hook that keeps agents working until task/review is complete
# Supports optional iteration limits for safety

set -euo pipefail

# Read hook input from stdin (provides transcript_path)
HOOK_INPUT=$(cat)

# Helper function to allow exit with proper JSON output
allow_exit() {
  echo '{"decision": "approve"}'
  exit 0
}

# Check if PROMPT.md exists (indicates we're in an agent worktree)
if [[ ! -f "PROMPT.md" ]]; then
  # Not an agent worktree - allow exit
  allow_exit
fi

# State file for iteration tracking (optional)
STATE_FILE=".claude/backlog-agent.local.md"

# Default values if no state file
ITERATION=1
MAX_ITERATIONS=0
MODE="implementation"

# Read state file if exists
if [[ -f "$STATE_FILE" ]]; then
  FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$STATE_FILE")
  ITERATION=$(echo "$FRONTMATTER" | grep '^iteration:' | sed 's/iteration: *//' || echo "1")
  MAX_ITERATIONS=$(echo "$FRONTMATTER" | grep '^max_iterations:' | sed 's/max_iterations: *//' || echo "0")
  MODE=$(echo "$FRONTMATTER" | grep '^mode:' | sed 's/mode: *//' | tr -d '"' || echo "implementation")

  # Validate numeric fields
  if [[ ! "$ITERATION" =~ ^[0-9]+$ ]]; then
    echo "⚠️  Backlog hook: Invalid iteration value in state file" >&2
    ITERATION=1
  fi
  if [[ ! "$MAX_ITERATIONS" =~ ^[0-9]+$ ]]; then
    MAX_ITERATIONS=0
  fi
fi

# Check if max iterations reached
if [[ $MAX_ITERATIONS -gt 0 ]] && [[ $ITERATION -ge $MAX_ITERATIONS ]]; then
  echo "🛑 Max iterations ($MAX_ITERATIONS) reached." >&2
  echo "   Task did not complete within iteration limit." >&2
  echo "   Check PROGRESS.md for current state." >&2
  [[ -f "$STATE_FILE" ]] && rm "$STATE_FILE"
  allow_exit
fi

# Get transcript path from hook input
TRANSCRIPT_PATH=$(echo "$HOOK_INPUT" | jq -r '.transcript_path')

if [[ ! -f "$TRANSCRIPT_PATH" ]]; then
  echo "⚠️  Backlog hook: Transcript file not found" >&2
  allow_exit
fi

# Check if there are any assistant messages
if ! grep -q '"role":"assistant"' "$TRANSCRIPT_PATH"; then
  # No assistant messages yet - allow exit (shouldn't normally happen)
  allow_exit
fi

# Extract last assistant message
LAST_LINE=$(grep '"role":"assistant"' "$TRANSCRIPT_PATH" | tail -1)
LAST_OUTPUT=$(echo "$LAST_LINE" | jq -r '
  .message.content |
  map(select(.type == "text")) |
  map(.text) |
  join("\n")
' 2>/dev/null || echo "")

# Check for completion promises using perl for multiline support
# Note: perl regex returns entire input if no match, so we check for actual tag presence first
if echo "$LAST_OUTPUT" | grep -q '<promise>'; then
  PROMISE_TEXT=$(echo "$LAST_OUTPUT" | perl -0777 -pe 's/.*?<promise>(.*?)<\/promise>.*/$1/s; s/^\s+|\s+$//g' 2>/dev/null || echo "")
else
  PROMISE_TEXT=""
fi

# Check for TASK_COMPLETE
if [[ "$PROMISE_TEXT" = "TASK_COMPLETE" ]]; then
  echo "✅ Task complete - implementation finished" >&2
  [[ -f "$STATE_FILE" ]] && rm "$STATE_FILE"
  allow_exit
fi

# Check for REVIEW_COMPLETE
if [[ "$PROMISE_TEXT" = "REVIEW_COMPLETE" ]]; then
  echo "✅ Review complete - code review finished" >&2
  [[ -f "$STATE_FILE" ]] && rm "$STATE_FILE"
  allow_exit
fi

# Check for TASK_BLOCKED (with optional reason)
if [[ "$PROMISE_TEXT" = "TASK_BLOCKED" ]] || [[ "$PROMISE_TEXT" == TASK_BLOCKED:* ]]; then
  echo "⚠️  Task blocked - agent reported blocker" >&2
  if [[ "$PROMISE_TEXT" == TASK_BLOCKED:* ]]; then
    REASON="${PROMISE_TEXT#TASK_BLOCKED:}"
    echo "   Reason: $REASON" >&2
  fi
  [[ -f "$STATE_FILE" ]] && rm "$STATE_FILE"
  allow_exit
fi

# Fallback: Check for Phase 1 completion indicators in the output text
# This catches cases where the agent doesn't output the exact promise tag format
if echo "$LAST_OUTPUT" | grep -qiE "phase.?1.*(complete|done|finished)" && \
   echo "$LAST_OUTPUT" | grep -qiE "main.?worktree|switch.*main|exit.*session|phase.?2"; then
  echo "✅ Phase 1 complete detected - allowing exit for worktree switch" >&2
  [[ -f "$STATE_FILE" ]] && rm "$STATE_FILE"
  allow_exit
fi

# Fallback: Check for "Pending Merge" status indicator (Phase 1 sets this)
if echo "$LAST_OUTPUT" | grep -qiE "pending.?merge" && \
   echo "$LAST_OUTPUT" | grep -qiE "phase.?2|main.?worktree|proceed.*main|switch.*main"; then
  echo "✅ Phase 1 complete detected (Pending Merge) - allowing exit for worktree switch" >&2
  [[ -f "$STATE_FILE" ]] && rm "$STATE_FILE"
  allow_exit
fi

# Fallback: Check for review mode configuration completion
if echo "$LAST_OUTPUT" | grep -qi "review mode.*configured\|configured.*review mode" && \
   echo "$LAST_OUTPUT" | grep -qi "new session\|start.*session\|exit.*session"; then
  echo "✅ Review mode configured - allowing exit for new session" >&2
  [[ -f "$STATE_FILE" ]] && rm "$STATE_FILE"
  allow_exit
fi

# Not complete - increment iteration and block exit
NEXT_ITERATION=$((ITERATION + 1))

# Update state file if exists
if [[ -f "$STATE_FILE" ]]; then
  TEMP_FILE="${STATE_FILE}.tmp.$$"
  sed "s/^iteration: .*/iteration: $NEXT_ITERATION/" "$STATE_FILE" > "$TEMP_FILE"
  mv "$TEMP_FILE" "$STATE_FILE"
fi

# Determine promise type based on mode
if [[ "$MODE" = "review" ]]; then
  PROMISE="REVIEW_COMPLETE"
else
  PROMISE="TASK_COMPLETE"
fi

# Build iteration info for system message
if [[ $MAX_ITERATIONS -gt 0 ]]; then
  ITER_INFO="Iteration $NEXT_ITERATION of $MAX_ITERATIONS"
else
  ITER_INFO="Iteration $NEXT_ITERATION (no limit)"
fi

# Output JSON to block the stop and provide continuation prompt
jq -n \
  --arg mode "$MODE" \
  --arg promise "$PROMISE" \
  --arg iter "$ITER_INFO" \
  '{
    "decision": "block",
    "reason": "Read PROMPT.md and continue from where you left off. Check PROGRESS.md for your prior work.",
    "systemMessage": ("🔄 " + $iter + " | " + $mode + " incomplete. If context is large, run /compact first. Then re-read PROMPT.md. Complete with <promise>" + $promise + "</promise>")
  }'

exit 0
