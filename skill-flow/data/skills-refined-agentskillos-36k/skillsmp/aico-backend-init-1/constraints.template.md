# Backend Constraints

> Project: [PROJECT_NAME]
> Created: [CREATED_DATE]
> Last Updated: [UPDATED_DATE]

## Tech Stack

### Language & Runtime

| Item            | Value                                 |
| --------------- | ------------------------------------- |
| Language        | TypeScript / Python / Go              |
| Runtime         | Node.js 20+ / Python 3.11+ / Go 1.21+ |
| Package Manager | pnpm / npm / pip / go mod             |

### Framework

| Item          | Value                                    |
| ------------- | ---------------------------------------- |
| Web Framework | Express / Fastify / FastAPI / Gin        |
| Validation    | Zod / Pydantic / go-playground/validator |
| ORM/Query     | Prisma / Drizzle / SQLAlchemy / GORM     |

### Database

| Item       | Value                                     |
| ---------- | ----------------------------------------- |
| Primary DB | PostgreSQL / MySQL / MongoDB              |
| Cache      | Redis / Memcached                         |
| Migrations | Prisma Migrate / Alembic / golang-migrate |

## Architecture

### API Style

- [ ] REST
- [ ] GraphQL
- [ ] gRPC
- [ ] WebSocket

### Layered Architecture

```
Controller/Handler (HTTP layer)
       ↓
    Service (Business logic)
       ↓
   Repository (Data access)
       ↓
    Database
```

### Directory Structure

```
src/
├── controllers/     # HTTP handlers
├── services/        # Business logic
├── repositories/    # Data access
├── models/          # Database models
├── types/           # TypeScript types/interfaces
├── middleware/      # Express/Fastify middleware
├── utils/           # Utility functions
└── config/          # Configuration
```

## Coding Standards

### Naming Conventions

| Type            | Convention  | Example           |
| --------------- | ----------- | ----------------- |
| Files           | kebab-case  | `user-service.ts` |
| Classes         | PascalCase  | `UserService`     |
| Functions       | camelCase   | `createUser`      |
| Constants       | UPPER_SNAKE | `MAX_RETRIES`     |
| Database tables | snake_case  | `user_sessions`   |

### Code Style

- Use ESLint/Prettier (TS), Ruff (Python), golangci-lint (Go)
- Max line length: 100 characters
- Use async/await over callbacks
- Explicit error handling (no silent failures)

## Testing

### Framework

| Type        | Tool                             |
| ----------- | -------------------------------- |
| Unit Tests  | Jest / Vitest / Pytest / Go test |
| Integration | Supertest / httptest             |
| Mocking     | jest.mock / unittest.mock        |

### Requirements

- [ ] All services must have unit tests
- [ ] All API endpoints must have integration tests
- [ ] Minimum 80% code coverage
- [ ] TDD: Write failing test before implementation

### Test Structure

```
src/
├── services/
│   ├── user.service.ts
│   └── __tests__/
│       └── user.service.test.ts
```

## Security

### Authentication

- [ ] JWT tokens
- [ ] Session-based
- [ ] OAuth 2.0
- [ ] API keys

### Password Handling

- Use bcrypt with cost factor 10+
- Never store plaintext passwords
- Never log passwords

### Input Validation

- Validate all inputs at API boundary
- Use schema validation (Zod/Pydantic)
- Sanitize user inputs

### OWASP Top 10

- [ ] SQL Injection: Use parameterized queries
- [ ] XSS: Escape output, use Content-Security-Policy
- [ ] CSRF: Use CSRF tokens for state-changing operations
- [ ] Auth: Secure session management

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": [...]
  }
}
```

### HTTP Status Codes

| Code | Usage                          |
| ---- | ------------------------------ |
| 200  | Success                        |
| 201  | Created                        |
| 400  | Bad Request (validation error) |
| 401  | Unauthorized                   |
| 403  | Forbidden                      |
| 404  | Not Found                      |
| 500  | Internal Server Error          |

## Logging

### Format

```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "level": "info",
  "message": "User created",
  "context": { "userId": "123" }
}
```

### Levels

| Level | Usage                        |
| ----- | ---------------------------- |
| error | Errors requiring attention   |
| warn  | Warnings, degraded operation |
| info  | Normal operations            |
| debug | Debugging information        |

## Environment

### Required Variables

```bash
# Database
DATABASE_URL=postgresql://...

# Auth
JWT_SECRET=...
JWT_EXPIRY=3600

# Server
PORT=3000
NODE_ENV=development
```

### Configuration

- Use environment variables for secrets
- Use config files for non-sensitive settings
- Never commit secrets to git

## API Design

### REST Conventions

| Method | Path       | Action      |
| ------ | ---------- | ----------- |
| GET    | /users     | List users  |
| GET    | /users/:id | Get user    |
| POST   | /users     | Create user |
| PUT    | /users/:id | Update user |
| DELETE | /users/:id | Delete user |

### Pagination

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

## Performance

### Database

- Use indexes for frequently queried columns
- Avoid N+1 queries
- Use connection pooling

### Caching

- Cache frequently accessed data
- Set appropriate TTL
- Invalidate on updates

### Rate Limiting

- Implement rate limiting for public APIs
- Use sliding window algorithm
- Return 429 Too Many Requests
