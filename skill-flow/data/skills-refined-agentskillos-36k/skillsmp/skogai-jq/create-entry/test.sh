#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing create-entry transformation..."

# Test 1: Basic entry creation with required fields
echo -n "Test 1: Basic entry creation... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "entry_123" \
  --arg title "Test Entry" \
  --arg category "lore" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --arg creator "tester" \
  --null-input)
if echo "$result" | jq -e '.id == "entry_123" and .title == "Test Entry" and .category == "lore"' > /dev/null; then
    echo "PASS"
else
    echo "FAIL (expected basic entry with id, title, category)"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Entry with character category
echo -n "Test 2: Character category... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "entry_456" \
  --arg title "Aria Nightwhisper" \
  --arg category "character" \
  --arg timestamp "2025-01-02T10:30:00Z" \
  --arg creator "skogix" \
  --null-input)
if echo "$result" | jq -e '.category == "character" and .title == "Aria Nightwhisper"' > /dev/null; then
    echo "PASS"
else
    echo "FAIL (expected character category)"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Timestamp preserved exactly
echo -n "Test 3: Timestamp preservation... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "entry_789" \
  --arg title "Test" \
  --arg category "place" \
  --arg timestamp "2025-12-13T15:45:30Z" \
  --arg creator "test" \
  --null-input)
created_at=$(echo "$result" | jq -r '.metadata.created_at')
updated_at=$(echo "$result" | jq -r '.metadata.updated_at')
if [[ "$created_at" == "2025-12-13T15:45:30Z" ]] && [[ "$updated_at" == "2025-12-13T15:45:30Z" ]]; then
    echo "PASS"
else
    echo "FAIL (expected timestamps to match input)"
    echo "  created_at: $created_at"
    echo "  updated_at: $updated_at"
    exit 1
fi

# Test 4: Empty arrays initialized
echo -n "Test 4: Empty arrays initialization... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "entry_101" \
  --arg title "Test" \
  --arg category "event" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --arg creator "test" \
  --null-input)
tags=$(echo "$result" | jq -r '.tags | type')
relationships=$(echo "$result" | jq -r '.relationships | type')
restricted=$(echo "$result" | jq -r '.visibility.restricted_to | type')
if [[ "$tags" == "array" ]] && [[ "$relationships" == "array" ]] && [[ "$restricted" == "array" ]]; then
    echo "PASS"
else
    echo "FAIL (expected arrays to be type 'array')"
    echo "  tags: $tags, relationships: $relationships, restricted_to: $restricted"
    exit 1
fi

# Test 5: Content field is empty string
echo -n "Test 5: Empty content field... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "entry_202" \
  --arg title "Test" \
  --arg category "object" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --arg creator "test" \
  --null-input)
content=$(echo "$result" | jq -r '.content')
summary=$(echo "$result" | jq -r '.summary')
if [[ "$content" == "" ]] && [[ "$summary" == "" ]]; then
    echo "PASS"
else
    echo "FAIL (expected empty strings for content and summary)"
    echo "  content: '$content', summary: '$summary'"
    exit 1
fi

# Test 6: Metadata structure correct
echo -n "Test 6: Metadata structure... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "entry_303" \
  --arg title "Test" \
  --arg category "concept" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --arg creator "alice" \
  --null-input)
creator=$(echo "$result" | jq -r '.metadata.created_by')
version=$(echo "$result" | jq -r '.metadata.version')
canonical=$(echo "$result" | jq -r '.metadata.canonical')
if [[ "$creator" == "alice" ]] && [[ "$version" == "1.0" ]] && [[ "$canonical" == "true" ]]; then
    echo "PASS"
else
    echo "FAIL (expected metadata with creator=alice, version=1.0, canonical=true)"
    echo "  creator: $creator, version: $version, canonical: $canonical"
    exit 1
fi

# Test 7: Visibility defaults
echo -n "Test 7: Visibility defaults... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "entry_404" \
  --arg title "Test" \
  --arg category "custom" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --arg creator "test" \
  --null-input)
public=$(echo "$result" | jq -r '.visibility.public')
restricted_count=$(echo "$result" | jq -r '.visibility.restricted_to | length')
if [[ "$public" == "true" ]] && [[ "$restricted_count" == "0" ]]; then
    echo "PASS"
else
    echo "FAIL (expected public=true, restricted_to=[])"
    echo "  public: $public, restricted_to length: $restricted_count"
    exit 1
fi

# Test 8: All required fields present
echo -n "Test 8: All required fields present... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "entry_505" \
  --arg title "Complete Test" \
  --arg category "lore" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --arg creator "test" \
  --null-input)
has_id=$(echo "$result" | jq -e 'has("id")' > /dev/null && echo "yes" || echo "no")
has_title=$(echo "$result" | jq -e 'has("title")' > /dev/null && echo "yes" || echo "no")
has_content=$(echo "$result" | jq -e 'has("content")' > /dev/null && echo "yes" || echo "no")
has_category=$(echo "$result" | jq -e 'has("category")' > /dev/null && echo "yes" || echo "no")
if [[ "$has_id" == "yes" ]] && [[ "$has_title" == "yes" ]] && [[ "$has_content" == "yes" ]] && [[ "$has_category" == "yes" ]]; then
    echo "PASS"
else
    echo "FAIL (missing required fields)"
    echo "  id: $has_id, title: $has_title, content: $has_content, category: $has_category"
    exit 1
fi

# Test 9: Attributes object exists
echo -n "Test 9: Attributes object... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "entry_606" \
  --arg title "Test" \
  --arg category "place" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --arg creator "test" \
  --null-input)
attr_type=$(echo "$result" | jq -r '.attributes | type')
if [[ "$attr_type" == "object" ]]; then
    echo "PASS"
else
    echo "FAIL (expected attributes to be object type)"
    echo "  Got: $attr_type"
    exit 1
fi

# Test 10: ID field preserved exactly as provided
echo -n "Test 10: ID preservation... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "entry_1734098765_a1b2c3d4" \
  --arg title "Test" \
  --arg category "event" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --arg creator "test" \
  --null-input)
output_id=$(echo "$result" | jq -r '.id')
if [[ "$output_id" == "entry_1734098765_a1b2c3d4" ]]; then
    echo "PASS"
else
    echo "FAIL (expected ID to be preserved exactly)"
    echo "  Expected: entry_1734098765_a1b2c3d4"
    echo "  Got: $output_id"
    exit 1
fi

echo ""
echo "All create-entry tests passed!"
