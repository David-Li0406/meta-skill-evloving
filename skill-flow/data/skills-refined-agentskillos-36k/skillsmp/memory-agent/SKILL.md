---
name: memory-agent
description: HAIOS Memory Agent for intelligent context retrieval and learning. Use BEFORE answering complex questions to retrieve relevant strategies and context. Use AFTER completing tasks to extract and store learnings. Closes the ReasoningBank loop by injecting strategies into reasoning.
---
# generated: 2025-12-05
# System Auto: last updated on: 2025-12-10 18:36:48

# Memory Agent

This skill implements the ReasoningBank pattern for experiential learning. It retrieves relevant past experiences before reasoning and extracts new learnings after task completion.

## Requirement Level

**SHOULD** invoke this skill:
- BEFORE complex tasks to retrieve relevant strategies
- AFTER completing significant work to extract learnings

## When to Use

### BEFORE Answering (Retrieval)
**SHOULD** use when:
- Answering questions about HAIOS architecture, ADRs, or system design
- Implementing features that may have been attempted before
- Debugging issues that may have known solutions
- Any task where past experience could help

### AFTER Completing (Extraction)
**SHOULD** use when:
- A complex task was successfully completed
- A novel solution was discovered
- An error was encountered and resolved
- Important context should be preserved for future sessions

## Instructions

### Step 1: Retrieve Context (BEFORE Reasoning)

When facing a complex question or task, FIRST search for relevant experience:

```
memory_search_with_experience(
    query="<describe the task or question>",
    space_id="dev_copilot"
)
```

The response includes:
- **results**: Matching concepts and entities from memory
- **relevant_strategies**: Past reasoning traces that succeeded or failed

### Step 2: Apply Retrieved Strategies (INJECT INTO REASONING)

**CRITICAL**: Do not just acknowledge the strategies - APPLY them to your reasoning.

Example injection pattern:
```
Based on past experience in this codebase:
- [Strategy 1 from memory_search_with_experience]
- [Strategy 2 from memory_search_with_experience]

Applying these learnings to the current task:
[Your enhanced reasoning here]
```

### Step 3: Extract Learnings (AFTER Task Completion)

After completing a significant task, extract and store the learning:

```
ingester_ingest(
    content="<what was learned, what worked, what failed>",
    source_path="session:<date>:<brief-context>",
    content_type_hint="techne"  # for practical knowledge
)
```

**MUST NOT** use `memory_store` (deprecated). Use `ingester_ingest` with `content_type_hint` parameter instead.

## Classification Guide

- **episteme**: Facts, definitions, verified truths
- **techne**: Practical knowledge, how-to, skills
- **doxa**: Opinions, beliefs, interpretations

## Example Workflow

### Scenario: Implementing a new feature

1. **BEFORE** - Retrieve context:
```
memory_search_with_experience(
    query="implement embedding generation for concepts",
    space_id="dev_copilot"
)
```

2. **INJECT** - Apply to reasoning:
```
Past experience shows:
- The Gemini API has rate limits of 1500 RPM
- Batch processing with 10-item chunks works well
- Always check for existing embeddings before regenerating

Applying this to current implementation...
```

3. **AFTER** - Store learnings:
```
ingester_ingest(
    content="For embedding generation, use batch_size=10 with 100ms delay between batches to avoid rate limits. Check concept.embedding IS NULL before processing.",
    source_path="session:2025-12-05:embedding-optimization",
    content_type_hint="techne"
)
```

## Related Tools

| Tool | Purpose |
|------|---------|
| `ingester_ingest` | **PRIMARY** - Auto-classify and store with entity extraction |
| `memory_search_with_experience` | Retrieve context + strategies |
| `memory_stats` | Check memory system status |
| `extract_content` | Entity/concept extraction |
| `interpreter_translate` | Natural language to directive |
| `memory_store` | **MUST NOT** use - deprecated, use `ingester_ingest` |

## The ReasoningBank Loop

```
         +-----------------+
         |   NEW QUERY     |
         +--------+--------+
                  |
                  v
    +-------------+-------------+
    |  RETRIEVE (Step 1)        |
    |  memory_search_with_exp   |
    +-------------+-------------+
                  |
                  v
    +-------------+-------------+
    |  INJECT (Step 2)          |
    |  Apply strategies to      |
    |  current reasoning        |<---- THIS CLOSES THE LOOP
    +-------------+-------------+
                  |
                  v
    +-------------+-------------+
    |  EXECUTE                  |
    |  Complete the task        |
    +-------------+-------------+
                  |
                  v
    +-------------+-------------+
    |  EXTRACT (Step 3)         |
    |  ingester_ingest          |
    +-------------+-------------+
                  |
                  v
         +--------+--------+
         |   MEMORY DB     |
         +-----------------+
```

## Best Practices

1. **Always retrieve before complex tasks** - Past failures are as valuable as successes
2. **Be specific in queries** - "embedding generation rate limits" beats "embeddings"
3. **Include context in source_path** - Makes future retrieval easier
4. **Extract both success AND failure** - The paper shows failures are valuable for learning
5. **Use space_id consistently** - "dev_copilot" for development context

## IMPORTANT: Use `ingester_ingest` for Storage

**PRIMARY TOOL:** Always use `ingester_ingest` for storing learnings. It provides:
- Auto-classification (no manual type required)
- Entity extraction
- Provenance tracking
- No parameter format issues

**DEPRECATED:** `memory_store` is deprecated and returns a deprecation warning.
If you see code using `memory_store`, migrate it to `ingester_ingest`.
