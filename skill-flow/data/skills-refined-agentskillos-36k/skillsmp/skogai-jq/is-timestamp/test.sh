#!/usr/bin/env bash
set -euo pipefail

# Test is-timestamp transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing is-timestamp transformation..."

# Test 1: Valid ISO 8601 timestamp with timezone (Z)
echo -n "Test 1: Valid ISO 8601 timestamp with timezone (Z)... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Valid ISO 8601 date only
echo -n "Test 2: Valid ISO 8601 date only... "
result=$(jq -c -f "$TRANSFORM" --arg path "date" "$SCRIPT_DIR/test-input-2.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Valid ISO 8601 with microseconds
echo -n "Test 3: Valid ISO 8601 with microseconds... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-3.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Valid ISO 8601 with timezone offset (+01:00)
echo -n "Test 4: Valid ISO 8601 with timezone offset (+01:00)... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-4.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Invalid format (slashes instead of dashes)
echo -n "Test 5: Invalid format (slashes instead of dashes)... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-5.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Empty string
echo -n "Test 6: Empty string... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-6.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Unix timestamp (number)
echo -n "Test 7: Unix timestamp (number)... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-7.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Null value
echo -n "Test 8: Null value... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-8.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Field doesn't exist
echo -n "Test 9: Field doesn't exist... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-9.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Nested path
echo -n "Test 10: Nested path... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.created_at" "$SCRIPT_DIR/test-input-10.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Boolean value
echo -n "Test 11: Boolean value... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-11.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Zero value
echo -n "Test 12: Zero value... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-12.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Empty array
echo -n "Test 13: Empty array... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-13.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Empty object
echo -n "Test 14: Empty object... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-14.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 15: Non-timestamp string
echo -n "Test 15: Non-timestamp string... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-15.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 16: Valid ISO 8601 without timezone
echo -n "Test 16: Valid ISO 8601 without timezone... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-16.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 17: Invalid date values (month 13, day 45)
echo -n "Test 17: Invalid date values (month 13, day 45)... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-17.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS (note: regex validates format, not semantic correctness)"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All is-timestamp tests passed!"
