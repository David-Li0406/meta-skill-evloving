#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing sort-by-field transformation..."

# Test 1: Sort strings ascending (default order)
echo -n "Test 1: Sort strings ascending (default)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "users" --arg field_name "name" "$SCRIPT_DIR/test-input-1.json")
expected='{"users":[{"name":"alice"},{"name":"bob"},{"name":"charlie"}]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 2: Sort strings descending
echo -n "Test 2: Sort strings descending... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "users" --arg field_name "name" --arg order "desc" "$SCRIPT_DIR/test-input-2.json")
expected='{"users":[{"name":"charlie"},{"name":"bob"},{"name":"alice"}]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 3: Sort numbers ascending
echo -n "Test 3: Sort numbers ascending... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "age" "$SCRIPT_DIR/test-input-3.json")
expected='{"items":[{"age":20},{"age":25},{"age":30},{"age":35}]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 4: Sort numbers descending
echo -n "Test 4: Sort numbers descending... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "age" --arg order "desc" "$SCRIPT_DIR/test-input-4.json")
expected='{"items":[{"age":35},{"age":30},{"age":25},{"age":20}]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 5: Sort booleans (false < true)
echo -n "Test 5: Sort booleans ascending... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "flags" --arg field_name "active" "$SCRIPT_DIR/test-input-5.json")
expected='{"flags":[{"active":false},{"active":false},{"active":true},{"active":true}]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 6: Empty array returns unchanged
echo -n "Test 6: Empty array returns unchanged... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "name" "$SCRIPT_DIR/test-input-6.json")
expected='{"items":[]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 7: Single element returns unchanged
echo -n "Test 7: Single element returns unchanged... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "value" "$SCRIPT_DIR/test-input-7.json")
expected='{"items":[{"value":42}]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 8: Missing field in some objects (nulls first in ascending)
echo -n "Test 8: Missing fields sort first (ascending)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "users" --arg field_name "name" "$SCRIPT_DIR/test-input-8.json")
expected='{"users":[{"other":"x"},{"name":null},{"name":"alice"},{"name":"bob"}]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 9: Missing field in some objects (nulls last in descending)
echo -n "Test 9: Missing fields sort last (descending)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "users" --arg field_name "name" --arg order "desc" "$SCRIPT_DIR/test-input-9.json")
expected='{"users":[{"name":"bob"},{"name":"alice"},{"name":null},{"other":"x"}]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 10: Nested field path (dot-separated)
echo -n "Test 10: Sort by nested field path... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "data.results" --arg field_name "profile.score" --arg order "desc" "$SCRIPT_DIR/test-input-10.json")
expected='{"data":{"results":[{"profile":{"score":90}},{"profile":{"score":85}},{"profile":{"score":75}}]}}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 11: Mixed types (stable sorting - maintains order for equal values)
echo -n "Test 11: Mixed types stable sort... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "value" "$SCRIPT_DIR/test-input-11.json")
expected='{"items":[{"type":"b","value":1},{"type":"a","value":2},{"type":"a","value":3}]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 12: Non-array field returns original object
echo -n "Test 12: Non-array field returns original... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "name" "$SCRIPT_DIR/test-input-12.json")
expected='{"items":"not-an-array"}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 13: Missing array path returns original object
echo -n "Test 13: Missing array path returns original... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "name" "$SCRIPT_DIR/test-input-13.json")
expected='{"other":"data"}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 14: Sort with zero values (0 is not null/missing)
echo -n "Test 14: Sort with zero values... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "val" "$SCRIPT_DIR/test-input-14.json")
expected='{"items":[{"val":-5},{"val":0},{"val":0},{"val":1}]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 15: Sort with empty strings (empty string is not null/missing)
echo -n "Test 15: Sort with empty strings... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "name" "$SCRIPT_DIR/test-input-15.json")
expected='{"items":[{"name":""},{"name":""},{"name":"alice"}]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

echo "All sort-by-field tests passed!"
