# Production Backend Kit

This project uses **Backend Engineering Kit (BEK)** for production backend patterns.

## CLI

```bash
bek search "error handling"    # Find patterns
bek show api-error-model       # View details
bek gate --checklist <id>      # Quality gate
```

## Core Patterns

### Error Handling

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request",
    "details": [{"field": "email", "message": "Invalid format"}],
    "requestId": "req_abc123"
  }
}
```

HTTP status codes:
- `400` Validation errors
- `401` Auth required
- `403` Permission denied
- `404` Not found
- `409` Conflict
- `429` Rate limited
- `500` Server error

### Pagination

Cursor-based (real-time data):
```json
{"data": [], "pagination": {"cursor": "abc", "hasMore": true}}
```

Offset-based (static lists):
```json
{"data": [], "pagination": {"total": 100, "page": 1, "hasMore": true}}
```

### Input Validation

- Validate at API boundary
- Use schema validation (Zod, Pydantic, etc.)
- Return field-level errors
- Sanitize before database ops

## Security

- Never log sensitive data
- Use parameterized queries
- Hash passwords (bcrypt/argon2)
- Implement rate limiting
- Validate all inputs

## Database

- Use connection pooling
- Add proper indexes
- Use transactions for multi-step ops
- Include timestamps

## Reliability

- Set timeouts for external calls
- Use circuit breakers
- Implement retries with backoff
- Add health checks

## Checklists

| ID | Purpose |
|----|---------|
| `checklist-api-review` | API review |
| `checklist-db-review` | Database review |
| `checklist-security-review` | Security audit |
| `checklist-reliability-review` | Resilience |
| `checklist-prod-readiness` | Pre-deploy |

## Best Practices

✅ Validate all inputs
✅ Use structured logging
✅ Include correlation IDs
✅ Document with OpenAPI
✅ Write tests for edge cases

❌ Never log passwords/tokens
❌ Never trust client input
❌ Never expose internal errors
