#!/usr/bin/env bash
set -euo pipefail

# Test is-empty-string transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing is-empty-string transformation..."

# Test 1: Empty string returns true
echo -n "Test 1: Empty string returns true... "
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

# Test 2: Whitespace string returns false
echo -n "Test 2: Whitespace string returns false... "
result=$(jq -f "$TRANSFORM" --arg path "text" "$SCRIPT_DIR/test-input-2.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Non-empty string returns false
echo -n "Test 3: Non-empty string returns false... "
result=$(jq -f "$TRANSFORM" --arg path "user.name" "$SCRIPT_DIR/test-input-3.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Null value returns false
echo -n "Test 4: Null value returns false... "
result=$(jq -f "$TRANSFORM" --arg path "value" "$SCRIPT_DIR/test-input-4.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Boolean false returns false
echo -n "Test 5: Boolean false returns false... "
result=$(jq -f "$TRANSFORM" --arg path "flag" "$SCRIPT_DIR/test-input-5.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Number 0 returns false
echo -n "Test 6: Number 0 returns false... "
result=$(jq -f "$TRANSFORM" --arg path "count" "$SCRIPT_DIR/test-input-6.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Empty array returns false
echo -n "Test 7: Empty array returns false... "
result=$(jq -f "$TRANSFORM" --arg path "items" "$SCRIPT_DIR/test-input-7.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Empty object returns false
echo -n "Test 8: Empty object returns false... "
result=$(jq -f "$TRANSFORM" --arg path "data" "$SCRIPT_DIR/test-input-8.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Non-existent field returns false
echo -n "Test 9: Non-existent field returns false... "
result=$(jq -f "$TRANSFORM" --arg path "missing" "$SCRIPT_DIR/test-input-9.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Nested empty string returns true
echo -n "Test 10: Nested empty string returns true... "
result=$(jq -f "$TRANSFORM" --arg path "user.profile.bio" "$SCRIPT_DIR/test-input-10.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Newline character is not empty string
echo -n "Test 11: Newline character is not empty string... "
result=$(jq -f "$TRANSFORM" --arg path "text" "$SCRIPT_DIR/test-input-11.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All is-empty-string tests passed!"
