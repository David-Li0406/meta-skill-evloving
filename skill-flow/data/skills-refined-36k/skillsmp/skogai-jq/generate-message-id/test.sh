#!/usr/bin/env bash
set -euo pipefail

# Test generate-message-id transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing generate-message-id transformation..."

# Test 1: Generate hash-based ID (default) at root level
echo -n "Test 1: Generate hash-based ID (default)... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-1.json")
# Check that ID field exists and starts with "msg-"
if echo "$result" | jq -e '.id | startswith("msg-")' > /dev/null && echo "$result" | jq -e '.content == "Hello world"' > /dev/null; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: object with .id starting with 'msg-' and original content"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Same content produces same hash ID (deterministic)
echo -n "Test 2: Same content produces same hash ID... "
result1=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-1.json" | jq -r '.id')
result2=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-2.json" | jq -r '.id')
if [[ "$result1" == "$result2" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: same ID for identical content"
    echo "  Got ID1: $result1"
    echo "  Got ID2: $result2"
    exit 1
fi

# Test 3: Different content produces different hash ID
echo -n "Test 3: Different content produces different hash ID... "
result1=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-1.json" | jq -r '.id')
result3=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-3.json" | jq -r '.id')
if [[ "$result1" != "$result3" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: different IDs for different content"
    echo "  Got ID1: $result1"
    echo "  Got ID3: $result3"
    exit 1
fi

# Test 4: Add ID to existing object without ID
echo -n "Test 4: Add ID to existing object... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-4.json")
if echo "$result" | jq -e '.id | startswith("msg-")' > /dev/null && echo "$result" | jq -e '.existing == "data"' > /dev/null; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: object with new .id and original data"
    echo "  Got: $result"
    exit 1
fi

# Test 5: Overwrite existing ID field
echo -n "Test 5: Overwrite existing ID field... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-5.json")
new_id=$(echo "$result" | jq -r '.id')
if [[ "$new_id" != "old-id" ]] && echo "$result" | jq -e '.id | startswith("msg-")' > /dev/null; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: new ID replacing old-id"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Empty object gets ID
echo -n "Test 6: Empty object gets ID... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-6.json")
# Empty object has very short base64 representation
if echo "$result" | jq -e '.id | startswith("msg-")' > /dev/null; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: object with .id starting with 'msg-'"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Nested path for ID field
echo -n "Test 7: Nested path for ID field... "
result=$(jq -c -f "$TRANSFORM" --arg id_field "message.id" "$SCRIPT_DIR/test-input-7.json")
if echo "$result" | jq -e '.message.id | startswith("msg-")' > /dev/null && echo "$result" | jq -e '.message.text == "nested"' > /dev/null; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: object with .message.id and original .message.text"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Null content value
echo -n "Test 8: Null content value... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-8.json")
if echo "$result" | jq -e '.id | startswith("msg-")' > /dev/null && echo "$result" | jq -e '.content == null' > /dev/null; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: object with ID and null content preserved"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Boolean false value
echo -n "Test 9: Boolean false value... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-9.json")
if echo "$result" | jq -e '.id | startswith("msg-")' > /dev/null && echo "$result" | jq -e '.value == false' > /dev/null; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: object with ID and false value preserved"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Zero value
echo -n "Test 10: Zero value... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-10.json")
if echo "$result" | jq -e '.id | startswith("msg-")' > /dev/null && echo "$result" | jq -e '.count == 0' > /dev/null; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: object with ID and zero value preserved"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Empty string value
echo -n "Test 11: Empty string value... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-11.json")
if echo "$result" | jq -e '.id | startswith("msg-")' > /dev/null && echo "$result" | jq -e '.text == ""' > /dev/null; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: object with ID and empty string preserved"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Empty array value
echo -n "Test 12: Empty array value... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-12.json")
if echo "$result" | jq -e '.id | startswith("msg-")' > /dev/null && echo "$result" | jq -e '.items == []' > /dev/null; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: object with ID and empty array preserved"
    echo "  Got: $result"
    exit 1
fi

# Test 13: ID format validation (length)
echo -n "Test 13: ID format validation (length)... "
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input-1.json" | jq -r '.id')
# ID should be "msg-" + 22 chars = 26 chars total
if [[ ${#result} -eq 26 ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: ID length of 26 characters"
    echo "  Got: $result (length: ${#result})"
    exit 1
fi

# Test 14: Timestamp strategy produces different IDs (non-deterministic)
echo -n "Test 14: Timestamp strategy... "
result=$(jq -c -f "$TRANSFORM" --arg strategy "timestamp" "$SCRIPT_DIR/test-input-1.json")
if echo "$result" | jq -e '.id' > /dev/null && ! echo "$result" | jq -e '.id | startswith("msg-")' > /dev/null; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: object with timestamp-based ID (not starting with 'msg-')"
    echo "  Got: $result"
    exit 1
fi

# Test 15: Hybrid strategy combines timestamp and hash
echo -n "Test 15: Hybrid strategy... "
result=$(jq -c -f "$TRANSFORM" --arg strategy "hybrid" "$SCRIPT_DIR/test-input-1.json")
id=$(echo "$result" | jq -r '.id')
# Hybrid format should be YYYYMMDD-<hash> (e.g., 20241206-abcd1234)
if [[ "$id" =~ ^[0-9]{8}-[A-Za-z0-9]{8}$ ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: hybrid ID format YYYYMMDD-XXXXXXXX"
    echo "  Got: $id"
    exit 1
fi

echo "All generate-message-id tests passed!"
