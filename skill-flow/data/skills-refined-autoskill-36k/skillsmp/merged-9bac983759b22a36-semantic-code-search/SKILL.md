---
name: semantic-code-search
description: Use this skill to perform semantic code searches that find code by meaning rather than exact keywords, helping users locate implementations and understand code behavior.
---

## When to Use

Use this skill when users ask conceptual questions about the codebase, such as "where is X implemented?", "how does Y work?", or "find the logic for Z". This tool is particularly useful for exploring unfamiliar codebases or when exact function names are unknown.

## Core Workflow

1. **Translate the Request**: Convert the user's question into 1–3 semantic search queries, including intent and any known identifiers.
2. **Run Semantic Search**: Use the `ogrep` or `osgrep` command to perform the search.
3. **Select and Fetch Evidence**: Review the top results and extract relevant code snippets using the chunk retrieval feature.
4. **Refine and Repeat**: If the evidence is insufficient, adjust the queries and repeat the search until enough information is gathered.
5. **Provide Citations**: Present the findings with file paths and line ranges, explaining the behavior based on the extracted code.

## Search Strategies

### For Architectural/System-Level Questions

1. **Broad Search**: Start with a conceptual query to map the landscape.
   - Example: `ogrep query "authentication checks"`
2. **Survey Results**: Identify patterns across files and layers.
3. **Strategic Reading**: Choose a few representative files to read.
4. **Refine Searches**: Use more specific queries as needed.

### For Targeted Implementation Details

1. **Specific Search**: Ask about precise logic.
   - Example: `ogrep query "logic for merging configurations"`
2. **Evaluate Results**: Check the relevance of snippets.
3. **One Search, One Read**: Pinpoint the best file and read it fully.

## Hybrid Search Strategy

Combining semantic search with traditional grep can enhance results. Use `ogrep` for exploration and `rg` (ripgrep) for precision.

### Example Workflow

1. **Discover with `ogrep`**: Find relevant files conceptually.
   - Example: `ogrep query "rate limiting"`
2. **Pinpoint with `rg`**: Search for exact matches in those files.
   - Example: `rg "RateLimiter" src/middleware/`

## Output Format

The output will include file paths, line numbers, and relevant code snippets. The format is as follows:

```
path/to/file:line [Tags] Code Snippet
```

### Tags

- `ORCHESTRATION`: Contains logic that coordinates other code.
- `DEFINITION`: Types, interfaces, classes.

## Efficiency Tips

- **More Words = Better**: Use specific queries for better results.
- **Prioritize ORCH Results**: Start with orchestration results for logic.
- **Trust the Semantics**: Use natural language queries instead of guessing terms.
- **Scope When Possible**: Limit searches to specific directories or file types.

## Commands Overview

```bash
# Index the codebase
ogrep index .

# Search by concept
ogrep query "how are payments processed"

# Expand context around a result
ogrep chunk "path/to/file:line" --context 1

# Get a file-level overview
ogrep query "authentication" --summarize
```

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `VOYAGE_API_KEY` | - | Voyage AI embeddings (recommended) |
| `OPENAI_API_KEY` | - | OpenAI embeddings (alternative) |
| `OGREP_SEARCH_MODE` | `hybrid` | Default search mode |

## Conclusion

This skill bridges the gap between user questions and code implementation, making it easier to explore and understand complex codebases without needing to know exact terms or file paths.