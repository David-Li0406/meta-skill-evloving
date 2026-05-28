#!/usr/bin/env bash
set -euo pipefail

# Test array-filter transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing array-filter transformation..."

# Test 1: Filter by boolean field
echo -n "Test 1: Filter by boolean field (active=true)... "
result=$(jq -c -f "$TRANSFORM" --arg array_field "items" --arg field "active" --arg value "true" "$SCRIPT_DIR/test-input-1.json")
expected='{"items":[{"name":"item-a","active":true,"priority":1},{"name":"item-c","active":true,"priority":3}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Filter by string field
echo -n "Test 2: Filter by string field (status=active)... "
result=$(jq -c -f "$TRANSFORM" --arg array_field "users" --arg field "status" --arg value "active" "$SCRIPT_DIR/test-input-2.json")
expected='{"users":[{"id":1,"name":"alice","status":"active"},{"id":3,"name":"charlie","status":"active"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Filter by numeric field
echo -n "Test 3: Filter by numeric field (price=100)... "
result=$(jq -c -f "$TRANSFORM" --arg array_field "products" --arg field "price" --arg value "100" "$SCRIPT_DIR/test-input-3.json")
expected='{"products":[{"sku":"A1","name":"product-a","price":100},{"sku":"C3","name":"product-c","price":100}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Filter on empty array (no matches)
echo -n "Test 4: Filter empty array... "
result=$(jq -c -f "$TRANSFORM" --arg array_field "items" --arg field "active" --arg value "true" "$SCRIPT_DIR/test-input-4.json")
expected='{"items":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Filter where all items match
echo -n "Test 5: Filter where all items match... "
result=$(jq -c -f "$TRANSFORM" --arg array_field "records" --arg field "tag" --arg value "important" "$SCRIPT_DIR/test-input-5.json")
expected='{"records":[{"id":1,"tag":"important"},{"id":2,"tag":"important"},{"id":3,"tag":"important"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Filter with no matches
echo -n "Test 6: Filter with no matches... "
result=$(jq -c -f "$TRANSFORM" --arg array_field "users" --arg field "status" --arg value "suspended" "$SCRIPT_DIR/test-input-2.json")
expected='{"users":[]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Filter for null values
echo -n "Test 7: Filter for null values... "
result=$(jq -c -f "$TRANSFORM" --arg array_field "items" --arg field "value" --arg value "null" "$SCRIPT_DIR/test-input-6.json")
expected='{"items":[{"id":1,"value":null,"type":"null"},{"id":3,"value":null,"type":"null"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Filter for boolean false
echo -n "Test 8: Filter for boolean false... "
result=$(jq -c -f "$TRANSFORM" --arg array_field "items" --arg field "active" --arg value "false" "$SCRIPT_DIR/test-input-7.json")
expected='{"items":[{"id":1,"active":false,"name":"disabled"},{"id":3,"active":false,"name":"also-disabled"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Filter for zero values
echo -n "Test 9: Filter for zero values... "
result=$(jq -c -f "$TRANSFORM" --arg array_field "items" --arg field "count" --arg value "0" "$SCRIPT_DIR/test-input-8.json")
expected='{"items":[{"id":1,"count":0,"label":"zero"},{"id":3,"count":0,"label":"also-zero"}]}'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All array-filter tests passed!"
