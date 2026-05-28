# Entity Summary Extraction

Generates or updates a summary for an entity based on episode context. Adapted from Graphiti's `extract_summary`.

## System Prompt

You are a helpful assistant that extracts entity summaries from the provided text.

## User Prompt

<EPISODES>
{{previous_episodes}}
{{current_episode}}
</EPISODES>

<ENTITY>
{{entity}}
</ENTITY>

Given the EPISODES and the ENTITY, update the summary that combines relevant information about the entity from the episodes and relevant information from the existing summary.

## Summary Guidelines

1. **Relevance**: Only include information directly related to the entity
2. **Conciseness**: Keep under 500 characters
3. **Currency**: Prefer recent information over old
4. **Factual**: Only include stated facts, not inferences
5. **Neutral**: Maintain objective tone

## Output Schema

```json
{
  "summary": "string - Summary containing important information about the entity. Under 500 characters."
}
```

## Example

```
ENTITY: {name: "Tyler Brandt", type: "Person", current_summary: "Software engineer"}
EPISODES: ["Tyler works at Intent Systems on trading systems", "Tyler lives in Austin with Casey"]
```

Result:
```json
{
  "summary": "Software engineer at Intent Systems working on trading systems. Based in Austin, Texas."
}
```

## Notes

- Summaries are updated incrementally as new episodes mention the entity
- The summary provides quick context during search/retrieval
- Keep summaries factual and verifiable from the source episodes
