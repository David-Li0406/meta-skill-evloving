#!/usr/bin/env bash
set -euo pipefail

# Test string-trim transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing string-trim transformation..."

# Test 1: Trim leading and trailing whitespace
echo -n "Test 1: Trim leading and trailing whitespace... "
result=$(jq -c -f "$TRANSFORM" --arg path "message" "$SCRIPT_DIR/test-input-1.json")
expected='{"message":"hello world"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Trim trailing whitespace only
echo -n "Test 2: Trim trailing whitespace only... "
result=$(jq -c -f "$TRANSFORM" --arg path "message" "$SCRIPT_DIR/test-input-2.json")
expected='{"message":"hello world"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Trim leading whitespace only
echo -n "Test 3: Trim leading whitespace only... "
result=$(jq -c -f "$TRANSFORM" --arg path "message" "$SCRIPT_DIR/test-input-3.json")
expected='{"message":"hello world"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Preserve internal whitespace
echo -n "Test 4: Preserve internal whitespace... "
result=$(jq -c -f "$TRANSFORM" --arg path "message" "$SCRIPT_DIR/test-input-4.json")
expected='{"message":"hello   world"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: All whitespace string becomes empty
echo -n "Test 5: All whitespace string becomes empty... "
result=$(jq -c -f "$TRANSFORM" --arg path "message" "$SCRIPT_DIR/test-input-5.json")
expected='{"message":""}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Empty string unchanged
echo -n "Test 6: Empty string unchanged... "
result=$(jq -c -f "$TRANSFORM" --arg path "message" "$SCRIPT_DIR/test-input-6.json")
expected='{"message":""}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: No whitespace unchanged
echo -n "Test 7: No whitespace unchanged... "
result=$(jq -c -f "$TRANSFORM" --arg path "message" "$SCRIPT_DIR/test-input-7.json")
expected='{"message":"no-whitespace"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Tabs and newlines trimmed
echo -n "Test 8: Tabs and newlines trimmed... "
result=$(jq -c -f "$TRANSFORM" --arg path "message" "$SCRIPT_DIR/test-input-8.json")
expected='{"message":"hello"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Field doesn't exist - return unchanged object
echo -n "Test 9: Field doesn't exist - return unchanged object... "
result=$(jq -c -f "$TRANSFORM" --arg path "message" "$SCRIPT_DIR/test-input-9.json")
expected='{"other":"field"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Field is not a string (number) - return unchanged object
echo -n "Test 10: Field is not a string (number) - return unchanged object... "
result=$(jq -c -f "$TRANSFORM" --arg path "message" "$SCRIPT_DIR/test-input-10.json")
expected='{"message":123}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Nested path with whitespace
echo -n "Test 11: Nested path with whitespace... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.name" "$SCRIPT_DIR/test-input-11.json")
expected='{"user":{"name":"nested"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Field is null - return unchanged object
echo -n "Test 12: Field is null - return unchanged object... "
result=$(jq -c -f "$TRANSFORM" --arg path "message" "$SCRIPT_DIR/test-input-12.json")
expected='{"message":null}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Field is boolean false - return unchanged object
echo -n "Test 13: Field is boolean false - return unchanged object... "
result=$(jq -c -f "$TRANSFORM" --arg path "message" "$SCRIPT_DIR/test-input-13.json")
expected='{"message":false}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All string-trim tests passed!"
