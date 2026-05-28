#!/usr/bin/env bash
set -euo pipefail

# Test deduplicate-by-content transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing deduplicate-by-content transformation..."

# Test 1: Remove exact duplicates
echo -n "Test 1: Remove exact duplicates... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-1.json")
expected='{"items":[{"id":1,"name":"alice"},{"id":2,"name":"bob"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Keep objects with different field order (same content)
echo -n "Test 2: Objects with different field order are treated as duplicates... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-2.json")
expected='{"items":[{"id":1,"name":"alice"},{"id":2,"name":"bob"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Empty array
echo -n "Test 3: Handle empty array... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-3.json")
expected='{"items":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Single element
echo -n "Test 4: Handle single element... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-4.json")
expected='{"items":[{"x":1}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: No duplicates (returns unchanged)
echo -n "Test 5: No duplicates returns unchanged... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-5.json")
expected='{"items":[{"x":1},{"x":2},{"x":3}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: All duplicates (returns single element)
echo -n "Test 6: All duplicates returns single element... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-6.json")
expected='{"items":[{"x":1}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Duplicates with null values
echo -n "Test 7: Handle duplicates with null values... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-7.json")
expected='{"items":[{"val":null},{"val":"test"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Duplicates with false values
echo -n "Test 8: Handle duplicates with false values... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-8.json")
expected='{"items":[{"active":false},{"active":true}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Duplicates with zero values
echo -n "Test 9: Handle duplicates with zero values... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-9.json")
expected='{"items":[{"count":0},{"count":1}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Nested objects with different field order
echo -n "Test 10: Handle nested objects with different field order... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-10.json")
expected='{"items":[{"user":{"name":"bob","age":25}},{"user":{"name":"alice","age":30}}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Array field doesn't exist
echo -n "Test 11: Handle missing array field gracefully... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-11.json")
expected='{"other":[1,2,3]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Non-array field (type safety)
echo -n "Test 12: Handle non-array field gracefully... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-12.json")
expected='{"items":"not-an-array"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Custom array field name
echo -n "Test 13: Use custom array field name... "
result=$(jq -c -f "$TRANSFORM" --arg array "users" "$SCRIPT_DIR/test-input-13.json")
expected='{"users":[{"b":2,"a":1},{"c":3}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Array values (order matters for arrays)
echo -n "Test 14: Array values where order matters... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-14.json")
expected='{"items":[{"arr":[1,2]},{"arr":[2,1]}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All deduplicate-by-content tests passed!"
