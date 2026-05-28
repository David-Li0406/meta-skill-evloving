#!/usr/bin/env bash
set -euo pipefail

# Test extract-first-line transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing extract-first-line transformation..."

# Test 1: Multiline string with Unix newlines (\n)
echo -n "Test 1: Multiline string with Unix newlines... "
result=$(jq -c -f "$TRANSFORM" --arg path "text" "$SCRIPT_DIR/test-input-1.json")
expected='"line1"'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Multiline string with Windows newlines (\r\n)
echo -n "Test 2: Multiline string with Windows newlines... "
result=$(jq -c -f "$TRANSFORM" --arg path "windows" "$SCRIPT_DIR/test-input-2.json")
expected='"line1"'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Single line (no newlines) returns entire string
echo -n "Test 3: Single line returns entire string... "
result=$(jq -c -f "$TRANSFORM" --arg path "single" "$SCRIPT_DIR/test-input-3.json")
expected='"only one line"'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Empty string returns empty string
echo -n "Test 4: Empty string returns empty string... "
result=$(jq -c -f "$TRANSFORM" --arg path "empty" "$SCRIPT_DIR/test-input-3.json")
expected='""'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: String with only newlines returns empty
echo -n "Test 5: String with only newlines returns empty... "
result=$(jq -c -f "$TRANSFORM" --arg path "newlines_only" "$SCRIPT_DIR/test-input-3.json")
expected='""'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Leading newline returns empty first line
echo -n "Test 6: Leading newline returns empty first line... "
result=$(jq -c -f "$TRANSFORM" --arg path "leading" "$SCRIPT_DIR/test-input-4.json")
expected='""'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Trailing newline doesn't affect first line
echo -n "Test 7: Trailing newline doesn't affect first line... "
result=$(jq -c -f "$TRANSFORM" --arg path "trailing" "$SCRIPT_DIR/test-input-4.json")
expected='"line1"'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Mixed newline types (Windows + Unix)
echo -n "Test 8: Mixed newline types... "
result=$(jq -c -f "$TRANSFORM" --arg path "mixed" "$SCRIPT_DIR/test-input-2.json")
expected='"first"'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Non-existent field returns null
echo -n "Test 9: Non-existent field returns null... "
result=$(jq -f "$TRANSFORM" --arg path "missing" "$SCRIPT_DIR/test-input-1.json")
expected='null'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Non-string value (number) returns null
echo -n "Test 10: Non-string value (number) returns null... "
result=$(jq -f "$TRANSFORM" --arg path "number" "$SCRIPT_DIR/test-input-5.json")
expected='null'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Non-string value (boolean false) returns null
echo -n "Test 11: Non-string value (boolean false) returns null... "
result=$(jq -f "$TRANSFORM" --arg path "boolean" "$SCRIPT_DIR/test-input-5.json")
expected='null'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Null value returns null
echo -n "Test 12: Null value returns null... "
result=$(jq -f "$TRANSFORM" --arg path "null_value" "$SCRIPT_DIR/test-input-5.json")
expected='null'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Non-string value (array) returns null
echo -n "Test 13: Non-string value (array) returns null... "
result=$(jq -f "$TRANSFORM" --arg path "array" "$SCRIPT_DIR/test-input-5.json")
expected='null'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Non-string value (object) returns null
echo -n "Test 14: Non-string value (object) returns null... "
result=$(jq -f "$TRANSFORM" --arg path "object" "$SCRIPT_DIR/test-input-5.json")
expected='null'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 15: Deeply nested path
echo -n "Test 15: Deeply nested path... "
result=$(jq -c -f "$TRANSFORM" --arg path "data.deep.nested" "$SCRIPT_DIR/test-input-6.json")
expected='"first line"'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 16: Nested path extraction
echo -n "Test 16: Nested path extraction... "
result=$(jq -c -f "$TRANSFORM" --arg path "nested.content" "$SCRIPT_DIR/test-input-1.json")
expected='"first"'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All extract-first-line tests passed!"
