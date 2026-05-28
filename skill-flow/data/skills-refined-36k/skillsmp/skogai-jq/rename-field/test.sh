#!/usr/bin/env bash
set -euo pipefail

# Test rename-field transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing rename-field transformation..."

# Test 1: Rename top-level field
echo -n "Test 1: Rename top-level field... "
result=$(jq -cS -f "$TRANSFORM" --arg old_path "name" --arg new_path "fullName" "$SCRIPT_DIR/test-input-1.json")
expected='{"age":30,"fullName":"alice"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Rename nested field within same parent
echo -n "Test 2: Rename nested field within same parent... "
result=$(jq -cS -f "$TRANSFORM" --arg old_path "user.name" --arg new_path "user.fullName" "$SCRIPT_DIR/test-input-2.json")
expected='{"user":{"age":25,"email":"bob@example.com","fullName":"bob"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Move field to different nested location (creates intermediate objects)
echo -n "Test 3: Move field to different nested location... "
result=$(jq -cS -f "$TRANSFORM" --arg old_path "profile.details.username" --arg new_path "user.name" "$SCRIPT_DIR/test-input-3.json")
expected='{"profile":{"details":{}},"user":{"name":"charlie"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Rename field with null value (CRITICAL)
echo -n "Test 4: Rename field with null value... "
result=$(jq -cS -f "$TRANSFORM" --arg old_path "data.value" --arg new_path "data.nullValue" "$SCRIPT_DIR/test-input-4.json")
expected='{"data":{"count":42,"nullValue":null}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Rename field with false value (CRITICAL)
echo -n "Test 5: Rename field with false value... "
result=$(jq -cS -f "$TRANSFORM" --arg old_path "settings.enabled" --arg new_path "settings.isEnabled" "$SCRIPT_DIR/test-input-5.json")
expected='{"settings":{"isEnabled":false,"timeout":30}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Rename field with 0 value (CRITICAL)
echo -n "Test 6: Rename field with 0 value... "
result=$(jq -cS -f "$TRANSFORM" --arg old_path "metrics.score" --arg new_path "metrics.totalScore" "$SCRIPT_DIR/test-input-6.json")
expected='{"metrics":{"attempts":5,"totalScore":0}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Rename field with empty string value (CRITICAL)
echo -n "Test 7: Rename field with empty string value... "
result=$(jq -cS -f "$TRANSFORM" --arg old_path "form.name" --arg new_path "form.username" "$SCRIPT_DIR/test-input-7.json")
expected='{"form":{"submitted":true,"username":""}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Rename field with array value (CRITICAL)
echo -n "Test 8: Rename field with array value... "
result=$(jq -cS -f "$TRANSFORM" --arg old_path "config.items" --arg new_path "config.itemList" "$SCRIPT_DIR/test-input-8.json")
expected='{"config":{"itemList":[1,2,3],"total":3}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Rename field with object value (CRITICAL)
echo -n "Test 9: Rename field with object value... "
result=$(jq -cS -f "$TRANSFORM" --arg old_path "app.settings" --arg new_path "app.config" "$SCRIPT_DIR/test-input-9.json")
expected='{"app":{"config":{"lang":"en","theme":"dark"}}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Rename non-existent field (should set null at new path, delete nothing)
echo -n "Test 10: Rename non-existent field... "
result=$(jq -cS -f "$TRANSFORM" --arg old_path "user.missing" --arg new_path "user.notFound" "$SCRIPT_DIR/test-input-10.json")
expected='{"user":{"name":"alice","notFound":null}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Rename field with empty array value (CRITICAL)
echo -n "Test 11: Rename field with empty array value... "
result=$(jq -cS -f "$TRANSFORM" --arg old_path "data.list" --arg new_path "data.items" "$SCRIPT_DIR/test-input-11.json")
expected='{"data":{"count":0,"items":[]}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Rename field with empty object value (CRITICAL)
echo -n "Test 12: Rename field with empty object value... "
result=$(jq -cS -f "$TRANSFORM" --arg old_path "info.meta" --arg new_path "info.metadata" "$SCRIPT_DIR/test-input-12.json")
expected='{"info":{"metadata":{},"ready":true}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All rename-field tests passed!"
