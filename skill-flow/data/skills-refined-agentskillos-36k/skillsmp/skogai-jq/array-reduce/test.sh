#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing array-reduce transformation..."

# Test 1: Sum
echo -n "Test 1: Sum array of numbers... "
result=$(jq -c -f "$TRANSFORM" --arg path "nums" --arg operation "sum" "$SCRIPT_DIR/test-input-1.json")
expected='15'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 2: Product
echo -n "Test 2: Product of numbers... "
result=$(jq -c -f "$TRANSFORM" --arg path "nums" --arg operation "product" "$SCRIPT_DIR/test-input-2.json")
expected='24'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 3: Concat
echo -n "Test 3: Concatenate strings... "
result=$(jq -c -f "$TRANSFORM" --arg path "words" --arg operation "concat" "$SCRIPT_DIR/test-input-3.json")
expected='"hello world"'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 4: Min
echo -n "Test 4: Find minimum... "
result=$(jq -c -f "$TRANSFORM" --arg path "nums" --arg operation "min" "$SCRIPT_DIR/test-input-4.json")
expected='1'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 5: Max
echo -n "Test 5: Find maximum... "
result=$(jq -c -f "$TRANSFORM" --arg path "nums" --arg operation "max" "$SCRIPT_DIR/test-input-4.json")
expected='9'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 6: Count
echo -n "Test 6: Count elements... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" --arg operation "count" "$SCRIPT_DIR/test-input-5.json")
expected='3'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 7: Sum with field extraction
echo -n "Test 7: Sum field from array of objects... "
result=$(jq -c -f "$TRANSFORM" --arg path "orders" --arg operation "sum" --arg field "total" "$SCRIPT_DIR/test-input-6.json")
expected='60'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 8: Empty array (sum)
echo -n "Test 8: Sum of empty array returns null... "
result=$(jq -c -f "$TRANSFORM" --arg path "nums" --arg operation "sum" "$SCRIPT_DIR/test-input-7.json")
expected='null'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 9: Empty array (concat)
echo -n "Test 9: Concat of empty array returns empty string... "
result=$(jq -c -f "$TRANSFORM" --arg path "nums" --arg operation "concat" "$SCRIPT_DIR/test-input-7.json")
expected='""'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 10: Non-array field
echo -n "Test 10: Non-array field returns null... "
result=$(jq -c -f "$TRANSFORM" --arg path "nums" --arg operation "sum" "$SCRIPT_DIR/test-input-8.json")
expected='null'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 11: Zero values (not same as missing)
echo -n "Test 11: Sum with zero values... "
result=$(jq -c -f "$TRANSFORM" --arg path "nums" --arg operation "sum" "$SCRIPT_DIR/test-input-9.json")
expected='3'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 12: Missing path
echo -n "Test 12: Missing path returns null... "
result=$(jq -c -f "$TRANSFORM" --arg path "nums" --arg operation "sum" "$SCRIPT_DIR/test-input-10.json")
expected='null'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

echo "All array-reduce tests passed!"
