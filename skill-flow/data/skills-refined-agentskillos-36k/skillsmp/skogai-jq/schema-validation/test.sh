#!/usr/bin/env bash
set -euo pipefail

# Test schema-validation transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing schema-validation transformation..."

# Test 1: Valid object passing all checks - happy path
echo -n "Test 1: Valid object passing all checks - happy path... "
result=$(jq -c -f "$TRANSFORM" --arg schema '{"required":["name","age"],"types":{"name":"string","age":"number"}}' "$SCRIPT_DIR/test-input-1.json")
expected='{"valid":true,"errors":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Nested field validation - happy path
echo -n "Test 2: Nested field validation - happy path... "
result=$(jq -c -f "$TRANSFORM" --arg schema '{"required":["user.name","user.profile.age"],"types":{"user.name":"string","user.profile.age":"number"}}' "$SCRIPT_DIR/test-input-5.json")
expected='{"valid":true,"errors":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: All JSON types validation - happy path
echo -n "Test 3: All JSON types validation - happy path... "
result=$(jq -c -f "$TRANSFORM" --arg schema '{"types":{"str":"string","num":"number","bool":"boolean","nil":"null","arr":"array","obj":"object"}}' "$SCRIPT_DIR/test-input-7.json")
expected='{"valid":true,"errors":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Field exists with null value (CRITICAL - falsy value)
echo -n "Test 4: Field exists with null value passes required check... "
result=$(jq -c -f "$TRANSFORM" --arg schema '{"required":["name"]}' "$SCRIPT_DIR/test-input-4.json")
expected='{"valid":true,"errors":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Boolean false is valid (CRITICAL - falsy value)
echo -n "Test 5: Boolean false is valid and passes type check... "
result=$(jq -c -f "$TRANSFORM" --arg schema '{"required":["enabled"],"types":{"enabled":"boolean"}}' "$SCRIPT_DIR/test-input-4.json")
expected='{"valid":true,"errors":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Number 0 is valid (CRITICAL - falsy value)
echo -n "Test 6: Number 0 is valid and passes type check... "
result=$(jq -c -f "$TRANSFORM" --arg schema '{"required":["count"],"types":{"count":"number"}}' "$SCRIPT_DIR/test-input-4.json")
expected='{"valid":true,"errors":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Empty string is valid (CRITICAL - falsy value)
echo -n "Test 7: Empty string is valid and passes type check... "
result=$(jq -c -f "$TRANSFORM" --arg schema '{"required":["description"],"types":{"description":"string"}}' "$SCRIPT_DIR/test-input-4.json")
expected='{"valid":true,"errors":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Empty array is valid (CRITICAL - falsy value)
echo -n "Test 8: Empty array is valid and passes type check... "
result=$(jq -c -f "$TRANSFORM" --arg schema '{"required":["items"],"types":{"items":"array"}}' "$SCRIPT_DIR/test-input-4.json")
expected='{"valid":true,"errors":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Empty object is valid (CRITICAL - falsy value)
echo -n "Test 9: Empty object is valid and passes type check... "
result=$(jq -c -f "$TRANSFORM" --arg schema '{"required":["metadata"],"types":{"metadata":"object"}}' "$SCRIPT_DIR/test-input-4.json")
expected='{"valid":true,"errors":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Missing required field (type safety)
echo -n "Test 10: Missing required field returns error... "
result=$(jq -c -f "$TRANSFORM" --arg schema '{"required":["email"]}' "$SCRIPT_DIR/test-input-2.json")
expected='{"valid":false,"errors":["Required field '\''email'\'' is missing"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Wrong type for field (type safety)
echo -n "Test 11: Wrong type for field returns error... "
result=$(jq -c -f "$TRANSFORM" --arg schema '{"types":{"name":"string"}}' "$SCRIPT_DIR/test-input-3.json")
expected='{"valid":false,"errors":["Field '\''name'\'' has type '\''number'\'', expected '\''string'\''"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Multiple validation errors (type safety)
echo -n "Test 12: Multiple validation errors combined... "
result=$(jq -c -f "$TRANSFORM" --arg schema '{"required":["email","phone"],"types":{"name":"string","age":"number"}}' "$SCRIPT_DIR/test-input-3.json")
# Should have 4 errors: 2 missing required fields + 2 wrong types
# Note: Using grep to check for valid:false and count errors
if echo "$result" | jq -e '.valid == false and (.errors | length) == 4' > /dev/null; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: 4 errors with valid=false"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Empty schema always passes (boundary condition)
echo -n "Test 13: Empty schema always passes... "
result=$(jq -c -f "$TRANSFORM" --arg schema '{}' "$SCRIPT_DIR/test-input-1.json")
expected='{"valid":true,"errors":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Empty object input with empty schema (boundary condition)
echo -n "Test 14: Empty object input with empty schema passes... "
result=$(jq -c -f "$TRANSFORM" --arg schema '{}' "$SCRIPT_DIR/test-input-6.json")
expected='{"valid":true,"errors":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 15: Empty object input fails required check (boundary condition)
echo -n "Test 15: Empty object input fails required field check... "
result=$(jq -c -f "$TRANSFORM" --arg schema '{"required":["name"]}' "$SCRIPT_DIR/test-input-6.json")
expected='{"valid":false,"errors":["Required field '\''name'\'' is missing"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 16: Nested missing field (type safety)
echo -n "Test 16: Nested missing field returns specific error... "
result=$(jq -c -f "$TRANSFORM" --arg schema '{"required":["user.profile.email"]}' "$SCRIPT_DIR/test-input-5.json")
expected='{"valid":false,"errors":["Required field '\''user.profile.email'\'' is missing"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 17: Null value vs null type (edge case)
echo -n "Test 17: Null value matches null type... "
result=$(jq -c -f "$TRANSFORM" --arg schema '{"types":{"value":"null"}}' "$SCRIPT_DIR/test-input-8.json")
expected='{"valid":true,"errors":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 18: Malformed schema JSON (error handling)
echo -n "Test 18: Malformed schema JSON returns valid=true (safe fallback)... "
result=$(jq -c -f "$TRANSFORM" --arg schema '{invalid json' "$SCRIPT_DIR/test-input-1.json")
expected='{"valid":true,"errors":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 19: Only required fields validation (no types)
echo -n "Test 19: Only required fields validation works... "
result=$(jq -c -f "$TRANSFORM" --arg schema '{"required":["name","age"]}' "$SCRIPT_DIR/test-input-1.json")
expected='{"valid":true,"errors":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 20: Only type validation (no required)
echo -n "Test 20: Only type validation works... "
result=$(jq -c -f "$TRANSFORM" --arg schema '{"types":{"name":"string","age":"number"}}' "$SCRIPT_DIR/test-input-1.json")
expected='{"valid":true,"errors":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All schema-validation tests passed!"
