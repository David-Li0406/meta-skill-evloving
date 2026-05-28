#!/usr/bin/env bash
set -euo pipefail

# Test to-string transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing to-string transformation..."

# Test 1: String value (pass through)
echo -n "Test 1: String value (pass through)... "
result=$(jq -c -f "$TRANSFORM" --arg path "text" "$SCRIPT_DIR/test-input-1.json")
expected='{"text":"already-a-string"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Empty string (pass through)
echo -n "Test 2: Empty string (pass through)... "
result=$(jq -c -f "$TRANSFORM" --arg path "text" "$SCRIPT_DIR/test-input-2.json")
expected='{"text":""}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Positive number to string
echo -n "Test 3: Positive number to string... "
result=$(jq -c -f "$TRANSFORM" --arg path "number" "$SCRIPT_DIR/test-input-3.json")
expected='{"number":"42"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Zero to string
echo -n "Test 4: Zero to string... "
result=$(jq -c -f "$TRANSFORM" --arg path "number" "$SCRIPT_DIR/test-input-4.json")
expected='{"number":"0"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Negative number to string
echo -n "Test 5: Negative number to string... "
result=$(jq -c -f "$TRANSFORM" --arg path "number" "$SCRIPT_DIR/test-input-5.json")
expected='{"number":"-15"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Decimal number to string
echo -n "Test 6: Decimal number to string... "
result=$(jq -c -f "$TRANSFORM" --arg path "decimal" "$SCRIPT_DIR/test-input-6.json")
expected='{"decimal":"3.14159"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Boolean true to string
echo -n "Test 7: Boolean true to string... "
result=$(jq -c -f "$TRANSFORM" --arg path "bool" "$SCRIPT_DIR/test-input-7.json")
expected='{"bool":"true"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Boolean false to string
echo -n "Test 8: Boolean false to string... "
result=$(jq -c -f "$TRANSFORM" --arg path "bool" "$SCRIPT_DIR/test-input-8.json")
expected='{"bool":"false"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Null to string "null"
echo -n "Test 9: Null to string \"null\"... "
result=$(jq -c -f "$TRANSFORM" --arg path "value" "$SCRIPT_DIR/test-input-9.json")
expected='{"value":"null"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Empty array to JSON string
echo -n "Test 10: Empty array to JSON string... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" "$SCRIPT_DIR/test-input-10.json")
expected='{"items":"[]"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Non-empty array to JSON string
echo -n "Test 11: Non-empty array to JSON string... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" "$SCRIPT_DIR/test-input-11.json")
expected='{"items":"[1,2,3]"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Empty object to JSON string
echo -n "Test 12: Empty object to JSON string... "
result=$(jq -c -f "$TRANSFORM" --arg path "data" "$SCRIPT_DIR/test-input-12.json")
expected='{"data":"{}"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Non-empty object to JSON string
echo -n "Test 13: Non-empty object to JSON string... "
result=$(jq -c -f "$TRANSFORM" --arg path "data" "$SCRIPT_DIR/test-input-13.json")
expected='{"data":"{\"name\":\"test\",\"count\":5}"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Non-existent field (creates field with "null")
echo -n "Test 14: Non-existent field (creates field with \"null\")... "
result=$(jq -c -f "$TRANSFORM" --arg path "missing" "$SCRIPT_DIR/test-input-14.json")
expected='{"other":"field","missing":"null"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 15: Nested path conversion
echo -n "Test 15: Nested path conversion... "
result=$(jq -c -f "$TRANSFORM" --arg path "nested.path.value" "$SCRIPT_DIR/test-input-15.json")
expected='{"nested":{"path":{"value":"99"}}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 16: Complex array with mixed types to JSON string
echo -n "Test 16: Complex array with mixed types to JSON string... "
result=$(jq -c -f "$TRANSFORM" --arg path "array" "$SCRIPT_DIR/test-input-16.json")
expected='{"array":"[true,false,null,\"text\",42,{\"key\":\"val\"}]"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All to-string tests passed!"
