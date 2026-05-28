---
name: meaning-query
description: Semantic search through .meaning/ index using natural language queries
allowed-tools:
  - Bash
  - Read
---

# /meaning-query — Semantic Query Engine

Natural language search through the `.meaning/` semantic index. Ask questions about the codebase and get structured answers using tags, relationships, intents, and concepts.

## Purpose

This skill provides **instant semantic search** without needing to grep, read files, or guess locations. The meaning index already contains structured metadata—this skill lets you query it conversationally.

**When to use:**
- "Where is X implemented?"
- "What tests file Y?"
- "Show me all configuration files"
- "What needs review?"
- "Files that do authentication"
- "What changed recently?"

**Key benefit:** Zero-latency semantic search (no LLM calls, pure structured queries).

## Usage

```bash
# User asks Claude: "Where is parsing done?"

# Claude runs:
python -m meaning query "where is parsing done?"
```

The query engine automatically:
1. Parses natural language intent
2. Maps to structured queries (tags, relationships, concepts)
3. Returns relevant files with context

## Supported Query Types

### 1. Status Queries
Ask about file health and maintenance needs.

**Examples:**
- "what needs review?"
- "what is stale?"
- "show me files that need attention"

**Returns:** Files filtered by `needs_review` or `is_stale()` flags.

---

### 2. Tag Queries
Find files by their semantic tags.

**Examples:**
- "show me all test files"
- "find config files"
- "list API files"
- "show me documentation"

**Returns:** Files tagged with matching vocabulary (test, config, api, doc, etc).

---

### 3. Relationship Queries
Traverse the semantic graph.

**Examples:**
- "what tests the core module?"
- "what documents the API?"
- "what imports src/meaning/meaning_core.py?"
- "show me files that implement the spec"

**Returns:** Files connected via typed relationships (tests, documents, imports, implements, configures, calls).

---

### 4. Intent Queries
Search by what files do (semantic purpose).

**Examples:**
- "files that do parsing"
- "files about authentication"
- "validation files"
- "files that handle errors"

**Returns:** Files whose intent strings match keywords.

---

### 5. Temporal Queries
Find recently modified files.

**Examples:**
- "what changed recently?"
- "show me latest files"
- "recently updated files"

**Returns:** Files sorted by `last_verified` timestamp (most recent first).

---

### 6. Concept Queries
Explore semantic groupings.

**Examples:**
- "show me the core library"
- "files in the testing concept"
- "what's in project documentation?"

**Returns:** All files in a named concept with its description.

## Output Format

Query results include:
- **File paths** with status indicators (⚠️ for needs_review)
- **Intents** (truncated to 80 chars)
- **Tags** (first 5 shown)
- **Relationships** (summarized by type)
- **Explanation** of what was matched
- **Query type** detected (status, tag, relationship, intent, temporal, concept)

## Example Session

```markdown
User: Where is parsing implemented?

Claude: Let me search the semantic index for parsing-related files.

[Runs: python -m meaning query "files that do parsing"]

🔍 Query Results: Files tagged with: parsing
   Type: tag

  Found 2 files (showing 2):

  1. src/meaning/meaning_core.py
      "Core Python library implementing YAML parsing, validation..."
      Tags: core, module, api, parsing, validation
      Relationships: implements(1)

  2. src/meaning/meaning_inference.py
      "Inference engine that automatically generates semantic metadata..."
      Tags: core, module, api, parsing
      Relationships: imports(1), implements(1)

Parsing is primarily implemented in `src/meaning/meaning_core.py`, with additional
parsing logic in `src/meaning/meaning_inference.py`. Both files are part of the
core library concept.
```

## Implementation

```python
import subprocess
import json
from pathlib import Path

def run_query(query: str) -> dict:
    """Run a semantic query and parse results."""
    result = subprocess.run(
        ["python", "-m", "meaning", "query", query],
        capture_output=True,
        text=True,
        cwd=Path.cwd()
    )

    if result.returncode != 0:
        return {"error": result.stderr}

    return {"output": result.stdout}

# Example usage in skill
query = "what tests the core?"
result = run_query(query)
print(result["output"])
```

## Query Patterns Reference

| User Question | Query String | Type |
|---------------|--------------|------|
| "What needs fixing?" | "what needs review?" | status |
| "Test files?" | "show me all test files" | tag |
| "What tests X?" | "what tests X" | relationship |
| "Files doing auth?" | "files that do authentication" | intent |
| "Recent changes?" | "what changed recently?" | temporal |
| "Core library?" | "show me the core library" | concept |

## Tips for Claude

1. **Always use exact file paths in relationship queries**
   - Good: "what tests src/meaning/meaning_core.py"
   - Bad: "what tests the core" (works but less precise)

2. **Use natural language—don't over-think it**
   - The query engine handles variations automatically
   - "test files", "testing files", "tests" all work

3. **Check query type in output**
   - Tells you which matching strategy was used
   - Helps refine follow-up queries

4. **Combine with file reads**
   - Query finds candidates
   - Read specific files for details
   - Much faster than reading everything

5. **Fallback gracefully**
   - If query returns nothing, try broader terms
   - "files about X" works when tag queries don't

## When NOT to Use

- **Needle queries**: Looking for a specific class/function name → use Grep
- **Full-text search**: Searching code content → use Grep
- **File existence**: Checking if a file exists → use Glob or Read
- **Exploring raw files**: Reading unindexed files → use Read directly

Use this skill for **semantic understanding**, not code searching.

## Integration with Other Skills

```markdown
# Typical workflow:

1. /meaning-query "what tests the API?"
   → Find test files semantically

2. Read the test files
   → Understand test coverage

3. /meaning-update
   → Sync any new files after changes

4. /meaning-validate
   → Verify index health
```

## Error Handling

```python
# No .meaning/ directory found
❌ No .meaning/ directory found in /path/to/project
💡 Initialize with: python -m meaning init

# No results found
🔍 Query Results: No files found matching query: 'nonexistent'
   Type: no_match

  No files found.
```

## Performance

- **Query latency:** < 50ms (pure Python, no LLM calls)
- **Scales to:** ~5000 files efficiently
- **Memory:** Loads full index into memory (~1MB per 1000 files)

## Philosophy

```
Semantic search beats full-text search when:
- You care about purpose, not syntax
- You want structured results, not string matches
- You need relationships, not just content
- You value speed over exhaustiveness
```

The meaning index is **intentionally curated**—it's not exhaustive, it's semantic. Use Grep for exhaustive searches, use `/meaning-query` for understanding.

---

**Last updated:** 2026-01-21
