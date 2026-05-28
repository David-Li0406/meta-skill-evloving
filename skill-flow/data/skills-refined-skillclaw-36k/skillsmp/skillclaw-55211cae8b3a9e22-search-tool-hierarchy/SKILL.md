---
name: search-tool-hierarchy
description: Use this skill when you need to efficiently search code using the appropriate tool based on the type of query.
---

# Search Tool Hierarchy

When searching code, use the following decision tree to select the most effective search tool based on your query type:

## Decision Tree

```
Query Type?
├── STRUCTURAL (code patterns)
│   → Use AST-grep
│   Examples: "def foo", "class Bar", "import X", "@decorator"
│
├── SEMANTIC (conceptual questions)
│   → Use LEANN
│   Examples: "how does auth work", "find error handling patterns"
│
├── LITERAL (exact identifiers)
│   → Use Grep
│   Examples: "TemporalMemory", "check_evocation", regex patterns
│
└── FULL CONTEXT (need complete understanding)
    → Use Read (last resort after finding the right file)
```

## Tool Comparison

| Tool      | Output Size | Best For                                      |
|-----------|-------------|-----------------------------------------------|
| AST-grep  | ~50 tokens  | Function/class definitions, imports, decorators|
| LEANN     | ~100 tokens | Conceptual questions, architecture, patterns   |
| Grep      | ~200-2000   | Exact identifiers, regex, file paths          |
| Read      | ~1500+      | Full understanding after finding the file     |

## DO

- Start with AST-grep for structural questions.
- Use LEANN for semantic queries.
- Use Grep for exact identifier matches.
- Read files only after identifying relevant ones.

## DON'T

- Use Grep for conceptual questions.
- Read files before determining relevance.
- Ignore tool suggestions.

## Examples

```bash
# STRUCTURAL → AST-grep
ast-grep --pattern "async def $FUNC($$$):" --lang python

# SEMANTIC → LEANN
leann search opc-dev "how does authentication work" --top-k 3

# LITERAL → Grep
grep "check_evocation" path=opc/scripts

# FULL CONTEXT → Read (after finding file)
read file_path=opc/scripts/z3_erotetic.py
```

## Optimal Flow

```
1. AST-grep: "Find async functions" → 3 file:line matches
2. Read: Top match only → Full understanding
3. Skip: 4 irrelevant files → 6000 tokens saved
```