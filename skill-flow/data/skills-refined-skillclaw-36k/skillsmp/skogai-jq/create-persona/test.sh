#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing create-persona transformation..."

# Test 1: Basic persona creation with required fields
echo -n "Test 1: Basic persona creation... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "persona_123" \
  --arg name "Aria Nightwhisper" \
  --arg voice_tone "poetic yet precise" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --null-input)
if echo "$result" | jq -e '.id == "persona_123" and .name == "Aria Nightwhisper" and .voice.tone == "poetic yet precise"' > /dev/null; then
    echo "PASS"
else
    echo "FAIL (expected basic persona with id, name, voice.tone)"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Timestamp preserved exactly
echo -n "Test 2: Timestamp preservation... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "persona_456" \
  --arg name "Test" \
  --arg voice_tone "neutral" \
  --arg timestamp "2025-12-13T15:45:30Z" \
  --null-input)
created=$(echo "$result" | jq -r '.meta.created')
modified=$(echo "$result" | jq -r '.meta.modified')
if [[ "$created" == "2025-12-13T15:45:30Z" ]] && [[ "$modified" == "2025-12-13T15:45:30Z" ]]; then
    echo "PASS"
else
    echo "FAIL (expected timestamps to match input)"
    echo "  created: $created"
    echo "  modified: $modified"
    exit 1
fi

# Test 3: Core traits structure
echo -n "Test 3: Core traits structure... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "persona_789" \
  --arg name "Test" \
  --arg voice_tone "analytical" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --null-input)
temperament=$(echo "$result" | jq -r '.core_traits.temperament')
values_type=$(echo "$result" | jq -r '.core_traits.values | type')
motivations_type=$(echo "$result" | jq -r '.core_traits.motivations | type')
if [[ "$temperament" == "balanced" ]] && [[ "$values_type" == "array" ]] && [[ "$motivations_type" == "array" ]]; then
    echo "PASS"
else
    echo "FAIL (expected core_traits with balanced temperament and arrays)"
    echo "  temperament: $temperament, values: $values_type, motivations: $motivations_type"
    exit 1
fi

# Test 4: Voice structure complete
echo -n "Test 4: Voice structure... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "persona_101" \
  --arg name "Test" \
  --arg voice_tone "mysterious" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --null-input)
tone=$(echo "$result" | jq -r '.voice.tone')
patterns_type=$(echo "$result" | jq -r '.voice.patterns | type')
vocabulary=$(echo "$result" | jq -r '.voice.vocabulary')
if [[ "$tone" == "mysterious" ]] && [[ "$patterns_type" == "array" ]] && [[ "$vocabulary" == "standard" ]]; then
    echo "PASS"
else
    echo "FAIL (expected voice with tone, patterns array, standard vocabulary)"
    echo "  tone: $tone, patterns: $patterns_type, vocabulary: $vocabulary"
    exit 1
fi

# Test 5: Background structure
echo -n "Test 5: Background structure... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "persona_202" \
  --arg name "Test" \
  --arg voice_tone "neutral" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --null-input)
origin=$(echo "$result" | jq -r '.background.origin')
events_type=$(echo "$result" | jq -r '.background.significant_events | type')
connections_type=$(echo "$result" | jq -r '.background.connections | type')
if [[ "$origin" == "" ]] && [[ "$events_type" == "array" ]] && [[ "$connections_type" == "array" ]]; then
    echo "PASS"
else
    echo "FAIL (expected background with empty origin and arrays)"
    echo "  origin: '$origin', events: $events_type, connections: $connections_type"
    exit 1
fi

# Test 6: Knowledge structure
echo -n "Test 6: Knowledge structure... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "persona_303" \
  --arg name "Test" \
  --arg voice_tone "neutral" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --null-input)
expertise_type=$(echo "$result" | jq -r '.knowledge.expertise | type')
limitations_type=$(echo "$result" | jq -r '.knowledge.limitations | type')
lore_books_type=$(echo "$result" | jq -r '.knowledge.lore_books | type')
if [[ "$expertise_type" == "array" ]] && [[ "$limitations_type" == "array" ]] && [[ "$lore_books_type" == "array" ]]; then
    echo "PASS"
else
    echo "FAIL (expected knowledge with all arrays)"
    echo "  expertise: $expertise_type, limitations: $limitations_type, lore_books: $lore_books_type"
    exit 1
fi

# Test 7: Interaction style defaults
echo -n "Test 7: Interaction style defaults... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "persona_404" \
  --arg name "Test" \
  --arg voice_tone "neutral" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --null-input)
formality=$(echo "$result" | jq -r '.interaction_style.formality')
humor=$(echo "$result" | jq -r '.interaction_style.humor')
directness=$(echo "$result" | jq -r '.interaction_style.directness')
if [[ "$formality" == "neutral" ]] && [[ "$humor" == "occasional" ]] && [[ "$directness" == "balanced" ]]; then
    echo "PASS"
else
    echo "FAIL (expected interaction_style with neutral/occasional/balanced defaults)"
    echo "  formality: $formality, humor: $humor, directness: $directness"
    exit 1
fi

# Test 8: All required fields present
echo -n "Test 8: All required fields present... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "persona_505" \
  --arg name "Complete Test" \
  --arg voice_tone "analytical" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --null-input)
has_id=$(echo "$result" | jq -e 'has("id")' > /dev/null && echo "yes" || echo "no")
has_name=$(echo "$result" | jq -e 'has("name")' > /dev/null && echo "yes" || echo "no")
has_core_traits=$(echo "$result" | jq -e 'has("core_traits")' > /dev/null && echo "yes" || echo "no")
has_voice=$(echo "$result" | jq -e 'has("voice")' > /dev/null && echo "yes" || echo "no")
if [[ "$has_id" == "yes" ]] && [[ "$has_name" == "yes" ]] && [[ "$has_core_traits" == "yes" ]] && [[ "$has_voice" == "yes" ]]; then
    echo "PASS"
else
    echo "FAIL (missing required fields)"
    echo "  id: $has_id, name: $has_name, core_traits: $has_core_traits, voice: $has_voice"
    exit 1
fi

# Test 9: Meta tags is empty array
echo -n "Test 9: Meta tags... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "persona_606" \
  --arg name "Test" \
  --arg voice_tone "neutral" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --null-input)
tags_type=$(echo "$result" | jq -r '.meta.tags | type')
tags_length=$(echo "$result" | jq -r '.meta.tags | length')
version=$(echo "$result" | jq -r '.meta.version')
if [[ "$tags_type" == "array" ]] && [[ "$tags_length" == "0" ]] && [[ "$version" == "1.0" ]]; then
    echo "PASS"
else
    echo "FAIL (expected meta.tags to be empty array and version 1.0)"
    echo "  tags type: $tags_type, length: $tags_length, version: $version"
    exit 1
fi

# Test 10: ID field preserved exactly as provided
echo -n "Test 10: ID preservation... "
result=$(jq -c -f "$TRANSFORM" \
  --arg id "persona_1734098765" \
  --arg name "Test" \
  --arg voice_tone "neutral" \
  --arg timestamp "2025-01-01T00:00:00Z" \
  --null-input)
output_id=$(echo "$result" | jq -r '.id')
if [[ "$output_id" == "persona_1734098765" ]]; then
    echo "PASS"
else
    echo "FAIL (expected ID to be preserved exactly)"
    echo "  Expected: persona_1734098765"
    echo "  Got: $output_id"
    exit 1
fi

echo ""
echo "All create-persona tests passed!"
