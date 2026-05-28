#!/usr/bin/env bash
set -euo pipefail

# Test test-generator transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing test-generator transformation..."

# Test 1: Generate bash test script from simple schema
echo -n "Test 1: Generate bash test script from simple schema... "
result=$(jq -r -f "$TRANSFORM" --arg format "bash" "$SCRIPT_DIR/test-input-1.json" | head -1)
expected='#!/usr/bin/env bash'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Generate JSON test cases from schema
echo -n "Test 2: Generate JSON test cases from schema... "
result=$(jq -c -f "$TRANSFORM" --arg format "json" "$SCRIPT_DIR/test-input-1.json")
expected='[{"test_number":1,"description":"Get existing value","input":{"user":{"name":"alice"}},"args":{"path":"user.name"},"expected":"alice"}]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Generate from schema with multiple examples
echo -n "Test 3: Generate from schema with multiple examples... "
result=$(jq -c -f "$TRANSFORM" --arg format "json" "$SCRIPT_DIR/test-input-2.json" | jq 'length')
expected='2'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Generate from schema with empty examples array
echo -n "Test 4: Generate from schema with empty examples array... "
result=$(jq -c -f "$TRANSFORM" --arg format "json" "$SCRIPT_DIR/test-input-3.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Handle null value in output (CRITICAL falsy value test)
echo -n "Test 5: Handle null value in output... "
result=$(jq -c -f "$TRANSFORM" --arg format "json" "$SCRIPT_DIR/test-input-4.json" | jq '.[0].expected')
expected='null'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Handle boolean false in output (CRITICAL falsy value test)
echo -n "Test 6: Handle boolean false in output... "
result=$(jq -c -f "$TRANSFORM" --arg format "json" "$SCRIPT_DIR/test-input-5.json" | jq '.[0].expected')
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Handle zero in output (CRITICAL falsy value test)
echo -n "Test 7: Handle zero in output... "
result=$(jq -c -f "$TRANSFORM" --arg format "json" "$SCRIPT_DIR/test-input-6.json" | jq '.[0].expected')
expected='0'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Handle empty string in output (CRITICAL falsy value test)
echo -n "Test 8: Handle empty string in output... "
result=$(jq -c -f "$TRANSFORM" --arg format "json" "$SCRIPT_DIR/test-input-7.json" | jq '.[0].expected')
expected='""'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Handle empty array in output (CRITICAL falsy value test)
echo -n "Test 9: Handle empty array in output... "
result=$(jq -c -f "$TRANSFORM" --arg format "json" "$SCRIPT_DIR/test-input-8.json" | jq '.[0].expected')
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Handle empty object in output (CRITICAL falsy value test)
echo -n "Test 10: Handle empty object in output... "
result=$(jq -c -f "$TRANSFORM" --arg format "json" "$SCRIPT_DIR/test-input-9.json" | jq '.[0].expected')
expected='{}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Handle examples without args field
echo -n "Test 11: Handle examples without args field... "
result=$(jq -c -f "$TRANSFORM" --arg format "json" "$SCRIPT_DIR/test-input-10.json" | jq '.[0].args')
expected='{}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Generate test with number output
echo -n "Test 12: Generate test with number output... "
result=$(jq -c -f "$TRANSFORM" --arg format "json" "$SCRIPT_DIR/test-input-11.json" | jq '.[0].expected')
expected='42'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Generate test with array output (should use -c flag in bash)
echo -n "Test 13: Generate test with array output... "
result=$(jq -r -f "$TRANSFORM" --arg format "bash" "$SCRIPT_DIR/test-input-12.json" | grep -c "jq -c -f")
expected='1'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected (should contain 'jq -c -f' for array output)"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Generate test with multiple arguments
echo -n "Test 14: Generate test with multiple arguments... "
result=$(jq -c -f "$TRANSFORM" --arg format "json" "$SCRIPT_DIR/test-input-13.json" | jq '.[0].args | length')
expected='3'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 15: Generate test with complex nested input
echo -n "Test 15: Generate test with complex nested input... "
result=$(jq -c -f "$TRANSFORM" --arg format "json" "$SCRIPT_DIR/test-input-14.json" | jq -c '.[0].input.level1.level2.level3.data')
expected='[1,2,3]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 16: Error on missing required field (name)
echo -n "Test 16: Error on missing required field (name)... "
result=$(jq -f "$TRANSFORM" "$SCRIPT_DIR/test-input-15.json" 2>&1 || echo "error")
if [[ "$result" == *"error"* ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: error message"
    echo "  Got: $result"
    exit 1
fi

# Test 17: Default format is bash when not specified
echo -n "Test 17: Default format is bash when not specified... "
result=$(jq -r -f "$TRANSFORM" "$SCRIPT_DIR/test-input-1.json" | head -1)
expected='#!/usr/bin/env bash'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All test-generator tests passed!"
