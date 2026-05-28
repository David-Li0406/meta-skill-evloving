#!/usr/bin/env bash
set -euo pipefail

# Test validate-required transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing validate-required transformation..."

# Test 1: All required fields exist
echo -n "Test 1: All required fields exist... "
result=$(jq -f "$TRANSFORM" --arg required_fields '["name","email"]' "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Missing one required field
echo -n "Test 2: Missing one required field... "
result=$(jq -f "$TRANSFORM" --arg required_fields '["name","email"]' "$SCRIPT_DIR/test-input-2.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Missing multiple required fields
echo -n "Test 3: Missing multiple required fields... "
result=$(jq -f "$TRANSFORM" --arg required_fields '["name","email","phone"]' "$SCRIPT_DIR/test-input-3.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Empty required fields list (always passes)
echo -n "Test 4: Empty required fields list... "
result=$(jq -f "$TRANSFORM" --arg required_fields '[]' "$SCRIPT_DIR/test-input-4.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Field exists with null value (validation passes - key exists!)
echo -n "Test 5: Field exists with null value... "
result=$(jq -f "$TRANSFORM" --arg required_fields '["name","email"]' "$SCRIPT_DIR/test-input-5.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Field exists with false value (validation passes)
echo -n "Test 6: Field exists with false value... "
result=$(jq -f "$TRANSFORM" --arg required_fields '["enabled"]' "$SCRIPT_DIR/test-input-6.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Field exists with 0 value (validation passes)
echo -n "Test 7: Field exists with 0 value... "
result=$(jq -f "$TRANSFORM" --arg required_fields '["count"]' "$SCRIPT_DIR/test-input-6.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Field exists with empty string value (validation passes)
echo -n "Test 8: Field exists with empty string value... "
result=$(jq -f "$TRANSFORM" --arg required_fields '["message"]' "$SCRIPT_DIR/test-input-6.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Nested field paths - all exist
echo -n "Test 9: Nested field paths - all exist... "
result=$(jq -f "$TRANSFORM" --arg required_fields '["user.name","user.profile.age"]' "$SCRIPT_DIR/test-input-7.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Non-existent nested path
echo -n "Test 10: Non-existent nested path... "
result=$(jq -f "$TRANSFORM" --arg required_fields '["user.profile.email"]' "$SCRIPT_DIR/test-input-9.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Empty object with required fields (should fail)
echo -n "Test 11: Empty object with required fields... "
result=$(jq -f "$TRANSFORM" --arg required_fields '["name"]' "$SCRIPT_DIR/test-input-8.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Field exists with empty array value (validation passes)
echo -n "Test 12: Field exists with empty array value... "
result=$(jq -f "$TRANSFORM" --arg required_fields '["items"]' "$SCRIPT_DIR/test-input-10.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Field exists with empty object value (validation passes)
echo -n "Test 13: Field exists with empty object value... "
result=$(jq -f "$TRANSFORM" --arg required_fields '["metadata"]' "$SCRIPT_DIR/test-input-10.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: All falsy values exist (comprehensive falsy check)
echo -n "Test 14: All falsy values exist... "
result=$(jq -f "$TRANSFORM" --arg required_fields '["enabled","count","message"]' "$SCRIPT_DIR/test-input-6.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All validate-required tests passed!"
