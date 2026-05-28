#!/bin/bash
# Ralph loop for Cortex Memory System
# Usage: ./ralph.sh [iterations] [logfile]
# Example: nohup ./ralph.sh 100 &

set -e

MAX_ITERATIONS=${1:-30}
LOG_FILE="${2:-$HOME/ralph-memory-$(date +%Y%m%d-%H%M%S).log}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Claude CLI location (installed by Claude Code)
CLAUDE_CLI="/Users/tyler/Library/Application Support/Claude/claude-code/2.0.72/claude"

# Logging function
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🧠 Starting Ralph for Cortex Memory System"
log "   Project: $PROJECT_DIR"
log "   Model: opus (claude-opus-4)"
log "   Max iterations: $MAX_ITERATIONS"
log "   Log file: $LOG_FILE"
log ""

cd "$PROJECT_DIR"

for i in $(seq 1 $MAX_ITERATIONS); do
  log "═══════════════════════════════════════════════════════════"
  log "  Iteration $i of $MAX_ITERATIONS"
  log "═══════════════════════════════════════════════════════════"
  
  START_TIME=$(date +%s)
  
  # Run Claude and capture output
  OUTPUT=$(cat "$SCRIPT_DIR/prompt.md" \
    | "$CLAUDE_CLI" --model opus --print --dangerously-skip-permissions 2>&1) || true
  
  END_TIME=$(date +%s)
  DURATION=$((END_TIME - START_TIME))
  
  # Log output to file
  echo "$OUTPUT" >> "$LOG_FILE"
  
  # Check for completion signal
  if echo "$OUTPUT" | grep -q "<promise>COMPLETE</promise>"; then
    log ""
    log "✅ All stories complete! Duration: ${DURATION}s"
    exit 0
  fi
  
  # Log iteration summary
  log ""
  log "Iteration $i complete. Duration: ${DURATION}s. Sleeping 5s..."
  sleep 5
done

log ""
log "⚠️  Max iterations ($MAX_ITERATIONS) reached"
exit 1
