#!/bin/bash
# Ralph BD - Multi-repo autonomous coding loop
# Contract: skills-lib-lkv (Ralph Contract v1)
#
# Key principle: Bash manages iteration loop, each iteration gets fresh Claude context

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Auto-detect RALPH_ID from git repo, allow override
detect_ralph_id() {
  if [ -n "$RALPH_ID" ]; then
    echo "$RALPH_ID"
  elif git rev-parse --show-toplevel &>/dev/null; then
    echo "ralph-$(basename "$(git rev-parse --show-toplevel)")"
  else
    echo "ralph-$(basename "$PWD")"
  fi
}

# Status command - list all running ralph sessions
show_status() {
  echo "=== Ralph Sessions ==="
  echo ""

  SESSIONS=$(tmux list-sessions -F '#{session_name}' 2>/dev/null | grep -E '^ralph-|plan$' || true)

  if [ -z "$SESSIONS" ]; then
    echo "No ralph sessions running."
    echo ""
    echo "Start one with: ./ralph.sh [max_iterations]"
    return 0
  fi

  for SESSION in $SESSIONS; do
    WINDOWS=$(tmux list-windows -t "$SESSION" 2>/dev/null | wc -l)
    WINDOW_NAMES=$(tmux list-windows -t "$SESSION" -F '#{window_name}' 2>/dev/null | tr '\n' ' ')
    printf "%-35s %d windows: %s\n" "$SESSION" "$WINDOWS" "$WINDOW_NAMES"
  done

  echo ""
  echo "Commands:"
  echo "  tmux attach -t <session>        # Watch a session"
  echo "  tmux kill-session -t <session>  # Kill a session"
}

# Parse arguments
case "${1:-}" in
  status|--status|-s)
    show_status
    exit 0
    ;;
  help|--help|-h)
    echo "Usage: ralph.sh [command|max_iterations]"
    echo ""
    echo "Commands:"
    echo "  status    List all running ralph sessions"
    echo "  help      Show this help"
    echo ""
    echo "Options:"
    echo "  [max_iterations]  Max iterations before stopping (default: 10)"
    echo ""
    echo "Environment variables:"
    echo "  RALPH_ID  Override auto-detected session name"
    echo ""
    echo "Contract: skills-lib-lkv (Ralph Contract v1)"
    exit 0
    ;;
esac

MAX_ITERATIONS=${1:-10}
SESSION=$(detect_ralph_id)
PROJECT_DIR="$PWD"

# Check if session already exists
if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "⚠ Session '$SESSION' already running."
  echo ""
  echo "Options:"
  echo "  tmux attach -t $SESSION         # Attach to existing"
  echo "  tmux kill-session -t $SESSION   # Kill and restart"
  echo "  RALPH_ID=other ./ralph.sh       # Use different name"
  exit 1
fi

# Create session with parent window
tmux new-session -d -s "$SESSION" -n "parent" -c "$PROJECT_DIR"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Ralph Session: $SESSION"
echo "║  Max iterations: $MAX_ITERATIONS"
echo "║  Project: $PROJECT_DIR"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "  Attach: tmux attach -t $SESSION"
echo ""

# Launch watchdog in background
"$SCRIPT_DIR/watchdog.sh" "$SESSION" 60 &
WATCHDOG_PID=$!
echo "Watchdog launched (PID: $WATCHDOG_PID)"
echo ""

# Build the single-iteration parent prompt
build_parent_prompt() {
  local ITER=$1
  cat << 'PROMPT_EOF'
# Ralph Parent - Iteration ITER_NUM of MAX_ITER

You are the parent orchestrator for ONE iteration of Ralph. Spawn subagents, then EXIT.

## Environment
- RALPH_ID: SESSION_ID
- PROJECT_DIR: PROJECT_PATH
- Iteration: ITER_NUM of MAX_ITER

## Your Job (Single Iteration)

1. Run `bd prime` to understand the project
2. Run `bd ready --limit 10` to see available work
3. If no work ready → output "NO_WORK_REMAINING" and exit
4. Analyze which issues can run in parallel (different files = parallel)
5. Spawn 3-5 subagent windows
6. Output "SUBAGENTS_SPAWNED" and exit - bash will wait for them

## Spawning Subagents

For each issue to work on:

```bash
ISSUE_ID="<full-issue-id>"
SHORT_ID=$(echo "$ISSUE_ID" | grep -oE '[a-z0-9]+$' | head -c 8)

tmux new-window -t "SESSION_ID" -n "$SHORT_ID" "cat << 'SUBAGENT_EOF' | claude --dangerously-skip-permissions
# Subagent: $ISSUE_ID

## Your Task
$(bd show $ISSUE_ID)

## Instructions
1. Run bd prime first
2. Implement this ONE issue
3. Run tests if applicable
4. On SUCCESS:
   - git add -A && git commit -m \"feat: $SHORT_ID - brief description\"
   - bd close $ISSUE_ID
5. On FAILURE:
   - Do NOT close the issue
   - bd comments add $ISSUE_ID \"Blocked: <reason>\"
6. Type /exit when done

Stay focused on THIS issue only.
SUBAGENT_EOF
echo 'Subagent exiting...'; sleep 2"
```

## Important Rules

- Spawn subagents then EXIT immediately
- Do NOT wait for subagents - bash handles that
- Do NOT loop - this is ONE iteration
- Always use "SESSION_ID" for tmux commands
- Window names must be short issue IDs

## After Spawning

Once you've spawned all subagent windows:
```
echo "SUBAGENTS_SPAWNED"
```
Then type /exit

Begin now. Run bd prime, check bd ready, spawn subagents, exit.
PROMPT_EOF
}

# Count non-system windows (exclude parent and watchdog)
count_subagent_windows() {
  tmux list-windows -t "$SESSION" -F '#{window_name}' 2>/dev/null | grep -vE '^(parent|watchdog)$' | wc -l
}

# Main iteration loop (bash manages this, not Claude)
echo "Starting iteration loop..."
echo ""

for ITER in $(seq 1 $MAX_ITERATIONS); do
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  ITERATION $ITER of $MAX_ITERATIONS"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  # Check if work remains
  READY_COUNT=$(cd "$PROJECT_DIR" && bd ready 2>/dev/null | grep -cE '^\[|^[0-9]+\.' || echo "0")

  if [ "$READY_COUNT" -eq 0 ]; then
    echo "✓ No work remaining. All done!"
    break
  fi

  echo "  Ready issues: $READY_COUNT"
  echo "  Spawning fresh parent Claude..."
  echo ""

  # Build prompt with substitutions
  PARENT_PROMPT=$(build_parent_prompt $ITER | sed "s/ITER_NUM/$ITER/g; s/MAX_ITER/$MAX_ITERATIONS/g; s/SESSION_ID/$SESSION/g; s|PROJECT_PATH|$PROJECT_DIR|g")

  # Write prompt to temp file to avoid escaping issues
  PROMPT_FILE="/tmp/ralph-parent-prompt-$$"
  echo "$PARENT_PROMPT" > "$PROMPT_FILE"

  # Spawn fresh Claude parent for this iteration
  tmux send-keys -t "$SESSION:parent" "cd '$PROJECT_DIR' && claude --dangerously-skip-permissions < '$PROMPT_FILE'; rm -f '$PROMPT_FILE'" Enter

  # Wait for parent to spawn subagents (give it time to analyze and spawn)
  echo "  Waiting for parent to spawn subagents..."
  sleep 30

  # Wait for all subagent windows to close
  echo "  Waiting for subagents to complete..."
  WAIT_COUNT=0
  MAX_WAIT=3600  # 1 hour max per iteration

  while true; do
    SUBAGENT_COUNT=$(count_subagent_windows)

    if [ "$SUBAGENT_COUNT" -eq 0 ]; then
      echo ""
      echo "  ✓ All subagents finished"
      break
    fi

    sleep 15
    WAIT_COUNT=$((WAIT_COUNT + 15))

    if [ $((WAIT_COUNT % 60)) -eq 0 ]; then
      echo "  ... ${WAIT_COUNT}s ($SUBAGENT_COUNT subagents running)"
    fi

    if [ "$WAIT_COUNT" -ge "$MAX_WAIT" ]; then
      echo "  ⚠ Iteration timeout reached"
      # Kill remaining subagent windows
      for WIN in $(tmux list-windows -t "$SESSION" -F '#{window_name}' 2>/dev/null | grep -vE '^(parent|watchdog)$'); do
        tmux kill-window -t "$SESSION:$WIN" 2>/dev/null || true
      done
      break
    fi

    # Check session still exists
    if ! tmux has-session -t "$SESSION" 2>/dev/null; then
      echo "  ⚠ Session died unexpectedly"
      exit 1
    fi
  done

  # Sync bd after each iteration
  echo "  Syncing bd..."
  (cd "$PROJECT_DIR" && bd sync 2>/dev/null) || true

  # Small delay between iterations
  sleep 5
  echo ""
done

# Final sync and summary
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  RALPH COMPLETE"
echo "════════════════════════════════════════════════════════════════"

cd "$PROJECT_DIR"
bd sync 2>/dev/null || true
git push 2>/dev/null || echo "(git push skipped or failed)"

echo ""
echo "Final stats:"
bd stats 2>/dev/null || true

echo ""
echo "Session '$SESSION' still running for review."
echo "  Attach: tmux attach -t $SESSION"
echo "  Kill:   tmux kill-session -t $SESSION"
