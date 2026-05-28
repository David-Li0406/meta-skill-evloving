# Edge Resolution (Deduplication)

Determines whether extracted relationships are duplicates of existing relationships. Adapted from Graphiti's `dedupe_edges.py`.

## System Prompt

You are a helpful assistant that determines whether extracted facts are duplicates of existing facts in a knowledge graph.

## User Prompt

<PREVIOUS_EPISODES>
{{previous_episodes}}
</PREVIOUS_EPISODES>

<CURRENT_EPISODE>
{{episode_content}}
</CURRENT_EPISODE>

<NEW_EDGE>
{{new_edge}}
</NEW_EDGE>

<EXISTING_EDGES>
{{existing_edges}}
</EXISTING_EDGES>

Given the NEW EDGE extracted from the conversation and the EXISTING EDGES in the knowledge graph, determine if the NEW EDGE is a duplicate of any existing edge.

## Rules

Edges should be considered duplicates if they:
- Connect the same two entities
- Express the same semantic relationship
- Have consistent temporal bounds

**Do NOT mark as duplicates if:**
- The relationship type is semantically different (e.g., WORKS_AT vs WORKED_AT)
- The temporal bounds conflict (one says current, other says past)
- The facts describe different aspects of the relationship

## Task

1. Compare NEW EDGE against each EXISTING EDGE
2. Identify if the NEW EDGE is semantically equivalent to any existing edge
3. If duplicate, return the index of the best match
4. If not duplicate, return -1

## Output Schema

```json
{
  "is_duplicate": "boolean - Whether this edge duplicates an existing edge",
  "duplicate_idx": "integer - Index of the duplicate edge, or -1 if not duplicate",
  "should_merge": "boolean - Whether the new edge has additional info to merge",
  "merge_notes": "string - What information should be merged (if any)"
}
```

## Example

**Duplicate case:**
```
NEW EDGE: {source: "Tyler", target: "Intent Systems", type: "WORKS_AT", fact: "Tyler works at Intent Systems"}
EXISTING: [{idx: 0, source: "Tyler Brandt", target: "Intent Systems", type: "WORKS_AT", fact: "Tyler has been at Intent Systems since 2024"}]
```
Result: {is_duplicate: true, duplicate_idx: 0, should_merge: false, merge_notes: ""}

**Not duplicate (different relationship):**
```
NEW EDGE: {source: "Tyler", target: "Casey", type: "LIVES_WITH", fact: "Tyler lives with Casey"}
EXISTING: [{idx: 0, source: "Tyler", target: "Casey", type: "DATING", fact: "Tyler is dating Casey"}]
```
Result: {is_duplicate: false, duplicate_idx: -1, should_merge: false, merge_notes: ""}

**Merge case (new temporal info):**
```
NEW EDGE: {source: "Tyler", target: "Intent Systems", type: "WORKS_AT", valid_at: "2024-01-01"}
EXISTING: [{idx: 0, source: "Tyler", target: "Intent Systems", type: "WORKS_AT", valid_at: null}]
```
Result: {is_duplicate: true, duplicate_idx: 0, should_merge: true, merge_notes: "New edge provides valid_at date"}
