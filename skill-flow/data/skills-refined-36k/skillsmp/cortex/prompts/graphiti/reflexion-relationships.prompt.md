# Relationship Extraction Reflexion

Self-check to find relationships that may have been missed in initial extraction. Adapted from Graphiti's reflexion pass.

## System Prompt

You are an AI assistant that determines which facts have not been extracted from the given context.

## User Prompt

<PREVIOUS_EPISODES>
{{previous_episodes}}
</PREVIOUS_EPISODES>

<CURRENT_EPISODE>
{{episode_content}}
</CURRENT_EPISODE>

<EXTRACTED_ENTITIES>
{{entities}}
</EXTRACTED_ENTITIES>

<EXTRACTED_FACTS>
{{extracted_facts}}
</EXTRACTED_FACTS>

Given the above EPISODES, list of EXTRACTED ENTITIES, and list of EXTRACTED FACTS, determine if any facts haven't been extracted.

## Task

Review the CURRENT_EPISODE carefully and identify any factual relationships between entities that should have been extracted but weren't.

Consider:
- Professional relationships (works at, manages, reports to)
- Personal relationships (knows, friends with, related to)
- Actions (created, modified, owns, uses)
- Attributes expressed as relationships (located in, part of)

## Output Schema

```json
{
  "missing_facts": [
    "array of string descriptions of facts that weren't extracted"
  ]
}
```

If no facts were missed, return: `{"missing_facts": []}`

## Notes

- This is a self-check pass to improve extraction completeness
- Facts must involve entities that were extracted
- Include temporal context if present (when it started/ended)
