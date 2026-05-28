#!/usr/bin/env bash
set -euo pipefail

# Test remove-field transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing remove-field transformation..."

# Test 1: Remove existing field
echo -n "Test 1: Remove existing field... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.email" "$SCRIPT_DIR/test-input-1.json")
expected='{"user":{"name":"skogix","phone":"123-456-7890"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Remove nested field
echo -n "Test 2: Remove nested field... "
result=$(jq -c -f "$TRANSFORM" --arg path "data.user.profile.age" "$SCRIPT_DIR/test-input-2.json")
expected='{"data":{"user":{"profile":{"location":"sweden","active":true}}}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Remove non-existent field (no error)
echo -n "Test 3: Remove non-existent field (no error)... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.phone" "$SCRIPT_DIR/test-input-3.json")
expected='{"user":{"name":"skogix"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Remove from root level
echo -n "Test 4: Remove from root level... "
result=$(jq -c -f "$TRANSFORM" --arg path "email" "$SCRIPT_DIR/test-input-10.json")
expected='{"name":"skogix"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Remove field with null value
echo -n "Test 5: Remove field with null value... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.name" "$SCRIPT_DIR/test-input-4.json")
expected='{"user":{"age":30}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Remove field with false value
echo -n "Test 6: Remove field with false value... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.active" "$SCRIPT_DIR/test-input-5.json")
expected='{"user":{"name":"skogix","email":"test@example.com"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Remove field with 0 value
echo -n "Test 7: Remove field with 0 value... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.score" "$SCRIPT_DIR/test-input-6.json")
expected='{"user":{"name":"skogix","email":"test@example.com"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Remove field with empty string
echo -n "Test 8: Remove field with empty string... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.bio" "$SCRIPT_DIR/test-input-7.json")
expected='{"user":{"name":"skogix","email":"test@example.com"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Remove field with array value
echo -n "Test 9: Remove field with array value... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.tags" "$SCRIPT_DIR/test-input-8.json")
expected='{"user":{"name":"skogix","email":"test@example.com"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Remove field with object value
echo -n "Test 10: Remove field with object value... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.metadata" "$SCRIPT_DIR/test-input-9.json")
expected='{"user":{"name":"skogix","email":"test@example.com"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All remove-field tests passed!"
