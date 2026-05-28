# ask_question

Ask any question about a GitHub repository.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| repoName | string | Yes | GitHub repository: owner/repo (e.g. "facebook/react") |
| question | string | Yes | The question to ask about the repository |

## Example

```bash
node ./scripts/mcp-caller.mjs call ask_question '{"repoName": "facebook/react", "question": "How do hooks work?"}'
```

Expected output:
```json
{
  "content": [{"type": "text", "text": "Hooks are functions that let you use React state and lifecycle features in function components...\n\nThe most common hooks are:\n- useState: manages state\n- useEffect: handles side effects\n..."}]
}
```
