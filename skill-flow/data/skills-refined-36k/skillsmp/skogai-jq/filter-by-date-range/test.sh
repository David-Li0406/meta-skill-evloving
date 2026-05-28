#!/usr/bin/env bash
set -euo pipefail

# Test filter-by-date-range transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing filter-by-date-range transformation..."

# Test 1: Filter within range (happy path)
echo -n "Test 1: Filter events within date range... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "events" --arg date_field "created_at" --arg start_date "2024-02-01" --arg end_date "2024-02-28" "$SCRIPT_DIR/test-input-1.json")
expected='{"events":[{"name":"Event B","created_at":"2024-02-20"},{"name":"Event D","created_at":"2024-02-05"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Filter excluding boundaries
echo -n "Test 2: Filter excluding boundaries... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "events" --arg date_field "created_at" --arg start_date "2024-02-02" --arg end_date "2024-02-27" "$SCRIPT_DIR/test-input-2.json")
expected='{"events":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Filter including boundaries
echo -n "Test 3: Filter including boundaries... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "events" --arg date_field "created_at" --arg start_date "2024-02-01" --arg end_date "2024-02-28" "$SCRIPT_DIR/test-input-3.json")
expected='{"events":[{"name":"Event A","created_at":"2024-02-01"},{"name":"Event B","created_at":"2024-02-15"},{"name":"Event C","created_at":"2024-02-28"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Empty array
echo -n "Test 4: Empty array... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "events" --arg date_field "created_at" --arg start_date "2024-02-01" --arg end_date "2024-02-28" "$SCRIPT_DIR/test-input-4.json")
expected='{"events":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: No matches (empty result)
echo -n "Test 5: No matches (empty result)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "events" --arg date_field "created_at" --arg start_date "2024-02-01" --arg end_date "2024-02-28" "$SCRIPT_DIR/test-input-5.json")
expected='{"events":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: All match
echo -n "Test 6: All match... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "events" --arg date_field "created_at" --arg start_date "2024-02-01" --arg end_date "2024-02-28" "$SCRIPT_DIR/test-input-6.json")
expected='{"events":[{"name":"Event A","created_at":"2024-02-10"},{"name":"Event B","created_at":"2024-02-15"},{"name":"Event C","created_at":"2024-02-20"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Invalid date format (skip gracefully)
echo -n "Test 7: Invalid date format (skip gracefully)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "events" --arg date_field "created_at" --arg start_date "2024-02-01" --arg end_date "2024-02-28" "$SCRIPT_DIR/test-input-7.json")
expected='{"events":[{"name":"Event A","created_at":"2024-02-15"},{"name":"Event C","created_at":"2024-02-20"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Missing date field in some objects
echo -n "Test 8: Missing date field in some objects... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "events" --arg date_field "created_at" --arg start_date "2024-02-01" --arg end_date "2024-02-28" "$SCRIPT_DIR/test-input-8.json")
expected='{"events":[{"name":"Event A","created_at":"2024-02-15"},{"name":"Event C","created_at":"2024-02-20"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Null date values
echo -n "Test 9: Null date values... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "events" --arg date_field "created_at" --arg start_date "2024-02-01" --arg end_date "2024-02-28" "$SCRIPT_DIR/test-input-9.json")
expected='{"events":[{"name":"Event B","created_at":"2024-02-15"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Start date only (no end)
echo -n "Test 10: Start date only (no end)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "events" --arg date_field "created_at" --arg start_date "2024-06-01" "$SCRIPT_DIR/test-input-10.json")
expected='{"events":[{"name":"Event A","created_at":"2024-06-15"},{"name":"Event B","created_at":"2024-12-31"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Nested path (data.events)
echo -n "Test 11: Nested path (data.events)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "data.events" --arg date_field "created_at" --arg start_date "2024-02-01" --arg end_date "2024-02-28" "$SCRIPT_DIR/test-input-11.json")
expected='{"data":{"events":[{"name":"Event A","created_at":"2024-02-10"},{"name":"Event B","created_at":"2024-02-20"}]}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Non-array field (type safety)
echo -n "Test 12: Non-array field (type safety)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "events" --arg date_field "created_at" --arg start_date "2024-02-01" --arg end_date "2024-02-28" "$SCRIPT_DIR/test-input-12.json")
expected='{"events":"not-an-array"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: ISO 8601 datetime format (with time component)
echo -n "Test 13: ISO 8601 datetime format (with time)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "events" --arg date_field "created_at" --arg start_date "2024-06-01" --arg end_date "2024-12-01" "$SCRIPT_DIR/test-input-13.json")
expected='{"events":[{"name":"Event B","created_at":"2024-06-15T14:30:00Z"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Number date field (type safety - should skip)
echo -n "Test 14: Number date field (type safety)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "events" --arg date_field "created_at" --arg start_date "2024-02-01" --arg end_date "2024-02-28" "$SCRIPT_DIR/test-input-14.json")
expected='{"events":[{"name":"Event B","created_at":"2024-02-15"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All filter-by-date-range tests passed!"
