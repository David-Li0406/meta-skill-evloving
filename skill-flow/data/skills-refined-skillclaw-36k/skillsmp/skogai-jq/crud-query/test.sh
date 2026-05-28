#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing crud-query transformation..."

# Test 1: Filter by string value
echo -n "Test 1: Filter users by status... "
result=$(jq -c -f "$TRANSFORM" --arg path "users" --arg field "status" --arg value '"active"' "$SCRIPT_DIR/test-input-1.json")
expected='[{"name":"alice","status":"active"},{"name":"charlie","status":"active"}]'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 2: Filter by boolean true
echo -n "Test 2: Filter by boolean true... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" --arg field "enabled" --arg value 'true' "$SCRIPT_DIR/test-input-2.json")
expected='[{"id":1,"enabled":true},{"id":3,"enabled":true}]'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 3: Filter by boolean false
echo -n "Test 3: Filter by boolean false... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" --arg field "enabled" --arg value 'false' "$SCRIPT_DIR/test-input-2.json")
expected='[{"id":2,"enabled":false}]'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 4: Filter by number
echo -n "Test 4: Filter by number... "
result=$(jq -c -f "$TRANSFORM" --arg path "scores" --arg field "score" --arg value '100' "$SCRIPT_DIR/test-input-3.json")
expected='[{"player":"alice","score":100},{"player":"charlie","score":100}]'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 5: Filter by null value
echo -n "Test 5: Filter by null value... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" --arg field "val" --arg value 'null' "$SCRIPT_DIR/test-input-4.json")
expected='[{"val":null},{"val":null}]'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 6: Filter by false value
echo -n "Test 6: Filter by false value... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" --arg field "val" --arg value 'false' "$SCRIPT_DIR/test-input-5.json")
expected='[{"val":false},{"val":false}]'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 7: Filter by zero value
echo -n "Test 7: Filter by zero value... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" --arg field "val" --arg value '0' "$SCRIPT_DIR/test-input-6.json")
expected='[{"val":0},{"val":0}]'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 8: Empty array returns empty array
echo -n "Test 8: Empty array... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" --arg field "val" --arg value '"test"' "$SCRIPT_DIR/test-input-7.json")
expected='[]'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 9: Non-array field returns null
echo -n "Test 9: Non-array field returns null... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" --arg field "val" --arg value '"test"' "$SCRIPT_DIR/test-input-8.json")
expected='null'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 10: Missing path returns null
echo -n "Test 10: Missing path returns null... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" --arg field "x" --arg value '1' "$SCRIPT_DIR/test-input-9.json")
expected='null'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

echo "All crud-query tests passed!"
