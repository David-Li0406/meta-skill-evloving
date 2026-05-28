#!/usr/bin/env bash
set -euo pipefail

# Test extract-code-blocks transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing extract-code-blocks transformation..."

# Test 1: Extract single code block
echo -n "Test 1: Extract single code block... "
result=$(jq -c -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-1.json")
expected='["```js\ncode\n```"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Extract multiple code blocks
echo -n "Test 2: Extract multiple code blocks... "
result=$(jq -c -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-2.json")
expected='["```python\nprint('\''hello'\'')\n```","```js\nconsole.log()\n```"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Extract from nested path
echo -n "Test 3: Extract from nested path... "
result=$(jq -c -f "$TRANSFORM" --arg path "nested.content" "$SCRIPT_DIR/test-input-3.json")
expected='["```rust\nfn main() {}\n```"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: No code blocks returns empty array
echo -n "Test 4: No code blocks returns empty array... "
result=$(jq -c -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-4.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Empty string returns empty array
echo -n "Test 5: Empty string returns empty array... "
result=$(jq -c -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-5.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Multiple blocks with and without language
echo -n "Test 6: Multiple blocks with and without language... "
result=$(jq -c -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-6.json")
expected='["```bash\nls -la\n```","```\nno language\n```","```python\n# nested\n```"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Code blocks with special characters
echo -n "Test 7: Code blocks with special characters... "
result=$(jq -c -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-7.json")
expected='["```special\n$var @symbol #hash\n```"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Field doesn't exist returns empty array
echo -n "Test 8: Field doesn't exist returns empty array... "
result=$(jq -c -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-8.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Field is not a string (number) returns empty array
echo -n "Test 9: Field is not a string (number) returns empty array... "
result=$(jq -c -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-9.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Field is null returns empty array
echo -n "Test 10: Field is null returns empty array... "
result=$(jq -c -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-10.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Field is boolean returns empty array
echo -n "Test 11: Field is boolean returns empty array... "
result=$(jq -c -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-11.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Field is array returns empty array
echo -n "Test 12: Field is array returns empty array... "
result=$(jq -c -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-12.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All extract-code-blocks tests passed!"
