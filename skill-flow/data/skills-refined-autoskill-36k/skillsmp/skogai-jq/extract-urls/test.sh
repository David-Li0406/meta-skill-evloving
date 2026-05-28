#!/usr/bin/env bash
set -euo pipefail

# Test extract-urls transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing extract-urls transformation..."

# Test 1: Single HTTP URL
echo -n "Test 1: Single HTTP URL... "
result=$(jq -c -f "$TRANSFORM" --arg path "text" "$SCRIPT_DIR/test-input-1.json")
expected='["http://example.com"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Multiple URLs (http, https, ftp)
echo -n "Test 2: Multiple URLs (http, https, ftp)... "
result=$(jq -c -f "$TRANSFORM" --arg path "content" "$SCRIPT_DIR/test-input-2.json")
expected='["https://google.com","http://github.com","ftp://files.example.org"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: HTTPS URL with query parameters
echo -n "Test 3: HTTPS URL with query parameters... "
result=$(jq -c -f "$TRANSFORM" --arg path "data" "$SCRIPT_DIR/test-input-3.json")
expected='["https://api.example.com/v1?key=abc&id=123"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: No URLs - empty array
echo -n "Test 4: No URLs - empty array... "
result=$(jq -c -f "$TRANSFORM" --arg path "text" "$SCRIPT_DIR/test-input-4.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: URL with fragment (#)
echo -n "Test 5: URL with fragment (#)... "
result=$(jq -c -f "$TRANSFORM" --arg path "url" "$SCRIPT_DIR/test-input-5.json")
expected='["https://example.com/path#section"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: URL in markdown link
echo -n "Test 6: URL in markdown link... "
result=$(jq -c -f "$TRANSFORM" --arg path "markdown" "$SCRIPT_DIR/test-input-6.json")
expected='["https://docs.example.com/guide"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Empty string - empty array
echo -n "Test 7: Empty string - empty array... "
result=$(jq -c -f "$TRANSFORM" --arg path "text" "$SCRIPT_DIR/test-input-7.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Field doesn't exist - empty array
echo -n "Test 8: Field doesn't exist - empty array... "
result=$(jq -c -f "$TRANSFORM" --arg path "text" "$SCRIPT_DIR/test-input-8.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Nested path
echo -n "Test 9: Nested path... "
result=$(jq -c -f "$TRANSFORM" --arg path "nested.text" "$SCRIPT_DIR/test-input-9.json")
expected='["https://nested.example.com/path"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Field is number - empty array
echo -n "Test 10: Field is number - empty array... "
result=$(jq -c -f "$TRANSFORM" --arg path "text" "$SCRIPT_DIR/test-input-10.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Field is null - empty array
echo -n "Test 11: Field is null - empty array... "
result=$(jq -c -f "$TRANSFORM" --arg path "text" "$SCRIPT_DIR/test-input-11.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Field is boolean - empty array
echo -n "Test 12: Field is boolean - empty array... "
result=$(jq -c -f "$TRANSFORM" --arg path "text" "$SCRIPT_DIR/test-input-12.json")
expected='[]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: FTP URL
echo -n "Test 13: FTP URL... "
result=$(jq -c -f "$TRANSFORM" --arg path "text" "$SCRIPT_DIR/test-input-13.json")
expected='["ftp://files.example.org/download/file.zip"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Uppercase scheme (case insensitive)
echo -n "Test 14: Uppercase scheme (case insensitive)... "
result=$(jq -c -f "$TRANSFORM" --arg path "text" "$SCRIPT_DIR/test-input-14.json")
expected='["HTTPS://UPPERCASE.COM/PATH"]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All extract-urls tests passed!"
