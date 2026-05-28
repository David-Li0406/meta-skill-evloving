# read_wiki_structure

Get a list of documentation topics for a GitHub repository.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| repoName | string | Yes | GitHub repository: owner/repo (e.g. "facebook/react") |

## Example

```bash
node ./scripts/mcp-caller.mjs call read_wiki_structure '{"repoName": "facebook/react"}'
```

Expected output:
```json
{
  "content": [{"type": "text", "text": "Available topics:\n1. Getting Started\n2. Hooks\n3. Components\n..."}]
}
```
