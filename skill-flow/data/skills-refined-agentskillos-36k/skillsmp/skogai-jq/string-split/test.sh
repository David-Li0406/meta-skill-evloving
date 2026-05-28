#!/usr/bin/env bash
set -euo pipefail

# Test string-split transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing string-split transformation..."

# Test 1: Split comma-separated values
echo -n "Test 1: Split comma-separated values... "
result=$(jq -c -f "$TRANSFORM" --arg path "data" --arg delimiter "," "$SCRIPT_DIR/test-input-1.json")
expected='["a","b","c"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Split nested string by dot
echo -n "Test 2: Split nested string by dot... "
result=$(jq -c -f "$TRANSFORM" --arg path "config.path" --arg delimiter "." "$SCRIPT_DIR/test-input-1.json")
expected='["x","y","z"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Split by space in deeply nested string
echo -n "Test 3: Split by space in deeply nested string... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.profile.tags" --arg delimiter " " "$SCRIPT_DIR/test-input-2.json")
expected='["hello","world","test"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Split empty string returns empty array
echo -n "Test 4: Split empty string returns empty array... "
result=$(jq -c -f "$TRANSFORM" --arg path "empty" --arg delimiter "," "$SCRIPT_DIR/test-input-3.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Split string where delimiter not found returns single element array
echo -n "Test 5: Split string where delimiter not found... "
result=$(jq -c -f "$TRANSFORM" --arg path "single" --arg delimiter "." "$SCRIPT_DIR/test-input-3.json")
expected='["nodots"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Non-existent path returns null
echo -n "Test 6: Non-existent path returns null... "
result=$(jq -f "$TRANSFORM" --arg path "missing.field" --arg delimiter "," "$SCRIPT_DIR/test-input-4.json")
expected='null'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Split with multi-character delimiter
echo -n "Test 7: Split with multi-character delimiter... "
result=$(jq -c -f "$TRANSFORM" --arg path "multichar" --arg delimiter "::" "$SCRIPT_DIR/test-input-3.json")
expected='["one","two","three"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Delimiter at start of string
echo -n "Test 8: Delimiter at start of string... "
result=$(jq -c -f "$TRANSFORM" --arg path "start" --arg delimiter "," "$SCRIPT_DIR/test-input-5.json")
expected='["","a","b"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Delimiter at end of string
echo -n "Test 9: Delimiter at end of string... "
result=$(jq -c -f "$TRANSFORM" --arg path "end" --arg delimiter "," "$SCRIPT_DIR/test-input-5.json")
expected='["a","b",""]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Consecutive delimiters
echo -n "Test 10: Consecutive delimiters... "
result=$(jq -c -f "$TRANSFORM" --arg path "consecutive" --arg delimiter "," "$SCRIPT_DIR/test-input-5.json")
expected='["a","","b"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: String containing only delimiter
echo -n "Test 11: String containing only delimiter... "
result=$(jq -c -f "$TRANSFORM" --arg path "only_delimiter" --arg delimiter "," "$SCRIPT_DIR/test-input-5.json")
expected='["",""]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Non-string value (number) returns null
echo -n "Test 12: Non-string value (number) returns null... "
result=$(jq -c -f "$TRANSFORM" --arg path "number" --arg delimiter "," "$SCRIPT_DIR/test-input-6.json")
expected='null'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Non-string value (boolean) returns null
echo -n "Test 13: Non-string value (boolean) returns null... "
result=$(jq -c -f "$TRANSFORM" --arg path "boolean" --arg delimiter "," "$SCRIPT_DIR/test-input-6.json")
expected='null'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Non-string value (null) returns null
echo -n "Test 14: Non-string value (null) returns null... "
result=$(jq -c -f "$TRANSFORM" --arg path "null_value" --arg delimiter "," "$SCRIPT_DIR/test-input-6.json")
expected='null'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All string-split tests passed!"
