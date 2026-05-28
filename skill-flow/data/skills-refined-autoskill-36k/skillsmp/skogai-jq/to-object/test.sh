#!/usr/bin/env bash
set -euo pipefail

# Test to-object transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing to-object transformation..."

# Test 1: Object value (pass through)
echo -n "Test 1: Object value (pass through)... "
result=$(jq -c -f "$TRANSFORM" --arg path "user" "$SCRIPT_DIR/test-input-1.json")
expected='{"user":{"name":"skogix","age":30}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Array of [key, value] pairs (convert to object)
echo -n "Test 2: Array of [key, value] pairs (convert to object)... "
result=$(jq -c -f "$TRANSFORM" --arg path "data" "$SCRIPT_DIR/test-input-2.json")
expected='{"data":{"name":"skogix","age":"30","active":"true"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Array of {key, value} objects (convert to object)
echo -n "Test 3: Array of {key, value} objects (convert to object)... "
result=$(jq -c -f "$TRANSFORM" --arg path "data" "$SCRIPT_DIR/test-input-3.json")
expected='{"data":{"name":"skogix","age":30,"active":true}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: String value (convert to empty object)
echo -n "Test 4: String value (convert to empty object)... "
result=$(jq -c -f "$TRANSFORM" --arg path "name" "$SCRIPT_DIR/test-input-4.json")
expected='{"name":{}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Null value (convert to empty object)
echo -n "Test 5: Null value (convert to empty object)... "
result=$(jq -c -f "$TRANSFORM" --arg path "value" "$SCRIPT_DIR/test-input-5.json")
expected='{"value":{}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Number value (convert to empty object)
echo -n "Test 6: Number value (convert to empty object)... "
result=$(jq -c -f "$TRANSFORM" --arg path "count" "$SCRIPT_DIR/test-input-6.json")
expected='{"count":{}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Boolean false (convert to empty object, preserve falsy value)
echo -n "Test 7: Boolean false (convert to empty object)... "
result=$(jq -c -f "$TRANSFORM" --arg path "active" "$SCRIPT_DIR/test-input-7.json")
expected='{"active":{}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Empty array (convert to empty object)
echo -n "Test 8: Empty array (convert to empty object)... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" "$SCRIPT_DIR/test-input-8.json")
expected='{"items":{}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Empty object (pass through)
echo -n "Test 9: Empty object (pass through)... "
result=$(jq -c -f "$TRANSFORM" --arg path "obj" "$SCRIPT_DIR/test-input-9.json")
expected='{"obj":{}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Nested path with object
echo -n "Test 10: Nested path with object... "
result=$(jq -c -f "$TRANSFORM" --arg path "data.nested.user" "$SCRIPT_DIR/test-input-10.json")
expected='{"data":{"nested":{"user":{"name":"test","age":25}}}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Number zero (convert to empty object, preserve falsy value)
echo -n "Test 11: Number zero (convert to empty object)... "
result=$(jq -c -f "$TRANSFORM" --arg path "zero" "$SCRIPT_DIR/test-input-11.json")
expected='{"zero":{}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Empty string (convert to empty object, preserve falsy value)
echo -n "Test 12: Empty string (convert to empty object)... "
result=$(jq -c -f "$TRANSFORM" --arg path "empty" "$SCRIPT_DIR/test-input-12.json")
expected='{"empty":{}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Boolean true (convert to empty object)
echo -n "Test 13: Boolean true (convert to empty object)... "
result=$(jq -c -f "$TRANSFORM" --arg path "bool" "$SCRIPT_DIR/test-input-13.json")
expected='{"bool":{}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Array of mixed types (not key-value pairs, convert to empty object)
echo -n "Test 14: Array of mixed types (convert to empty object)... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" "$SCRIPT_DIR/test-input-14.json")
expected='{"items":{}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 15: Array with single [key, value] pair
echo -n "Test 15: Array with single [key, value] pair... "
result=$(jq -c -f "$TRANSFORM" --arg path "data" "$SCRIPT_DIR/test-input-15.json")
expected='{"data":{"single":"value"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 16: Array of {key, value} with null value
echo -n "Test 16: Array of {key, value} with null value... "
result=$(jq -c -f "$TRANSFORM" --arg path "data" "$SCRIPT_DIR/test-input-16.json")
expected='{"data":{"name":"test","value":null}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 17: Array of {key, value} with false value
echo -n "Test 17: Array of {key, value} with false value... "
result=$(jq -c -f "$TRANSFORM" --arg path "data" "$SCRIPT_DIR/test-input-17.json")
expected='{"data":{"active":false,"enabled":true}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 18: Array of {key, value} with zero value
echo -n "Test 18: Array of {key, value} with zero value... "
result=$(jq -c -f "$TRANSFORM" --arg path "data" "$SCRIPT_DIR/test-input-18.json")
expected='{"data":{"count":0,"total":100}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All to-object tests passed!"
