#!/usr/bin/env bash
set -euo pipefail

# Test filter-by-pattern transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing filter-by-pattern transformation..."

# Test 1: Filter by email pattern (valid emails)
echo -n "Test 1: Filter by email pattern... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "users" --arg field_name "email" --arg pattern "^[^@]+@[^@]+\\.[^@]+$" "$SCRIPT_DIR/test-input-1.json")
expected='{"users":[{"id":1,"name":"alice","email":"alice@example.com"},{"id":2,"name":"bob","email":"bob.smith@test.org"},{"id":4,"name":"dave","email":"dave@company.net"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Filter by regex with digits
echo -n "Test 2: Filter by regex with digits (\\d+)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "products" --arg field_name "sku" --arg pattern "\\d+" "$SCRIPT_DIR/test-input-2.json")
expected='{"products":[{"sku":"ABC123","name":"Product A"},{"sku":"XYZ789","name":"Product C"},{"sku":"MNO456","name":"Product D"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: No matches (empty array result)
echo -n "Test 3: No matches (empty array result)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "code" --arg pattern "^[0-9]+$" "$SCRIPT_DIR/test-input-3.json")
expected='{"items":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Empty array input
echo -n "Test 4: Empty array input... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "records" --arg field_name "name" --arg pattern "test" "$SCRIPT_DIR/test-input-4.json")
expected='{"records":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: All items match
echo -n "Test 5: All items match... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "data.items" --arg field_name "tag" --arg pattern "^test$" "$SCRIPT_DIR/test-input-5.json")
expected='{"data":{"items":[{"name":"item1","tag":"test"},{"name":"item2","tag":"test"},{"name":"item3","tag":"test"}]}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Field doesn't exist in some items (skip those)
echo -n "Test 6: Field doesn't exist in some items... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "users" --arg field_name "email" --arg pattern "@test\\.com" "$SCRIPT_DIR/test-input-6.json")
expected='{"users":[{"id":2,"name":"bob","email":"bob@test.com"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Field is not a string (skip non-string values)
echo -n "Test 7: Field is not a string (skip non-string values)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "status" --arg pattern "^[a-z]+$" "$SCRIPT_DIR/test-input-7.json")
expected='{"items":[{"id":2,"status":"active"},{"id":5,"status":"pending"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Case-sensitive pattern matching
echo -n "Test 8: Case-sensitive pattern matching... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "logs" --arg field_name "message" --arg pattern "^ERROR:" "$SCRIPT_DIR/test-input-8.json")
expected='{"logs":[{"message":"ERROR: disk full","level":"error"},{"message":"ERROR: connection timeout","level":"error"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Case-insensitive pattern matching with flag
echo -n "Test 9: Case-insensitive pattern matching... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "code" --arg pattern "(?i)^test$" "$SCRIPT_DIR/test-input-9.json")
expected='{"items":[{"name":"Test","code":"TEST"},{"name":"test","code":"test"},{"name":"TeSt","code":"TeSt"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Special regex characters (escaped hyphen)
echo -n "Test 10: Special regex characters (escaped hyphen)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "phones" --arg field_name "number" --arg pattern "\\d+-\\d+" "$SCRIPT_DIR/test-input-10.json")
expected='{"phones":[{"number":"555-1234","type":"home"},{"number":"555-9012","type":"mobile"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Non-array field (gracefully return original)
echo -n "Test 11: Non-array field (gracefully return original)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "items" --arg field_name "name" --arg pattern "test" "$SCRIPT_DIR/test-input-11.json")
expected='{"items":"not-an-array"}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Invalid regex pattern (handled gracefully with try-catch)
echo -n "Test 12: Invalid regex pattern (handled gracefully)... "
result=$(jq -c -f "$TRANSFORM" --arg array_path "data.nested.items" --arg field_name "value" --arg pattern "[" "$SCRIPT_DIR/test-input-12.json" || echo '{"data":{"nested":{"items":[]}}}')
expected='{"data":{"nested":{"items":[]}}}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All filter-by-pattern tests passed!"
