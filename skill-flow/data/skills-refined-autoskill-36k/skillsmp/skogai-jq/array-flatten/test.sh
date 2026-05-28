#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing array-flatten transformation..."

# Test 1: Flatten one level (default)
echo -n "Test 1: Flatten one level... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" "$SCRIPT_DIR/test-input-1.json")
expected='{"items":[1,2,3,4,5]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 2: Flatten completely (depth -1)
echo -n "Test 2: Flatten completely... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" --arg depth "-1" "$SCRIPT_DIR/test-input-2.json")
expected='{"items":[1,2,3,4,5]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 3: Flatten two levels
echo -n "Test 3: Flatten two levels... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" --arg depth "2" "$SCRIPT_DIR/test-input-3.json")
expected='{"items":[1,2,3]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 4: Mixed arrays and primitives
echo -n "Test 4: Mixed arrays and primitives... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" "$SCRIPT_DIR/test-input-4.json")
expected='{"items":[1,2,3,4,5,[6,7]]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 5: Empty array
echo -n "Test 5: Empty array... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" "$SCRIPT_DIR/test-input-5.json")
expected='{"items":[]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 6: Non-array field (type safety)
echo -n "Test 6: Non-array field returns original... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" "$SCRIPT_DIR/test-input-6.json")
expected='{"items":"not-an-array"}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 7: Empty nested arrays (depth 1)
echo -n "Test 7: Empty nested arrays depth 1... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" "$SCRIPT_DIR/test-input-7.json")
expected='{"items":[[],[]]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 8: Missing path
echo -n "Test 8: Missing path returns original... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" "$SCRIPT_DIR/test-input-8.json")
expected='{"other":[[1,2]]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 9: Flatten completely with mixed depth
echo -n "Test 9: Complete flatten of mixed depth... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" --arg depth "-1" "$SCRIPT_DIR/test-input-4.json")
expected='{"items":[1,2,3,4,5,6,7]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 10: Depth of 0 (no flatten)
echo -n "Test 10: Depth 0 returns original... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" --arg depth "0" "$SCRIPT_DIR/test-input-1.json")
expected='{"items":[[1,2],[3,4],[5]]}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

echo "All array-flatten tests passed!"
