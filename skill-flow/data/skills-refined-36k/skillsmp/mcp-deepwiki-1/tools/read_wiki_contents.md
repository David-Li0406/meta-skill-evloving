# read_wiki_contents

View documentation about a GitHub repository.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| repoName | string | Yes | GitHub repository: owner/repo (e.g. "facebook/react") |

## Example

```bash
node ./scripts/mcp-caller.mjs call read_wiki_contents '{"repoName": "facebook/react"}'
```

Expected output:
```json
{
  "content": [{"type": "text", "text": "# React Documentation\n\nReact is a JavaScript library for building user interfaces...\n\n## Key Concepts\n..."}]
}
```
