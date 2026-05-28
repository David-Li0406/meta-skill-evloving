#!/usr/bin/env bash
set -euo pipefail

# Test filter-by-role transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing filter-by-role transformation..."

# Test 1: Filter user messages (happy path)
echo -n "Test 1: Filter user messages... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-1.json")
expected='{"messages":[{"role":"user","content":"Hello"},{"role":"user","content":"How are you?"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Filter assistant messages (happy path)
echo -n "Test 2: Filter assistant messages... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "assistant" "$SCRIPT_DIR/test-input-2.json")
expected='{"messages":[{"role":"assistant","content":"Hi there"},{"role":"assistant","content":"I'\''m doing well"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Filter system messages (happy path)
echo -n "Test 3: Filter system messages... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "system" "$SCRIPT_DIR/test-input-3.json")
expected='{"messages":[{"role":"system","content":"You are a helpful assistant"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Empty array (boundary condition)
echo -n "Test 4: Empty array... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-4.json")
expected='{"messages":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: All messages match same role
echo -n "Test 5: All messages match same role... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-5.json")
expected='{"messages":[{"role":"user","content":"Message 1"},{"role":"user","content":"Message 2"},{"role":"user","content":"Message 3"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: No matches (filter returns empty array)
echo -n "Test 6: No matches... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "system" "$SCRIPT_DIR/test-input-6.json")
expected='{"messages":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Non-array field (type safety - returns original)
echo -n "Test 7: Non-array field... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "data" --arg role "user" "$SCRIPT_DIR/test-input-7.json")
expected='{"data":"not-an-array"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Content with null value (falsy value)
echo -n "Test 8: Content with null value... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-8.json")
expected='{"messages":[{"role":"user","content":null},{"role":"user","content":"Test"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Content with false/0 values (falsy values)
echo -n "Test 9: Content with false/0 values... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-9.json")
expected='{"messages":[{"role":"user","content":false},{"role":"user","content":0}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Content with empty string (falsy value)
echo -n "Test 10: Content with empty string... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-10.json")
expected='{"messages":[{"role":"user","content":""},{"role":"user","content":"More"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Missing content field
echo -n "Test 11: Missing content field... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-11.json")
expected='{"messages":[{"role":"user"},{"role":"user","extra":"field"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Mixed types in array (primitives + objects)
echo -n "Test 12: Mixed types in array... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-12.json")
expected='{"messages":[{"role":"user","content":"Hello"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Non-existent array path (type safety - returns original)
echo -n "Test 13: Non-existent array path... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-13.json")
expected='{}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Content with various JSON types (objects, arrays, strings)
echo -n "Test 14: Content with various JSON types... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-14.json")
expected='{"messages":[{"role":"user","content":{"nested":"object"}},{"role":"user","content":"string"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 15: Missing role field in objects
echo -n "Test 15: Missing role field in objects... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "messages" --arg role "user" "$SCRIPT_DIR/test-input-15.json")
expected='{"messages":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All filter-by-role tests passed!"
