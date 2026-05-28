#!/usr/bin/env bash
set -euo pipefail

# Test validate-types transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing validate-types transformation..."

# Test 1: All fields match types - happy path
echo -n "Test 1: All fields match types - happy path... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"name":"string","age":"number","active":"boolean"}' "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: One field wrong type (string instead of number)
echo -n "Test 2: One field wrong type (string instead of number)... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"name":"string","age":"number"}' "$SCRIPT_DIR/test-input-2.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: String type validation
echo -n "Test 3: String type validation... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"name":"string"}' "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Number type validation (integer)
echo -n "Test 4: Number type validation (integer)... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"age":"number"}' "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Number type validation (decimal)
echo -n "Test 5: Number type validation (decimal)... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"score":"number"}' "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Boolean type validation (true)
echo -n "Test 6: Boolean type validation (true)... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"active":"boolean"}' "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Boolean type validation (false)
echo -n "Test 7: Boolean type validation (false)... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"enabled":"boolean"}' "$SCRIPT_DIR/test-input-4.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Array type validation
echo -n "Test 8: Array type validation... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"tags":"array"}' "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Object type validation
echo -n "Test 9: Object type validation... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"profile":"object"}' "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Null type validation
echo -n "Test 10: Null type validation... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"value":"null"}' "$SCRIPT_DIR/test-input-4.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Field doesn't exist (returns false)
echo -n "Test 11: Field doesn't exist (returns false)... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"missing":"string"}' "$SCRIPT_DIR/test-input-1.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Empty type rules (returns true)
echo -n "Test 12: Empty type rules (returns true)... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{}' "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Nested field validation (all match)
echo -n "Test 13: Nested field validation (all match)... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"user.name":"string","user.profile.age":"number"}' "$SCRIPT_DIR/test-input-3.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 14: Nested field with wrong type
echo -n "Test 14: Nested field with wrong type... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"user.name":"number"}' "$SCRIPT_DIR/test-input-3.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 15: All JSON types in single object
echo -n "Test 15: All JSON types in single object... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"string_field":"string","number_field":"number","bool_field":"boolean","null_field":"null","array_field":"array","object_field":"object"}' "$SCRIPT_DIR/test-input-7.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 16: Boolean false is not null (edge case)
echo -n "Test 16: Boolean false is not null (edge case)... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"enabled":"null"}' "$SCRIPT_DIR/test-input-4.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 17: Number 0 is not null (edge case)
echo -n "Test 17: Number 0 is not null (edge case)... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"count":"number"}' "$SCRIPT_DIR/test-input-4.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 18: Empty string is not null (edge case)
echo -n "Test 18: Empty string is not null (edge case)... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"empty":"string"}' "$SCRIPT_DIR/test-input-4.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 19: Empty array is array type (edge case)
echo -n "Test 19: Empty array is array type (edge case)... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"items":"array"}' "$SCRIPT_DIR/test-input-4.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 20: Empty object is object type (edge case)
echo -n "Test 20: Empty object is object type (edge case)... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"data":"object"}' "$SCRIPT_DIR/test-input-4.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 21: Multiple fields with mixed match (some pass, one fails = overall false)
echo -n "Test 21: Multiple fields with mixed match (some pass, one fails)... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"items":"array","config":"string"}' "$SCRIPT_DIR/test-input-5.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 22: Empty object input with empty rules (edge case)
echo -n "Test 22: Empty object input with empty rules (edge case)... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{}' "$SCRIPT_DIR/test-input-8.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 23: Empty object input with field requirement (fails)
echo -n "Test 23: Empty object input with field requirement (fails)... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"title":"string"}' "$SCRIPT_DIR/test-input-8.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 24: Malformed type_rules JSON (returns true - safe fallback)
echo -n "Test 24: Malformed type_rules JSON (returns true - safe fallback)... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{invalid json' "$SCRIPT_DIR/test-input-1.json")
expected='true'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 25: Case sensitivity of types (number vs Number)
echo -n "Test 25: Wrong type case (Number vs number) fails... "
result=$(jq -c -f "$TRANSFORM" --arg type_rules '{"age":"Number"}' "$SCRIPT_DIR/test-input-1.json")
expected='false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All validate-types tests passed!"
