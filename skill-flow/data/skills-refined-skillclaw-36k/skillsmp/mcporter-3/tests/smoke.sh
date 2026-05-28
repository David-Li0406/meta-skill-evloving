#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== MCPorter Skill Smoke Tests ==="
echo ""

# Test 1: Help command
echo "Test 1: Help command"
if "$SKILL_DIR/scripts/mcporter.sh" help > /dev/null 2>&1; then
    echo "  PASS: Help command works"
else
    echo "  FAIL: Help command failed"
    exit 1
fi

# Test 2: Discover command (may fail if no MCPs configured, but should not error)
echo "Test 2: Discover command"
if "$SKILL_DIR/scripts/mcporter.sh" discover 2>&1 | head -5; then
    echo "  PASS: Discover command executed"
else
    echo "  WARN: Discover returned non-zero (may be expected if no MCPs configured)"
fi

# Test 3: List with missing argument should error gracefully
echo "Test 3: List with missing argument"
if ! "$SKILL_DIR/scripts/mcporter.sh" list 2>&1 | grep -q "Server name required"; then
    echo "  WARN: Expected error message not found"
else
    echo "  PASS: Missing argument handled correctly"
fi

# Test 4: Call with invalid format should error gracefully
echo "Test 4: Call with invalid format"
if ! "$SKILL_DIR/scripts/mcporter.sh" call "invalid" 2>&1 | grep -q "Invalid format"; then
    echo "  WARN: Expected error message not found"
else
    echo "  PASS: Invalid format handled correctly"
fi

echo ""
echo "=== Smoke tests completed ==="
