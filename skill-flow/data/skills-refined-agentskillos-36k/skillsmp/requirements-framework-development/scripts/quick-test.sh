#!/bin/bash
# Quick Test Runner
#
# Runs the requirements framework test suite with summary output.
# Usage: ./quick-test.sh [test-pattern]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

TEST_FILE="$HOME/.claude/hooks/test_requirements.py"

if [ ! -f "$TEST_FILE" ]; then
    echo -e "${RED}❌ Test file not found: $TEST_FILE${NC}"
    echo "Run: ./sync.sh deploy"
    exit 1
fi

echo "🧪 Requirements Framework Test Suite"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Build command
CMD="python3 $TEST_FILE"

# Add pattern filter if provided
if [ -n "$1" ]; then
    CMD="$CMD -k $1"
    echo "Filter: $1"
    echo ""
fi

# Run tests and capture output
start_time=$(date +%s)

if $CMD; then
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${GREEN}✅ All tests passed${NC} (${duration}s)"
else
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${RED}❌ Some tests failed${NC} (${duration}s)"
    exit 1
fi
