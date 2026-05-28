---
name: context7-library-documentation
description: Use this skill to access up-to-date library documentation when working with external libraries, frameworks, or packages to ensure correct API usage.
---

# Context7 Library Documentation

## Overview

This skill provides access to up-to-date, version-specific documentation for libraries through the Context7 MCP server. Instead of relying on potentially outdated training data, use Context7 to fetch current documentation, API references, and code examples directly from library sources.

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
2. **Fetch Documentation**: Call `get-library-docs` with the resolved library ID and specific topic to retrieve relevant documentation.
3. **Implement**: Write code based on the retrieved documentation, ensuring to follow current best practices and API patterns.

## Example Usage

### Example 1: Adding NextAuth

```
1. Resolve library ID: resolve-library-id("nextauth", "how to set up authentication")
2. Fetch docs: get-library-docs(libraryId, "NextAuth setup and configuration")
3. Implement based on current docs
```

### Example 2: Implementing Framework Features

```
1. Resolve library ID: resolve-library-id("next.js")
2. Fetch docs: get-library-docs("/vercel/next.js", "server actions and mutations", 5000)
3. Review documentation for current patterns
4. Implement features following docs
```

## Critical Rules

- **Never trust training data alone** for library APIs.
- Query docs **before** writing library code.
- Use specific queries to get relevant documentation.
- Limit to 3 calls per question; use the best result if not found.

## Best Practices

1. **Be specific**: Use detailed queries for better documentation matches.
2. **Check versions**: Library APIs change between versions; verify compatibility.
3. **Verify examples**: Cross-reference multiple code snippets when available.
4. **Cache knowledge**: Reuse resolved library IDs within the same session.
5. **Combine multiple sources** for complex features spanning different libraries.

## Troubleshooting

### Library ID Not Found
If `resolve-library-id` doesn't find a library:
1. Try alternative names (e.g., "next" vs "next.js").
2. Search for the library on GitHub to find the org/repo structure.

### Documentation Too Broad
If returned docs are too general:
1. Make the topic more specific.
2. Include the exact API or feature name.

### Version Mismatch
If the version in Context7 differs from your package.json:
1. Request a specific version.
2. Consult CHANGELOG for breaking changes.

## Configuration Check

Before using this skill, verify Context7 MCP is configured:

**Check MCP configuration:**
```bash
claude mcp list
```

Ensure `context7` is in the list of available MCP servers. If not configured, follow the setup instructions provided in the original documentation.

## Summary

This skill ensures you always have access to current, accurate library documentation when building features. By proactively using Context7, you reduce bugs, follow best practices, and implement features correctly the first time. Always fetch Context7 docs before implementing any library API or feature.