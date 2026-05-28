#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing validate-message-schema transformation..."

# Test 1: Valid message with all required fields - happy path
echo -n "Test 1: Valid message with all required fields - happy path... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-1.json")
expected='{"valid":true,"errors":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Valid message with optional timestamp field
echo -n "Test 2: Valid message with optional timestamp field... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-2.json")
expected='{"valid":true,"errors":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Valid system message
echo -n "Test 3: Valid system message... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-3.json")
expected='{"valid":true,"errors":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Missing required field (content)
echo -n "Test 4: Missing required field (content)... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-4.json")
expected='{"valid":false,"errors":["Required field '\''content'\'' is missing"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Missing required field (role)
echo -n "Test 5: Missing required field (role)... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-5.json")
expected='{"valid":false,"errors":["Required field '\''role'\'' is missing"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Invalid role value
echo -n "Test 6: Invalid role value... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-6.json")
expected='{"valid":false,"errors":["Field '\''role'\'' has invalid value '\''admin'\'' (must be one of: user, assistant, system)"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Wrong type for content field (number instead of string)
echo -n "Test 7: Wrong type for content field (number instead of string)... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-7.json")
expected='{"valid":false,"errors":["Field '\''content'\'' has wrong type (expected string, got number)"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Null value for content field (falsy value test - CRITICAL)
echo -n "Test 8: Null value for content field (falsy value test)... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-8.json")
expected='{"valid":false,"errors":["Field '\''content'\'' has wrong type (expected string, got null)"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: False value for content field (falsy value test - CRITICAL)
echo -n "Test 9: False value for content field (falsy value test)... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-9.json")
expected='{"valid":false,"errors":["Field '\''content'\'' has wrong type (expected string, got boolean)"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Empty string for content (falsy value test - should PASS as it's valid string)
echo -n "Test 10: Empty string for content (falsy value test - should PASS)... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-10.json")
expected='{"valid":true,"errors":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Extra unexpected fields
echo -n "Test 11: Extra unexpected fields... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-11.json")
expected='{"valid":false,"errors":["Unexpected fields: extra"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Wrong type for role field (number instead of string)
echo -n "Test 12: Wrong type for role field (number instead of string)... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-12.json")
expected='{"valid":false,"errors":["Field '\''role'\'' has wrong type (expected string, got number)"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Wrong type for timestamp field (number instead of string)
echo -n "Test 13: Wrong type for timestamp field (number instead of string)... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-13.json")
expected='{"valid":false,"errors":["Field '\''timestamp'\'' has wrong type (expected string, got number)"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Empty object (missing both required fields)
echo -n "Test 14: Empty object (missing both required fields)... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-14.json")
# Sort errors to handle potential order differences
result_valid=$(echo "$result" | jq -c '.valid')
result_errors=$(echo "$result" | jq -c '.errors | sort')
expected_valid='false'
expected_errors='["Required field '\''content'\'' is missing","Required field '\''role'\'' is missing"]'
if [[ "$result_valid" == "$expected_valid" && "$result_errors" == "$expected_errors" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected valid: $expected_valid, errors: $expected_errors"
    echo "  Got valid: $result_valid, errors: $result_errors"
    exit 1
fi

# Test 15: Input is not an object (string)
echo -n "Test 15: Input is not an object (string)... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-15.json")
expected='{"valid":false,"errors":["Input must be an object"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 16: Empty string for role (edge case - valid type, invalid enum value)
echo -n "Test 16: Empty string for role (edge case - valid type, invalid enum)... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-16.json")
expected='{"valid":false,"errors":["Field '\''role'\'' has invalid value '\'''\'' (must be one of: user, assistant, system)"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 17: Empty string for optional timestamp (should PASS - correct type)
echo -n "Test 17: Empty string for optional timestamp (should PASS)... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-17.json")
expected='{"valid":true,"errors":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All validate-message-schema tests passed!"
