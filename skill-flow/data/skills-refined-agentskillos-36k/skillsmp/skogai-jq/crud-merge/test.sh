#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing crud-merge transformation..."

# Test 1: Basic nested merge
echo -n "Test 1: Merge nested objects... "
result=$(jq -cS -f "$TRANSFORM" --arg source_path "source" --arg target_path "target" "$SCRIPT_DIR/test-input-1.json")
expected='{"source":{"a":1,"b":{"c":2}},"target":{"a":1,"b":{"c":2,"d":3},"e":4}}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 2: Conflicting keys (source wins)
echo -n "Test 2: Conflicting keys (source wins)... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "source" --arg target_path "target" "$SCRIPT_DIR/test-input-2.json")
expected='{"source":{"x":"new"},"target":{"x":"new","y":"kept"}}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 3: Deep nesting (3 levels)
echo -n "Test 3: Deep nesting merge... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "source" --arg target_path "target" "$SCRIPT_DIR/test-input-3.json")
expected='{"source":{"a":{"b":{"c":1}}},"target":{"a":{"b":{"c":1,"d":2}}}}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 4: Empty source
echo -n "Test 4: Empty source object... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "source" --arg target_path "target" "$SCRIPT_DIR/test-input-4.json")
expected='{"source":{},"target":{"x":1}}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 5: Empty target
echo -n "Test 5: Empty target object... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "source" --arg target_path "target" "$SCRIPT_DIR/test-input-5.json")
expected='{"source":{"x":1},"target":{"x":1}}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 6: Missing source (no-op)
echo -n "Test 6: Missing source path (no-op)... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "source" --arg target_path "target" "$SCRIPT_DIR/test-input-6.json")
expected='{"target":{"x":1}}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 7: Missing target (create)
echo -n "Test 7: Missing target path (create)... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "source" --arg target_path "target" "$SCRIPT_DIR/test-input-7.json")
expected='{"source":{"x":1},"target":{"x":1}}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 8: Merge with null value
echo -n "Test 8: Merge with null value... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "source" --arg target_path "target" "$SCRIPT_DIR/test-input-8.json")
expected='{"source":{"x":null},"target":{"x":null,"y":2}}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 9: Merge with false value
echo -n "Test 9: Merge with false value... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "source" --arg target_path "target" "$SCRIPT_DIR/test-input-9.json")
expected='{"source":{"x":false},"target":{"x":false,"y":2}}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

# Test 10: Merge with zero value
echo -n "Test 10: Merge with zero value... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "source" --arg target_path "target" "$SCRIPT_DIR/test-input-10.json")
expected='{"source":{"x":0},"target":{"x":0,"y":2}}'
[[ "$result" == "$expected" ]] && echo "PASS" || { echo "FAIL (expected: $expected, got: $result)"; exit 1; }

echo "All crud-merge tests passed!"
