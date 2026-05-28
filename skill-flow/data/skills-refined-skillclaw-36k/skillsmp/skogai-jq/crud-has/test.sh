#!/usr/bin/env bash
set -euo pipefail

# Test crud-has transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing crud-has transformation..."

# Test 1: Check for existing nested value
echo -n "Test 1: Check for existing nested value... "
result=$(jq -f "$TRANSFORM" --arg path "user.name" "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Check for deeply nested value that exists
echo -n "Test 2: Check for deeply nested value that exists... "
result=$(jq -f "$TRANSFORM" --arg path "user.profile.age" "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Check for non-existent path
echo -n "Test 3: Check for non-existent path... "
result=$(jq -f "$TRANSFORM" --arg path "user.phone" "$SCRIPT_DIR/test-input-2.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Check for any path in empty object
echo -n "Test 4: Check for any path in empty object... "
result=$(jq -f "$TRANSFORM" --arg path "anything" "$SCRIPT_DIR/test-input-4.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Check for array value
echo -n "Test 5: Check for array value... "
result=$(jq -f "$TRANSFORM" --arg path "data.items" "$SCRIPT_DIR/test-input-3.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Check for top-level key that exists
echo -n "Test 6: Check for top-level key that exists... "
result=$(jq -f "$TRANSFORM" --arg path "items" "$SCRIPT_DIR/test-input-5.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Path exists with null value (KEY exists, value is null)
echo -n "Test 7: Path exists with null value... "
result=$(jq -f "$TRANSFORM" --arg path "user.name" "$SCRIPT_DIR/test-input-6.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Boolean false value (should return true - key exists)
echo -n "Test 8: Boolean false value exists... "
result=$(jq -f "$TRANSFORM" --arg path "settings.enabled" "$SCRIPT_DIR/test-input-7.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Number zero value (should return true - key exists)
echo -n "Test 9: Number zero value exists... "
result=$(jq -f "$TRANSFORM" --arg path "settings.count" "$SCRIPT_DIR/test-input-7.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Empty string value (should return true - key exists)
echo -n "Test 10: Empty string value exists... "
result=$(jq -f "$TRANSFORM" --arg path "settings.name" "$SCRIPT_DIR/test-input-7.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Intermediate missing key (user.profile.name where profile doesn't exist)
echo -n "Test 11: Intermediate missing key... "
result=$(jq -f "$TRANSFORM" --arg path "user.profile.name" "$SCRIPT_DIR/test-input-8.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All crud-has tests passed!"
