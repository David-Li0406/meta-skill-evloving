#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing array-chunk transformation..."

# Test 1: Chunk array evenly (size divides length)
echo -n "Test 1: Chunk array evenly... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg size "2" "$SCRIPT_DIR/test-input-1.json")
expected='{"items":[[1,2],[3,4],[5,6]]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 2: Chunk with remainder (last chunk smaller)
echo -n "Test 2: Chunk with remainder... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg size "2" "$SCRIPT_DIR/test-input-2.json")
expected='{"items":[[1,2],[3,4],[5]]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 3: Chunk size 1 (each element separate)
echo -n "Test 3: Chunk size 1... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg size "1" "$SCRIPT_DIR/test-input-3.json")
expected='{"items":[["a"],["b"],["c"]]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 4: Chunk size larger than array
echo -n "Test 4: Chunk size larger than array... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg size "10" "$SCRIPT_DIR/test-input-4.json")
expected='{"items":[[1,2]]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 5: Empty array
echo -n "Test 5: Empty array... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg size "3" "$SCRIPT_DIR/test-input-5.json")
expected='{"items":[]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 6: Array path doesn't exist
echo -n "Test 6: Array path doesn't exist... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "missing" --arg size "3" "$SCRIPT_DIR/test-input-6.json")
expected='{"other":"data"}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 7: Array field is not an array
echo -n "Test 7: Array field is not an array... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg size "3" "$SCRIPT_DIR/test-input-7.json")
expected='{"items":"not-an-array"}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 8: Size is 0 (handle gracefully)
echo -n "Test 8: Size is 0 returns original... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg size "0" "$SCRIPT_DIR/test-input-1.json")
expected='{"items":[1,2,3,4,5,6]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 9: Size is negative (handle gracefully)
echo -n "Test 9: Size is negative returns original... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg size "-5" "$SCRIPT_DIR/test-input-1.json")
expected='{"items":[1,2,3,4,5,6]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 10: Array contains null, false, 0 (preserve values)
echo -n "Test 10: Array contains falsy values... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg size "2" "$SCRIPT_DIR/test-input-8.json")
expected='{"items":[[null,false],[0,""],[true]]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 11: Nested path
echo -n "Test 11: Nested path... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "data.items" --arg size "3" "$SCRIPT_DIR/test-input-9.json")
expected='{"data":{"items":[[1,2,3],[4,5,6],[7]]}}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 12: Chunk array of objects
echo -n "Test 12: Chunk array of objects... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg size "2" "$SCRIPT_DIR/test-input-10.json")
expected='{"items":[[{"id":1},{"id":2}],[{"id":3}]]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 13: Single element array
echo -n "Test 13: Single element array... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg size "5" "$SCRIPT_DIR/test-input-11.json")
expected='{"items":[[42]]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

echo "All array-chunk tests passed!"
