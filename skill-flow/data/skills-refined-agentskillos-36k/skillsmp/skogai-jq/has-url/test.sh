#!/usr/bin/env bash
set -euo pipefail

# Test has-url transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing has-url transformation..."

# Test 1: Has HTTP URL (true)
echo -n "Test 1: Has HTTP URL (true)... "
result=$(jq -c -f "$TRANSFORM" --arg path "text" "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Has HTTPS URL (true)
echo -n "Test 2: Has HTTPS URL (true)... "
result=$(jq -c -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-2.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Has FTP URL (true)
echo -n "Test 3: Has FTP URL (true)... "
result=$(jq -c -f "$TRANSFORM" --arg path "data" "$SCRIPT_DIR/test-input-3.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: No URL (false)
echo -n "Test 4: No URL (false)... "
result=$(jq -c -f "$TRANSFORM" --arg path "text" "$SCRIPT_DIR/test-input-4.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Empty string (false)
echo -n "Test 5: Empty string (false)... "
result=$(jq -c -f "$TRANSFORM" --arg path "empty" "$SCRIPT_DIR/test-input-5.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Partial URL without scheme (false)
echo -n "Test 6: Partial URL without scheme (false)... "
result=$(jq -c -f "$TRANSFORM" --arg path "partial" "$SCRIPT_DIR/test-input-6.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: URL in markdown link (true)
echo -n "Test 7: URL in markdown link (true)... "
result=$(jq -c -f "$TRANSFORM" --arg path "markdown" "$SCRIPT_DIR/test-input-7.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Field doesn't exist (false)
echo -n "Test 8: Field doesn't exist (false)... "
result=$(jq -c -f "$TRANSFORM" --arg path "nonexistent" "$SCRIPT_DIR/test-input-8.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Field is not a string - number (false)
echo -n "Test 9: Field is not a string - number (false)... "
result=$(jq -c -f "$TRANSFORM" --arg path "number" "$SCRIPT_DIR/test-input-9.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Field is not a string - boolean (false)
echo -n "Test 10: Field is not a string - boolean (false)... "
result=$(jq -c -f "$TRANSFORM" --arg path "boolean" "$SCRIPT_DIR/test-input-9.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Field is null (false)
echo -n "Test 11: Field is null (false)... "
result=$(jq -c -f "$TRANSFORM" --arg path "null_value" "$SCRIPT_DIR/test-input-9.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Field is object (false)
echo -n "Test 12: Field is object (false)... "
result=$(jq -c -f "$TRANSFORM" --arg path "object" "$SCRIPT_DIR/test-input-9.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Field is array (false)
echo -n "Test 13: Field is array (false)... "
result=$(jq -c -f "$TRANSFORM" --arg path "array" "$SCRIPT_DIR/test-input-9.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Nested path with URL (true)
echo -n "Test 14: Nested path with URL (true)... "
result=$(jq -c -f "$TRANSFORM" --arg path "nested.field" "$SCRIPT_DIR/test-input-10.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 15: Multiple URLs in text (true)
echo -n "Test 15: Multiple URLs in text (true)... "
result=$(jq -c -f "$TRANSFORM" --arg path "multi" "$SCRIPT_DIR/test-input-11.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All has-url tests passed!"
