#!/usr/bin/env bash
set -euo pipefail

# Test has-code-block transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing has-code-block transformation..."

# Test 1: Has single code block (true)
echo -n "Test 1: Has single code block... "
result=$(jq -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Has multiple code blocks (true)
echo -n "Test 2: Has multiple code blocks... "
result=$(jq -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-2.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Has inline code only (false)
echo -n "Test 3: Has inline code only (false)... "
result=$(jq -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-3.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: No code blocks (false)
echo -n "Test 4: No code blocks (false)... "
result=$(jq -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-4.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Empty string (false)
echo -n "Test 5: Empty string (false)... "
result=$(jq -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-5.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Code block with language tag (true)
echo -n "Test 6: Code block with language tag (true)... "
result=$(jq -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-6.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Partial code block (false)
echo -n "Test 7: Partial code block (false)... "
result=$(jq -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-7.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Field doesn't exist (false)
echo -n "Test 8: Field doesn't exist (false)... "
result=$(jq -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-8.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Field is not a string (false)
echo -n "Test 9: Field is not a string (false)... "
result=$(jq -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-9.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Nested path (true)
echo -n "Test 10: Nested path (true)... "
result=$(jq -f "$TRANSFORM" --arg path "nested.content" "$SCRIPT_DIR/test-input-10.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Field is null (false)
echo -n "Test 11: Field is null (false)... "
result=$(jq -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-11.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Field is boolean (false)
echo -n "Test 12: Field is boolean (false)... "
result=$(jq -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-12.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Field is array (false)
echo -n "Test 13: Field is array (false)... "
result=$(jq -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-13.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All has-code-block tests passed!"
