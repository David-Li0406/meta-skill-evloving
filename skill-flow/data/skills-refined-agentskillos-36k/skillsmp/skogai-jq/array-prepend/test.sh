#!/usr/bin/env bash
set -euo pipefail

# Test array-prepend transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing array-prepend transformation..."

# Test 1: Prepend string to existing array
echo -n "Test 1: Prepend string to existing array... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg value '"a"' "$SCRIPT_DIR/test-input-1.json")
expected='{"items":["a","b","c","d"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Prepend to empty array
echo -n "Test 2: Prepend to empty array... "
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

# Test 3: Prepend to non-existent path (creates array)
echo -n "Test 3: Prepend to non-existent path (creates array)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg value '"new"' "$SCRIPT_DIR/test-input-3.json")
expected='{"items":["new"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Type safety - non-array field returns original unchanged
echo -n "Test 4: Type safety - non-array field returns original... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg value '"test"' "$SCRIPT_DIR/test-input-4.json")
expected='{"items":"not-an-array"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Prepend object to array
echo -n "Test 5: Prepend object to array... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "users" --arg value '{"id":1,"name":"alice"}' "$SCRIPT_DIR/test-input-5.json")
expected='{"users":[{"id":1,"name":"alice"},{"id":2,"name":"bob"},{"id":3,"name":"charlie"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Prepend to nested array path
echo -n "Test 6: Prepend to nested array path... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "data.items" --arg value '1' "$SCRIPT_DIR/test-input-6.json")
expected='{"data":{"items":[1,2,3,4]}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Prepend null value (falsy value test)
echo -n "Test 7: Prepend null value... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg value 'null' "$SCRIPT_DIR/test-input-7.json")
expected='{"items":[null,1,2,3]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Prepend false value (falsy value test)
echo -n "Test 8: Prepend false value... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg value 'false' "$SCRIPT_DIR/test-input-8.json")
expected='{"items":[false,true,false]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Prepend zero value (falsy value test)
echo -n "Test 9: Prepend zero value... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg value '0' "$SCRIPT_DIR/test-input-7.json")
expected='{"items":[0,1,2,3]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Prepend empty string (falsy value test)
echo -n "Test 10: Prepend empty string... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg value '""' "$SCRIPT_DIR/test-input-9.json")
expected='{"items":["","test"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Prepend empty array (falsy value test)
echo -n "Test 11: Prepend empty array... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg value '[]' "$SCRIPT_DIR/test-input-11.json")
expected='{"items":[[],[1,2],[3,4]]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Prepend empty object (falsy value test)
echo -n "Test 12: Prepend empty object... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg value '{}' "$SCRIPT_DIR/test-input-10.json")
expected='{"items":[{},{"nested":"value"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Prepend number to numeric array
echo -n "Test 13: Prepend number to numeric array... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg value '5' "$SCRIPT_DIR/test-input-12.json")
expected='{"items":[5,10]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Prepend array to array of arrays
echo -n "Test 14: Prepend array to array of arrays... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg value '[0,0]' "$SCRIPT_DIR/test-input-11.json")
expected='{"items":[[0,0],[1,2],[3,4]]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All array-prepend tests passed!"
