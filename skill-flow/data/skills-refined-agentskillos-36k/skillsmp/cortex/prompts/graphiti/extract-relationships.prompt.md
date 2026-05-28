# Relationship Extraction

Extracts relationships (facts) connecting entities. Run after entity extraction and resolution.

## System Prompt

You are an AI assistant that extracts relationships from text.
Your task is to identify facts connecting the provided entities, including temporal and identity information.

## User Prompt

<RESOLVED_ENTITIES>
{{resolved_entities}}
</RESOLVED_ENTITIES>

<!-- Example resolved_entities:
[
  {"id": 0, "uuid": "ent_abc123", "name": "Tyler", "entity_type": "Person"},
  {"id": 1, "uuid": "ent_def456", "name": "Casey", "entity_type": "Person"},
  {"id": 2, "uuid": "ent_ghi789", "name": "Anthropic", "entity_type": "Company"},
  {"id": 3, "uuid": "ent_jkl012", "name": "Cortex", "entity_type": "Project"}
]
-->

<REFERENCE_TIME>
{{reference_time}}
</REFERENCE_TIME>

{{#if previous_episodes}}
<PREVIOUS_EPISODES>
{{previous_episodes}}
</PREVIOUS_EPISODES>
{{/if}}

<CURRENT_EPISODE>
{{episode_content}}
</CURRENT_EPISODE>

## Instructions

Extract relationships (facts) from the CURRENT_EPISODE.

### Relationship Structure

Each relationship is a triple: `(source_entity) --RELATION_TYPE--> (target)`

The target is either:
- **Another entity** (`target_entity_id`) — for most relationships
- **A literal value** (`target_literal`) — for identity and temporal relationships

### target_literal Relationships

These relationship types use `target_literal` instead of `target_entity_id`:

| Category | Relationship Types | Format | Promoted to Alias? |
|----------|-------------------|--------|-------------------|
| **Identity** | HAS_EMAIL | `tyler@example.com` | Yes |
| **Identity** | HAS_PHONE | `+1-707-287-6731` | Yes |
| **Identity** | HAS_HANDLE | `@tnapathy` | Yes |
| **Identity** | HAS_USERNAME | `tnapathy` | Yes |
| **Identity** | ALSO_KNOWN_AS | `Ty` | Yes |
| **Temporal** | BORN_ON | `1990-05-15` | No |
| **Temporal** | ANNIVERSARY_ON | `2023-02-18` | No |
| **Temporal** | OCCURRED_ON | `2026-01-22` | No |
| **Temporal** | SCHEDULED_FOR | `2026-01-25` | No |
| **Temporal** | STARTED_ON | `2024-01` | No |
| **Temporal** | ENDED_ON | `2025-12` | No |

**Date format:** ISO 8601 — `YYYY-MM-DD` (full date), `YYYY-MM` (month), or `YYYY` (year).

Use REFERENCE_TIME to resolve relative dates ("yesterday", "last month", "next week").

### target_entity_id Relationships

All other relationships point to entities:

| Category | Relationship Types | Target Entity Type |
|----------|-------------------|-------------------|
| Personal | BORN_IN, LIVES_IN | Location |
| Personal | HAS_PET | Pet |
| Professional | WORKS_AT, OWNS, FOUNDED | Company |
| Professional | ATTENDED | Company (school) or Event |
| Social | KNOWS, FRIEND_OF, SPOUSE_OF, PARENT_OF, DATING | Person |
| Projects | CREATED, BUILDING, WORKING_ON, CONTRIBUTED_TO | Project |
| Events | ATTENDED, HOSTED | Event |
| Location | LOCATED_IN, VISITED | Location |
| Content | AUTHORED, REFERENCES | Document |

### Required Fields

- `source_entity_id`: ID from RESOLVED_ENTITIES
- `relation_type`: SCREAMING_SNAKE_CASE
- `target_entity_id` OR `target_literal`: Where the relationship points
- `fact`: Natural language description
- `source_type`: `self_disclosed` / `mentioned` / `inferred`

### Optional Fields

- `valid_at`: ISO date when relationship became true
- `invalid_at`: ISO date when relationship stopped being true

{{custom_extraction_instructions}}

## Output Schema

```json
{
  "extracted_relationships": [
    {
      "source_entity_id": "integer - ID from RESOLVED_ENTITIES",
      "relation_type": "string - SCREAMING_SNAKE_CASE",
      "target_entity_id": "integer (optional) - ID from RESOLVED_ENTITIES",
      "target_literal": "string (optional) - For identity/temporal relationships",
      "fact": "string - Natural language description",
      "source_type": "string - 'self_disclosed', 'mentioned', or 'inferred'",
      "valid_at": "string (optional) - ISO date when became true",
      "invalid_at": "string (optional) - ISO date when stopped being true"
    }
  ]
}
```

## Examples

### Example 1: Identity and Employment

**Input:**
```
Tyler: My email is tyler@example.com. I started at Anthropic in January.
```

**Resolved Entities:**
```json
[
  {"id": 0, "uuid": "ent_tyler", "name": "Tyler", "entity_type": "Person"},
  {"id": 1, "uuid": "ent_anthropic", "name": "Anthropic", "entity_type": "Company"}
]
```

**Output:**
```json
{
  "extracted_relationships": [
    {
      "source_entity_id": 0,
      "relation_type": "HAS_EMAIL",
      "target_literal": "tyler@example.com",
      "fact": "Tyler's email is tyler@example.com",
      "source_type": "self_disclosed"
    },
    {
      "source_entity_id": 0,
      "relation_type": "WORKS_AT",
      "target_entity_id": 1,
      "fact": "Tyler started at Anthropic",
      "source_type": "self_disclosed",
      "valid_at": "2024-01"
    }
  ]
}
```

### Example 2: Temporal with Job Change

**Input:**
```
Tyler: I left Intent Systems last month and joined Anthropic. My birthday is May 15th, 1990.
```

**Resolved Entities:**
```json
[
  {"id": 0, "uuid": "ent_tyler", "name": "Tyler", "entity_type": "Person"},
  {"id": 1, "uuid": "ent_intent", "name": "Intent Systems", "entity_type": "Company"},
  {"id": 2, "uuid": "ent_anthropic", "name": "Anthropic", "entity_type": "Company"}
]
```

**Output:**
```json
{
  "extracted_relationships": [
    {
      "source_entity_id": 0,
      "relation_type": "WORKS_AT",
      "target_entity_id": 1,
      "fact": "Tyler worked at Intent Systems",
      "source_type": "self_disclosed",
      "invalid_at": "2025-12"
    },
    {
      "source_entity_id": 0,
      "relation_type": "WORKS_AT",
      "target_entity_id": 2,
      "fact": "Tyler joined Anthropic",
      "source_type": "self_disclosed",
      "valid_at": "2026-01"
    },
    {
      "source_entity_id": 0,
      "relation_type": "BORN_ON",
      "target_literal": "1990-05-15",
      "fact": "Tyler was born on May 15th, 1990",
      "source_type": "self_disclosed"
    }
  ]
}
```

### Example 3: Social Relationships

**Input:**
```
Tyler and Casey have been dating since February 2023. Casey lives in Austin.
```

**Resolved Entities:**
```json
[
  {"id": 0, "uuid": "ent_tyler", "name": "Tyler", "entity_type": "Person"},
  {"id": 1, "uuid": "ent_casey", "name": "Casey", "entity_type": "Person"},
  {"id": 2, "uuid": "ent_austin", "name": "Austin", "entity_type": "Location"}
]
```

**Output:**
```json
{
  "extracted_relationships": [
    {
      "source_entity_id": 0,
      "relation_type": "DATING",
      "target_entity_id": 1,
      "fact": "Tyler and Casey have been dating since February 2023",
      "source_type": "mentioned",
      "valid_at": "2023-02"
    },
    {
      "source_entity_id": 1,
      "relation_type": "LIVES_IN",
      "target_entity_id": 2,
      "fact": "Casey lives in Austin",
      "source_type": "mentioned"
    }
  ]
}
```

## Notes

- **Extraction is graph-independent** — deduplication happens at edge resolution
- Use `target_literal` for identity and temporal relationships; `target_entity_id` for everything else
- Only set `valid_at`/`invalid_at` when explicitly stated or clearly implied
- The `fact` field should be human-readable and preserve the original meaning
- Dates must be ISO 8601: `YYYY-MM-DD`, `YYYY-MM`, or `YYYY`
