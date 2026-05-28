#!/usr/bin/env bash
set -euo pipefail

# Test map-transform transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing map-transform transformation..."

# Test 1: Extract simple field from array elements
echo -n "Test 1: Extract simple field from array... "
result=$(jq -c -f "$TRANSFORM" --arg field "name" "$SCRIPT_DIR/test-input-1.json")
expected='{"items":["alice","bob","charlie"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Apply multiplication operation
echo -n "Test 2: Apply multiplication to field values... "
result=$(jq -c -f "$TRANSFORM" --arg field "price" --arg operation "multiply" --arg operand "1.1" "$SCRIPT_DIR/test-input-2.json")
expected='{"items":[11,22,16.5]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Handle empty array
echo -n "Test 3: Handle empty array... "
result=$(jq -c -f "$TRANSFORM" --arg field "name" "$SCRIPT_DIR/test-input-3.json")
expected='{"items":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Handle single element array
echo -n "Test 4: Handle single element array... "
result=$(jq -c -f "$TRANSFORM" --arg field "value" "$SCRIPT_DIR/test-input-4.json")
expected='{"items":[42]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Transform with nested array path
echo -n "Test 5: Transform with nested array path... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "data.users" --arg field "id" "$SCRIPT_DIR/test-input-5.json")
expected='{"data":{"users":[1,2]}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Apply uppercase operation
echo -n "Test 6: Apply uppercase string operation... "
result=$(jq -c -f "$TRANSFORM" --arg field "name" --arg operation "uppercase" "$SCRIPT_DIR/test-input-6.json")
expected='{"items":["ALICE","BOB"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Apply addition operation
echo -n "Test 7: Apply addition operation... "
result=$(jq -c -f "$TRANSFORM" --arg field "count" --arg operation "add" --arg operand "5" "$SCRIPT_DIR/test-input-7.json")
expected='{"items":[10,15,8]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Handle non-array field gracefully
echo -n "Test 8: Handle non-array field gracefully... "
result=$(jq -c -f "$TRANSFORM" --arg field "name" "$SCRIPT_DIR/test-input-8.json")
expected='{"items":"not-an-array"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Handle falsy values (null, false, 0, empty string)
echo -n "Test 9: Handle falsy values correctly... "
result=$(jq -c -f "$TRANSFORM" --arg field "status" "$SCRIPT_DIR/test-input-9.json")
expected='{"items":[null,false,0,""]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Apply division operation
echo -n "Test 10: Apply division operation... "
result=$(jq -c -f "$TRANSFORM" --arg field "value" --arg operation "divide" --arg operand "2" "$SCRIPT_DIR/test-input-10.json")
expected='{"items":[50,100]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Apply tostring operation
echo -n "Test 11: Apply tostring operation... "
result=$(jq -c -f "$TRANSFORM" --arg field "id" --arg operation "tostring" "$SCRIPT_DIR/test-input-11.json")
expected='{"items":["1","2"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Apply lowercase operation
echo -n "Test 12: Apply lowercase operation... "
result=$(jq -c -f "$TRANSFORM" --arg field "text" --arg operation "lowercase" "$SCRIPT_DIR/test-input-12.json")
expected='{"items":["hello","world"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All map-transform tests passed!"
