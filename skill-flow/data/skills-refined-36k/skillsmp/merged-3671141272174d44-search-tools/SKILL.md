---
name: search-tools
description: Use this skill when you need to efficiently search code using various tools based on the type of query.
---

# Search Tool Hierarchy

When searching code, use the following decision tree to select the appropriate tool based on your query type:

## Decision Tree

```
Need CONCEPTUAL/SEMANTIC search?
  (how does X work, find patterns, understand architecture)
  → Use LEANN (embedding-based semantic search)
  → PreToolUse hook auto-redirects semantic Grep queries

Need to understand code STRUCTURE?
  (find function calls, class usages, refactor patterns)
  → Use AST-grep

Need to find TEXT in code?
  → Use Morph (20x faster text search)
  → If no Morph API key: fall back to Grep tool

Simple one-off search?
  → Use built-in Grep tool directly
```

## Tool Comparison

| Tool      | Best For                                                                 | Requires         |
|-----------|--------------------------------------------------------------------------|------------------|
| **LEANN** | Semantic search: "how does caching work", "error handling patterns"     | Index built      |
| **AST-grep** | Structural patterns: "find all calls to `foo()`", refactoring         | MCP server       |
| **Morph** | Fast text search: "find files mentioning error"                         | API key          |
| **Grep**  | Literal patterns, class/function names, regex                            | Nothing (built-in)|

## Examples

**LEANN** (semantic/conceptual):
- "how does authentication work"
- "find error handling patterns"
- "where is rate limiting implemented"

**AST-grep** (structural):
- "Find all functions that return a Promise"
- "Find all React components using useState"
- "Refactor all imports of X to Y"

**Morph** (text search):
- "Find all files mentioning 'authentication'"
- "Search for TODO comments"

**Grep** (literal):
- `class ProviderAdapter`
- `def __init__`
- Regex patterns

## LEANN Commands

```bash
# Search with semantic query
leann search opc-dev "how does blackboard communication work" --top-k 5

# List available indexes
leann list

# Rebuild index (when code changes)
leann build opc-dev --docs dir1 dir2 --no-recompute --no-compact --force
```

## Optimal Flow

1. Start with AST-grep for code structure questions.
2. Use LEANN for conceptual queries.
3. Use Morph for fast text searches.
4. Use Grep for exact identifier matches.

## DO

- Follow the decision tree to select the appropriate tool.
- Use the hooks to optimize your search process.

## DON'T

- Use Grep for conceptual questions (returns nothing).
- Read files before knowing which ones are relevant.
- Ignore hook suggestions.