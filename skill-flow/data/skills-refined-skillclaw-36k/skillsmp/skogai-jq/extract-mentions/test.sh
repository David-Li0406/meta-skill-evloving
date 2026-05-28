#!/usr/bin/env bash
set -euo pipefail

# Test extract-mentions transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing extract-mentions transformation..."

# Test 1: Single mention
echo -n "Test 1: Single mention... "
result=$(jq -c -f "$TRANSFORM" --arg path "message" "$SCRIPT_DIR/test-input-1.json")
expected='["@skogix"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Multiple mentions
echo -n "Test 2: Multiple mentions... "
result=$(jq -c -f "$TRANSFORM" --arg path "comment" "$SCRIPT_DIR/test-input-2.json")
expected='["@alice","@bob","@charlie"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: No mentions (empty array)
echo -n "Test 3: No mentions (empty array)... "
result=$(jq -c -f "$TRANSFORM" --arg path "text" "$SCRIPT_DIR/test-input-3.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Mentions with numbers (@user123)
echo -n "Test 4: Mentions with numbers (@user123)... "
result=$(jq -c -f "$TRANSFORM" --arg path "post" "$SCRIPT_DIR/test-input-4.json")
expected='["@user123","@test_user"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Mentions at start/middle/end
echo -n "Test 5: Mentions at start/middle/end... "
result=$(jq -c -f "$TRANSFORM" --arg path "msg" "$SCRIPT_DIR/test-input-5.json")
expected='["@start","@middle","@end"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Duplicate mentions (keep all)
echo -n "Test 6: Duplicate mentions (keep all)... "
result=$(jq -c -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-6.json")
expected='["@alice","@bob","@alice"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Empty string
echo -n "Test 7: Empty string... "
result=$(jq -c -f "$TRANSFORM" --arg path "empty" "$SCRIPT_DIR/test-input-7.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Field doesn't exist
echo -n "Test 8: Field doesn't exist... "
result=$(jq -c -f "$TRANSFORM" --arg path "missing" "$SCRIPT_DIR/test-input-8.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Field is number (not string)
echo -n "Test 9: Field is number (not string)... "
result=$(jq -c -f "$TRANSFORM" --arg path "number" "$SCRIPT_DIR/test-input-9.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Field is boolean
echo -n "Test 10: Field is boolean... "
result=$(jq -c -f "$TRANSFORM" --arg path "boolean" "$SCRIPT_DIR/test-input-9.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Field is null
echo -n "Test 11: Field is null... "
result=$(jq -c -f "$TRANSFORM" --arg path "null_value" "$SCRIPT_DIR/test-input-9.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Field is object
echo -n "Test 12: Field is object... "
result=$(jq -c -f "$TRANSFORM" --arg path "object" "$SCRIPT_DIR/test-input-9.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Field is array
echo -n "Test 13: Field is array... "
result=$(jq -c -f "$TRANSFORM" --arg path "array" "$SCRIPT_DIR/test-input-9.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Nested path
echo -n "Test 14: Nested path... "
result=$(jq -c -f "$TRANSFORM" --arg path "nested.field" "$SCRIPT_DIR/test-input-10.json")
expected='["@mention","@deep"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 15: @ in email address (extracts all @ patterns including from emails)
echo -n "Test 15: @ in email address (extracts all @ patterns)... "
result=$(jq -c -f "$TRANSFORM" --arg path "special" "$SCRIPT_DIR/test-input-11.json")
expected='["@user","@example","@user"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 16: Whitespace-only string
echo -n "Test 16: Whitespace-only string... "
result=$(jq -c -f "$TRANSFORM" --arg path "whitespace" "$SCRIPT_DIR/test-input-12.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All extract-mentions tests passed!"
