---
name: context7
description: Look up current library documentation via Context7 MCP. Use when writing code that uses external libraries, frameworks, or packages to ensure correct API usage.
compatibility: opencode
metadata:
  workflow: documentation
---

## What I do

- Query up-to-date documentation for any library or framework
- Resolve library identifiers for accurate documentation lookup
- Provide current API references and code examples
- Ensure correct usage of external dependencies

## When to use me

Use this when working with external libraries, frameworks, or packages to ensure you're using the correct and current API syntax.

## Workflow

1. **Resolve library ID**: Call `context7_resolve-library-id` with the library name and your query
2. **Query documentation**: Call `context7_query-docs` with the resolved library ID and specific question
3. **Implement**: Write code based on the retrieved documentation

## When to Use

- External libraries (React, FastAPI, Prisma, Next.js, etc.)
- Frequently-updated packages where APIs may have changed
- Uncertain about API syntax or method signatures
- Any non-trivial import or library usage

## Example

```
User: "Add NextAuth"

1. context7_resolve-library-id("nextauth", "how to set up authentication")
2. context7_query-docs(libraryId, "NextAuth setup and configuration")
3. Implement based on current docs
```

## Critical Rules

- **Never trust training data alone** for library APIs
- Query docs BEFORE writing library code
- Use specific queries to get relevant documentation
- Limit to 3 calls per question - use best result if not found

## Best Practices

1. **Be specific**: Use detailed queries for better documentation matches
2. **Check versions**: Library APIs change between versions
3. **Verify examples**: Cross-reference multiple code snippets when available
4. **Cache knowledge**: Reuse resolved library IDs within the same session
