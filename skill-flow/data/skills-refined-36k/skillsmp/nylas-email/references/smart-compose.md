# Smart Compose API

AI-powered email generation using LLM.

## Generate New Message
```
POST /v3/grants/{grant_id}/messages/smart-compose
```

```json
{
  "prompt": "Write an email about..."
}
```

## Generate Reply
```
POST /v3/grants/{grant_id}/messages/{message_id}/smart-compose
```

```json
{
  "prompt": "Reply accepting the invitation..."
}
```

## Response Options

**REST (single response):**
```
Accept: application/json
```

**Streaming (SSE):**
```
Accept: text/event-stream
```

## Limitations
- Max prompt: 1,000 tokens
- Latency varies with complexity
- Requires Google or Microsoft grant
