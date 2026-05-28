#!/usr/bin/env bash
set -euo pipefail

# Test to-number transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing to-number transformation..."

# Test 1: Number value (pass through)
echo -n "Test 1: Number value (pass through)... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.age" "$SCRIPT_DIR/test-input-1.json")
expected='{"user":{"age":42}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: String number (parse)
echo -n "Test 2: String number (parse)... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.age" "$SCRIPT_DIR/test-input-2.json")
expected='{"user":{"age":123}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: String float (parse)
echo -n "Test 3: String float (parse)... "
result=$(jq -c -f "$TRANSFORM" --arg path "price" "$SCRIPT_DIR/test-input-3.json")
expected='{"price":3.14}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: String invalid (null)
echo -n "Test 4: String invalid (null)... "
result=$(jq -c -f "$TRANSFORM" --arg path "count" "$SCRIPT_DIR/test-input-4.json")
expected='{"count":null}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Boolean true (1)
echo -n "Test 5: Boolean true (1)... "
result=$(jq -c -f "$TRANSFORM" --arg path "active" "$SCRIPT_DIR/test-input-5.json")
expected='{"active":1}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Boolean false (0)
echo -n "Test 6: Boolean false (0)... "
result=$(jq -c -f "$TRANSFORM" --arg path "active" "$SCRIPT_DIR/test-input-6.json")
expected='{"active":0}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Null value (0)
echo -n "Test 7: Null value (0)... "
result=$(jq -c -f "$TRANSFORM" --arg path "value" "$SCRIPT_DIR/test-input-7.json")
expected='{"value":0}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Empty string (null)
echo -n "Test 8: Empty string (null)... "
result=$(jq -c -f "$TRANSFORM" --arg path "text" "$SCRIPT_DIR/test-input-8.json")
expected='{"text":null}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Array (null)
echo -n "Test 9: Array (null)... "
result=$(jq -c -f "$TRANSFORM" --arg path "data" "$SCRIPT_DIR/test-input-9.json")
expected='{"data":null}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Object (null)
echo -n "Test 10: Object (null)... "
result=$(jq -c -f "$TRANSFORM" --arg path "config" "$SCRIPT_DIR/test-input-10.json")
expected='{"config":null}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Field doesn't exist (object unchanged, path created with null)
echo -n "Test 11: Field doesn't exist (null)... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.age" "$SCRIPT_DIR/test-input-11.json")
expected='{"user":{"name":"skogix","age":null}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: String "0" (parse to 0)
echo -n "Test 12: String '0' (parse to 0)... "
result=$(jq -c -f "$TRANSFORM" --arg path "num" "$SCRIPT_DIR/test-input-12.json")
expected='{"num":0}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Negative number string (parse)
echo -n "Test 13: Negative number string (parse)... "
result=$(jq -c -f "$TRANSFORM" --arg path "num" "$SCRIPT_DIR/test-input-13.json")
expected='{"num":-42}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All to-number tests passed!"
