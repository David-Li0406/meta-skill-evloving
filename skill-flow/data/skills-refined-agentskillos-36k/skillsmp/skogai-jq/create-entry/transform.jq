# Create a new lore entry with all required schema fields
# Usage: jq -f create-entry/transform.jq --arg id "entry_123" --arg title "Title" --arg category "lore" --arg timestamp "2025-01-01T00:00:00Z" --arg creator "user" --null-input
#
# Arguments:
#   id: Entry ID (required)
#   title: Entry title (required)
#   category: Entry category from enum (required)
#   timestamp: ISO 8601 timestamp (required)
#   creator: Creator username (required)
#
# Input: null
# Output: Complete entry JSON matching knowledge/core/lore/schema.json

{
  "id": $ARGS.named.id,
  "title": $ARGS.named.title,
  "content": "",
  "summary": "",
  "category": $ARGS.named.category,
  "tags": [],
  "relationships": [],
  "attributes": {},
  "metadata": {
    "created_by": $ARGS.named.creator,
    "created_at": $ARGS.named.timestamp,
    "updated_at": $ARGS.named.timestamp,
    "version": "1.0",
    "canonical": true
  },
  "visibility": {
    "public": true,
    "restricted_to": []
  }
}
