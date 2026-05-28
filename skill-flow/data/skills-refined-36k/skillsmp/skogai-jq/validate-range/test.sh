#!/usr/bin/env bash
set -euo pipefail

# Test validate-range transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing validate-range transformation..."

# Test 1: Valid value within inclusive range
echo -n "Test 1: Valid value within inclusive range (30 in [0,120])... "
result=$(jq -f "$TRANSFORM" --arg path "user.age" --arg min "0" --arg max "120" "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Valid value in middle of range
echo -n "Test 2: Valid decimal value in range (25.5 in [0,100])... "
result=$(jq -f "$TRANSFORM" --arg path "sensor.temp" --arg min "0" --arg max "100" "$SCRIPT_DIR/test-input-2.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Value exactly at max boundary (inclusive)
echo -n "Test 3: Value exactly at max boundary inclusive (100 in [0,100])... "
result=$(jq -f "$TRANSFORM" --arg path "test.score" --arg min "0" --arg max "100" "$SCRIPT_DIR/test-input-3.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Value exactly at min boundary (inclusive) - zero is valid!
echo -n "Test 4: Value exactly at min boundary inclusive (0 in [0,100])... "
result=$(jq -f "$TRANSFORM" --arg path "test.score" --arg min "0" --arg max "100" "$SCRIPT_DIR/test-input-4.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Value above max (out of range)
echo -n "Test 5: Value above max (101 not in [0,100])... "
result=$(jq -f "$TRANSFORM" --arg path "test.score" --arg min "0" --arg max "100" "$SCRIPT_DIR/test-input-5.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Value below min (out of range)
echo -n "Test 6: Value below min (-1 not in [0,100])... "
result=$(jq -f "$TRANSFORM" --arg path "test.score" --arg min "0" --arg max "100" "$SCRIPT_DIR/test-input-6.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Exclusive range - value at boundary fails
echo -n "Test 7: Exclusive range - value at boundary fails (0 not in (0,100))... "
result=$(jq -f "$TRANSFORM" --arg path "sensor.temp" --arg min "0" --arg max "100" --arg exclusive "true" "$SCRIPT_DIR/test-input-7.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Exclusive range - value just inside boundary passes
echo -n "Test 8: Exclusive range - value just inside boundary passes (0.1 in (0,100))... "
result=$(jq -f "$TRANSFORM" --arg path "sensor.temp" --arg min "0" --arg max "100" --arg exclusive "true" "$SCRIPT_DIR/test-input-8.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Non-existent path returns true
echo -n "Test 9: Non-existent path returns true... "
result=$(jq -f "$TRANSFORM" --arg path "user.age" --arg min "0" --arg max "120" "$SCRIPT_DIR/test-input-9.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Non-numeric value (string) returns false
echo -n "Test 10: Non-numeric value (string) returns false... "
result=$(jq -f "$TRANSFORM" --arg path "user.age" --arg min "0" --arg max "120" "$SCRIPT_DIR/test-input-10.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Null value returns true (path doesn't exist)
echo -n "Test 11: Null value returns true (path doesn't exist)... "
result=$(jq -f "$TRANSFORM" --arg path "user.age" --arg min "0" --arg max "120" "$SCRIPT_DIR/test-input-11.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Boolean false value returns false (not a number)
echo -n "Test 12: Boolean false value returns false (not a number)... "
result=$(jq -f "$TRANSFORM" --arg path "user.age" --arg min "0" --arg max "120" "$SCRIPT_DIR/test-input-12.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Only min boundary (unbounded max)
echo -n "Test 13: Only min boundary - valid (50 >= 0)... "
result=$(jq -f "$TRANSFORM" --arg path "product.quantity" --arg min "0" "$SCRIPT_DIR/test-input-13.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Only min boundary (unbounded max) - invalid
echo -n "Test 14: Only min boundary - invalid (-10 < 0)... "
result=$(jq -f "$TRANSFORM" --arg path "product.quantity" --arg min "0" "$SCRIPT_DIR/test-input-14.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 15: Empty object returns true
echo -n "Test 15: Empty object returns true... "
result=$(jq -f "$TRANSFORM" --arg path "user.age" --arg min "0" --arg max "120" "$SCRIPT_DIR/test-input-15.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 16: Array value returns false (not a number)
echo -n "Test 16: Array value returns false (not a number)... "
result=$(jq -f "$TRANSFORM" --arg path "user.age" --arg min "0" --arg max "120" "$SCRIPT_DIR/test-input-16.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 17: Object value returns false (not a number)
echo -n "Test 17: Object value returns false (not a number)... "
result=$(jq -f "$TRANSFORM" --arg path "user.age" --arg min "0" --arg max "120" "$SCRIPT_DIR/test-input-17.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All validate-range tests passed!"
