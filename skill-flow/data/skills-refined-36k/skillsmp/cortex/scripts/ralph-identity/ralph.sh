#!/bin/bash
# Ralph Identity Resolution Runner
# Run after Eve→Comms migration is complete

set -e

MAX_ITERATIONS=${1:-10}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "🔍 Starting Ralph - Identity Resolution"
echo "   Project: $PROJECT_ROOT"
echo "   Max iterations: $MAX_ITERATIONS"
echo ""

# Check prerequisites (use pattern that matches "CREATE TABLE IF NOT EXISTS")
if ! grep -q "CREATE TABLE.*conversations" "$PROJECT_ROOT/internal/db/schema.sql" 2>/dev/null; then
    echo "❌ Prerequisites not met: conversations table not found"
    echo "   Run Eve→Comms migration first (scripts/ralph/)"
    exit 1
fi

if ! grep -q "CREATE TABLE.*analysis_types" "$PROJECT_ROOT/internal/db/schema.sql" 2>/dev/null; then
    echo "❌ Prerequisites not met: analysis_types table not found"
    echo "   Run Eve→Comms migration first (scripts/ralph/)"
    exit 1
fi

echo "✅ Prerequisites met - migration tables found"
echo ""

cd "$PROJECT_ROOT"

for i in $(seq 1 $MAX_ITERATIONS); do
    echo "═══════════════════════════════════════════════════════════════"
    echo "  Iteration $i of $MAX_ITERATIONS"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    
    # Run the agent with the prompt using Claude Code CLI
    OUTPUT=$(cat "$SCRIPT_DIR/prompt.md" \
        | claude --dangerously-skip-permissions 2>&1 \
        | tee /dev/stderr) || true
    
    # Check for completion signal
    if echo "$OUTPUT" | grep -q "<promise>COMPLETE</promise>"; then
        echo ""
        echo "✅ All stories complete!"
        echo ""
        
        # Show final stats
        echo "📊 Final Statistics:"
        go run ./cmd/cortex identify status --json 2>/dev/null || echo "   (status command not yet implemented)"
        
        exit 0
    fi
    
    # Brief pause between iterations
    sleep 2
done

echo ""
echo "⚠️  Max iterations ($MAX_ITERATIONS) reached"
echo "    Check progress.txt for current state"
echo ""

exit 1
