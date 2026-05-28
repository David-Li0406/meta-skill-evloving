#!/usr/bin/env bash
set -euo pipefail

# Test string-match transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing string-match transformation..."

# Test 1: Pattern matches - email format
echo -n "Test 1: Pattern matches - email format... "
result=$(jq -c -f "$TRANSFORM" --arg path "email" --arg pattern "^[^@]+@[^@]+\\.[^@]+$" "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Pattern matches - digits only
echo -n "Test 2: Pattern matches - digits only... "
result=$(jq -c -f "$TRANSFORM" --arg path "code" --arg pattern "^[0-9]+$" "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Pattern doesn't match - contains digits
echo -n "Test 3: Pattern doesn't match - contains digits... "
result=$(jq -c -f "$TRANSFORM" --arg path "name" --arg pattern "^[0-9]+$" "$SCRIPT_DIR/test-input-1.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Nested path pattern match
echo -n "Test 4: Nested path pattern match... "
result=$(jq -c -f "$TRANSFORM" --arg path "nested.field" --arg pattern "^[a-z]+$" "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Empty pattern (matches everything)
echo -n "Test 5: Empty pattern (matches everything)... "
result=$(jq -c -f "$TRANSFORM" --arg path "name" --arg pattern "" "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Empty string with pattern
echo -n "Test 6: Empty string with pattern... "
result=$(jq -c -f "$TRANSFORM" --arg path "empty" --arg pattern "^$" "$SCRIPT_DIR/test-input-3.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Regex special characters - dot
echo -n "Test 7: Regex special characters - dot... "
result=$(jq -c -f "$TRANSFORM" --arg path "special" --arg pattern "\\." "$SCRIPT_DIR/test-input-5.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Case sensitivity - uppercase pattern fails on mixed case
echo -n "Test 8: Case sensitivity - uppercase pattern fails on mixed case... "
result=$(jq -c -f "$TRANSFORM" --arg path "case_sensitive" --arg pattern "^[A-Z]+$" "$SCRIPT_DIR/test-input-6.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Partial match (pattern found anywhere in string)
echo -n "Test 9: Partial match (pattern found anywhere in string)... "
result=$(jq -c -f "$TRANSFORM" --arg path "partial" --arg pattern "[0-9]+" "$SCRIPT_DIR/test-input-6.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Full match vs partial (using anchors)
echo -n "Test 10: Full match vs partial (using anchors)... "
result=$(jq -c -f "$TRANSFORM" --arg path "partial" --arg pattern "^[0-9]+$" "$SCRIPT_DIR/test-input-6.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Invalid regex (unclosed bracket) - should return false
echo -n "Test 11: Invalid regex (unclosed bracket) - returns false... "
result=$(jq -c -f "$TRANSFORM" --arg path "name" --arg pattern "[abc" "$SCRIPT_DIR/test-input-1.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Field doesn't exist - returns false
echo -n "Test 12: Field doesn't exist - returns false... "
result=$(jq -c -f "$TRANSFORM" --arg path "missing.field" --arg pattern ".*" "$SCRIPT_DIR/test-input-1.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Field is not a string (number) - returns false
echo -n "Test 13: Field is not a string (number) - returns false... "
result=$(jq -c -f "$TRANSFORM" --arg path "number" --arg pattern ".*" "$SCRIPT_DIR/test-input-4.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Field is boolean - returns false
echo -n "Test 14: Field is boolean - returns false... "
result=$(jq -c -f "$TRANSFORM" --arg path "boolean" --arg pattern ".*" "$SCRIPT_DIR/test-input-4.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 15: Field is null - returns false
echo -n "Test 15: Field is null - returns false... "
result=$(jq -c -f "$TRANSFORM" --arg path "null_value" --arg pattern ".*" "$SCRIPT_DIR/test-input-4.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 16: Field is object - returns false
echo -n "Test 16: Field is object - returns false... "
result=$(jq -c -f "$TRANSFORM" --arg path "object" --arg pattern ".*" "$SCRIPT_DIR/test-input-4.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 17: Field is array - returns false
echo -n "Test 17: Field is array - returns false... "
result=$(jq -c -f "$TRANSFORM" --arg path "array" --arg pattern ".*" "$SCRIPT_DIR/test-input-4.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 18: Whitespace-only string matches whitespace pattern
echo -n "Test 18: Whitespace-only string matches whitespace pattern... "
result=$(jq -c -f "$TRANSFORM" --arg path "whitespace" --arg pattern "^\\s+$" "$SCRIPT_DIR/test-input-3.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 19: Multiline string with newline
echo -n "Test 19: Multiline string with newline... "
result=$(jq -c -f "$TRANSFORM" --arg path "newline" --arg pattern "\\n" "$SCRIPT_DIR/test-input-3.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 20: Complex regex - phone number pattern
echo -n "Test 20: Complex regex - phone number pattern... "
result=$(jq -c -f "$TRANSFORM" --arg path "phone" --arg pattern "^\\+[0-9]-[0-9]{3}-[0-9]{4}$" "$SCRIPT_DIR/test-input-2.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All string-match tests passed!"
