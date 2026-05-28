#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Context7 Docs Skill Smoke Tests ==="
echo ""

# Test 1: Help command
echo "Test 1: Help command"
if "$SKILL_DIR/scripts/docs.sh" help > /dev/null 2>&1; then
    echo "  PASS: Help command works"
else
    echo "  FAIL: Help command failed"
    exit 1
fi

# Test 2: Search with missing argument should error gracefully
echo "Test 2: Search with missing argument"
if "$SKILL_DIR/scripts/docs.sh" search 2>&1 | grep -q "Library name required"; then
    echo "  PASS: Missing argument handled correctly"
else
    echo "  WARN: Expected error message not found"
fi

# Test 3: Docs with missing argument should error gracefully
echo "Test 3: Docs with missing argument"
if "$SKILL_DIR/scripts/docs.sh" docs 2>&1 | grep -q "Library name required"; then
    echo "  PASS: Missing argument handled correctly"
else
    echo "  WARN: Expected error message not found"
fi

# Test 4: Search for a library (may fail if Context7 not configured)
echo "Test 4: Search for library (requires Context7 MCP)"
if "$SKILL_DIR/scripts/docs.sh" search react 2>&1 | head -3; then
    echo "  PASS: Search command executed"
else
    echo "  WARN: Search returned non-zero (may be expected if Context7 not configured)"
fi

echo ""
echo "=== Smoke tests completed ==="
