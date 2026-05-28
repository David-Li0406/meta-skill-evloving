#!/usr/bin/env bash
set -euo pipefail

# Test string-replace transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing string-replace transformation..."

# Test 1: Replace all occurrences of a pattern
echo -n "Test 1: Replace all occurrences of pattern... "
result=$(jq -c -f "$TRANSFORM" --arg path "data" --arg pattern "\\d" --arg replacement "X" "$SCRIPT_DIR/test-input-1.json")
expected='{"data":"Phone: XXX-XXX-XXXX","nested":{"message":"Hello world!"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Replace word in nested path
echo -n "Test 2: Replace word in nested path... "
result=$(jq -c -f "$TRANSFORM" --arg path "nested.message" --arg pattern "world" --arg replacement "universe" "$SCRIPT_DIR/test-input-1.json")
expected='{"data":"Phone: 123-456-7890","nested":{"message":"Hello universe!"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Replace multiple occurrences in one string
echo -n "Test 3: Replace multiple occurrences... "
result=$(jq -c -f "$TRANSFORM" --arg path "text" --arg pattern "foo" --arg replacement "bar" "$SCRIPT_DIR/test-input-2.json")
expected='{"text":"bar bar bar baz bar "}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Pattern not found (returns original string)
echo -n "Test 4: Pattern not found returns original... "
result=$(jq -c -f "$TRANSFORM" --arg path "nomatch" --arg pattern "xyz" --arg replacement "abc" "$SCRIPT_DIR/test-input-3.json")
expected='{"empty":"","nomatch":"testing with no pattern match"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Empty string (no matches)
echo -n "Test 5: Empty string returns empty string... "
result=$(jq -c -f "$TRANSFORM" --arg path "empty" --arg pattern "test" --arg replacement "x" "$SCRIPT_DIR/test-input-3.json")
expected='{"empty":"","nomatch":"testing with no pattern match"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Empty replacement (delete matches)
echo -n "Test 6: Empty replacement deletes matches... "
result=$(jq -c -f "$TRANSFORM" --arg path "text" --arg pattern "foo " --arg replacement "" "$SCRIPT_DIR/test-input-2.json")
expected='{"text":"bar baz "}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Non-existent path returns original object
echo -n "Test 7: Non-existent path returns original... "
result=$(jq -c -f "$TRANSFORM" --arg path "missing.field" --arg pattern "test" --arg replacement "x" "$SCRIPT_DIR/test-input-4.json")
expected='{"exists":"some value"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Field is number (not string) returns original
echo -n "Test 8: Number field returns original object... "
result=$(jq -c -f "$TRANSFORM" --arg path "number" --arg pattern "4" --arg replacement "X" "$SCRIPT_DIR/test-input-5.json")
expected='{"number":42,"boolean":false,"null_value":null,"object":{"key":"value"},"array":[1,2,3]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Field is boolean (not string) returns original
echo -n "Test 9: Boolean field returns original object... "
result=$(jq -c -f "$TRANSFORM" --arg path "boolean" --arg pattern "false" --arg replacement "true" "$SCRIPT_DIR/test-input-5.json")
expected='{"number":42,"boolean":false,"null_value":null,"object":{"key":"value"},"array":[1,2,3]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Field is null returns original
echo -n "Test 10: Null field returns original object... "
result=$(jq -c -f "$TRANSFORM" --arg path "null_value" --arg pattern "test" --arg replacement "x" "$SCRIPT_DIR/test-input-5.json")
expected='{"number":42,"boolean":false,"null_value":null,"object":{"key":"value"},"array":[1,2,3]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Field is object (not string) returns original
echo -n "Test 11: Object field returns original object... "
result=$(jq -c -f "$TRANSFORM" --arg path "object" --arg pattern "key" --arg replacement "x" "$SCRIPT_DIR/test-input-5.json")
expected='{"number":42,"boolean":false,"null_value":null,"object":{"key":"value"},"array":[1,2,3]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Field is array (not string) returns original
echo -n "Test 12: Array field returns original object... "
result=$(jq -c -f "$TRANSFORM" --arg path "array" --arg pattern "1" --arg replacement "x" "$SCRIPT_DIR/test-input-5.json")
expected='{"number":42,"boolean":false,"null_value":null,"object":{"key":"value"},"array":[1,2,3]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Regex special characters (dollar sign)
echo -n "Test 13: Regex special characters (dollar)... "
result=$(jq -c -f "$TRANSFORM" --arg path "special" --arg pattern "\\$" --arg replacement "" "$SCRIPT_DIR/test-input-6.json")
expected='{"special":"Price: 19.99 (sale!)","brackets":"array[0] = value","dots":"file.txt.bak"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Regex special characters (brackets)
echo -n "Test 14: Regex special characters (brackets)... "
result=$(jq -c -f "$TRANSFORM" --arg path "brackets" --arg pattern "\\[\\d+\\]" --arg replacement "[X]" "$SCRIPT_DIR/test-input-6.json")
expected='{"special":"Price: $19.99 (sale!)","brackets":"array[X] = value","dots":"file.txt.bak"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 15: Replace with regex pattern (dots)
echo -n "Test 15: Replace dot pattern... "
result=$(jq -c -f "$TRANSFORM" --arg path "dots" --arg pattern "\\." --arg replacement "_" "$SCRIPT_DIR/test-input-6.json")
expected='{"special":"Price: $19.99 (sale!)","brackets":"array[0] = value","dots":"file_txt_bak"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All string-replace tests passed!"
