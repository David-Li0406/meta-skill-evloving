---
name: context7-documentation-lookup
description: Use this skill when you need to access up-to-date library documentation to ensure correct API usage while working with external libraries, frameworks, or packages.
---

# Skill body

## Overview

This skill provides access to current, version-specific documentation for libraries through the Context7 MCP server. Always consult Context7 for accurate API references, patterns, and examples when working with project dependencies.

## When to Use Context7

**Always use Context7 when:**
- Implementing new features with any library
- Debugging library-specific issues or errors
- Understanding correct API usage or patterns
- Working with version-specific features
- Needing code examples for library functionality
- Uncertain about current best practices for a library

## Workflow

1. **Resolve Library ID**: Call `resolve-library-id` with the library name and your query to get the exact Context7-compatible library ID.
   ```plaintext
   resolve-library-id("next.js")
   ```
   
2. **Fetch Documentation**: Use the resolved library ID to fetch documentation for your specific use case.
   ```plaintext
   get-library-docs("/vercel/next.js", "routing and server components", 5000)
   ```

3. **Implement**: Write code based on the retrieved documentation, ensuring to verify API signatures and patterns.

## Critical Rules

- **Never trust training data alone** for library APIs.
- Query docs **before** writing library code.
- Use specific queries to get relevant documentation.
- Limit to 3 calls per question; use the best result if not found.

## Best Practices

1. **Be specific**: Use detailed queries for better documentation matches.
2. **Check versions**: Library APIs change between versions.
3. **Verify examples**: Cross-reference multiple code snippets when available.
4. **Cache knowledge**: Reuse resolved library IDs within the same session.

## Example

**User**: "Add NextAuth"

1. `resolve-library-id("nextauth", "how to set up authentication")`
2. `get-library-docs(libraryId, "NextAuth setup and configuration", 5000)`
3. Implement based on current docs.