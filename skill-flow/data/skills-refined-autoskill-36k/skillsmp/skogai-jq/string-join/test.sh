#!/usr/bin/env bash
set -euo pipefail

# Test string-join transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing string-join transformation..."

# Test 1: Join simple array with comma
echo -n "Test 1: Join simple array with comma... "
result=$(jq -r -f "$TRANSFORM" --arg path "items" --arg delimiter "," "$SCRIPT_DIR/test-input-1.json")
expected="a,b,c"
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Join nested array with space
echo -n "Test 2: Join nested array with space... "
result=$(jq -r -f "$TRANSFORM" --arg path "nested.tags" --arg delimiter " " "$SCRIPT_DIR/test-input-1.json")
expected="x y z"
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Join array of numbers with dash
echo -n "Test 3: Join array of numbers with dash... "
result=$(jq -r -f "$TRANSFORM" --arg path "data.scores" --arg delimiter "-" "$SCRIPT_DIR/test-input-2.json")
expected="100-95-88"
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Join array of booleans
echo -n "Test 4: Join array of booleans... "
result=$(jq -r -f "$TRANSFORM" --arg path "deep.level.values" --arg delimiter "|" "$SCRIPT_DIR/test-input-2.json")
expected="true|false|true"
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Join empty array returns empty string
echo -n "Test 5: Join empty array returns empty string... "
result=$(jq -r -f "$TRANSFORM" --arg path "empty" --arg delimiter "," "$SCRIPT_DIR/test-input-3.json")
expected=""
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Join single element array
echo -n "Test 6: Join single element array... "
result=$(jq -r -f "$TRANSFORM" --arg path "single" --arg delimiter "," "$SCRIPT_DIR/test-input-3.json")
expected="only"
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Join mixed types (numbers, strings, booleans, null, false, 0)
echo -n "Test 7: Join mixed types including null, false, 0... "
result=$(jq -r -f "$TRANSFORM" --arg path "mixed" --arg delimiter "," "$SCRIPT_DIR/test-input-3.json")
expected="1,two,true,null,false,0"
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Join with multi-character delimiter
echo -n "Test 8: Join with multi-character delimiter... "
result=$(jq -r -f "$TRANSFORM" --arg path "items" --arg delimiter " :: " "$SCRIPT_DIR/test-input-1.json")
expected="a :: b :: c"
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Non-existent path returns null
echo -n "Test 9: Non-existent path returns null... "
result=$(jq -f "$TRANSFORM" --arg path "missing.field" --arg delimiter "," "$SCRIPT_DIR/test-input-1.json")
expected="null"
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Non-array value (string) returns null
echo -n "Test 10: Non-array value (string) returns null... "
result=$(jq -f "$TRANSFORM" --arg path "notArray" --arg delimiter "," "$SCRIPT_DIR/test-input-4.json")
expected="null"
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Non-array value (number) returns null
echo -n "Test 11: Non-array value (number) returns null... "
result=$(jq -f "$TRANSFORM" --arg path "number" --arg delimiter "," "$SCRIPT_DIR/test-input-4.json")
expected="null"
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Non-array value (boolean) returns null
echo -n "Test 12: Non-array value (boolean) returns null... "
result=$(jq -f "$TRANSFORM" --arg path "boolean" --arg delimiter "," "$SCRIPT_DIR/test-input-4.json")
expected="null"
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Non-array value (null) returns null
echo -n "Test 13: Non-array value (null) returns null... "
result=$(jq -f "$TRANSFORM" --arg path "null_value" --arg delimiter "," "$SCRIPT_DIR/test-input-4.json")
expected="null"
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Non-array value (object) returns null
echo -n "Test 14: Non-array value (object) returns null... "
result=$(jq -f "$TRANSFORM" --arg path "object" --arg delimiter "," "$SCRIPT_DIR/test-input-4.json")
expected="null"
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 15: Join array with decimal numbers
echo -n "Test 15: Join array with decimal numbers... "
result=$(jq -r -f "$TRANSFORM" --arg path "decimals" --arg delimiter "," "$SCRIPT_DIR/test-input-5.json")
expected="10.5,20.0,15.75"
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 16: Join array with negative numbers
echo -n "Test 16: Join array with negative numbers... "
result=$(jq -r -f "$TRANSFORM" --arg path "negatives" --arg delimiter " " "$SCRIPT_DIR/test-input-5.json")
expected="-1 -2 -3"
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 17: Join array of zeros (falsy but valid values)
echo -n "Test 17: Join array of zeros... "
result=$(jq -r -f "$TRANSFORM" --arg path "zeros" --arg delimiter "," "$SCRIPT_DIR/test-input-5.json")
expected="0,0,0"
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All string-join tests passed!"
