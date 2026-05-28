#!/usr/bin/env bash
set -euo pipefail

# Test is-uuid transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing is-uuid transformation..."

# Test 1: Valid UUID v4
echo -n "Test 1: Valid UUID v4... "
result=$(jq -c -f "$TRANSFORM" --arg path "id" "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Valid UUID v1
echo -n "Test 2: Valid UUID v1... "
result=$(jq -c -f "$TRANSFORM" --arg path "id" "$SCRIPT_DIR/test-input-2.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Invalid UUID (wrong format)
echo -n "Test 3: Invalid UUID (wrong format)... "
result=$(jq -c -f "$TRANSFORM" --arg path "id" "$SCRIPT_DIR/test-input-3.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Empty string
echo -n "Test 4: Empty string... "
result=$(jq -c -f "$TRANSFORM" --arg path "id" "$SCRIPT_DIR/test-input-4.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Non-string value (number)
echo -n "Test 5: Non-string value (number)... "
result=$(jq -c -f "$TRANSFORM" --arg path "id" "$SCRIPT_DIR/test-input-5.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Null value
echo -n "Test 6: Null value... "
result=$(jq -c -f "$TRANSFORM" --arg path "id" "$SCRIPT_DIR/test-input-6.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: UUID with uppercase (should be valid)
echo -n "Test 7: UUID with uppercase (should be valid)... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.guid" "$SCRIPT_DIR/test-input-7.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: UUID with wrong length (too short)
echo -n "Test 8: UUID with wrong length (too short)... "
result=$(jq -c -f "$TRANSFORM" --arg path "id" "$SCRIPT_DIR/test-input-8.json")
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
result=$(jq -c -f "$TRANSFORM" --arg path "id" "$SCRIPT_DIR/test-input-9.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Nested path with valid UUID
echo -n "Test 10: Nested path with valid UUID... "
result=$(jq -c -f "$TRANSFORM" --arg path "data.nested.id" "$SCRIPT_DIR/test-input-10.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: UUID with extra characters (invalid)
echo -n "Test 11: UUID with extra characters (invalid)... "
result=$(jq -c -f "$TRANSFORM" --arg path "id" "$SCRIPT_DIR/test-input-11.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: UUID without dashes (invalid)
echo -n "Test 12: UUID without dashes (invalid)... "
result=$(jq -c -f "$TRANSFORM" --arg path "id" "$SCRIPT_DIR/test-input-12.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All is-uuid tests passed!"
