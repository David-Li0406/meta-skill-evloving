#!/usr/bin/env bash
set -euo pipefail

# Test add-field transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing add-field transformation..."

# Test 1: Add field to nested object
echo -n "Test 1: Add field to nested object... "
result=$(jq -c -f "$TRANSFORM" --arg path "user" --arg field_name "email" --arg value "alice@example.com" "$SCRIPT_DIR/test-input-1.json")
expected='{"user":{"name":"alice","email":"alice@example.com"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Add field creating intermediate objects (nested path)
echo -n "Test 2: Add field creating intermediate objects... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.profile" --arg field_name "age" --arg value "30" "$SCRIPT_DIR/test-input-3.json")
expected='{"user":{"profile":{"age":"30"}}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Add field to root level (empty path)
echo -n "Test 3: Add field to root level... "
result=$(jq -c -f "$TRANSFORM" --arg path "" --arg field_name "status" --arg value "active" "$SCRIPT_DIR/test-input-1.json")
expected='{"user":{"name":"alice"},"status":"active"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Add null value (falsy value test)
echo -n "Test 4: Add null value... "
result=$(jq -c -f "$TRANSFORM" --arg path "user" --arg field_name "middle_name" --arg value "null" "$SCRIPT_DIR/test-input-1.json")
expected='{"user":{"name":"alice","middle_name":"null"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Add false value (falsy value test)
echo -n "Test 5: Add false value... "
result=$(jq -c -f "$TRANSFORM" --arg path "settings" --arg field_name "enabled" --arg value "false" "$SCRIPT_DIR/test-input-7.json")
expected='{"settings":{"debug":true,"enabled":"false"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Add 0 value (falsy value test)
echo -n "Test 6: Add 0 value... "
result=$(jq -c -f "$TRANSFORM" --arg path "product" --arg field_name "discount" --arg value "0" "$SCRIPT_DIR/test-input-10.json")
expected='{"product":{"price":100,"discount":"0"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Add empty string value (falsy value test)
echo -n "Test 7: Add empty string value... "
result=$(jq -c -f "$TRANSFORM" --arg path "user" --arg field_name "nickname" --arg value "" "$SCRIPT_DIR/test-input-5.json")
expected='{"user":{"name":"bob","email":"bob@example.com","nickname":""}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Add array value (as string representation)
echo -n "Test 8: Add array value... "
result=$(jq -c -f "$TRANSFORM" --arg path "data" --arg field_name "tags" --arg value "[\"tag1\",\"tag2\"]" "$SCRIPT_DIR/test-input-4.json")
expected='{"data":{"items":[1,2,3],"tags":"[\"tag1\",\"tag2\"]"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Add object value (as string representation)
echo -n "Test 9: Add object value... "
result=$(jq -c -f "$TRANSFORM" --arg path "app" --arg field_name "config" --arg value "{\"debug\":true}" "$SCRIPT_DIR/test-input-9.json")
expected='{"app":{"name":"test","config":"{\"debug\":true}"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Add field to empty object
echo -n "Test 10: Add field to empty object at root... "
result=$(jq -c -f "$TRANSFORM" --arg path "" --arg field_name "version" --arg value "1.0.0" "$SCRIPT_DIR/test-input-3.json")
expected='{"version":"1.0.0"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Add field to empty nested object
echo -n "Test 11: Add field to empty nested object... "
result=$(jq -c -f "$TRANSFORM" --arg path "config" --arg field_name "timeout" --arg value "30" "$SCRIPT_DIR/test-input-6.json")
expected='{"config":{"timeout":"30"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Add field to deeply nested object
echo -n "Test 12: Add field to deeply nested object... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.profile" --arg field_name "city" --arg value "Stockholm" "$SCRIPT_DIR/test-input-2.json")
expected='{"user":{"profile":{"country":"Sweden","city":"Stockholm"}}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All add-field tests passed!"
