# Entity Resolution (Deduplication)

Determines whether extracted entities are duplicates of existing entities. Adapted from Graphiti's `dedupe_nodes.py`.

## System Prompt

You are a helpful assistant that determines whether or not a NEW ENTITY is a duplicate of any EXISTING ENTITIES.

## User Prompt

<PREVIOUS_EPISODES>
{{previous_episodes}}
</PREVIOUS_EPISODES>

<CURRENT_EPISODE>
{{episode_content}}
</CURRENT_EPISODE>

<NEW_ENTITY>
{{extracted_entity}}
</NEW_ENTITY>

<ENTITY_TYPE_DESCRIPTION>
{{entity_type_description}}
</ENTITY_TYPE_DESCRIPTION>

<EXISTING_ENTITIES>
{{existing_entities}}
</EXISTING_ENTITIES>

Given the above EXISTING ENTITIES and their attributes, CURRENT EPISODE, and PREVIOUS EPISODES, determine if the NEW ENTITY extracted from the conversation is a duplicate of one of the EXISTING ENTITIES.

## Rules

Entities should only be considered duplicates if they refer to the **same real-world object or concept**.

**Semantic Equivalence**: If a descriptive label in existing_entities clearly refers to a named entity in context, treat them as duplicates.

**Do NOT mark entities as duplicates if:**
- They are related but distinct.
- They have similar names or purposes but refer to separate instances or concepts.

## Task

1. Compare NEW ENTITY against each item in EXISTING ENTITIES.
2. If it refers to the same real-world object or concept, collect its index.
3. Let `duplicate_idx` = the smallest collected index, or -1 if none.
4. Let `duplicates` = the sorted list of all collected indices (empty list if none).

## Output Schema

```json
{
  "entity_resolutions": [
    {
      "id": "integer - ID from NEW ENTITY",
      "name": "string - Best full name for the entity (use most complete/descriptive)",
      "duplicate_idx": "integer - Index of best duplicate in EXISTING ENTITIES, or -1 if none",
      "duplicates": "array - Sorted list of all duplicate indices (deduplicated, [] when none)"
    }
  ]
}
```

Only reference indices that appear in EXISTING ENTITIES, and return [] / -1 when unsure.

## Examples

**Duplicate case:**
- NEW ENTITY: {id: 0, name: "Tyler"}
- EXISTING ENTITIES: [{idx: 0, name: "Tyler Brandt", type: "Person"}]
- Context suggests they're the same person
- Result: {id: 0, name: "Tyler Brandt", duplicate_idx: 0, duplicates: [0]}

**Not duplicate:**
- NEW ENTITY: {id: 0, name: "Intent Systems"}
- EXISTING ENTITIES: [{idx: 0, name: "Anthropic", type: "Company"}]
- Different companies
- Result: {id: 0, name: "Intent Systems", duplicate_idx: -1, duplicates: []}
