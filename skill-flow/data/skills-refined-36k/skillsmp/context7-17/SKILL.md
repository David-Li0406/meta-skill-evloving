---
name: context7
description: Retrieve up-to-date documentation and code examples from Context7. Use when you need library/framework documentation or API examples.
license: Apache 2.0
---

## Context7 Integration

Context7 is an MCP server that provides up-to-date documentation and code examples for programming libraries and frameworks.

## When to Use Context7

Use Context7 when you need:
- Latest documentation for any programming library or framework
- Code examples and usage patterns
- API reference information
- Best practices for specific libraries

**Before using Context7**, you must:
1. Call `context7_resolve-library-id` to get the exact library ID
2. Then call `context7_query-docs` with that library ID

## Required Workflow

### Step 1: Resolve Library ID

Use `context7_resolve-library-id` first:

```
context7_resolve-library-id({
  libraryName: "react",
  query: "How do I use React hooks?"
})
```

This returns the exact Context7-compatible library ID (e.g., `/vercel/next.js/v14.3.0-canary.87`).

**Only skip this step** if the user explicitly provides a library ID in the format `/org/project` or `/org/project/version`.

### Step 2: Query Documentation

Use `context7_query-docs` with the resolved library ID:

```
context7_query-docs({
  libraryId: "/vercel/next.js/v14.3.0-canary.87",
  query: "How to implement server-side rendering with next 14?"
})
```

## Important Rules

- **NEVER** use `context7_query-docs` without first calling `context7_resolve-library-id` (unless user provides library ID)
- **NEVER** call these tools more than 3 times per question
- If you can't find what you need after 3 attempts, use the best information you have
- Don't include sensitive information (API keys, credentials, secrets) in queries
- Be specific and include relevant details in your query

## Examples

### Basic Example
```
# User asks: "How do I use React Query?"

1. Call context7_resolve-library-id:
   - libraryName: "react-query"
   - query: "How do I use React Query?"

2. Get result: /tanstack/react-query

3. Call context7_query-docs:
   - libraryId: "/tanstack/react-query"
   - query: "How do I use React Query? Include setup examples and basic usage patterns"
```

### Version-Specific Example
```
# User asks: "What's new in Next.js 14?"

1. Call context7_resolve-library-id:
   - libraryName: "next.js"
   - query: "What's new in Next.js 14?"

2. Get result: /vercel/next.js/v14.3.0-canary.87

3. Call context7_query-docs:
   - libraryId: "/vercel/next.js/v14.3.0-canary.87"
   - query: "What's new in Next.js 14? List new features and breaking changes"
```

### With User-Provided Library ID
```
# User asks: "Show me examples of /mongodb/docs aggregation"

1. Skip resolve-library-id (user provided ID)
2. Call context7_query-docs directly:
   - libraryId: "/mongodb/docs"
   - query: "Show me aggregation pipeline examples"
```

## What Context7 Provides

- Code snippets
- API documentation
- Usage examples
- Best practices
- Version-specific information
- Multiple library versions (when available)

## When NOT to Use Context7

Don't use Context7 for:
- Searching local codebase
- General web searches
- Running shell commands or local operations
- File operations (read/write files)
- Git operations

## Keywords

Context7, documentation, library docs, API reference, code examples, framework documentation, react, next.js, mongodb, express, django, rails, programming libraries, npm packages
