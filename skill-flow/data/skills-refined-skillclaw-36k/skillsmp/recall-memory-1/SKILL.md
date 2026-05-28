---
name: recall-memory
description: Use when needing to retrieve information from past sessions, conversations, or stored knowledge. Triggers on questions that could benefit from historical context including user preferences, past discussions, workflows, coding patterns, or any query where previous session information would be helpful. Activates broadly for retrieval queries.
context: fork
---

# Recall Memory

Retrieve information stored across sessions using memU's agentic memory framework.

## Overview

This skill retrieves information from memU - a three-layer memory hierarchy that processes conversations into structured knowledge:

- **Resources**: Raw conversation data from past sessions
- **Items**: Extracted memory units (preferences, skills, opinions, habits, facts)
- **Categories**: Aggregated summaries with full traceability

**How it works**: Conversations are automatically memorized when sessions end (via SessionEnd hook). This skill retrieves that stored knowledge when needed.

## Script Path Construction

**IMPORTANT**: Always use full paths to call scripts. Do NOT use `cd` to change to the scripts directory.

The skill is located at: **Base directory for this skill** (shown when skill loads)

To call scripts, concatenate:
- **Skill base directory** + `/scripts/` + **script name**

Example:
```bash
# If skill base is: /home/user/.claude/plugins/memu/skills/recall-memory
# Then memu.py is at:
/home/user/.claude/plugins/memu/skills/recall-memory/scripts/memu.py
```

In examples below, we use `scripts/memu.py` as shorthand, but replace `scripts/` with the full path based on the skill's base directory.

## Retrieval Methods

memU supports two retrieval methods - choose based on query complexity:

### RAG (Recommended)

**When to use**: Specific factual queries, direct questions, known topics

- Fast vector-based similarity search
- Returns results in <2 seconds
- Good for: "What are my preferences?", "Do I use TypeScript or JavaScript?", "How do I handle errors?"
- Best when you know what you're looking for

**Example**:
```bash
scripts/memu.py retrieve --query "What coding style do I prefer?" --method rag
```

### LLM

**When to use**: Complex queries, ambiguous questions, need deep understanding

- Deep semantic understanding with adaptive refinement
- Slower (~5-10 seconds) but more thorough
- Good for: "What patterns do I follow when refactoring?", "How do I approach testing?", open-ended questions
- Best for nuanced or multi-faceted questions

**Example**:
```bash
scripts/memu.py retrieve --query "What patterns do I use in React components?" --method llm
```

**Choosing**: Start with RAG (faster). If results are insufficient or query is complex, use LLM.

## The Process

Follow these steps to retrieve memory:

### Step 1: Formulate Query

Convert user's question into a clear query string:

- User asks: "What do you know about my testing approach?"
- Query: "What is the user's testing approach?"

- User asks: "How do I usually name variables?"
- Query: "How does the user name variables?"

### Step 2: Choose Method

- Simple/direct question → RAG
- Complex/ambiguous question → LLM

### Step 3: Execute Retrieval

Call the script with appropriate method:

```bash
scripts/memu.py retrieve --query "your query here" --method rag
```

or

```bash
scripts/memu.py retrieve --query "your query here" --method llm
```

### Step 4: Parse Response

The script returns JSON with this structure:

```json
{
  "status": "ok",
  "data": {
    "categories": [
      {
        "name": "Coding Preferences",
        "summary": "User prefers TypeScript with strict typing..."
      }
    ],
    "items": [
      {
        "memory_type": "preference",
        "summary": "Prefers TypeScript over JavaScript"
      }
    ],
    "resources": [
      {
        "modality": "conversation",
        "url": "session-2024-01-15"
      }
    ]
  }
}
```

### Step 5: Integrate Results

Extract relevant information from the response:

1. Check `categories` for high-level summaries
2. Check `items` for specific facts/preferences
3. Integrate into your response to the user

## Command Reference

| Command | Purpose | Speed |
|---------|---------|-------|
| `scripts/memu.py retrieve --query "..." --method rag` | Fast retrieval (default) | <2s |
| `scripts/memu.py retrieve --query "..." --method llm` | Deep semantic retrieval | 5-10s |

**Required parameters**:
- `--query`: The question/search query (string)
- `--method`: Either `rag` or `llm` (default: `rag`)

**Output**: JSON to stdout with `status` and `data` fields

## Output Formats

### Success Response

```json
{
  "status": "ok",
  "data": {
    "categories": [/* category objects */],
    "items": [/* item objects */],
    "resources": [/* resource objects */]
  }
}
```

### Error Response

```json
{
  "status": "error",
  "error": "Error message here"
}
```

**Common errors**:
- `MEMU_API_KEY environment variable not set` - User needs to configure API key
- `API request failed` - Network issue or API down
- Empty results - No matching memories found (not an error, just empty data arrays)

## Practical Examples

### Example 1: Retrieving Code Preferences (RAG)

**User asks**: "What languages do I prefer?"

**Process**:
```bash
scripts/memu.py retrieve --query "What programming languages does the user prefer?" --method rag
```

**Response**:
```json
{
  "status": "ok",
  "data": {
    "items": [
      {"memory_type": "preference", "summary": "Prefers TypeScript over JavaScript"},
      {"memory_type": "preference", "summary": "Uses Python for scripting"}
    ]
  }
}
```

**Your response to user**: "Based on our previous discussions, you prefer TypeScript over JavaScript for application development, and you use Python for scripting tasks."

### Example 2: Complex Workflow Question (LLM)

**User asks**: "How do I usually approach refactoring?"

**Process**:
```bash
scripts/memu.py retrieve --query "How does the user approach refactoring code?" --method llm
```

**Response**:
```json
{
  "status": "ok",
  "data": {
    "categories": [
      {
        "name": "Refactoring Patterns",
        "summary": "User follows a systematic approach: write tests first, refactor in small steps, run tests after each change. Prefers extracting functions over inline complexity."
      }
    ]
  }
}
```

**Your response to user**: "You typically follow a systematic refactoring approach: you start by writing tests to ensure behavior is preserved, then refactor in small incremental steps, running tests after each change. You prefer extracting functions rather than leaving complex logic inline."

### Example 3: No Results

**User asks**: "What do you know about my deployment process?"

**Process**:
```bash
scripts/memu.py retrieve --query "What is the user's deployment process?" --method rag
```

**Response**:
```json
{
  "status": "ok",
  "data": {
    "categories": [],
    "items": [],
    "resources": []
  }
}
```

**Your response to user**: "I don't have any stored information about your deployment process yet. We haven't discussed this in previous sessions."

## Quick Reference

| Scenario | Method | Query Example |
|----------|--------|---------------|
| Specific preference | RAG | "What editor does the user prefer?" |
| Yes/no fact | RAG | "Does the user use TypeScript?" |
| Open-ended pattern | LLM | "How does the user structure React components?" |
| Complex workflow | LLM | "What is the user's testing strategy?" |
| No prior discussion | Either | (Will return empty results) |

**Remember**: Conversations are auto-memorized at session end, so knowledge accumulates over time.
