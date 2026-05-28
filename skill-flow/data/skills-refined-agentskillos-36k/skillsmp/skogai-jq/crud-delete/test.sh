#!/usr/bin/env bash
set -euo pipefail

# Test crud-delete transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing crud-delete transformation..."

# Test 1: Delete existing field
echo -n "Test 1: Delete existing field... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.email" "$SCRIPT_DIR/test-input-1.json")
expected='{"user":{"name":"skogix","phone":"123-456-7890"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Delete deeply nested field
echo -n "Test 2: Delete deeply nested field... "
result=$(jq -c -f "$TRANSFORM" --arg path "data.user.profile.age" "$SCRIPT_DIR/test-input-2.json")
expected='{"data":{"user":{"profile":{"location":"sweden"}}}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Delete non-existent path (no change)
echo -n "Test 3: Delete non-existent path... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.phone" "$SCRIPT_DIR/test-input-3.json")
expected='{"user":{"name":"skogix"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Delete top-level field
echo -n "Test 4: Delete top-level field... "
result=$(jq -c -f "$TRANSFORM" --arg path "user" "$SCRIPT_DIR/test-input-3.json")
expected='{}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Delete one of multiple fields
echo -n "Test 5: Delete one of multiple fields... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.phone" "$SCRIPT_DIR/test-input-1.json")
expected='{"user":{"name":"skogix","email":"test@example.com"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All crud-delete tests passed!"
