#!/bin/bash

# Ralph Loop Stop Hook
# Prevents session exit when a ralph-loop is active
# Supports multiple concurrent loops via session binding

set -euo pipefail

# Skip hook entirely for fresh context loops
# Fresh loops spawn new Claude instances and need clean exits
if [[ "${RALPH_FRESH_MODE:-}" == "1" ]]; then
  exit 0
fi

# Read hook input from stdin (advanced stop hook API)
HOOK_INPUT=$(cat)

# Get transcript path from hook input - this is our session identifier
TRANSCRIPT_PATH=$(echo "$HOOK_INPUT" | jq -r '.transcript_path' 2>/dev/null) || {
  echo "⚠️  Ralph stop hook: Failed to parse hook input" >&2
  exit 0
}

if [[ -z "$TRANSCRIPT_PATH" ]] || [[ "$TRANSCRIPT_PATH" == "null" ]]; then
  # No transcript - can't identify session, allow exit
  exit 0
fi

# Find all ralph loop state files
RALPH_STATE_FILES=$(ls .claude/ralph-loop*.local.md 2>/dev/null || true)

if [[ -z "$RALPH_STATE_FILES" ]]; then
  # No active loops - allow exit
  exit 0
fi

# Find the loop that belongs to this session (or claim an unclaimed one)
MY_LOOP=""
UNCLAIMED_LOOPS=()

for STATE_FILE in $RALPH_STATE_FILES; do
  if [[ ! -f "$STATE_FILE" ]]; then
    continue
  fi

  # Parse frontmatter (file may disappear due to concurrent hooks, so handle gracefully)
  FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$STATE_FILE" 2>/dev/null) || continue
  SESSION=$(echo "$FRONTMATTER" | grep '^session_transcript:' | sed 's/session_transcript: *//' | sed 's/^"\(.*\)"$/\1/')

  if [[ "$SESSION" == "$TRANSCRIPT_PATH" ]]; then
    # This loop belongs to current session
    MY_LOOP="$STATE_FILE"
    break
  elif [[ "$SESSION" == "null" ]] || [[ -z "$SESSION" ]]; then
    # Unclaimed loop - remember ALL unclaimed loops
    UNCLAIMED_LOOPS+=("$STATE_FILE")
  fi
done

# If no claimed loop, delete any unclaimed ones - they're stale from dead sessions
if [[ -z "$MY_LOOP" ]]; then
  if [[ ${#UNCLAIMED_LOOPS[@]} -gt 0 ]]; then
    echo "⚠️  Found ${#UNCLAIMED_LOOPS[@]} stale Ralph loop(s) - cleaning up:" >&2
    for loop in "${UNCLAIMED_LOOPS[@]}"; do
      task_id=$(grep '^task_id:' "$loop" 2>/dev/null | sed 's/task_id: *//' | sed 's/^"\(.*\)"$/\1/' || echo "unknown")
      echo "   Removing stale loop: $task_id ($loop)" >&2
      rm -f "$loop"
    done
  fi
  # No active loop for this session - allow exit
  exit 0
fi

if [[ -z "$MY_LOOP" ]]; then
  # No loop for this session - allow exit
  exit 0
fi

RALPH_STATE_FILE="$MY_LOOP"

# Parse markdown frontmatter (YAML between ---) and extract values
# Add error suppression in case file was deleted by concurrent hook
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$RALPH_STATE_FILE" 2>/dev/null) || {
  # File disappeared - allow exit
  exit 0
}
ITERATION=$(echo "$FRONTMATTER" | grep '^iteration:' | sed 's/iteration: *//')
MAX_ITERATIONS=$(echo "$FRONTMATTER" | grep '^max_iterations:' | sed 's/max_iterations: *//')
TASK_ID=$(echo "$FRONTMATTER" | grep '^task_id:' | sed 's/task_id: *//' | sed 's/^"\(.*\)"$/\1/')
# Extract completion_promise and strip surrounding quotes if present
COMPLETION_PROMISE=$(echo "$FRONTMATTER" | grep '^completion_promise:' | sed 's/completion_promise: *//' | sed 's/^"\(.*\)"$/\1/')
# Extract mode (yolo or review)
MODE=$(echo "$FRONTMATTER" | grep '^mode:' | sed 's/mode: *//' | sed 's/^"\(.*\)"$/\1/')

# Default task_id for backwards compatibility
if [[ -z "$TASK_ID" ]]; then
  TASK_ID="default"
fi

# Default mode for backwards compatibility
if [[ -z "$MODE" ]]; then
  MODE="yolo"
fi

# Validate numeric fields before arithmetic operations
if [[ ! "$ITERATION" =~ ^[0-9]+$ ]]; then
  echo "⚠️  Ralph loop [$TASK_ID]: State file corrupted" >&2
  echo "   File: $RALPH_STATE_FILE" >&2
  echo "   Problem: 'iteration' field is not a valid number (got: '$ITERATION')" >&2
  echo "" >&2
  echo "   This usually means the state file was manually edited or corrupted." >&2
  echo "   Ralph loop is stopping. Run /ralph-loop again to start fresh." >&2
  rm "$RALPH_STATE_FILE"
  exit 0
fi

if [[ ! "$MAX_ITERATIONS" =~ ^[0-9]+$ ]]; then
  echo "⚠️  Ralph loop [$TASK_ID]: State file corrupted" >&2
  echo "   File: $RALPH_STATE_FILE" >&2
  echo "   Problem: 'max_iterations' field is not a valid number (got: '$MAX_ITERATIONS')" >&2
  echo "" >&2
  echo "   This usually means the state file was manually edited or corrupted." >&2
  echo "   Ralph loop is stopping. Run /ralph-loop again to start fresh." >&2
  rm "$RALPH_STATE_FILE"
  exit 0
fi

# Check if max iterations reached
if [[ $MAX_ITERATIONS -gt 0 ]] && [[ $ITERATION -ge $MAX_ITERATIONS ]]; then
  echo "🛑 Ralph loop [$TASK_ID]: Max iterations ($MAX_ITERATIONS) reached."
  rm "$RALPH_STATE_FILE"
  exit 0
fi

if [[ ! -f "$TRANSCRIPT_PATH" ]]; then
  echo "⚠️  Ralph loop [$TASK_ID]: Transcript file not found" >&2
  echo "   Expected: $TRANSCRIPT_PATH" >&2
  echo "   This is unusual and may indicate a Claude Code internal issue." >&2
  echo "   Ralph loop is stopping." >&2
  rm "$RALPH_STATE_FILE"
  exit 0
fi

# Read last assistant message from transcript (JSONL format - one JSON per line)
# First check if there are any assistant messages
if ! grep -q '"role":"assistant"' "$TRANSCRIPT_PATH"; then
  echo "⚠️  Ralph loop [$TASK_ID]: No assistant messages found in transcript" >&2
  echo "   Transcript: $TRANSCRIPT_PATH" >&2
  echo "   This is unusual and may indicate a transcript format issue" >&2
  echo "   Ralph loop is stopping." >&2
  rm "$RALPH_STATE_FILE"
  exit 0
fi

# Extract last assistant message with explicit error handling
LAST_LINE=$(grep '"role":"assistant"' "$TRANSCRIPT_PATH" | tail -1)
if [[ -z "$LAST_LINE" ]]; then
  echo "⚠️  Ralph loop [$TASK_ID]: Failed to extract last assistant message" >&2
  echo "   Ralph loop is stopping." >&2
  rm "$RALPH_STATE_FILE"
  exit 0
fi

# Parse JSON with error handling
LAST_OUTPUT=$(echo "$LAST_LINE" | jq -r '
  .message.content |
  map(select(.type == "text")) |
  map(.text) |
  join("\n")
' 2>&1)

# Check if jq succeeded
if [[ $? -ne 0 ]]; then
  echo "⚠️  Ralph loop [$TASK_ID]: Failed to parse assistant message JSON" >&2
  echo "   Error: $LAST_OUTPUT" >&2
  echo "   This may indicate a transcript format issue" >&2
  echo "   Ralph loop is stopping." >&2
  rm "$RALPH_STATE_FILE"
  exit 0
fi

if [[ -z "$LAST_OUTPUT" ]]; then
  echo "⚠️  Ralph loop [$TASK_ID]: Assistant message contained no text content" >&2
  echo "   Ralph loop is stopping." >&2
  rm "$RALPH_STATE_FILE"
  exit 0
fi

# Check for completion promise (only if set)
if [[ "$COMPLETION_PROMISE" != "null" ]] && [[ -n "$COMPLETION_PROMISE" ]]; then
  # Extract text from <promise> tags using Perl for multiline support
  # -0777 slurps entire input, s flag makes . match newlines
  # .*? is non-greedy (takes FIRST tag), whitespace normalized
  PROMISE_TEXT=$(echo "$LAST_OUTPUT" | perl -0777 -pe 's/.*?<promise>(.*?)<\/promise>.*/$1/s; s/^\s+|\s+$//g; s/\s+/ /g' 2>/dev/null || echo "")

  # Use = for literal string comparison (not pattern matching)
  # == in [[ ]] does glob pattern matching which breaks with *, ?, [ characters
  if [[ -n "$PROMISE_TEXT" ]] && [[ "$PROMISE_TEXT" = "$COMPLETION_PROMISE" ]]; then
    echo "✅ Ralph loop [$TASK_ID]: Detected <promise>$COMPLETION_PROMISE</promise>"
    rm "$RALPH_STATE_FILE"
    exit 0
  fi
fi

# Not complete - continue loop with SAME PROMPT
NEXT_ITERATION=$((ITERATION + 1))

# Extract prompt (everything after the closing ---)
# Skip first --- line, skip until second --- line, then print everything after
# Use i>=2 instead of i==2 to handle --- in prompt content
PROMPT_TEXT=$(awk '/^---$/{i++; next} i>=2' "$RALPH_STATE_FILE" 2>/dev/null) || {
  # File disappeared - allow exit
  exit 0
}

if [[ -z "$PROMPT_TEXT" ]]; then
  echo "⚠️  Ralph loop [$TASK_ID]: State file corrupted or incomplete" >&2
  echo "   File: $RALPH_STATE_FILE" >&2
  echo "   Problem: No prompt text found" >&2
  echo "" >&2
  echo "   This usually means:" >&2
  echo "     • State file was manually edited" >&2
  echo "     • File was corrupted during writing" >&2
  echo "" >&2
  echo "   Ralph loop is stopping. Run /ralph-loop again to start fresh." >&2
  rm "$RALPH_STATE_FILE"
  exit 0
fi

# Update iteration in frontmatter (portable across macOS and Linux)
# Create temp file, then atomically replace
TEMP_FILE="${RALPH_STATE_FILE}.tmp.$$"
if ! sed "s/^iteration: .*/iteration: $NEXT_ITERATION/" "$RALPH_STATE_FILE" > "$TEMP_FILE" 2>/dev/null; then
  # File disappeared - allow exit
  rm -f "$TEMP_FILE"
  exit 0
fi
mv "$TEMP_FILE" "$RALPH_STATE_FILE"

# Check for pending steering questions (only in review mode)
STEERING_FILE=".claude/ralph-steering-${TASK_ID}.md"
STEERING_QUESTION=""
if [[ "$MODE" == "review" ]] && [[ -f "$STEERING_FILE" ]]; then
  STEERING_STATUS=$(grep '^status:' "$STEERING_FILE" | sed 's/status: *//')
  if [[ "$STEERING_STATUS" == "pending" ]]; then
    # Extract the question and options
    STEERING_QUESTION=$(sed -n '/^## Question/,/^## Response/p' "$STEERING_FILE" | head -n -1)
  fi
fi

# Build system message with iteration count and completion promise info
if [[ "$COMPLETION_PROMISE" != "null" ]] && [[ -n "$COMPLETION_PROMISE" ]]; then
  SYSTEM_MSG="🔄 Ralph [$TASK_ID] iteration $NEXT_ITERATION | To stop: output <promise>$COMPLETION_PROMISE</promise> (ONLY when statement is TRUE - do not lie to exit!)

AT THE END of this iteration, update .claude/ralph-progress-${TASK_ID}.md with:
- What you completed this iteration
- Files changed
- Next steps
- Any blockers"
else
  SYSTEM_MSG="🔄 Ralph [$TASK_ID] iteration $NEXT_ITERATION | No completion promise set - loop runs infinitely

AT THE END of this iteration, update .claude/ralph-progress-${TASK_ID}.md with:
- What you completed this iteration
- Files changed
- Next steps
- Any blockers"
fi

# Append steering question to system message if pending
if [[ -n "$STEERING_QUESTION" ]]; then
  SYSTEM_MSG="$SYSTEM_MSG

⚠️ PENDING QUESTION FOR USER - ACTION REQUIRED:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$STEERING_QUESTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CRITICAL: You MUST use the AskUserQuestion tool to get the user's response.
Do NOT just output text - the loop will continue without waiting!

After getting the answer via AskUserQuestion:
1. Update $STEERING_FILE with status: answered
2. Add their response under ## Response
3. Continue with the task using their decision"
fi

# Output JSON to block the stop and feed prompt back
# The "reason" field contains the prompt that will be sent back to Claude
jq -n \
  --arg prompt "$PROMPT_TEXT" \
  --arg msg "$SYSTEM_MSG" \
  '{
    "decision": "block",
    "reason": $prompt,
    "systemMessage": $msg
  }'

# Exit 0 for successful hook execution
exit 0
