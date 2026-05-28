# resolve-library-id

Resolves a package/product name to a Context7-compatible library ID and returns matching libraries.

You MUST call this function before 'query-docs' to obtain a valid Context7-compatible library ID UNLESS the user explicitly provides a library ID in the format '/org/project' or '/org/project/version' in their query.

**Selection Process:**
1. Analyze the query to understand what library/package the user is looking for
2. Return the most relevant match based on:
   - Name similarity to the query (exact matches prioritized)
   - Description relevance to the query's intent
   - Documentation coverage (prioritize libraries with higher Code Snippet counts)
   - Source reputation (consider libraries with High or Medium reputation more authoritative)
   - Benchmark Score: Quality indicator (100 is the highest score)

**Response Format:**
- Return the selected library ID in a clearly marked section
- Provide a brief explanation for why this library was chosen
- If multiple good matches exist, acknowledge this but proceed with the most relevant one
- If no good matches exist, clearly state this and suggest query refinements

For ambiguous queries, request clarification before proceeding with a best-guess match.

**IMPORTANT**: Do not call this tool more than 3 times per question. If you cannot find what you need after 3 calls, use the best result you have.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | The user's original question or task. This is used to rank library results by relevance to what the user is trying to accomplish. IMPORTANT: Do not include any sensitive or confidential information such as API keys, passwords, credentials, or personal data in your query. |
| libraryName | string | Yes | Library name to search for and retrieve a Context7-compatible library ID. |

## Example

```bash
node ./scripts/mcp-caller.mjs call resolve-library-id '{"query": "How to use React hooks?", "libraryName": "react"}'
```

Expected output:
```json
{
  "content": [{"type": "text", "text": "Library ID: /facebook/react\n\nDescription: A JavaScript library for building user interfaces...\nBenchmark Score: 95\nCode Snippets: 1500+"}]
}
```
