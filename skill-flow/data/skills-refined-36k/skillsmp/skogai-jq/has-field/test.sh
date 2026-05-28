#!/usr/bin/env bash
set -euo pipefail

# Test has-field transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing has-field transformation..."

# Test 1: Field exists with string value (happy path)
echo -n "Test 1: Field exists with string value... "
result=$(jq -f "$TRANSFORM" --arg path "user.name" "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Field doesn't exist (non-existent path)
echo -n "Test 2: Field doesn't exist... "
result=$(jq -f "$TRANSFORM" --arg path "user.phone" "$SCRIPT_DIR/test-input-2.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Field exists with null value (CRITICAL - field exists even with null)
echo -n "Test 3: Field exists with null value... "
result=$(jq -f "$TRANSFORM" --arg path "user.name" "$SCRIPT_DIR/test-input-3.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Field exists with false value (CRITICAL - field exists even with false)
echo -n "Test 4: Field exists with false value... "
result=$(jq -f "$TRANSFORM" --arg path "settings.enabled" "$SCRIPT_DIR/test-input-4.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Field exists with 0 value (CRITICAL - field exists even with 0)
echo -n "Test 5: Field exists with 0 value... "
result=$(jq -f "$TRANSFORM" --arg path "config.count" "$SCRIPT_DIR/test-input-5.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Field exists with empty string (CRITICAL - field exists even with "")
echo -n "Test 6: Field exists with empty string... "
result=$(jq -f "$TRANSFORM" --arg path "settings.name" "$SCRIPT_DIR/test-input-6.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Nested field exists (deep path - 4 levels)
echo -n "Test 7: Nested field exists (deep path)... "
result=$(jq -f "$TRANSFORM" --arg path "data.nested.deep.value" "$SCRIPT_DIR/test-input-7.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Nested field doesn't exist (intermediate path exists but final field missing)
echo -n "Test 8: Nested field doesn't exist... "
result=$(jq -f "$TRANSFORM" --arg path "data.nested.deep.missing" "$SCRIPT_DIR/test-input-8.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Root level field exists
echo -n "Test 9: Root level field exists... "
result=$(jq -f "$TRANSFORM" --arg path "name" "$SCRIPT_DIR/test-input-9.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Empty object - field doesn't exist
echo -n "Test 10: Empty object - field doesn't exist... "
result=$(jq -f "$TRANSFORM" --arg path "anything" "$SCRIPT_DIR/test-input-10.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Intermediate path has null value (user.profile is null, checking user.profile.name)
echo -n "Test 11: Intermediate path has null value... "
result=$(jq -f "$TRANSFORM" --arg path "user.profile.name" "$SCRIPT_DIR/test-input-11.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Deeply nested field with multiple levels (happy path)
echo -n "Test 12: Deeply nested field with multiple levels... "
result=$(jq -f "$TRANSFORM" --arg path "user.profile.age" "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All has-field tests passed!"
