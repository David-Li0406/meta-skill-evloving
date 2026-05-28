---
name: context7
description: Use this skill to retrieve the latest documentation and code examples for software libraries and frameworks via the Context7 API, ensuring up-to-date information and preventing reliance on outdated training data.
---

# Context7 Documentation Retrieval

This skill enables the retrieval of current documentation and code examples for programming libraries and frameworks by querying the Context7 API.

**Prerequisite:** Set `CONTEXT7_API_KEY` environment variable.

## Workflow

### Step 1: Search for the Library

To find the Context7 library ID, query the search endpoint:

```bash
curl "https://context7.com/api/v2/libs/search?libraryName=<library_name>&query=<topic>" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

**Parameters:**
- `libraryName` (required): The name of the library (e.g., "react", "next.js").
- `query` (required): A description of the topic for relevance ranking.

**Response fields:**
- `id`: Library identifier for the context endpoint.
- `title`: Human-readable library name.
- `description`: Brief description of the library.
- `totalSnippets`: Number of documentation snippets available.

### Step 2: Fetch Documentation

To retrieve documentation, use the library ID obtained from the search:

```bash
curl "https://context7.com/api/v2/context?libraryId=<library_id>&query=<specific_query>&type=<format>" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

**Parameters:**
- `libraryId` (required): The library ID from search results.
- `query` (required): The specific topic to retrieve documentation for.
- `type` (optional): Response format - `json` (default) or `txt` (plain text).

## Usage Scenarios

Use this skill in the following cases:

1. **Explicit instruction**: When the user instructs "use context7" or "check the latest documentation".
2. **Library usage questions**: When asked about how to use a specific library's API, hooks, or functions.
3. **Code example requests**: When asked for code examples using a specific library.
4. **Version-specific information**: When library information for a specific version is needed.
5. **Uncertain API information**: When your knowledge might be outdated and latest information verification is needed.

## Best Practices

- Use `type=txt` for more readable output.
- Be specific with the `query` parameter to improve relevance ranking.
- If the first search result is not correct, check additional results in the array.
- URL-encode query parameters containing spaces (use `+` or `%20`).

## Error Handling

| Error | Solution |
|-------|----------|
| 404 (Not Found) | Search again with a different library name. |
| 429 (Rate Limit) | Wait a moment and retry. |
| Empty response | Retry with a more general query. |

## Resources

For detailed API specifications, see the Context7 API documentation.