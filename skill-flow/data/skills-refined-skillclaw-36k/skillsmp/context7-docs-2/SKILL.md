---
name: context7-docs
description: Use when asked about library/framework APIs, version-specific features, or when user mentions outdated docs. Requires Context7 MCP server.
---

# Context7 Documentation Lookup

Fetch up-to-date library documentation via Context7 MCP instead of relying on stale training data.

**Requires:** Context7 MCP configured (`context7` in mcp list)

## When to Use

**Use Context7 when:**
- User asks about library/framework APIs
- Version-specific features (React 19, Next.js 15, etc.)
- User mentions outdated docs or getting errors
- Unsure if training data is current

**Do NOT rely on training data for library APIs.** Use Context7 to fetch live docs.

## Workflow

1. `resolve-library-id` → Get library ID (e.g., "/facebook/react")
2. `query-docs` → Fetch docs for specific topic
3. Answer using fetched documentation

## Example

User: "How do I use React 19's `use` hook?"

```
resolve-library-id("react") → "/facebook/react"
query-docs(library_id="/facebook/react", query="use hook") → [docs]
Answer from fetched docs
```

## Red Flags - Use Context7

- "How do I..." + library name
- Version numbers (v19, 15.x)
- "docs seem outdated"
- "I keep getting errors"

## Do NOT Skip Because

| Excuse | Reality |
|--------|---------|
| "I know this library" | APIs change. Fetch current docs. |
| "Basic usage" | Basics change between versions. |
| "User can correct me" | Wrong answers waste time. Verify first. |

## If Context7 Unavailable

Check `mcp list` for context7. If not configured, fall back to WebSearch but warn user that docs may not be current.
