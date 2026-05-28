#!/usr/bin/env bash
set -euo pipefail

# Test count-by-field transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing count-by-field transformation..."

# Test 1: Count by string field
echo -n "Test 1: Count by string field... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "status" "$SCRIPT_DIR/test-input-1.json")
expected='{"active":3,"inactive":1}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Count by number field
echo -n "Test 2: Count by number field... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "data.results" --arg field_name "score" "$SCRIPT_DIR/test-input-2.json")
expected='{"85":2,"90":1,"100":2}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Count by boolean field
echo -n "Test 3: Count by boolean field... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "enabled" "$SCRIPT_DIR/test-input-3.json")
expected='{"false":3,"true":2}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Empty array returns empty counts
echo -n "Test 4: Empty array returns empty counts... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "status" "$SCRIPT_DIR/test-input-4.json")
expected='{}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Single element
echo -n "Test 5: Single element... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "status" "$SCRIPT_DIR/test-input-5.json")
expected='{"active":1}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: All same value (count = length)
echo -n "Test 6: All same value (count = length)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "status" "$SCRIPT_DIR/test-input-6.json")
expected='{"active":3}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Mixed types in field
echo -n "Test 7: Mixed types in field... "
result=$(jq -c -S -f "$TRANSFORM" --arg array_path "items" --arg field_name "type" "$SCRIPT_DIR/test-input-7.json")
expected='{"123":1,"true":1,"user":2}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Field doesn't exist in some objects
echo -n "Test 8: Field doesn't exist in some objects... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "status" "$SCRIPT_DIR/test-input-8.json")
expected='{"active":2,"null":2}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Nested field path
echo -n "Test 9: Nested field path... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "users" --arg field_name "profile.role" "$SCRIPT_DIR/test-input-9.json")
expected='{"admin":2,"guest":1,"user":1}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Array contains null values
echo -n "Test 10: Array contains null values... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "value" "$SCRIPT_DIR/test-input-10.json")
expected='{"null":2,"test":2}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Non-array field returns null
echo -n "Test 11: Non-array field returns null... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "status" "$SCRIPT_DIR/test-input-11.json")
expected='null'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Non-existent path returns null
echo -n "Test 12: Non-existent path returns null... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "status" "$SCRIPT_DIR/test-input-12.json")
expected='null'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Count with zero values
echo -n "Test 13: Count with zero values... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "count" "$SCRIPT_DIR/test-input-13.json")
expected='{"0":3,"1":1,"2":1}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Count with empty string values
echo -n "Test 14: Count with empty string values... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "value" "$SCRIPT_DIR/test-input-14.json")
expected='{"":2,"test":2}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All count-by-field tests passed!"
