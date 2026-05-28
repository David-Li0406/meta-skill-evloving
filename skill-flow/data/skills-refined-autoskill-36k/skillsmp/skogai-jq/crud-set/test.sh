#!/usr/bin/env bash
set -euo pipefail

# Test crud-set transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing crud-set transformation..."

# Test 1: Set existing nested value
echo -n "Test 1: Set existing nested value... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.name" --arg value "new-name" "$SCRIPT_DIR/test-input-1.json")
expected='{"user":{"name":"new-name","email":"test@example.com"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Create nested path and set value
echo -n "Test 2: Create nested path and set value... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.profile.age" --arg value "30" "$SCRIPT_DIR/test-input-2.json")
expected='{"user":{"profile":{"age":"30"}}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Add new field to existing object
echo -n "Test 3: Add new field to existing object... "
result=$(jq -c -f "$TRANSFORM" --arg path "data.count" --arg value "3" "$SCRIPT_DIR/test-input-3.json")
expected='{"data":{"items":[1,2,3],"count":"3"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Set top-level field
echo -n "Test 4: Set top-level field... "
result=$(jq -c -f "$TRANSFORM" --arg path "newfield" --arg value "newvalue" "$SCRIPT_DIR/test-input-2.json")
expected='{"newfield":"newvalue"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Override existing value with different type
echo -n "Test 5: Override existing value... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.email" --arg value "newemail@example.com" "$SCRIPT_DIR/test-input-1.json")
expected='{"user":{"name":"old-name","email":"newemail@example.com"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All crud-set tests passed!"
