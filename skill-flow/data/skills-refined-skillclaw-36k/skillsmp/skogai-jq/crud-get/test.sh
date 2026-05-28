#!/usr/bin/env bash
set -euo pipefail

# Test crud-get transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing crud-get transformation..."

# Test 1: Get existing nested value
echo -n "Test 1: Get existing nested value... "
result=$(jq -f "$TRANSFORM" --arg path "user.name" "$SCRIPT_DIR/test-input-1.json")
expected='"skogix"'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Get deeply nested value
echo -n "Test 2: Get deeply nested value... "
result=$(jq -f "$TRANSFORM" --arg path "user.profile.age" "$SCRIPT_DIR/test-input-1.json")
expected='30'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Get non-existent path with default
echo -n "Test 3: Get non-existent path with default... "
result=$(jq -f "$TRANSFORM" --arg path "user.phone" --arg default "unknown" "$SCRIPT_DIR/test-input-2.json")
expected='"unknown"'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Get non-existent path without default (returns null)
echo -n "Test 4: Get non-existent path without default... "
result=$(jq -f "$TRANSFORM" --arg path "user.email" "$SCRIPT_DIR/test-input-2.json")
expected='null'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Get array value
echo -n "Test 5: Get array value... "
result=$(jq -c -f "$TRANSFORM" --arg path "data.items" "$SCRIPT_DIR/test-input-3.json")
expected='[1,2,3]'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All crud-get tests passed!"
