#!/usr/bin/env bash
set -euo pipefail

# Test validate-format transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing validate-format transformation..."

# Test 1: Valid email format
echo -n "Test 1: Valid email format... "
result=$(jq -c -f "$TRANSFORM" --arg path "email" --arg format "email" "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Invalid email format
echo -n "Test 2: Invalid email format... "
result=$(jq -c -f "$TRANSFORM" --arg path "email" --arg format "email" "$SCRIPT_DIR/test-input-2.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Valid URL format (https)
echo -n "Test 3: Valid URL format (https)... "
result=$(jq -c -f "$TRANSFORM" --arg path "url" --arg format "url" "$SCRIPT_DIR/test-input-3.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Valid URL format (http with port and path)
echo -n "Test 4: Valid URL format (http with port and path)... "
result=$(jq -c -f "$TRANSFORM" --arg path "url" --arg format "url" "$SCRIPT_DIR/test-input-4.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Invalid URL format
echo -n "Test 5: Invalid URL format... "
result=$(jq -c -f "$TRANSFORM" --arg path "url" --arg format "url" "$SCRIPT_DIR/test-input-5.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Valid UUID format (lowercase)
echo -n "Test 6: Valid UUID format (lowercase)... "
result=$(jq -c -f "$TRANSFORM" --arg path "id" --arg format "uuid" "$SCRIPT_DIR/test-input-6.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Valid UUID format (uppercase)
echo -n "Test 7: Valid UUID format (uppercase)... "
result=$(jq -c -f "$TRANSFORM" --arg path "id" --arg format "uuid" "$SCRIPT_DIR/test-input-7.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Invalid UUID format
echo -n "Test 8: Invalid UUID format... "
result=$(jq -c -f "$TRANSFORM" --arg path "id" --arg format "uuid" "$SCRIPT_DIR/test-input-8.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Valid timestamp format (basic with timezone)
echo -n "Test 9: Valid timestamp format (basic with timezone)... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" --arg format "timestamp" "$SCRIPT_DIR/test-input-9.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Valid timestamp format (with microseconds)
echo -n "Test 10: Valid timestamp format (with microseconds)... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" --arg format "timestamp" "$SCRIPT_DIR/test-input-10.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Valid timestamp format (date only matches timestamp pattern)
echo -n "Test 11: Date matches timestamp pattern... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" --arg format "timestamp" "$SCRIPT_DIR/test-input-11.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Invalid timestamp format
echo -n "Test 12: Invalid timestamp format... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" --arg format "timestamp" "$SCRIPT_DIR/test-input-12.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Valid date format
echo -n "Test 13: Valid date format... "
result=$(jq -c -f "$TRANSFORM" --arg path "date" --arg format "date" "$SCRIPT_DIR/test-input-13.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Timestamp doesn't match strict date format
echo -n "Test 14: Timestamp doesn't match strict date format... "
result=$(jq -c -f "$TRANSFORM" --arg path "date" --arg format "date" "$SCRIPT_DIR/test-input-14.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 15: Null value returns false (edge case)
echo -n "Test 15: Null value returns false (edge case)... "
result=$(jq -c -f "$TRANSFORM" --arg path "email" --arg format "email" "$SCRIPT_DIR/test-input-15.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 16: Boolean false value returns false (edge case)
echo -n "Test 16: Boolean false value returns false (edge case)... "
result=$(jq -c -f "$TRANSFORM" --arg path "email" --arg format "email" "$SCRIPT_DIR/test-input-16.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 17: Number 0 value returns false (edge case)
echo -n "Test 17: Number 0 value returns false (edge case)... "
result=$(jq -c -f "$TRANSFORM" --arg path "email" --arg format "email" "$SCRIPT_DIR/test-input-17.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 18: Empty string returns false (edge case)
echo -n "Test 18: Empty string returns false (edge case)... "
result=$(jq -c -f "$TRANSFORM" --arg path "email" --arg format "email" "$SCRIPT_DIR/test-input-18.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 19: Field doesn't exist returns false
echo -n "Test 19: Field doesn't exist returns false... "
result=$(jq -c -f "$TRANSFORM" --arg path "email" --arg format "email" "$SCRIPT_DIR/test-input-19.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 20: Nested path validation
echo -n "Test 20: Nested path validation... "
result=$(jq -c -f "$TRANSFORM" --arg path "user.email" --arg format "email" "$SCRIPT_DIR/test-input-20.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 21: Complex email with tags and subdomains
echo -n "Test 21: Complex email with tags and subdomains... "
result=$(jq -c -f "$TRANSFORM" --arg path "email" --arg format "email" "$SCRIPT_DIR/test-input-21.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 22: Unknown format returns false
echo -n "Test 22: Unknown format returns false... "
result=$(jq -c -f "$TRANSFORM" --arg path "url" --arg format "unknown" "$SCRIPT_DIR/test-input-3.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All validate-format tests passed!"
