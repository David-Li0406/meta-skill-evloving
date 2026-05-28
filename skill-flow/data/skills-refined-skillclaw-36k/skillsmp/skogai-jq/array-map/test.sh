#!/usr/bin/env bash
set -euo pipefail

# Test array-map transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing array-map transformation..."

# Test 1: Extract string field from array of objects
echo -n "Test 1: Extract string field from array... "
result=$(jq -c -f "$TRANSFORM" --arg field "name" "$SCRIPT_DIR/test-input-1.json")
expected='["alice","bob","charlie"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Extract numeric field from array
echo -n "Test 2: Extract numeric field from array... "
result=$(jq -c -f "$TRANSFORM" --arg field "age" "$SCRIPT_DIR/test-input-1.json")
expected='[30,25,35]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Extract from custom array field name
echo -n "Test 3: Extract from custom array field name... "
result=$(jq -c -f "$TRANSFORM" --arg field "id" --arg array "users" "$SCRIPT_DIR/test-input-3.json")
expected='[101,102]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Extract from empty array
echo -n "Test 4: Extract from empty array... "
result=$(jq -c -f "$TRANSFORM" --arg field "name" "$SCRIPT_DIR/test-input-4.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Extract field with missing values (returns null for missing fields)
echo -n "Test 5: Extract field with missing values... "
result=$(jq -c -f "$TRANSFORM" --arg field "email" "$SCRIPT_DIR/test-input-5.json")
expected='["alice@example.com",null,"charlie@example.com"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Extract price field with decimal values
echo -n "Test 6: Extract price field with decimal values... "
result=$(jq -c -f "$TRANSFORM" --arg field "price" "$SCRIPT_DIR/test-input-2.json")
expected='[10.50,20.00,15.75]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Handle non-array field gracefully (type safety)
echo -n "Test 7: Handle non-array field gracefully... "
result=$(jq -c -f "$TRANSFORM" --arg field "name" "$SCRIPT_DIR/test-input-6.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Handle array of primitives (returns null for each)
echo -n "Test 8: Handle array of primitives... "
result=$(jq -c -f "$TRANSFORM" --arg field "name" "$SCRIPT_DIR/test-input-7.json")
expected='[null,null,null,null,null]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Handle mixed types in array
echo -n "Test 9: Handle mixed types in array... "
result=$(jq -c -f "$TRANSFORM" --arg field "name" "$SCRIPT_DIR/test-input-8.json")
expected='["alice",null,"bob",null,"charlie",null]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Extract boolean values
echo -n "Test 10: Extract boolean values... "
result=$(jq -c -f "$TRANSFORM" --arg field "active" "$SCRIPT_DIR/test-input-9.json")
expected='[true,false,true]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All array-map tests passed!"
