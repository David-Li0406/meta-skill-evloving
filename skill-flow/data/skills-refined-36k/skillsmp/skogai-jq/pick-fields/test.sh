#!/usr/bin/env bash
set -euo pipefail

# Test pick-fields transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing pick-fields transformation..."

# Test 1: Pick multiple fields from object
echo -n "Test 1: Pick multiple fields from object... "
result=$(jq -c -f "$TRANSFORM" --arg fields "name,email" "$SCRIPT_DIR/test-input-1.json")
expected='{"name":"skogix","email":"test@example.com"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Pick single field
echo -n "Test 2: Pick single field... "
result=$(jq -c -f "$TRANSFORM" --arg fields "user" "$SCRIPT_DIR/test-input-2.json")
expected='{"user":"john"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Pick three fields from object with multiple fields
echo -n "Test 3: Pick three fields from object... "
result=$(jq -c -f "$TRANSFORM" --arg fields "name,age,phone" "$SCRIPT_DIR/test-input-1.json")
expected='{"name":"skogix","age":30,"phone":"123-456-7890"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Pick fields with missing field (should include null)
echo -n "Test 4: Pick fields including missing field... "
result=$(jq -c -f "$TRANSFORM" --arg fields "name,missing,email" "$SCRIPT_DIR/test-input-1.json")
expected='{"name":"skogix","missing":null,"email":"test@example.com"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Pick field with array value
echo -n "Test 5: Pick field with array value... "
result=$(jq -c -f "$TRANSFORM" --arg fields "title,tags" "$SCRIPT_DIR/test-input-3.json")
expected='{"title":"test","tags":["a","b","c"]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Pick field with object value
echo -n "Test 6: Pick field with object value... "
result=$(jq -c -f "$TRANSFORM" --arg fields "id,metadata" "$SCRIPT_DIR/test-input-3.json")
expected='{"id":42,"metadata":{"key":"value"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Fields with whitespace around commas
echo -n "Test 7: Fields with whitespace around commas... "
result=$(jq -c -f "$TRANSFORM" --arg fields "name , email , age" "$SCRIPT_DIR/test-input-1.json")
expected='{"name":"skogix","email":"test@example.com","age":30}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Field order preservation
echo -n "Test 8: Field order preservation... "
result=$(jq -c -f "$TRANSFORM" --arg fields "m,z,a" "$SCRIPT_DIR/test-input-5.json")
expected='{"m":3,"z":1,"a":2}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Boolean, zero, null, empty values
echo -n "Test 9: Boolean, zero, null, empty values... "
result=$(jq -c -f "$TRANSFORM" --arg fields "active,count,value,tags,metadata" "$SCRIPT_DIR/test-input-4.json")
expected='{"active":true,"count":0,"value":null,"tags":[],"metadata":{}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Duplicate field names
echo -n "Test 10: Duplicate field names... "
result=$(jq -c -f "$TRANSFORM" --arg fields "name,email,name" "$SCRIPT_DIR/test-input-1.json")
expected='{"name":"skogix","email":"test@example.com"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All pick-fields tests passed!"
