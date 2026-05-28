---
name: search
description: Search CYNIC's collective memory for past judgments, patterns, and decisions. Use when asked to find, search, look up, query, or recall previous evaluations, patterns, or knowledge.
user-invocable: true
---

# /search - CYNIC Memory Search

*"The pack remembers everything"*

## Quick Start

```
/search <query>
```

## What It Does

Searches across CYNIC's knowledge base:
- **Judgments**: Past evaluations and scores
- **Patterns**: Detected recurring structures
- **Decisions**: Recorded choices
- **Knowledge**: Extracted facts

## Search Types

| Type | Searches |
|------|----------|
| `judgment` | Past evaluations |
| `pattern` | Detected patterns |
| `decision` | Decision records |
| `all` | Everything (default) |

## Examples

### Find Past Judgments
```
/search authentication security judgments
```

### Find Patterns
```
/search error handling patterns
```

### General Search
```
/search token quality
```

## Implementation

Use the 3-layer progressive search for efficiency:

```javascript
// Step 1: Get index (lightweight)
brain_search_index({ query: "<search terms>", limit: 20 })

// Step 2: Get context around interesting results
brain_timeline({ anchor: "jdg_abc123" })

// Step 3: Fetch full details only for filtered IDs
brain_get_observations({ ids: ["jdg_abc123", "pat_def456"] })
```

Or use the simple search:

```javascript
brain_search({
  query: "<search terms>",
  type: "judgment|pattern|decision|all",
  limit: 10
})
```

## Tips

- Be specific: "security vulnerabilities in auth" > "security"
- Use type filters to narrow results
- Check patterns for recurring issues

## See Also

- `/patterns` - Browse all patterns
- `/judge` - Create new judgments
- `/digest` - Add knowledge to search
