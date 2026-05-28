#!/usr/bin/env bash
set -euo pipefail

# Test try-transform transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing try-transform transformation..."

# Test 1: Transform succeeds - return result (identity)
echo -n "Test 1: Transform succeeds (identity)... "
result=$(jq -c -f "$TRANSFORM" --arg transform_expr "identity" --arg fallback "null" "$SCRIPT_DIR/test-input-1.json")
expected='{"name":"alice","age":30}'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 2: Transform succeeds - get nested field
echo -n "Test 2: Transform succeeds (getpath)... "
result=$(jq -f "$TRANSFORM" --arg transform_expr "getpath:user.name" --arg fallback "null" "$SCRIPT_DIR/test-input-2.json")
expected='"alice"'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 3: Transform fails - missing nested path, use fallback
echo -n "Test 3: Transform fails on missing path... "
result=$(jq -f "$TRANSFORM" --arg transform_expr "getpath:user.profile.bio" --arg fallback '"unknown"' "$SCRIPT_DIR/test-input-3.json")
expected='"unknown"'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 4: Division by zero - return fallback
echo -n "Test 4: Division by zero error... "
result=$(jq -f "$TRANSFORM" --arg transform_expr "divide:count:0" --arg fallback "null" "$SCRIPT_DIR/test-input-4.json")
expected='null'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 5: Invalid tonumber conversion
echo -n "Test 5: Invalid tonumber conversion... "
result=$(jq -f "$TRANSFORM" --arg transform_expr "tonumber:value" --arg fallback "-1" "$SCRIPT_DIR/test-input-5.json")
expected='-1'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 6: Array out-of-bounds access
echo -n "Test 6: Array out-of-bounds access... "
result=$(jq -f "$TRANSFORM" --arg transform_expr "array_access:items:10" --arg fallback "null" "$SCRIPT_DIR/test-input-6.json")
expected='null'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 7: Fallback is null
echo -n "Test 7: Fallback is null... "
result=$(jq -f "$TRANSFORM" --arg transform_expr "getpath:missing.field" --arg fallback "null" "$SCRIPT_DIR/test-input-7.json")
expected='null'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 8: Fallback is object
echo -n "Test 8: Fallback is custom object... "
result=$(jq -c -f "$TRANSFORM" --arg transform_expr "getpath:missing.data" --arg fallback '{"error":"not found"}' "$SCRIPT_DIR/test-input-8.json")
expected='{"error":"not found"}'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 9: Fallback is array
echo -n "Test 9: Fallback is empty array... "
result=$(jq -c -f "$TRANSFORM" --arg transform_expr "getpath:items.missing" --arg fallback "[]" "$SCRIPT_DIR/test-input-9.json")
expected='[]'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 10: Successful division (no error)
echo -n "Test 10: Successful division... "
result=$(jq -f "$TRANSFORM" --arg transform_expr "divide:count:2" --arg fallback "0" "$SCRIPT_DIR/test-input-10.json")
expected='5'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 11: Successful tonumber conversion
echo -n "Test 11: Successful tonumber... "
result=$(jq -f "$TRANSFORM" --arg transform_expr "tonumber:value" --arg fallback "0" "$SCRIPT_DIR/test-input-11.json")
expected='42'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 12: Successful array access
echo -n "Test 12: Successful array access... "
result=$(jq -f "$TRANSFORM" --arg transform_expr "array_access:items:1" --arg fallback "null" "$SCRIPT_DIR/test-input-12.json")
expected='"beta"'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 13: Invalid JSON parsing with fallback
echo -n "Test 13: Invalid JSON parsing... "
result=$(jq -c -f "$TRANSFORM" --arg transform_expr "fromjson:data" --arg fallback '{}' "$SCRIPT_DIR/test-input-13.json")
expected='{}'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 14: Valid JSON parsing succeeds
echo -n "Test 14: Valid JSON parsing... "
result=$(jq -c -f "$TRANSFORM" --arg transform_expr "fromjson:data" --arg fallback '{}' "$SCRIPT_DIR/test-input-14.json")
expected='{"parsed":true}'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 15: Nested field access with intermediate missing keys
echo -n "Test 15: Nested field with missing intermediate keys... "
result=$(jq -f "$TRANSFORM" --arg transform_expr "nested:a.b.c.d.e" --arg fallback '"default"' "$SCRIPT_DIR/test-input-15.json")
expected='"default"'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 16: Fallback is boolean false
echo -n "Test 16: Fallback is boolean false... "
result=$(jq -f "$TRANSFORM" --arg transform_expr "getpath:nonexistent" --arg fallback "false" "$SCRIPT_DIR/test-input-16.json")
expected='false'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 17: Fallback is number zero
echo -n "Test 17: Fallback is zero... "
result=$(jq -f "$TRANSFORM" --arg transform_expr "getpath:missing" --arg fallback "0" "$SCRIPT_DIR/test-input-17.json")
expected='0'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

# Test 18: Fallback is empty string
echo -n "Test 18: Fallback is empty string... "
result=$(jq -f "$TRANSFORM" --arg transform_expr "getpath:nowhere" --arg fallback '""' "$SCRIPT_DIR/test-input-18.json")
expected='""'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

echo "All try-transform tests passed!"
