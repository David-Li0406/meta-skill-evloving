#!/usr/bin/env bash
set -euo pipefail

# Test copy-field transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing copy-field transformation..."

# Test 1: Copy existing field to new path
echo -n "Test 1: Copy existing field to new path... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "user.name" --arg dest_path "profile.username" "$SCRIPT_DIR/test-input-1.json")
expected='{"user":{"name":"skogix","email":"test@example.com"},"profile":{"username":"skogix"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Copy nested field to root
echo -n "Test 2: Copy nested field to root... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "user.profile.age" --arg dest_path "age" "$SCRIPT_DIR/test-input-2.json")
expected='{"user":{"profile":{"age":30}},"age":30}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Copy to nested path (creates intermediate objects)
echo -n "Test 3: Copy to nested path creating intermediate objects... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "name" --arg dest_path "data.user.name" "$SCRIPT_DIR/test-input-3.json")
expected='{"name":"test","data":{"user":{"name":"test"}}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Copy non-existent field (copies null)
echo -n "Test 4: Copy non-existent field... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "missing" --arg dest_path "copy" "$SCRIPT_DIR/test-input-4.json")
expected='{"copy":null}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Copy null value
echo -n "Test 5: Copy null value... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "value" --arg dest_path "copied" "$SCRIPT_DIR/test-input-5.json")
expected='{"value":null,"copied":null}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Copy false value
echo -n "Test 6: Copy false value... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "active" --arg dest_path "status.active" "$SCRIPT_DIR/test-input-6.json")
expected='{"active":false,"status":{"active":false}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Copy 0 value
echo -n "Test 7: Copy 0 value... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "count" --arg dest_path "backup.count" "$SCRIPT_DIR/test-input-7.json")
expected='{"count":0,"backup":{"count":0}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Copy empty string value
echo -n "Test 8: Copy empty string value... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "text" --arg dest_path "message" "$SCRIPT_DIR/test-input-8.json")
expected='{"text":"","message":""}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Copy array value
echo -n "Test 9: Copy array value... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "items" --arg dest_path "backup.items" "$SCRIPT_DIR/test-input-9.json")
expected='{"items":[1,2,3],"backup":{"items":[1,2,3]}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Copy object value
echo -n "Test 10: Copy object value... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "config" --arg dest_path "backup.config" "$SCRIPT_DIR/test-input-10.json")
expected='{"config":{"settings":{"debug":true}},"backup":{"config":{"settings":{"debug":true}}}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Copy empty array value
echo -n "Test 11: Copy empty array value... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "empty" --arg dest_path "copied.empty" "$SCRIPT_DIR/test-input-11.json")
expected='{"empty":[],"copied":{"empty":[]}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Copy empty object value
echo -n "Test 12: Copy empty object value... "
result=$(jq -c -f "$TRANSFORM" --arg source_path "obj" --arg dest_path "backup.obj" "$SCRIPT_DIR/test-input-12.json")
expected='{"obj":{},"backup":{"obj":{}}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All copy-field tests passed!"
