#!/usr/bin/env bash
set -euo pipefail

# Test to-array transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing to-array transformation..."

# Test 1: Array value (pass through)
echo -n "Test 1: Array value (pass through)... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" "$SCRIPT_DIR/test-input-1.json")
expected='{"items":[1,2,3]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: String value (wrap in array)
echo -n "Test 2: String value (wrap in array)... "
result=$(jq -c -f "$TRANSFORM" --arg path "name" "$SCRIPT_DIR/test-input-2.json")
expected='{"name":["skogix"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Number value (wrap in array)
echo -n "Test 3: Number value (wrap in array)... "
result=$(jq -c -f "$TRANSFORM" --arg path "count" "$SCRIPT_DIR/test-input-3.json")
expected='{"count":[42]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Boolean false (wrap in array)
echo -n "Test 4: Boolean false (wrap in array)... "
result=$(jq -c -f "$TRANSFORM" --arg path "active" "$SCRIPT_DIR/test-input-4.json")
expected='{"active":[false]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Null value (wrap in array)
echo -n "Test 5: Null value (wrap in array)... "
result=$(jq -c -f "$TRANSFORM" --arg path "value" "$SCRIPT_DIR/test-input-5.json")
expected='{"value":[null]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Object value (wrap in array)
echo -n "Test 6: Object value (wrap in array)... "
result=$(jq -c -f "$TRANSFORM" --arg path "user" "$SCRIPT_DIR/test-input-6.json")
expected='{"user":[{"name":"test","age":30}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Empty array (pass through)
echo -n "Test 7: Empty array (pass through)... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" "$SCRIPT_DIR/test-input-7.json")
expected='{"items":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Nested path
echo -n "Test 8: Nested path... "
result=$(jq -c -f "$TRANSFORM" --arg path "data.nested.items" "$SCRIPT_DIR/test-input-8.json")
expected='{"data":{"nested":{"items":["value"]}}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Field doesn't exist (create array with null)
echo -n "Test 9: Field doesn't exist (create array with null)... "
result=$(jq -c -f "$TRANSFORM" --arg path "missing" "$SCRIPT_DIR/test-input-9.json")
expected='{"other":"field","missing":[null]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Array with multiple elements (pass through)
echo -n "Test 10: Array with multiple elements (pass through)... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" "$SCRIPT_DIR/test-input-10.json")
expected='{"items":["a","b","c"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Number zero (wrap in array, preserve falsy value)
echo -n "Test 11: Number zero (wrap in array)... "
result=$(jq -c -f "$TRANSFORM" --arg path "zero" "$SCRIPT_DIR/test-input-11.json")
expected='{"zero":[0]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Empty string (wrap in array, preserve falsy value)
echo -n "Test 12: Empty string (wrap in array)... "
result=$(jq -c -f "$TRANSFORM" --arg path "empty" "$SCRIPT_DIR/test-input-12.json")
expected='{"empty":[""]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Boolean true (wrap in array)
echo -n "Test 13: Boolean true (wrap in array)... "
result=$(jq -c -f "$TRANSFORM" --arg path "bool" "$SCRIPT_DIR/test-input-13.json")
expected='{"bool":[true]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Empty object (wrap in array)
echo -n "Test 14: Empty object (wrap in array)... "
result=$(jq -c -f "$TRANSFORM" --arg path "obj" "$SCRIPT_DIR/test-input-14.json")
expected='{"obj":[{}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All to-array tests passed!"
