# Create a new lore book with all required schema fields
# Usage: jq -f create-book/transform.jq --arg id "book_123" --arg title "Title" --arg description "Desc" --arg timestamp "2025-01-01T00:00:00Z" --arg creator "user" --null-input
#
# Arguments:
#   id: Book ID (required)
#   title: Book title (required)
#   description: Book description (required)
#   timestamp: ISO 8601 timestamp (required)
#   creator: Creator username (required)
#
# Input: null
# Output: Complete book JSON matching knowledge/core/book-schema.json

{
  "id": $ARGS.named.id,
  "title": $ARGS.named.title,
  "description": $ARGS.named.description,
  "entries": [],
  "categories": {},
  "tags": [],
  "owners": [],
  "readers": [],
  "metadata": {
    "created_by": $ARGS.named.creator,
    "created_at": $ARGS.named.timestamp,
    "updated_at": $ARGS.named.timestamp,
    "version": "1.0",
    "status": "draft"
  },
  "structure": [
    {
      "name": "Introduction",
      "description": "Overview of this lore book",
      "entries": [],
      "subsections": []
    }
  ],
  "visibility": {
    "public": false,
    "system": false
  }
}
