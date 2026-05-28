# Create a new persona with all required schema fields
# Usage: jq -f create-persona/transform.jq --arg id "persona_123" --arg name "Name" --arg voice_tone "neutral" --arg timestamp "2025-01-01T00:00:00Z" --null-input
#
# Arguments:
#   id: Persona ID (required)
#   name: Persona name (required)
#   voice_tone: Voice tone (required)
#   timestamp: ISO 8601 timestamp (required)
#
# Input: null
# Output: Complete persona JSON matching knowledge/core/persona/schema.json

{
  "id": $ARGS.named.id,
  "name": $ARGS.named.name,
  "core_traits": {
    "temperament": "balanced",
    "values": [],
    "motivations": []
  },
  "voice": {
    "tone": $ARGS.named.voice_tone,
    "patterns": [],
    "vocabulary": "standard"
  },
  "background": {
    "origin": "",
    "significant_events": [],
    "connections": []
  },
  "knowledge": {
    "expertise": [],
    "limitations": [],
    "lore_books": []
  },
  "interaction_style": {
    "formality": "neutral",
    "humor": "occasional",
    "directness": "balanced"
  },
  "meta": {
    "version": "1.0",
    "created": $ARGS.named.timestamp,
    "modified": $ARGS.named.timestamp,
    "tags": []
  }
}
