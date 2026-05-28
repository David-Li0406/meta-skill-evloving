# Error Handling Reference

Comprehensive guide for handling Jira API errors in read operations.

## HTTP Status Codes

### 4xx Client Errors

| Status | Name | Cause | Action |
|--------|------|-------|--------|
| 400 | Bad Request | Invalid JQL syntax, malformed request | Parse error message, fix query syntax |
| 401 | Unauthorized | Missing or invalid API token | Check credentials, do not retry |
| 403 | Forbidden | Valid auth but no permission | Check project/issue permissions |
| 404 | Not Found | Issue/project doesn't exist | Return clear "not found" message |
| 405 | Method Not Allowed | Wrong HTTP method | Internal error, check API call |
| 429 | Too Many Requests | Rate limit exceeded | Implement exponential backoff |

### 5xx Server Errors

| Status | Name | Cause | Action |
|--------|------|-------|--------|
| 500 | Internal Server Error | Jira server issue | Retry with backoff, max 3 attempts |
| 502 | Bad Gateway | Proxy/load balancer issue | Retry after 5 seconds |
| 503 | Service Unavailable | Jira maintenance/overload | Check Jira status, retry later |
| 504 | Gateway Timeout | Request took too long | Simplify query, reduce scope |

## Common Error Scenarios

### JQL Syntax Errors

**Error**: `The value 'xxx' does not exist for the field 'project'`
```
Cause: Project key doesn't exist or no access
Fix: Verify project key, check permissions
```

**Error**: `Field 'xxx' does not exist or you do not have permission`
```
Cause: Custom field not available or restricted
Fix: Use field ID (customfield_XXXXX) or check permissions
```

**Error**: `The operator 'xxx' is not supported by field 'yyy'`
```
Cause: Wrong operator for field type
Fix: Use correct operator (e.g., ~ for text, = for exact match)
```

### Authentication Errors

**Error**: `Basic authentication with passwords is deprecated`
```
Cause: Using password instead of API token
Fix: Generate API token at https://id.atlassian.com/manage/api-tokens
```

**Error**: `Unauthorized (401)`
```
Cause: Invalid or expired API token
Fix: Regenerate API token, update configuration
```

### Rate Limiting

**Error**: `Rate limit exceeded (429)`
```
Strategy:
1. Check Retry-After header for wait time
2. Implement exponential backoff: 1s, 2s, 4s, 8s...
3. Maximum 5 retry attempts
4. Consider caching frequently accessed data
```

## Retry Strategy

```
Attempt 1: Immediate
Attempt 2: Wait 1 second
Attempt 3: Wait 2 seconds
Attempt 4: Wait 4 seconds
Attempt 5: Wait 8 seconds
After 5 attempts: Fail with clear error message
```

### Retryable vs Non-Retryable

| Retryable | Non-Retryable |
|-----------|---------------|
| 429 (Rate Limit) | 400 (Bad Request) |
| 500 (Server Error) | 401 (Unauthorized) |
| 502 (Bad Gateway) | 403 (Forbidden) |
| 503 (Unavailable) | 404 (Not Found) |
| 504 (Timeout) | 405 (Method Not Allowed) |
| Network errors | JQL syntax errors |

## Error Response Format

When returning errors to the agent, use this structure:

```json
{
  "error": true,
  "code": "NOT_FOUND",
  "message": "Issue PROJ-999 not found",
  "details": {
    "issueKey": "PROJ-999",
    "suggestion": "Verify the issue key exists and you have access"
  },
  "retryable": false
}
```

## Security Considerations

- Never expose full API tokens in error messages
- Sanitize error details before logging
- Don't reveal internal paths or configurations
- Log request IDs for debugging without sensitive data
