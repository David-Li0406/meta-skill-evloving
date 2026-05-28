#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing create-book transformation..."

# Test 1: Basic book creation with required fields
echo -n "Test 1: Basic book creation... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "book_123" \
  --arg title "Test Chronicles" \
  --arg description "A test book" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --arg creator "tester" \
  --null-input)
if echo "$result" | jq -e '.id == "book_123" and .title == "Test Chronicles" and .description == "A test book"' > /dev/null; then
    echo "PASS"
else
    echo "FAIL (expected basic book with id, title, description)"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Timestamp preserved exactly
echo -n "Test 2: Timestamp preservation... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "book_456" \
  --arg title "Test" \
  --arg description "Test description" \
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

# Test 3: Empty arrays initialized
echo -n "Test 3: Empty arrays initialization... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "book_789" \
  --arg title "Test" \
  --arg description "Test" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --arg creator "test" \
  --null-input)
entries=$(echo "$result" | jq -r '.entries | type')
tags=$(echo "$result" | jq -r '.tags | type')
owners=$(echo "$result" | jq -r '.owners | type')
readers=$(echo "$result" | jq -r '.readers | type')
if [[ "$entries" == "array" ]] && [[ "$tags" == "array" ]] && [[ "$owners" == "array" ]] && [[ "$readers" == "array" ]]; then
    echo "PASS"
else
    echo "FAIL (expected all arrays to be type 'array')"
    echo "  entries: $entries, tags: $tags, owners: $owners, readers: $readers"
    exit 1
fi

# Test 4: Categories is empty object
echo -n "Test 4: Categories empty object... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "book_101" \
  --arg title "Test" \
  --arg description "Test" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --arg creator "test" \
  --null-input)
categories_type=$(echo "$result" | jq -r '.categories | type')
categories_length=$(echo "$result" | jq -r '.categories | length')
if [[ "$categories_type" == "object" ]] && [[ "$categories_length" == "0" ]]; then
    echo "PASS"
else
    echo "FAIL (expected categories to be empty object)"
    echo "  type: $categories_type, length: $categories_length"
    exit 1
fi

# Test 5: Metadata structure correct
echo -n "Test 5: Metadata structure... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "book_202" \
  --arg title "Test" \
  --arg description "Test" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --arg creator "alice" \
  --null-input)
creator=$(echo "$result" | jq -r '.metadata.created_by')
version=$(echo "$result" | jq -r '.metadata.version')
status=$(echo "$result" | jq -r '.metadata.status')
if [[ "$creator" == "alice" ]] && [[ "$version" == "1.0" ]] && [[ "$status" == "draft" ]]; then
    echo "PASS"
else
    echo "FAIL (expected metadata with creator=alice, version=1.0, status=draft)"
    echo "  creator: $creator, version: $version, status: $status"
    exit 1
fi

# Test 6: Visibility defaults
echo -n "Test 6: Visibility defaults... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "book_303" \
  --arg title "Test" \
  --arg description "Test" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --arg creator "test" \
  --null-input)
public=$(echo "$result" | jq -r '.visibility.public')
system=$(echo "$result" | jq -r '.visibility.system')
if [[ "$public" == "false" ]] && [[ "$system" == "false" ]]; then
    echo "PASS"
else
    echo "FAIL (expected public=false, system=false)"
    echo "  public: $public, system: $system"
    exit 1
fi

# Test 7: Structure default section exists
echo -n "Test 7: Structure default section... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "book_404" \
  --arg title "Test" \
  --arg description "Test" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --arg creator "test" \
  --null-input)
structure_length=$(echo "$result" | jq -r '.structure | length')
section_name=$(echo "$result" | jq -r '.structure[0].name')
section_entries=$(echo "$result" | jq -r '.structure[0].entries | type')
if [[ "$structure_length" == "1" ]] && [[ "$section_name" == "Introduction" ]] && [[ "$section_entries" == "array" ]]; then
    echo "PASS"
else
    echo "FAIL (expected structure with Introduction section)"
    echo "  length: $structure_length, name: $section_name, entries type: $section_entries"
    exit 1
fi

# Test 8: All required fields present
echo -n "Test 8: All required fields present... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "book_505" \
  --arg title "Complete Test" \
  --arg description "Complete description" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --arg creator "test" \
  --null-input)
has_id=$(echo "$result" | jq -e 'has("id")' > /dev/null && echo "yes" || echo "no")
has_title=$(echo "$result" | jq -e 'has("title")' > /dev/null && echo "yes" || echo "no")
has_description=$(echo "$result" | jq -e 'has("description")' > /dev/null && echo "yes" || echo "no")
if [[ "$has_id" == "yes" ]] && [[ "$has_title" == "yes" ]] && [[ "$has_description" == "yes" ]]; then
    echo "PASS"
else
    echo "FAIL (missing required fields)"
    echo "  id: $has_id, title: $has_title, description: $has_description"
    exit 1
fi

# Test 9: Structure subsections is empty array
echo -n "Test 9: Structure subsections... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "book_606" \
  --arg title "Test" \
  --arg description "Test" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --arg creator "test" \
  --null-input)
subsections_type=$(echo "$result" | jq -r '.structure[0].subsections | type')
subsections_length=$(echo "$result" | jq -r '.structure[0].subsections | length')
if [[ "$subsections_type" == "array" ]] && [[ "$subsections_length" == "0" ]]; then
    echo "PASS"
else
    echo "FAIL (expected subsections to be empty array)"
    echo "  type: $subsections_type, length: $subsections_length"
    exit 1
fi

# Test 10: ID field preserved exactly as provided
echo -n "Test 10: ID preservation... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "book_1734098765_a1b2c3d4" \
  --arg title "Test" \
  --arg description "Test" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --arg creator "test" \
  --null-input)
output_id=$(echo "$result" | jq -r '.id')
if [[ "$output_id" == "book_1734098765_a1b2c3d4" ]]; then
    echo "PASS"
else
    echo "FAIL (expected ID to be preserved exactly)"
    echo "  Expected: book_1734098765_a1b2c3d4"
    echo "  Got: $output_id"
    exit 1
fi

echo ""
echo "All create-book tests passed!"
