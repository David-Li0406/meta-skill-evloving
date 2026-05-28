---
name: context7
description: Use Context7 MCP to access up-to-date library documentation when working with project dependencies. Always consult Context7 for accurate API references, patterns, and examples when doing in-depth work with libraries.
---

# Context7 Library Documentation

## Overview

This skill provides access to up-to-date, version-specific documentation for libraries through the Context7 MCP server. Instead of relying on potentially outdated training data, use Context7 to fetch current documentation, API references, and code examples directly from library sources.

## When to Use Context7

**ALWAYS use Context7 when:**
- Implementing new features with any library
- Debugging library-specific issues or errors
- Understanding correct API usage or patterns
- Working with version-specific features
- Needing code examples for library functionality
- Uncertain about current best practices for a library

**Before starting significant work** with any library, use Context7 to:
1. Verify current API patterns and signatures
2. Get version-specific documentation
3. Find official code examples and best practices
4. Understand breaking changes or deprecations

## How to Use Context7 MCP

### Step 1: Resolve Library ID

Before fetching documentation, resolve the library ID (if not already known):

```
Use the Context7 MCP tool: resolve-library-id
Arguments: { "libraryName": "next.js" }
```

This returns the exact Context7-compatible library ID and available versions.

### Step 2: Fetch Documentation

Once you have the library ID, fetch documentation for your specific use case:

```
Use the Context7 MCP tool: get-library-docs
Arguments: {
  "context7CompatibleLibraryID": "/vercel/next.js",
  "topic": "routing and server components",
  "tokens": 5000
}
```

**Recommended token ranges:**
- Quick reference: 2000-3000 tokens
- Feature implementation: 5000-8000 tokens
- Complex patterns: 8000-12000 tokens

### Step 3: Apply Documentation

Use the fetched documentation to:
1. Verify API signatures and patterns
2. Follow current best practices
3. Implement features correctly
4. Avoid deprecated patterns

## Workflow Examples

### Example 1: Implementing Framework Features

```
1. Resolve library ID: resolve-library-id("next.js")
2. Fetch docs: get-library-docs("/vercel/next.js", "server actions and mutations", 5000)
3. Review documentation for current patterns
4. Implement features following docs
5. If errors occur, fetch more specific docs about the error
```

### Example 2: Configuring Backend Middleware

```
1. Resolve library ID: resolve-library-id("fastapi")
2. Fetch docs: get-library-docs("/tiangolo/fastapi", "middleware and CORS", 4000)
3. Review middleware patterns and configuration
4. Implement middleware based on official examples
5. Verify implementation matches current best practices
```

### Example 3: Using Validation Libraries

```
1. Resolve library IDs: resolve-library-id("zod")
2. Fetch docs: get-library-docs("/colinhacks/zod", "schema validation and type inference", 3000)
3. Review schema definition patterns
4. Create schemas following docs
5. Validate integration with framework patterns
```

## Best Practices

### 1. Always Fetch First for New Features

Before implementing any significant feature with a library, fetch Context7 docs to ensure you're using current patterns and APIs.

### 2. Use Specific Topics

Be specific in your topic parameter:
- ✅ "server actions and form validation"
- ✅ "async generators and streaming"
- ❌ "next.js" (too broad)
- ❌ "help" (not specific)

### 3. Verify Version Compatibility

When fetching docs, note the version returned and compare with your package.json version. Request specific versions if needed:
```
context7CompatibleLibraryID: "/vercel/next.js/v15.0.0"
```

### 4. Cache Common Patterns Mentally

After fetching docs for a common pattern, remember the key insights for similar use cases. Re-fetch if uncertain or if significant time has passed.

### 5. Combine Multiple Sources for Complex Features

For features spanning multiple libraries, fetch docs for each relevant library.

### 6. Use Context7 for Error Resolution

When encountering library-specific errors:
1. Identify the specific library causing the error
2. Fetch docs with the error message or feature as the topic
3. Review breaking changes or migration guides
4. Apply fixes based on current documentation

## Integration with Development Workflow

### Planning Phase
- Identify all libraries involved in the feature
- Resolve Context7 IDs for each library
- Fetch high-level documentation for architecture planning

### Implementation Phase
- Fetch detailed docs for specific APIs and patterns
- Reference examples and code snippets
- Verify type signatures and function parameters

### Debugging Phase
- Fetch docs about error-related features
- Review troubleshooting sections
- Check for known issues or breaking changes

### Code Review Phase
- Verify implementations match current best practices
- Check for deprecated patterns
- Ensure version compatibility

## Troubleshooting

### Library ID Not Found
If `resolve-library-id` doesn't find a library:
1. Try alternative names (e.g., "next" vs "next.js")
2. Try organization name (e.g., "vercel/next.js")
3. Search for the library on GitHub to find the org/repo structure
4. For custom/vendored libraries, skip Context7 and use code directly

### Documentation Too Broad
If returned docs are too general:
1. Make topic more specific
2. Include the exact API or feature name
3. Mention the use case in the topic

### Version Mismatch
If the version in Context7 differs from your package.json:
1. Request specific version: `/org/lib/v1.2.3`
2. Check if patterns still apply to your version
3. Consult CHANGELOG for breaking changes
4. Consider updating the library if feasible

## Configuration Check

Before using this skill, verify Context7 MCP is configured:

**Check MCP configuration:**
```bash
claude mcp list
```

Should show `context7` in the list of available MCP servers.

**If not configured**, the .mcp.json file in this plugin provides the configuration. Ensure it's loaded or add Context7 MCP manually:
```bash
# Remote server
claude mcp add --transport http context7 https://mcp.context7.com/mcp \
  --header "CONTEXT7_API_KEY: ctx7sk_your_api_key"

# OR local server
claude mcp add context7 -- npx -y @upstash/context7-mcp \
  --api-key ctx7sk_your_api_key
```

## Summary

This skill ensures you always have access to current, accurate library documentation when building features. By proactively using Context7, you reduce bugs, follow best practices, and implement features correctly the first time.

**Remember**: When in doubt about any library API, pattern, or feature, fetch Context7 docs before implementing.
