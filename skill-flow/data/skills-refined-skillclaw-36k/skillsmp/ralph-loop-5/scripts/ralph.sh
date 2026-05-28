#!/bin/bash
#
# Ralph Loop - External Bash Loop for Claude Code
#
# Key difference from ralph-wiggum: This is an EXTERNAL loop that spawns
# fresh Claude sessions. No stop hook, no context accumulation.
#
# Usage: ~/.claude/skills/ralph-loop/scripts/ralph.sh [options]
#

set -euo pipefail

# ============================================================================
# Configuration (can be overridden via environment)
# ============================================================================

MAX_ITERATIONS="${RALPH_MAX_ITERATIONS:-25}"
MAX_ATTEMPTS="${RALPH_MAX_ATTEMPTS:-5}"
TIMEOUT="${RALPH_TIMEOUT:-1800}"  # 30 minutes per iteration
COMPLETION_PROMISE="${RALPH_PROMISE:-DONE}"
CLAUDE_MODEL="${RALPH_MODEL:-}"  # Empty = use default
VERBOSE="${RALPH_VERBOSE:-0}"

# ============================================================================
# Colors and formatting
# ============================================================================

if [[ -t 1 ]] && [[ -z "${NO_COLOR:-}" ]]; then
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[0;33m'
  BLUE='\033[0;34m'
  CYAN='\033[0;36m'
  BOLD='\033[1m'
  NC='\033[0m'
else
  RED='' GREEN='' YELLOW='' BLUE='' CYAN='' BOLD='' NC=''
fi

log() { echo -e "${CYAN}[ralph]${NC} $*"; }
log_success() { echo -e "${GREEN}[ralph]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[ralph]${NC} $*"; }
log_error() { echo -e "${RED}[ralph]${NC} $*" >&2; }

# ============================================================================
# State management
# ============================================================================

RALPH_DIR=".ralph"
STATE_FILE="$RALPH_DIR/state.json"
SPEC_FILE="$RALPH_DIR/spec.md"
PROGRESS_LOG="$RALPH_DIR/progress.log"
EVIDENCE_DIR="$RALPH_DIR/evidence"
BLOCKED_FILE="$RALPH_DIR/blocked.md"

init_state() {
  if [[ ! -f "$STATE_FILE" ]]; then
    log_error "No ralph state found. Run /ralph-init first."
    exit 1
  fi
}

read_state() {
  local key="$1"
  jq -r ".$key // empty" "$STATE_FILE"
}

write_state() {
  local key="$1"
  local value="$2"
  local tmp_file
  tmp_file=$(mktemp)
  jq ".$key = $value" "$STATE_FILE" > "$tmp_file"
  mv "$tmp_file" "$STATE_FILE"
}

increment_state() {
  local key="$1"
  local current
  current=$(read_state "$key")
  write_state "$key" "$((current + 1))"
}

# ============================================================================
# Progress logging
# ============================================================================

log_progress() {
  local timestamp
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  echo "[$timestamp] $*" >> "$PROGRESS_LOG"
}

# ============================================================================
# Re-anchoring prompt generation
# ============================================================================

generate_prompt() {
  local iteration="$1"
  local prompt_file
  prompt_file=$(mktemp)

  # Build the re-anchoring prompt
  cat > "$prompt_file" << 'PROMPT_HEADER'
# Ralph Loop Iteration

You are in a Ralph loop - an autonomous development loop where each iteration
gets fresh context. Your state is in FILES, not in conversation history.

## CRITICAL: Re-Anchor Before Working

Before doing ANYTHING, you MUST read and understand:
1. The task specification below
2. Your previous work (in files and git)
3. Test results and evidence from previous iterations

Do NOT rely on memory - re-read the sources of truth.

## Completion

When the task is GENUINELY complete (all requirements met, tests passing):
Output exactly: <promise>DONE</promise>

ONLY output this when the statement is TRUE. Do not lie to exit the loop.

---

PROMPT_HEADER

  # Add iteration info
  echo "## Current State" >> "$prompt_file"
  echo "" >> "$prompt_file"
  echo "- **Iteration**: $iteration of $MAX_ITERATIONS" >> "$prompt_file"
  echo "- **Attempts on current task**: $(read_state 'attempts')" >> "$prompt_file"
  echo "- **Max attempts before block**: $MAX_ATTEMPTS" >> "$prompt_file"
  echo "" >> "$prompt_file"

  # Add spec
  echo "## Task Specification" >> "$prompt_file"
  echo "" >> "$prompt_file"
  cat "$SPEC_FILE" >> "$prompt_file"
  echo "" >> "$prompt_file"

  # Add git state for re-anchoring
  echo "## Current Git State (Re-Anchor Point)" >> "$prompt_file"
  echo "" >> "$prompt_file"
  echo '```' >> "$prompt_file"
  git status --short 2>/dev/null || echo "(not a git repo)"
  echo '```' >> "$prompt_file"
  echo "" >> "$prompt_file"

  # Add recent commits
  echo "## Recent Commits" >> "$prompt_file"
  echo "" >> "$prompt_file"
  echo '```' >> "$prompt_file"
  git log --oneline -5 2>/dev/null || echo "(no commits)"
  echo '```' >> "$prompt_file"
  echo "" >> "$prompt_file"

  # Add previous iteration summary if exists
  local prev_iter=$((iteration - 1))
  local prev_log="$EVIDENCE_DIR/iter-$(printf '%03d' $prev_iter).log"
  if [[ -f "$prev_log" ]]; then
    echo "## Previous Iteration Output (Last 50 Lines)" >> "$prompt_file"
    echo "" >> "$prompt_file"
    echo '```' >> "$prompt_file"
    tail -50 "$prev_log" >> "$prompt_file"
    echo '```' >> "$prompt_file"
    echo "" >> "$prompt_file"
  fi

  # Add instructions
  cat >> "$prompt_file" << 'PROMPT_FOOTER'

## Your Task

1. **Re-read** the specification above carefully
2. **Check** what work has already been done (files, git log)
3. **Identify** what remains to be done
4. **Execute** the next logical step
5. **Verify** your work (run tests, check output)
6. If complete, output: <promise>DONE</promise>

Remember: Each iteration is a fresh context. You cannot remember previous
conversations. All state is in FILES. Re-anchor from files before working.
PROMPT_FOOTER

  echo "$prompt_file"
}

# ============================================================================
# Claude invocation
# ============================================================================

run_claude() {
  local prompt_file="$1"
  local output_file="$2"
  local claude_args=()

  # Build claude command
  claude_args+=("-p" "$prompt_file")
  claude_args+=("--output-format" "text")

  if [[ -n "$CLAUDE_MODEL" ]]; then
    claude_args+=("--model" "$CLAUDE_MODEL")
  fi

  # Run with timeout
  if timeout "$TIMEOUT" claude "${claude_args[@]}" > "$output_file" 2>&1; then
    return 0
  else
    local exit_code=$?
    if [[ $exit_code -eq 124 ]]; then
      log_warn "Iteration timed out after ${TIMEOUT}s"
      echo "TIMEOUT: Iteration exceeded ${TIMEOUT} seconds" >> "$output_file"
    fi
    return $exit_code
  fi
}

# ============================================================================
# Verdict extraction
# ============================================================================

check_completion() {
  local output_file="$1"

  # Look for completion promise
  if grep -q "<promise>$COMPLETION_PROMISE</promise>" "$output_file"; then
    return 0
  fi
  return 1
}

# ============================================================================
# Main loop
# ============================================================================

main() {
  log "${BOLD}Ralph Loop Starting${NC}"
  log "Max iterations: $MAX_ITERATIONS"
  log "Completion promise: $COMPLETION_PROMISE"
  echo ""

  # Validate state exists
  init_state

  # Create evidence directory
  mkdir -p "$EVIDENCE_DIR"

  # Log start
  log_progress "=== Ralph loop started ==="
  log_progress "Max iterations: $MAX_ITERATIONS"
  log_progress "Completion promise: $COMPLETION_PROMISE"

  local iteration=1
  local attempts

  while [[ $iteration -le $MAX_ITERATIONS ]]; do
    attempts=$(read_state 'attempts')

    # Check if blocked
    if [[ -f "$BLOCKED_FILE" ]]; then
      log_error "Task is blocked. See $BLOCKED_FILE"
      log_progress "BLOCKED: Task exceeded max attempts"
      exit 1
    fi

    # Check max attempts
    if [[ $attempts -ge $MAX_ATTEMPTS ]]; then
      log_error "Max attempts ($MAX_ATTEMPTS) exceeded"
      cat > "$BLOCKED_FILE" << EOF
# Task Blocked

The task has been blocked after $MAX_ATTEMPTS failed attempts.

## What to do

1. Review the evidence logs in \`.ralph/evidence/\`
2. Identify what's causing repeated failures
3. Either:
   - Fix the underlying issue manually
   - Update the spec to be more achievable
   - Reset attempts: \`jq '.attempts = 0' .ralph/state.json | sponge .ralph/state.json\`
EOF
      log_progress "BLOCKED: Exceeded $MAX_ATTEMPTS attempts"
      exit 1
    fi

    log "${BOLD}--- Iteration $iteration/$MAX_ITERATIONS ---${NC}"
    log "Attempts: $attempts/$MAX_ATTEMPTS"
    log_progress "Iteration $iteration started (attempt $((attempts + 1)))"

    # Generate re-anchoring prompt
    local prompt_file
    prompt_file=$(generate_prompt "$iteration")

    # Output file for this iteration
    local output_file="$EVIDENCE_DIR/iter-$(printf '%03d' $iteration).log"

    # Run Claude with fresh context
    log "Spawning fresh Claude session..."
    local start_time
    start_time=$(date +%s)

    if run_claude "$prompt_file" "$output_file"; then
      local end_time
      end_time=$(date +%s)
      local duration=$((end_time - start_time))

      log "Iteration completed in ${duration}s"
      log_progress "Iteration $iteration completed (${duration}s)"

      # Check for completion
      if check_completion "$output_file"; then
        log_success "${BOLD}Task completed!${NC}"
        log_success "Completion promise detected: <promise>$COMPLETION_PROMISE</promise>"
        log_progress "SUCCESS: Completion promise detected"

        # Update state
        write_state 'status' '"completed"'
        write_state 'completed_at' "\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\""

        # Clean up
        rm -f "$prompt_file"

        echo ""
        log_success "Ralph loop finished successfully after $iteration iterations"
        exit 0
      fi

      # Not complete - continue
      log "No completion promise found, continuing..."
      log_progress "No completion promise, continuing to next iteration"

      # Reset attempts on progress (you could add smarter progress detection here)
      # For now, each iteration is considered an attempt
      increment_state 'attempts'

    else
      log_warn "Claude exited with error"
      log_progress "Iteration $iteration failed"
      increment_state 'attempts'
    fi

    # Update iteration counter
    write_state 'iteration' "$iteration"
    iteration=$((iteration + 1))

    # Clean up temp prompt file
    rm -f "$prompt_file"

    # Small delay between iterations
    sleep 2
  done

  # Max iterations reached
  log_warn "Max iterations ($MAX_ITERATIONS) reached without completion"
  log_progress "STOPPED: Max iterations reached"
  write_state 'status' '"max_iterations"'
  exit 1
}

# ============================================================================
# Entry point
# ============================================================================

# Handle Ctrl+C gracefully
trap 'log_warn "Interrupted by user"; log_progress "INTERRUPTED by user"; exit 130' INT

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      cat << 'EOF'
Ralph Loop - External Bash Loop for Claude Code

Usage: ralph.sh [options]

Options:
  -h, --help              Show this help
  -n, --max-iterations N  Maximum iterations (default: 25)
  -a, --max-attempts N    Max attempts before blocking (default: 5)
  -t, --timeout SECONDS   Timeout per iteration (default: 1800)
  -p, --promise TEXT      Completion promise (default: DONE)
  -m, --model MODEL       Claude model to use
  -v, --verbose           Verbose output

Environment variables:
  RALPH_MAX_ITERATIONS    Same as --max-iterations
  RALPH_MAX_ATTEMPTS      Same as --max-attempts
  RALPH_TIMEOUT           Same as --timeout
  RALPH_PROMISE           Same as --promise
  RALPH_MODEL             Same as --model
  RALPH_VERBOSE           Same as --verbose

Example:
  ralph.sh --max-iterations 10 --promise "ALL_TESTS_PASS"
EOF
      exit 0
      ;;
    -n|--max-iterations)
      MAX_ITERATIONS="$2"
      shift 2
      ;;
    -a|--max-attempts)
      MAX_ATTEMPTS="$2"
      shift 2
      ;;
    -t|--timeout)
      TIMEOUT="$2"
      shift 2
      ;;
    -p|--promise)
      COMPLETION_PROMISE="$2"
      shift 2
      ;;
    -m|--model)
      CLAUDE_MODEL="$2"
      shift 2
      ;;
    -v|--verbose)
      VERBOSE=1
      shift
      ;;
    *)
      log_error "Unknown option: $1"
      exit 1
      ;;
  esac
done

main
