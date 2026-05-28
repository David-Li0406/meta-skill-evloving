#!/usr/bin/env bash
set -euo pipefail

# Test pipe transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing pipe transformation..."

# Test 1: Pipe two set transformations
echo -n "Test 1: Pipe two set transformations... "
result=$(jq -c -f "$TRANSFORM" --argjson steps '[{"op":"set","path":"user.age","value":30},{"op":"set","path":"user.active","value":true}]' "$SCRIPT_DIR/test-input-1.json")
expected='{"user":{"name":"alice","age":30,"active":true}}'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 2: Pipe three transformations (set, set, delete)
echo -n "Test 2: Pipe three transformations... "
result=$(jq -c -f "$TRANSFORM" --argjson steps '[{"op":"set","path":"data.y","value":2},{"op":"set","path":"data.z","value":3},{"op":"delete","path":"data.x"}]' "$SCRIPT_DIR/test-input-3.json")
expected='{"data":{"y":2,"z":3}}'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 3: Single transformation (pass through style)
echo -n "Test 3: Single transformation... "
result=$(jq -c -f "$TRANSFORM" --argjson steps '[{"op":"set","path":"new","value":"field"}]' "$SCRIPT_DIR/test-input-4.json")
expected='{"existing":"value","new":"field"}'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 4: Empty pipe (return input unchanged)
echo -n "Test 4: Empty pipe returns input unchanged... "
result=$(jq -c -f "$TRANSFORM" --argjson steps '[]' "$SCRIPT_DIR/test-input-8.json")
expected='{"test":"data"}'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 5: Order matters (set then delete vs delete then set)
echo -n "Test 5: Order matters (set then delete)... "
result=$(jq -c -f "$TRANSFORM" --argjson steps '[{"op":"set","path":"x","value":999},{"op":"delete","path":"x"}]' "$SCRIPT_DIR/test-input-9.json")
expected='{}'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 6: Order matters reverse (delete then set)
echo -n "Test 6: Order matters (delete then set)... "
result=$(jq -c -f "$TRANSFORM" --argjson steps '[{"op":"delete","path":"val"},{"op":"set","path":"val","value":"new"}]' "$SCRIPT_DIR/test-input-10.json")
expected='{"val":"new"}'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 7: Each step modifies result (cumulative)
echo -n "Test 7: Each step modifies result cumulatively... "
result=$(jq -c -f "$TRANSFORM" --argjson steps '[{"op":"set","path":"a","value":10},{"op":"set","path":"b","value":20},{"op":"set","path":"c","value":30}]' "$SCRIPT_DIR/test-input-2.json")
expected='{"a":10,"b":20,"c":30}'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 8: Invalid step (missing op) - gracefully skip
echo -n "Test 8: Invalid step (missing op) gracefully skipped... "
result=$(jq -c -f "$TRANSFORM" --argjson steps '[{"path":"ignored"},{"op":"set","path":"added","value":"ok"}]' "$SCRIPT_DIR/test-input-8.json")
expected='{"test":"data","added":"ok"}'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 9: Invalid step (missing path) - gracefully skip
echo -n "Test 9: Invalid step (missing path) gracefully skipped... "
result=$(jq -c -f "$TRANSFORM" --argjson steps '[{"op":"set","value":"ignored"},{"op":"set","path":"valid","value":"data"}]' "$SCRIPT_DIR/test-input-8.json")
expected='{"test":"data","valid":"data"}'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 10: Complex chaining with nested paths
echo -n "Test 10: Complex chaining with nested paths... "
result=$(jq -c -f "$TRANSFORM" --argjson steps '[{"op":"set","path":"a.b.c","value":"deep"},{"op":"set","path":"a.b.d","value":"also"},{"op":"delete","path":"a.b.c"}]' "$SCRIPT_DIR/test-input-2.json")
expected='{"a":{"b":{"d":"also"}}}'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 11: Type changes through pipeline (falsy values)
echo -n "Test 11: Setting falsy values (null, false, 0)... "
result=$(jq -c -f "$TRANSFORM" --argjson steps '[{"op":"set","path":"counter","value":100},{"op":"set","path":"flag","value":"yes"},{"op":"set","path":"name","value":"bob"}]' "$SCRIPT_DIR/test-input-6.json")
expected='{"counter":100,"flag":"yes","name":"bob"}'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 12: Delete multiple fields in sequence
echo -n "Test 12: Delete multiple fields in sequence... "
result=$(jq -c -f "$TRANSFORM" --argjson steps '[{"op":"delete","path":"a"},{"op":"delete","path":"b"}]' "$SCRIPT_DIR/test-input-11.json")
expected='{}'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 13: Non-array steps argument (returns input unchanged)
echo -n "Test 13: Non-array steps returns input unchanged... "
result=$(jq -c -f "$TRANSFORM" --argjson steps '{"not":"array"}' "$SCRIPT_DIR/test-input-8.json")
expected='{"test":"data"}'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 14: Setting array and object values
echo -n "Test 14: Setting array and object values... "
result=$(jq -c -f "$TRANSFORM" --argjson steps '[{"op":"set","path":"arr","value":[1,2,3]},{"op":"set","path":"obj","value":{"nested":"val"}}]' "$SCRIPT_DIR/test-input-2.json")
expected='{"arr":[1,2,3],"obj":{"nested":"val"}}'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 15: Preserving existing nested structures while modifying
echo -n "Test 15: Preserve existing nested structure... "
result=$(jq -c -f "$TRANSFORM" --argjson steps '[{"op":"set","path":"a.b.e","value":"new"},{"op":"delete","path":"a.b.c"}]' "$SCRIPT_DIR/test-input-5.json")
expected='{"a":{"b":{"e":"new"}}}'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

echo "All pipe tests passed!"
