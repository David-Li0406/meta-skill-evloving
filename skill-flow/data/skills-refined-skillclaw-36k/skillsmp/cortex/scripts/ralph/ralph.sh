#!/bin/bash
# Ralph loop for comms project
set -e

MAX_ITERATIONS=${1:-20}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "🚀 Starting Ralph for comms"
echo "   Project: $PROJECT_DIR"
echo "   Max iterations: $MAX_ITERATIONS"
echo ""

cd "$PROJECT_DIR"

for i in $(seq 1 $MAX_ITERATIONS); do
  echo "═══════════════════════════════════════════════════════════"
  echo "  Iteration $i of $MAX_ITERATIONS"
  echo "═══════════════════════════════════════════════════════════"
  
  OUTPUT=$(cat "$SCRIPT_DIR/prompt.md" \
    | claude --dangerously-skip-permissions 2>&1 \
    | tee /dev/stderr) || true
  
  if echo "$OUTPUT" | grep -q "<promise>COMPLETE</promise>"; then
    echo ""
    echo "✅ All stories complete!"
    exit 0
  fi
  
  echo ""
  echo "Iteration $i complete. Sleeping 2s..."
  sleep 2
done

echo ""
echo "⚠️  Max iterations ($MAX_ITERATIONS) reached"
exit 1
