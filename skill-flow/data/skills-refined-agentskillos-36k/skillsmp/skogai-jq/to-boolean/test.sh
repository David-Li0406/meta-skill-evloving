#!/usr/bin/env bash
set -euo pipefail

# Test to-boolean transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing to-boolean transformation..."

# Test 1: Boolean true (pass through)
echo -n "Test 1: Boolean true (pass through)... "
result=$(jq -c -f "$TRANSFORM" --arg path "bool_true" "$SCRIPT_DIR/test-input-1.json")
expected='{"bool_true":true}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Boolean false (pass through)
echo -n "Test 2: Boolean false (pass through)... "
result=$(jq -c -f "$TRANSFORM" --arg path "bool_false" "$SCRIPT_DIR/test-input-2.json")
expected='{"bool_false":false}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Null value (convert to false)
echo -n "Test 3: Null value (convert to false)... "
result=$(jq -c -f "$TRANSFORM" --arg path "value" "$SCRIPT_DIR/test-input-3.json")
expected='{"value":false}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Number 0 (convert to false)
echo -n "Test 4: Number 0 (convert to false)... "
result=$(jq -c -f "$TRANSFORM" --arg path "number" "$SCRIPT_DIR/test-input-4.json")
expected='{"number":false}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Non-zero number (convert to true)
echo -n "Test 5: Non-zero number (convert to true)... "
result=$(jq -c -f "$TRANSFORM" --arg path "number" "$SCRIPT_DIR/test-input-5.json")
expected='{"number":true}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Empty string (convert to false)
echo -n "Test 6: Empty string (convert to false)... "
result=$(jq -c -f "$TRANSFORM" --arg path "text" "$SCRIPT_DIR/test-input-6.json")
expected='{"text":false}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Non-empty string (convert to true)
echo -n "Test 7: Non-empty string (convert to true)... "
result=$(jq -c -f "$TRANSFORM" --arg path "text" "$SCRIPT_DIR/test-input-7.json")
expected='{"text":true}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Empty array (convert to false)
echo -n "Test 8: Empty array (convert to false)... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" "$SCRIPT_DIR/test-input-8.json")
expected='{"items":false}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Non-empty array (convert to true)
echo -n "Test 9: Non-empty array (convert to true)... "
result=$(jq -c -f "$TRANSFORM" --arg path "items" "$SCRIPT_DIR/test-input-9.json")
expected='{"items":true}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Empty object (convert to false)
echo -n "Test 10: Empty object (convert to false)... "
result=$(jq -c -f "$TRANSFORM" --arg path "data" "$SCRIPT_DIR/test-input-10.json")
expected='{"data":false}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Non-empty object (convert to true)
echo -n "Test 11: Non-empty object (convert to true)... "
result=$(jq -c -f "$TRANSFORM" --arg path "data" "$SCRIPT_DIR/test-input-11.json")
expected='{"data":true}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Field doesn't exist (getpath returns null, convert to false)
echo -n "Test 12: Field doesn't exist (convert to false)... "
result=$(jq -c -f "$TRANSFORM" --arg path "missing" "$SCRIPT_DIR/test-input-12.json")
expected='{"other":"field","missing":false}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Nested path with truthy value
echo -n "Test 13: Nested path with truthy value... "
result=$(jq -c -f "$TRANSFORM" --arg path "nested.path.value" "$SCRIPT_DIR/test-input-13.json")
expected='{"nested":{"path":{"value":true}}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Negative number (truthy)
echo -n "Test 14: Negative number (truthy)... "
result=$(jq -c -f "$TRANSFORM" --arg path "number" "$SCRIPT_DIR/test-input-14.json")
expected='{"number":true}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 15: Decimal 0.0 (falsy)
echo -n "Test 15: Decimal 0.0 (falsy)... "
result=$(jq -c -f "$TRANSFORM" --arg path "decimal" "$SCRIPT_DIR/test-input-15.json")
expected='{"decimal":false}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 16: Decimal 0.5 (truthy)
echo -n "Test 16: Decimal 0.5 (truthy)... "
result=$(jq -c -f "$TRANSFORM" --arg path "decimal" "$SCRIPT_DIR/test-input-16.json")
expected='{"decimal":true}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All to-boolean tests passed!"
