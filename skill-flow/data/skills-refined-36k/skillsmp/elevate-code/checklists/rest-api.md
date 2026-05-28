# REST API Checklist

Complete validation checklist for REST APIs (FastAPI/Express).

---

## Project Structure (Python/FastAPI)

```
my-api/
├── pyproject.toml
├── src/
│   └── my_api/
│       ├── __init__.py
│       ├── main.py          # FastAPI app, routers
│       ├── config.py        # Settings (Pydantic)
│       ├── models/          # Pydantic models
│       ├── routes/          # Route handlers
│       ├── services/        # Business logic
│       ├── db/              # Database (if applicable)
│       └── middleware/      # Custom middleware
├── tests/
├── alembic/                 # Migrations (if using DB)
└── docker-compose.yml
```

## Project Structure (Node/Express)

```
my-api/
├── package.json
├── src/
│   ├── index.js             # Entry point
│   ├── app.js               # Express app setup
│   ├── config.js            # Configuration
│   ├── routes/              # Route handlers
│   ├── services/            # Business logic
│   ├── middleware/          # Custom middleware
│   └── models/              # Data models
├── tests/
└── docker-compose.yml
```

---

## The Triad (Adapted for APIs)

### Health (Doctor)
- [ ] `GET /health` endpoint returns status
- [ ] `GET /health/ready` checks database, cache, dependencies
- [ ] `GET /health/live` for kubernetes liveness probe
- [ ] Startup validates: DB connection, required env vars, external services

### Safety (Safety Net)
- [ ] Destructive endpoints require explicit confirmation or idempotency key
- [ ] Soft delete (set `deleted_at`) instead of hard delete
- [ ] Audit log for all mutations
- [ ] Database transactions for multi-step operations

### Resilience (Statekeeper)
- [ ] Circuit breaker for external service calls
- [ ] Retry with backoff for transient failures
- [ ] Graceful degradation when dependencies fail
- [ ] Request timeout configuration

---

## 12-Factor App Principles

- [ ] **Codebase**: One repo, many deploys
- [ ] **Dependencies**: Explicitly declared (requirements.txt/package.json)
- [ ] **Config**: Environment variables, not code
- [ ] **Backing Services**: Treat as attached resources (URLs)
- [ ] **Build/Release/Run**: Strictly separated stages
- [ ] **Processes**: Stateless, share-nothing
- [ ] **Port Binding**: Self-contained, export via port
- [ ] **Concurrency**: Scale via process model
- [ ] **Disposability**: Fast startup, graceful shutdown
- [ ] **Dev/Prod Parity**: Keep environments similar
- [ ] **Logs**: Treat as event streams (stdout)
- [ ] **Admin Processes**: Run as one-off tasks

---

## API Design

### REST Conventions
- [ ] Resource-based URLs (`/users`, `/users/{id}`)
- [ ] HTTP methods: GET (read), POST (create), PUT/PATCH (update), DELETE
- [ ] Plural nouns for collections
- [ ] Consistent naming (snake_case or camelCase)

### Response Format
- [ ] Consistent JSON structure
- [ ] Meaningful HTTP status codes
- [ ] Error responses include: code, message, details
- [ ] Pagination for lists (offset/limit or cursor)

```json
// Success
{
  "data": { ... },
  "meta": { "total": 100, "page": 1 }
}

// Error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [{ "field": "email", "message": "Invalid format" }]
  }
}
```

### OpenAPI/Swagger
- [ ] OpenAPI spec generated from code
- [ ] All endpoints documented
- [ ] Request/response schemas defined
- [ ] Examples provided
- [ ] `/docs` endpoint serves Swagger UI

---

## Security

- [ ] HTTPS only in production
- [ ] Authentication (JWT, OAuth, API keys)
- [ ] Authorization (role-based or permission-based)
- [ ] Input validation on all endpoints
- [ ] Rate limiting
- [ ] CORS configuration
- [ ] SQL injection prevention (parameterized queries)
- [ ] No sensitive data in logs
- [ ] Secrets in environment variables (not code)

---

## Configuration

```python
# FastAPI with Pydantic Settings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str | None = None
    api_key: str
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```

```javascript
// Express with dotenv
require('dotenv').config();

const config = {
  port: process.env.PORT || 3000,
  databaseUrl: process.env.DATABASE_URL,
  apiKey: process.env.API_KEY,
  debug: process.env.DEBUG === 'true',
};

module.exports = config;
```

---

## Middleware

- [ ] Request logging (method, path, status, duration)
- [ ] Error handling (catch-all, format response)
- [ ] Authentication middleware
- [ ] Rate limiting middleware
- [ ] Request ID injection
- [ ] CORS handling

---

## Testing

- [ ] Unit tests for business logic
- [ ] Integration tests for endpoints
- [ ] Database mocked or test database
- [ ] External APIs mocked
- [ ] Test client setup (TestClient/supertest)
- [ ] Coverage on critical paths

---

## Database (if applicable)

- [ ] Migrations versioned (Alembic/Prisma/Knex)
- [ ] Connection pooling configured
- [ ] Indexes on frequently queried columns
- [ ] Transactions for multi-table operations
- [ ] Soft delete with `deleted_at` column

---

## Deployment

- [ ] Dockerfile (multi-stage build)
- [ ] docker-compose.yml for local dev
- [ ] Health check in container
- [ ] Graceful shutdown handler
- [ ] Environment-based configuration
- [ ] CI/CD pipeline

---

## Quick Validation

```bash
# Check health endpoint
curl http://localhost:8000/health

# Check OpenAPI spec
curl http://localhost:8000/openapi.json

# Check 12-factor: config from env
grep -rE "os.environ|process.env" src/

# Check for hardcoded secrets
grep -rE "(password|secret|key)\s*=" src/ | grep -v ".env"
```
