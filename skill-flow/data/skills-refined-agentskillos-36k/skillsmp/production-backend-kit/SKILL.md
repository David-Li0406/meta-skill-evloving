# Production Backend Kit

This project uses **Backend Engineering Kit (BEK)** - a production-grade knowledge base with 45+ patterns and 6 checklists for backend development.

## CLI Reference

```bash
# Install globally
npm install -g production-backend-kit

# Verify installation
bek doctor

# Search for patterns
bek search "error handling"
bek search "authentication" --scope security

# View pattern details
bek show api-error-model

# Run quality gate
bek gate --checklist checklist-api-review
bek gate --checklist checklist-security-review
```

## Available Patterns

Access patterns in `.shared/production-backend-kit/patterns/`:

### API Design
- `api.error-model.md` - Structured error responses with codes
- `api.pagination-filter-sort.md` - RESTful pagination patterns
- `api.versioning.md` - API versioning strategies
- `api.idempotency.md` - Idempotent request handling

### Security
- `sec.auth-jwt.md` - JWT authentication patterns
- `sec.rbac.md` - Role-based access control
- `sec.rate-limiting.md` - Rate limiting strategies
- `sec.input-validation.md` - Input sanitization

### Database
- `db.migrations.md` - Migration strategies
- `db.indexing.md` - Index optimization
- `db.connection-pool.md` - Connection pooling
- `db.transactions.md` - Transaction patterns

### Reliability
- `rel.circuit-breaker.md` - Circuit breaker pattern
- `rel.retry-backoff.md` - Exponential backoff
- `rel.timeouts.md` - Timeout configuration
- `rel.health-checks.md` - Health check endpoints

### Observability
- `obs.structured-logging.md` - JSON structured logs
- `obs.correlation-id.md` - Request tracing
- `obs.metrics.md` - RED/USE metrics

## Available Checklists

| ID | Purpose |
|----|---------|
| `checklist-api-review` | API design and implementation review |
| `checklist-db-review` | Database schema and query review |
| `checklist-security-review` | Security controls audit |
| `checklist-reliability-review` | Resilience patterns check |
| `checklist-multitenancy-review` | Multi-tenant isolation audit |
| `checklist-prod-readiness` | Pre-deployment checklist |

## Workflow

When implementing backend features:

1. **Search** for relevant patterns: `bek search "<topic>"`
2. **Read** the pattern's Solution section
3. **Apply** all Checklist items
4. **Avoid** documented Pitfalls
5. **Validate** with quality gate: `bek gate --checklist <id>`

## Code Standards

### Error Handling
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [{"field": "email", "message": "Must be valid email"}],
    "requestId": "req_abc123"
  }
}
```

### HTTP Status Codes
- `400` - Validation errors
- `401` - Authentication required
- `403` - Permission denied
- `404` - Resource not found
- `409` - Conflict
- `429` - Rate limited
- `500` - Internal error

### Best Practices
- Always validate input at API boundary
- Use parameterized queries (no SQL injection)
- Never log sensitive data (passwords, tokens, PII)
- Include correlation IDs for tracing
- Set appropriate timeouts for external calls
- Use structured logging (JSON format)
