#!/usr/bin/env bash
set -euo pipefail

# Test extract-role-content transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing extract-role-content transformation..."

# Test 1: Extract user messages
echo -n "Test 1: Extract user messages... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-1.json")
expected='["Hello","How are you?"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Extract assistant messages
echo -n "Test 2: Extract assistant messages... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "assistant" "$SCRIPT_DIR/test-input-2.json")
expected='["Hi there","I am doing well"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Extract system messages
echo -n "Test 3: Extract system messages... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "system" "$SCRIPT_DIR/test-input-3.json")
expected='["You are a helpful assistant"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Role doesn't exist (empty array)
echo -n "Test 4: Role doesn't exist... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "nonexistent" "$SCRIPT_DIR/test-input-4.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Empty messages array
echo -n "Test 5: Empty messages array... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-5.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Mixed roles extraction
echo -n "Test 6: Mixed roles extraction... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-6.json")
expected='["First user message","Second user message"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Multiple messages same role
echo -n "Test 7: Multiple messages same role... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "assistant" "$SCRIPT_DIR/test-input-7.json")
expected='["Response 1","Response 2","Response 3"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Null content field
echo -n "Test 8: Null content field... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-8.json")
expected='[null]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Missing content field
echo -n "Test 9: Missing content field... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-9.json")
expected='[null]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Array field doesn't exist
echo -n "Test 10: Array field doesn't exist... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-10.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Field is not an array
echo -n "Test 11: Field is not an array... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-11.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Content with different types (number, boolean, object)
echo -n "Test 12: Content with different types... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-12.json")
expected='[42,false,{"nested":"object"}]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Empty string content
echo -n "Test 13: Empty string content... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-13.json")
expected='[""]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Array contains non-object items (primitives) - filters non-objects
echo -n "Test 14: Array contains non-objects... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-14.json")
expected='["only this should be extracted if non-objects were filtered"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All extract-role-content tests passed!"
