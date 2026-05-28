#!/usr/bin/env bash
set -euo pipefail

# Test array-append transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing array-append transformation..."

# Test 1: Append object to existing array
echo -n "Test 1: Append object to existing array... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg value '{"id":3,"name":"charlie"}' "$SCRIPT_DIR/test-input-1.json")
expected='{"items":[{"id":1,"name":"alice"},{"id":2,"name":"bob"},{"id":3,"name":"charlie"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Append to empty array
echo -n "Test 2: Append to empty array... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg value '"first"' "$SCRIPT_DIR/test-input-2.json")
expected='{"items":["first"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Append to non-existent path (creates array)
echo -n "Test 3: Append to non-existent path (creates array)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "new_items" --arg value '"item1"' "$SCRIPT_DIR/test-input-3.json")
expected='{"new_items":["item1"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Append to nested path
echo -n "Test 4: Append to nested path... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "data.nested.items" --arg value '4' "$SCRIPT_DIR/test-input-4.json")
expected='{"data":{"nested":{"items":[1,2,3,4]}}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Field is not an array (type safety - returns original)
echo -n "Test 5: Field is not an array (returns original)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg value '"test"' "$SCRIPT_DIR/test-input-5.json")
expected='{"items":"not-an-array"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Append null value (falsy value test)
echo -n "Test 6: Append null value... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "tags" --arg value 'null' "$SCRIPT_DIR/test-input-6.json")
expected='{"tags":["alpha","beta",null]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Append false value (falsy value test)
echo -n "Test 7: Append false value... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "flags" --arg value 'false' "$SCRIPT_DIR/test-input-7.json")
expected='{"flags":[true,false,false]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Append 0 value (falsy value test)
echo -n "Test 8: Append 0 value... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "numbers" --arg value '0' "$SCRIPT_DIR/test-input-8.json")
expected='{"numbers":[1,2,0,0]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Append empty string (falsy value test)
echo -n "Test 9: Append empty string... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "strings" --arg value '""' "$SCRIPT_DIR/test-input-12.json")
expected='{"strings":["","non-empty",""]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Append empty array (falsy value test)
echo -n "Test 10: Append empty array... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "values" --arg value '[]' "$SCRIPT_DIR/test-input-9.json")
expected='{"values":[null,"test",[]]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Append empty object (falsy value test)
echo -n "Test 11: Append empty object... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "empty" --arg value '{}' "$SCRIPT_DIR/test-input-11.json")
expected='{"empty":[{}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Append complex object
echo -n "Test 12: Append complex object... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "mixed" --arg value '{"nested":{"key":"value"}}' "$SCRIPT_DIR/test-input-10.json")
expected='{"mixed":[{"a":1},"string",42,true,null,{"nested":{"key":"value"}}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Append array (nested array)
echo -n "Test 13: Append array (nested array)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg value '[1,2,3]' "$SCRIPT_DIR/test-input-2.json")
expected='{"items":[[1,2,3]]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Append number to string array
echo -n "Test 14: Append number to string array... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "tags" --arg value '42' "$SCRIPT_DIR/test-input-6.json")
expected='{"tags":["alpha","beta",42]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All array-append tests passed!"
