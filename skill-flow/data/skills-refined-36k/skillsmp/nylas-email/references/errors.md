# Error Handling

## Common Status Codes

| Code | Type | Description |
|------|------|-------------|
| 200 | Success | Request completed |
| 400 | Bad Request | Invalid JSON or parameters |
| 402 | Message Rejected | Provider rejected (content/recipients) |
| 403 | Unauthorized | Auth failed with provider |
| 422 | Provider Error | Provider-side sending error |
| 429 | Rate Limited | Quota exceeded or throttled |
| 503 | Service Unavailable | Provider connection error |

## Error Response Format
```json
{
  "type": "string",
  "message": "string",
  "server_error": "string (optional, provider error)"
}
```

## Best Practices
- Implement exponential backoff for 503 errors
- Wait 10-20 minutes after repeated 503s before retrying
- Set 150-second timeout for send operations

## Rate Limits

**Nylas:** Varies by plan tier (429 when exceeded)

**Google:** ~100 messages/second, sending quotas per account

**Microsoft:** Varies by subscription type

**IMAP:** Provider-specific

**Mitigation:**
- Filter results with query parameters
- Use pagination
- Implement caching
- Use webhooks instead of polling
