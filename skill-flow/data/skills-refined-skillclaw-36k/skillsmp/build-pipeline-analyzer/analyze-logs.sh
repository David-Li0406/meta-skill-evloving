#!/bin/bash
# Build failure log analyzer for FanHub project
# Usage: ./analyze-logs.sh <log-file>

set -e

LOG_FILE="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PATTERNS_DIR="$SCRIPT_DIR/log-patterns"

if [ -z "$LOG_FILE" ]; then
  echo "Usage: $0 <log-file>"
  exit 1
fi

if [ ! -f "$LOG_FILE" ]; then
  echo "Error: Log file '$LOG_FILE' not found"
  exit 1
fi

echo "Analyzing build failure: $LOG_FILE"
echo "=========================================="

# Check for missing dependency errors
if grep -qf "$PATTERNS_DIR/missing-dependency.txt" "$LOG_FILE"; then
  echo "✗ MISSING DEPENDENCY DETECTED"
  echo "  Issue: Required npm package not installed"
  grep -f "$PATTERNS_DIR/missing-dependency.txt" "$LOG_FILE" | head -5
  echo ""
  echo "  Fix: Run 'npm install' or check package.json"
  echo ""
fi

# Check for TypeScript errors
if grep -qf "$PATTERNS_DIR/typescript-error.txt" "$LOG_FILE"; then
  echo "✗ TYPESCRIPT ERROR DETECTED"
  echo "  Issue: Type checking failure"
  grep -f "$PATTERNS_DIR/typescript-error.txt" "$LOG_FILE" | head -5
  echo ""
  echo "  Fix: Check type definitions or add @ts-ignore"
  echo ""
fi

# Check for memory exhaustion
if grep -qf "$PATTERNS_DIR/memory-exhaustion.txt" "$LOG_FILE"; then
  echo "✗ MEMORY EXHAUSTION DETECTED"
  echo "  Issue: Node process ran out of memory"
  grep -f "$PATTERNS_DIR/memory-exhaustion.txt" "$LOG_FILE" | head -3
  echo ""
  echo "  Fix: Increase Node memory with NODE_OPTIONS=--max_old_space_size=4096"
  echo ""
fi

echo "=========================================="
echo "Analysis complete"
