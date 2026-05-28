# Entity Extraction Reflexion

Self-check to find entities that may have been missed in initial extraction. Adapted from Graphiti's reflexion pass.

## System Prompt

You are an AI assistant that determines which entities have not been extracted from the given context.

## User Prompt

<PREVIOUS_EPISODES>
{{previous_episodes}}
</PREVIOUS_EPISODES>

<CURRENT_EPISODE>
{{episode_content}}
</CURRENT_EPISODE>

<EXTRACTED_ENTITIES>
{{extracted_entities}}
</EXTRACTED_ENTITIES>

Given the above previous episodes, current episode, and list of extracted entities, determine if any entities haven't been extracted.

## Task

Review the CURRENT_EPISODE carefully and identify any significant entities that should have been extracted but weren't.

Consider:
- Named people, places, organizations
- Concepts or topics being discussed
- Systems, projects, or products mentioned
- Files, tools, or technologies referenced

## Output Schema

```json
{
  "missed_entities": [
    "array of string names of entities that weren't extracted"
  ]
}
```

If no entities were missed, return: `{"missed_entities": []}`

## Notes

- This is a self-check pass to improve extraction completeness
- Focus on entities in the CURRENT_EPISODE, not previous episodes
- Don't extract temporal information (dates, times)
- Don't extract relationships or actions
