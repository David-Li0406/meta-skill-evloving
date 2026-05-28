---
name: context7-documentation-retrieval
description: Use this skill to retrieve up-to-date documentation and code examples for programming libraries and frameworks via the Context7 API.
---

# Context7 Documentation Retrieval

This skill allows you to fetch the latest documentation, API references, and code examples for various programming libraries and frameworks using the Context7 API.

## When to Use

Activate this skill when:
- You need the latest documentation for any programming library or framework.
- You are looking for code examples and usage patterns.
- You require API reference information or best practices for specific libraries.
- The user asks about how to use a library, requests code examples, or mentions a specific library version.

## Workflow

### Step 1: Resolve Library ID

First, search for the library ID using the search endpoint:

```bash
curl -s "https://context7.com/api/v2/libs/search?libraryName=<library_name>&query=<topic>" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

**Parameters:**
- `libraryName` (required): The name of the library (e.g., "react", "next.js").
- `query` (required): A description of the topic for relevance ranking.

### Step 2: Fetch Documentation

Once you have the library ID, retrieve the documentation:

```bash
curl -s "https://context7.com/api/v2/context?libraryId=<library_id>&query=<specific_query>&type=<format>" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

**Parameters:**
- `libraryId` (required): The library ID obtained from the search results.
- `query` (required): The specific topic to retrieve documentation for.
- `type` (optional): Response format - `json` (default) or `txt` (for more readable output).

## Example Usage

### Example 1: Fetching React Hooks Documentation

1. **Search for React Library ID:**
   ```bash
   curl -s "https://context7.com/api/v2/libs/search?libraryName=react&query=hooks" \
     -H "Authorization: Bearer $CONTEXT7_API_KEY"
   ```

2. **Fetch Hooks Documentation:**
   ```bash
   curl -s "https://context7.com/api/v2/context?libraryId=/facebook/react&query=useState&type=txt" \
     -H "Authorization: Bearer $CONTEXT7_API_KEY"
   ```

### Example 2: Fetching Next.js Routing Documentation

1. **Search for Next.js Library ID:**
   ```bash
   curl -s "https://context7.com/api/v2/libs/search?libraryName=next.js&query=routing" \
     -H "Authorization: Bearer $CONTEXT7_API_KEY"
   ```

2. **Fetch Routing Documentation:**
   ```bash
   curl -s "https://context7.com/api/v2/context?libraryId=/vercel/next.js&query=app+router&type=txt" \
     -H "Authorization: Bearer $CONTEXT7_API_KEY"
   ```

## Important Notes

- Always search for the library ID first if unsure.
- Use specific queries to improve relevance ranking.
- URL-encode query parameters containing spaces.
- No API key is required for basic usage, but it is recommended for higher rate limits.

## Common Library IDs

| Library | ID |
| ------- | -- |
| React | `/facebook/react` |
| Next.js | `/vercel/next.js` |
| Prisma | `/prisma/prisma` |
| TailwindCSS | `/tailwindlabs/tailwindcss` |

## Error Handling

If requests fail:
- Verify that the library ID format is correct.
- Check network connectivity.
- Retry with a more general query if necessary.

## Conclusion

This skill provides a streamlined approach to accessing the latest documentation and code examples for various libraries, ensuring you have the most accurate and up-to-date information at your fingertips.