# Contradiction Detection (Edge Invalidation)

Determines which existing facts are contradicted by new information. Adapted from Graphiti's `invalidate_edges.py`.

## System Prompt

You are an AI assistant that determines which facts contradict each other.

## User Prompt

<EXISTING_FACTS>
{{existing_edges}}
</EXISTING_FACTS>

<NEW_FACT>
{{new_edge}}
</NEW_FACT>

Based on the provided EXISTING FACTS and a NEW FACT, determine which existing facts the new fact contradicts.

Return a list containing all IDs of the facts that are contradicted by the NEW FACT.
If there are no contradicted facts, return an empty list.

## Rules

A fact is contradicted when:
- The NEW FACT explicitly negates it (e.g., "Tyler no longer works at X" contradicts "Tyler works at X")
- The NEW FACT states an incompatible relationship (e.g., "Tyler works at Y" contradicts "Tyler works at X" for exclusive roles)
- The temporal bounds conflict (e.g., new fact says relationship ended)

**Do NOT mark as contradicted:**
- Facts that are simply not mentioned in the new episode
- Facts about different aspects of the same relationship
- Facts that can coexist (e.g., working at two companies part-time)

## Output Schema

```json
{
  "contradicted_facts": [
    "array of integer IDs of facts that should be invalidated"
  ]
}
```

If no facts are contradicted, return: `{"contradicted_facts": []}`

## Examples

**Contradiction - job change:**
```
EXISTING: [{id: 0, fact: "Tyler works at Intent Systems", type: "WORKS_AT"}]
NEW: {fact: "Tyler left Intent Systems to join Anthropic", type: "WORKS_AT"}
```
Result: {"contradicted_facts": [0]}

**Contradiction - relationship ended:**
```
EXISTING: [{id: 0, fact: "Tyler and Jane are married", valid_at: "2020-01-01", invalid_at: null}]
NEW: {fact: "Tyler divorced Jane in 2024"}
```
Result: {"contradicted_facts": [0]}
(The existing edge should have invalid_at set to 2024)

**No contradiction - different relationship:**
```
EXISTING: [{id: 0, fact: "Tyler works at Intent Systems"}]
NEW: {fact: "Tyler is friends with Casey"}
```
Result: {"contradicted_facts": []}

**No contradiction - can coexist:**
```
EXISTING: [{id: 0, fact: "Tyler works on HTAA project"}]
NEW: {fact: "Tyler also works on Cortex project"}
```
Result: {"contradicted_facts": []}

## Notes

- Contradiction detection happens AFTER entity and edge resolution
- Contradicted edges are not deleted - their `invalid_at` timestamp is set
- This preserves history while marking facts as no longer current
- Be conservative - when uncertain, do not mark as contradicted
