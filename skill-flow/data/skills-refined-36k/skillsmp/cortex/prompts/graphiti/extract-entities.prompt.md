# Entity Extraction

Extracts entity nodes from episode content. Graph-independent — disambiguation happens at resolution time.

## System Prompt

You are an AI assistant that extracts entity nodes from text.
Your primary task is to extract and classify significant entities mentioned in the provided content.

## User Prompt

<ENTITY_TYPES>
{{entity_types}}
</ENTITY_TYPES>

<!-- Default entity_types:
[
  {"id": 0, "name": "Entity", "description": "Default/unknown type"},
  {"id": 1, "name": "Person", "description": "A human being"},
  {"id": 2, "name": "Company", "description": "Business, organization, or institution"},
  {"id": 3, "name": "Project", "description": "A project, product, or codebase"},
  {"id": 4, "name": "Location", "description": "A place (city, address, country, venue)"},
  {"id": 5, "name": "Event", "description": "A meeting, conference, or named occurrence"},
  {"id": 6, "name": "Document", "description": "A file, article, or written work"},
  {"id": 7, "name": "Pet", "description": "An animal companion"}
]
-->

{{#if previous_episodes}}
<PREVIOUS_EPISODES>
{{previous_episodes}}
</PREVIOUS_EPISODES>
{{/if}}

<CURRENT_EPISODE>
{{episode_content}}
</CURRENT_EPISODE>

## Instructions

Extract **entity nodes** from the CURRENT_EPISODE.

### What to Extract

1. **People**: Extract by name. If only a role is mentioned ("my dad", "the CEO"), use a descriptive name like "Dad" or "the CEO".
2. **Organizations**: Companies, schools, institutions.
3. **Projects**: Software, products, codebases, initiatives being discussed.
4. **Locations**: Cities, addresses, countries, venues.
5. **Events**: Named meetings, conferences, occurrences (e.g., "the standup", "HTAA meeting").
6. **Documents**: Files, articles, specs being referenced.
7. **Pets**: Named animals.

### What NOT to Extract

- **Dates**: These are captured as `target_literal` in relationships, not as entities.
- **AI agents**: Claude, GPT, etc. — no durable identity; the content is what matters.
- **Concepts, technologies, activities, professions**: Searchable via episode text, not entities.
- **Relationships or actions**: "works at" is a relationship, not an entity.
- **Entities only in PREVIOUS_EPISODES**: Those are for coreference context only.

### Formatting Rules

- Use the most complete name available (full names over nicknames)
- Resolve pronouns to their referent when clear from context
- For conversations: always extract speakers as entities (if they're people)

{{custom_extraction_instructions}}

## Output Schema

```json
{
  "extracted_entities": [
    {
      "id": "integer - Temporary ID for reference (0, 1, 2, ...)",
      "name": "string - Name of the extracted entity",
      "entity_type_id": "integer - ID from ENTITY_TYPES"
    }
  ]
}
```

## Example

**Input:**
```
Tyler: I'm meeting Casey at Anthropic tomorrow to discuss the Cortex project. My birthday is May 15th.
```

**Output:**
```json
{
  "extracted_entities": [
    {"id": 0, "name": "Tyler", "entity_type_id": 1},
    {"id": 1, "name": "Casey", "entity_type_id": 1},
    {"id": 2, "name": "Anthropic", "entity_type_id": 2},
    {"id": 3, "name": "Cortex", "entity_type_id": 3}
  ]
}
```

Note: "tomorrow" and "May 15th" are dates — they're captured in relationship extraction as `target_literal`, not as entities here.

## Notes

- **Extraction is graph-independent** — disambiguation happens at resolution time
- Entity IDs are temporary (0, 1, 2...) for this extraction only; resolution assigns real UUIDs
- Since Cortex episodes are rich (grouped events), previous_episodes may not be needed
- Entity types are configurable per-domain
