#!/usr/bin/env bash
set -euo pipefail

# Test array-unique transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing array-unique transformation..."

# Test 1: Duplicate numbers
echo -n "Test 1: Remove duplicate numbers... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-1.json")
expected='{"items":[1,2,3,4,5]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Duplicate strings
echo -n "Test 2: Remove duplicate strings... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-2.json")
expected='{"items":["apple","banana","cherry","date"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Duplicate objects
echo -n "Test 3: Remove duplicate objects... "
result=$(jq -c -f "$TRANSFORM" --arg array "users" "$SCRIPT_DIR/test-input-3.json")
expected='{"users":[{"id":1,"name":"alice"},{"id":2,"name":"bob"},{"id":3,"name":"charlie"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Empty array
echo -n "Test 4: Handle empty array... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-4.json")
expected='{"items":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Non-array field (type safety)
echo -n "Test 5: Handle non-array field gracefully... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-5.json")
expected='{"items":"not-an-array"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Missing array field
echo -n "Test 6: Handle missing array field... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-6.json")
expected='{"other":[1,2,3]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Mixed types with null
echo -n "Test 7: Remove duplicates with null values... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-7.json")
expected='{"items":[null,false,true,1,"text"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Boolean values (false is not the same as missing)
echo -n "Test 8: Remove duplicate booleans... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-8.json")
expected='{"items":[false,true]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Zero values (0 is not the same as missing)
echo -n "Test 9: Remove duplicates with zero values... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-9.json")
expected='{"items":[0,1,2,3]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Custom array field name
echo -n "Test 10: Use custom array field name... "
result=$(jq -c -f "$TRANSFORM" --arg array "data" "$SCRIPT_DIR/test-input-10.json")
expected='{"data":[5,10,15,20]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Empty objects
echo -n "Test 11: Remove duplicate empty objects... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-11.json")
expected='{"items":[{},{"a":1}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All array-unique tests passed!"
