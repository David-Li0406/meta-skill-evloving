#!/usr/bin/env bash
set -euo pipefail

# Test normalize-timestamp transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing normalize-timestamp transformation..."

# Test 1: ISO 8601 already normalized (pass through)
echo -n "Test 1: ISO 8601 already normalized (pass through)... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-1.json")
expected='{"timestamp":"2024-01-15T10:30:00Z"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Unix timestamp (seconds)
echo -n "Test 2: Unix timestamp (seconds)... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-2.json")
expected='{"timestamp":"2024-01-15T10:30:00Z"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Unix timestamp (milliseconds)
echo -n "Test 3: Unix timestamp (milliseconds)... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-3.json")
expected='{"timestamp":"2024-01-15T10:30:00Z"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Date-only format (adds time component)
echo -n "Test 4: Date-only format (adds time component)... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-4.json")
expected='{"timestamp":"2024-01-15T00:00:00Z"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Invalid timestamp (returns original)
echo -n "Test 5: Invalid timestamp (returns original)... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-5.json")
expected='{"timestamp":"not-a-timestamp"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Null value
echo -n "Test 6: Null value... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-6.json")
expected='{"timestamp":null}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Empty string
echo -n "Test 7: Empty string... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-7.json")
expected='{"timestamp":""}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Field doesn't exist (returns null)
echo -n "Test 8: Field doesn't exist (returns null)... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-8.json")
expected='{"other":"value","timestamp":null}'
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
result=$(jq -c -f "$TRANSFORM" --arg path "user.created_at" "$SCRIPT_DIR/test-input-9.json")
expected='{"user":{"created_at":"2024-01-15T10:30:00Z"}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: String ISO 8601 with milliseconds (pass through)
echo -n "Test 10: String ISO 8601 with milliseconds (pass through)... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-10.json")
expected='{"timestamp":"2024-01-15T10:30:00.123Z"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Boolean false (returns null)
echo -n "Test 11: Boolean false (returns null)... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-11.json")
expected='{"timestamp":null}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Zero value (epoch time)
echo -n "Test 12: Zero value (epoch time)... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-12.json")
expected='{"timestamp":"1970-01-01T00:00:00Z"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Empty array (returns null)
echo -n "Test 13: Empty array (returns null)... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-13.json")
expected='{"timestamp":null}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Empty object (returns null)
echo -n "Test 14: Empty object (returns null)... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-14.json")
expected='{"timestamp":null}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 15: String containing unix timestamp (converts)
echo -n "Test 15: String containing unix timestamp (converts)... "
result=$(jq -c -f "$TRANSFORM" --arg path "timestamp" "$SCRIPT_DIR/test-input-15.json")
expected='{"timestamp":"2024-01-15T10:30:00Z"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All normalize-timestamp tests passed!"
