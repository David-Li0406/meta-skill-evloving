#!/usr/bin/env bash
set -euo pipefail

# Test string-truncate transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing string-truncate transformation..."

# Test 1: Truncate long string (longer than max)
echo -n "Test 1: Truncate long string (longer than max)... "
result=$(jq -c -f "$TRANSFORM" --arg path "bio" --argjson max_length 10 "$SCRIPT_DIR/test-input-1.json")
expected='{"bio":"This is a "}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Short string unchanged (shorter than max)
echo -n "Test 2: Short string unchanged (shorter than max)... "
result=$(jq -c -f "$TRANSFORM" --arg path "bio" --argjson max_length 10 "$SCRIPT_DIR/test-input-2.json")
expected='{"bio":"Short"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: String exactly max length (should not be truncated)
echo -n "Test 3: String exactly max length (should not be truncated)... "
result=$(jq -c -f "$TRANSFORM" --arg path "bio" --argjson max_length 10 "$SCRIPT_DIR/test-input-3.json")
expected='{"bio":"Exactly10C"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Empty string unchanged
echo -n "Test 4: Empty string unchanged... "
result=$(jq -c -f "$TRANSFORM" --arg path "bio" --argjson max_length 10 "$SCRIPT_DIR/test-input-4.json")
expected='{"bio":""}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Max length 0 (truncate to empty)
echo -n "Test 5: Max length 0 (truncate to empty)... "
result=$(jq -c -f "$TRANSFORM" --arg path "bio" --argjson max_length 0 "$SCRIPT_DIR/test-input-1.json")
expected='{"bio":""}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: With ellipsis enabled (adds "..." to truncated strings)
echo -n "Test 6: With ellipsis enabled (adds ... to truncated strings)... "
result=$(jq -c -f "$TRANSFORM" --arg path "bio" --argjson max_length 10 --arg ellipsis "true" "$SCRIPT_DIR/test-input-5.json")
expected='{"bio":"Testing..."}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Without ellipsis (default behavior)
echo -n "Test 7: Without ellipsis (default behavior)... "
result=$(jq -c -f "$TRANSFORM" --arg path "bio" --argjson max_length 10 "$SCRIPT_DIR/test-input-5.json")
expected='{"bio":"Testing wi"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Unicode characters (count correctly)
echo -n "Test 8: Unicode characters (count correctly)... "
result=$(jq -c -f "$TRANSFORM" --arg path "bio" --argjson max_length 10 "$SCRIPT_DIR/test-input-6.json")
expected='{"bio":"Unicode te"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Field doesn't exist (return unchanged)
echo -n "Test 9: Field doesn't exist (return unchanged)... "
result=$(jq -c -f "$TRANSFORM" --arg path "bio" --argjson max_length 10 "$SCRIPT_DIR/test-input-7.json")
expected='{"other":"field"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Field is not a string (return unchanged)
echo -n "Test 10: Field is not a string (return unchanged)... "
result=$(jq -c -f "$TRANSFORM" --arg path "bio" --argjson max_length 10 "$SCRIPT_DIR/test-input-8.json")
expected='{"bio":12345}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Nested path truncation
echo -n "Test 11: Nested path truncation... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.description" --argjson max_length 12 "$SCRIPT_DIR/test-input-9.json")
expected='{"user":{"description":"Nested field"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Ellipsis with very short max_length (less than 3)
echo -n "Test 12: Ellipsis with very short max_length (less than 3)... "
result=$(jq -c -f "$TRANSFORM" --arg path "bio" --argjson max_length 2 --arg ellipsis "true" "$SCRIPT_DIR/test-input-10.json")
expected='{"bio":".."}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Ellipsis doesn't exceed max_length
echo -n "Test 13: Ellipsis doesn't exceed max_length... "
result=$(jq -c -f "$TRANSFORM" --arg path "bio" --argjson max_length 7 --arg ellipsis "true" "$SCRIPT_DIR/test-input-1.json")
expected='{"bio":"This..."}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Null value (return unchanged)
echo -n "Test 14: Null value (return unchanged)... "
result=$(jq -c -f "$TRANSFORM" --arg path "bio" --argjson max_length 10 "$SCRIPT_DIR/test-input-11.json")
expected='{"bio":null}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 15: Boolean value (return unchanged)
echo -n "Test 15: Boolean value (return unchanged)... "
result=$(jq -c -f "$TRANSFORM" --arg path "bio" --argjson max_length 10 "$SCRIPT_DIR/test-input-12.json")
expected='{"bio":false}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All string-truncate tests passed!"
