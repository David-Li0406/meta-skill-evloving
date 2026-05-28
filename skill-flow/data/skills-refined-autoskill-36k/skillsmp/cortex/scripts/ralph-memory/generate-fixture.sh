#!/bin/bash
# Generate fixture from cortex.db
# Usage: ./generate-fixture.sh <thread_id> <output_dir> [limit] [offset_days_from_end] [contact_name]
#
# Example: ./generate-fixture.sh "imessage:+16319056994" "fixtures/imessage/casey-dense" 100 30 "Casey"

set -e

CORTEX_DB="/Users/tyler/Library/Application Support/Cortex/cortex.db"
THREAD_ID="${1:-imessage:+16319056994}"
OUTPUT_DIR="${2:-fixtures/imessage/generated}"
LIMIT="${3:-100}"
OFFSET_DAYS="${4:-0}"
CONTACT_NAME="${5:-Contact}"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Get thread info
echo "Generating fixture from thread: $THREAD_ID"
echo "Contact name: $CONTACT_NAME"
echo "Limit: $LIMIT events, Offset: $OFFSET_DAYS days from end"

# Calculate timestamp cutoff
if [ "$OFFSET_DAYS" -gt 0 ]; then
    MAX_TS=$(sqlite3 "$CORTEX_DB" "SELECT MAX(timestamp) FROM events WHERE thread_id = '$THREAD_ID'")
    CUTOFF_TS=$((MAX_TS - (OFFSET_DAYS * 86400)))
    WHERE_CLAUSE="AND timestamp <= $CUTOFF_TS"
else
    WHERE_CLAUSE=""
fi

# Extract identifier from thread_id (e.g., +16319056994 from imessage:+16319056994)
IDENTIFIER=$(echo "$THREAD_ID" | sed 's/^[^:]*://')

# Generate episode.json
sqlite3 -json "$CORTEX_DB" "
SELECT 
    id,
    datetime(timestamp, 'unixepoch') || 'Z' as timestamp,
    direction,
    content
FROM events 
WHERE thread_id = '$THREAD_ID' 
  AND content IS NOT NULL 
  AND content != ''
  $WHERE_CLAUSE
ORDER BY timestamp DESC
LIMIT $LIMIT
" | jq --arg thread "$THREAD_ID" \
       --arg ref "$(date -Iseconds)" \
       --arg contact "$CONTACT_NAME" \
       --arg contact_id "$IDENTIFIER" '{
    id: "fixture-generated-001",
    source: "imessage",
    channel: "imessage", 
    thread_id: $thread,
    reference_time: $ref,
    events: [.[] | {
        id: .id,
        timestamp: .timestamp,
        sender: (if .direction == "sent" then "Tyler" else $contact end),
        sender_identifier: (if .direction == "sent" then "+17072876731" else $contact_id end),
        content: .content,
        direction: (if .direction == "sent" then "outbound" else "inbound" end)
    }] | reverse,
    metadata: {
        description: ("Dense window from " + $contact + " thread"),
        coverage_tags: ["generated", "dense_window", "large_scale"],
        notes: "Generated with generate-fixture.sh"
    }
}' > "$OUTPUT_DIR/episode.json"

# Generate basic expectations.yaml
cat > "$OUTPUT_DIR/expectations.yaml" << EOF
# Auto-generated expectations for $CONTACT_NAME thread
description: "Dense window from $CONTACT_NAME - verify entity/relationship extraction at scale"

entities:
  must_have:
    - name_contains: "Tyler"
      entity_type: Person
      
    - name_contains: "$CONTACT_NAME"
      entity_type: Person

relationships:
  optional:
    - relation_type: KNOWS
    - relation_type: DATING
    - relation_type: HAS_EMAIL
    - relation_type: HAS_PHONE

episode_entity_mentions:
  must_have:
    - entity_name_contains: "Tyler"
EOF

echo "Generated fixture in $OUTPUT_DIR/"
echo "Events: $(jq '.events | length' "$OUTPUT_DIR/episode.json")"
echo ""
echo "Preview of first 3 events:"
jq -r '.events[:3] | .[] | "\(.timestamp) \(.sender): \(.content[:60])..."' "$OUTPUT_DIR/episode.json"
