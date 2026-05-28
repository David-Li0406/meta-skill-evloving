#!/usr/bin/env bash
set -euo pipefail

# Test group-by-field transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing group-by-field transformation..."

# Test 1: Group by string field
echo -n "Test 1: Group by string field... "
result=$(jq -c -S -f "$TRANSFORM" --arg array_path "items" --arg field_name "status" "$SCRIPT_DIR/test-input-1.json")
expected='{"active":[{"name":"alice","status":"active"},{"name":"bob","status":"active"}],"inactive":[{"name":"charlie","status":"inactive"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Group by number field
echo -n "Test 2: Group by number field... "
result=$(jq -c -S -f "$TRANSFORM" --arg array_path "data.results" --arg field_name "score" "$SCRIPT_DIR/test-input-2.json")
expected='{"100":[{"name":"alice","score":100},{"name":"charlie","score":100}],"85":[{"name":"bob","score":85}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Group by boolean field
echo -n "Test 3: Group by boolean field... "
result=$(jq -c -S -f "$TRANSFORM" --arg array_path "items" --arg field_name "enabled" "$SCRIPT_DIR/test-input-3.json")
expected='{"false":[{"enabled":false,"name":"bob"}],"true":[{"enabled":true,"name":"alice"},{"enabled":true,"name":"charlie"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Empty array
echo -n "Test 4: Empty array... "
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
result=$(jq -c -S -f "$TRANSFORM" --arg array_path "items" --arg field_name "status" "$SCRIPT_DIR/test-input-5.json")
expected='{"active":[{"name":"alice","status":"active"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: All same value (single group)
echo -n "Test 6: All same value (single group)... "
result=$(jq -c -S -f "$TRANSFORM" --arg array_path "items" --arg field_name "status" "$SCRIPT_DIR/test-input-6.json")
expected='{"active":[{"name":"alice","status":"active"},{"name":"bob","status":"active"},{"name":"charlie","status":"active"}]}'
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
expected='{"123":[{"name":"bob","type":123}],"true":[{"name":"charlie","type":true}],"user":[{"name":"alice","type":"user"},{"name":"dave","type":"user"}]}'
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
result=$(jq -c -S -f "$TRANSFORM" --arg array_path "items" --arg field_name "status" "$SCRIPT_DIR/test-input-8.json")
expected='{"active":[{"name":"alice","status":"active"},{"name":"charlie","status":"active"}],"null":[{"name":"bob"},{"name":"dave"}]}'
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
result=$(jq -c -S -f "$TRANSFORM" --arg array_path "users" --arg field_name "profile.role" "$SCRIPT_DIR/test-input-9.json")
expected='{"admin":[{"name":"alice","profile":{"role":"admin"}},{"name":"charlie","profile":{"role":"admin"}}],"guest":[{"name":"dave","profile":{"role":"guest"}}],"user":[{"name":"bob","profile":{"role":"user"}}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Null values in field
echo -n "Test 10: Null values in field... "
result=$(jq -c -S -f "$TRANSFORM" --arg array_path "items" --arg field_name "value" "$SCRIPT_DIR/test-input-10.json")
expected='{"null":[{"name":"alice","value":null},{"name":"charlie","value":null}],"test":[{"name":"bob","value":"test"},{"name":"dave","value":"test"}]}'
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

# Test 12: Group by zero values
echo -n "Test 12: Group by zero values... "
result=$(jq -c -S -f "$TRANSFORM" --arg array_path "data.results" --arg field_name "count" "$SCRIPT_DIR/test-input-12.json")
expected='{"0":[{"count":0,"name":"alice"},{"count":0,"name":"charlie"}],"1":[{"count":1,"name":"bob"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Group by empty string values
echo -n "Test 13: Group by empty string values... "
result=$(jq -c -S -f "$TRANSFORM" --arg array_path "items" --arg field_name "value" "$SCRIPT_DIR/test-input-13.json")
expected='{"":[{"name":"alice","value":""},{"name":"charlie","value":""}],"test":[{"name":"bob","value":"test"},{"name":"dave","value":"test"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All group-by-field tests passed!"
