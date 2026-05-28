#!/usr/bin/env bash
set -euo pipefail

# Test generate-stats transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing generate-stats transformation..."

# Test 1: Basic stats for number array
echo -n "Test 1: Basic stats for number array... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "scores" "$SCRIPT_DIR/test-input-1.json")
expected='{"min":10,"max":50,"avg":30,"sum":150,"count":5}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Extract field from objects
echo -n "Test 2: Extract field from objects... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "orders" --arg field "total" "$SCRIPT_DIR/test-input-2.json")
expected='{"min":100,"max":200,"avg":150,"sum":450,"count":3}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Empty array (null stats with count 0)
echo -n "Test 3: Empty array (null stats with count 0)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" "$SCRIPT_DIR/test-input-3.json")
expected='{"min":null,"max":null,"avg":null,"sum":null,"count":0}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Single element
echo -n "Test 4: Single element... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "values" "$SCRIPT_DIR/test-input-4.json")
expected='{"min":42,"max":42,"avg":42,"sum":42,"count":1}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: All same value
echo -n "Test 5: All same value... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "data" "$SCRIPT_DIR/test-input-5.json")
expected='{"min":5,"max":5,"avg":5,"sum":20,"count":4}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Negative numbers
echo -n "Test 6: Negative numbers... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "temps" "$SCRIPT_DIR/test-input-6.json")
expected='{"min":-10,"max":10,"avg":0,"sum":0,"count":5}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Decimal numbers
echo -n "Test 7: Decimal numbers... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "prices" "$SCRIPT_DIR/test-input-7.json")
expected='{"min":1.5,"max":4.5,"avg":3,"sum":12,"count":4}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Mixed with nulls (skip nulls)
echo -n "Test 8: Mixed with nulls (skip nulls)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "data" "$SCRIPT_DIR/test-input-8.json")
expected='{"min":10,"max":30,"avg":20,"sum":60,"count":3}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Non-numeric values (skip them)
echo -n "Test 9: Non-numeric values (skip them)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "mixed" "$SCRIPT_DIR/test-input-9.json")
expected='{"min":0,"max":30,"avg":15,"sum":60,"count":4}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Nested array path
echo -n "Test 10: Nested array path... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "nested.data.values" "$SCRIPT_DIR/test-input-10.json")
expected='{"min":5,"max":25,"avg":15,"sum":45,"count":3}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Non-array field (returns null)
echo -n "Test 11: Non-array field (returns null)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "not_an_array" "$SCRIPT_DIR/test-input-11.json")
expected='null'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Non-existent path (returns null)
echo -n "Test 12: Non-existent path (returns null)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "missing.path" "$SCRIPT_DIR/test-input-12.json")
expected='null'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: All non-numeric values (returns null stats with count 0)
echo -n "Test 13: All non-numeric values (returns null stats with count 0)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "all_non_numeric" "$SCRIPT_DIR/test-input-13.json")
expected='{"min":null,"max":null,"avg":null,"sum":null,"count":0}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Extract nested field from objects
echo -n "Test 14: Extract nested field from objects... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "products" --arg field "price" "$SCRIPT_DIR/test-input-14.json")
expected='{"min":10.5,"max":20.0,"avg":15.416666666666666,"sum":46.25,"count":3}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All generate-stats tests passed!"
