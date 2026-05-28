# Backend Services & APIs

Specific guidance for building backend services, REST APIs, GraphQL APIs, and microservices.

## Product Requirements Focus

### Typical Personas
- **API Consumer/Developer**: Integrates with your API
- **System Administrator**: Deploys and operates the service
- **Internal Service**: Another service that depends on this one
- **End User** (indirect): Benefits from the API through a frontend

### Key Questions to Ask
1. Who will consume this API? (Internal services, third parties, public)
2. What authentication/authorization is required?
3. What are the expected traffic patterns?
4. What SLAs must be met?
5. What data does this service own?

### Backend-Specific User Stories

```markdown
**As a** API consumer
**I expect to** authenticate and receive a token
**So that** I can make authorized requests

**As a** system administrator
**I expect to** view service health and metrics
**So that** I can monitor and troubleshoot issues

**As a** dependent service
**I expect to** receive consistent error responses
**So that** I can handle failures gracefully
```

## Technical Requirements Focus

### Backend-Specific NFRs

| Category | Typical Requirements |
|----------|---------------------|
| **Latency** | p50 < 50ms, p95 < 200ms, p99 < 500ms |
| **Throughput** | X requests/second per instance |
| **Availability** | 99.9% (8.76 hours downtime/year) |
| **Scalability** | Horizontal scaling to N instances |
| **Data Consistency** | Strong/eventual consistency model |

### Security Considerations
- [ ] Authentication (JWT, OAuth2, API keys)
- [ ] Authorization (RBAC, ABAC, scopes)
- [ ] Input validation and sanitization
- [ ] Rate limiting
- [ ] Audit logging
- [ ] Encryption (at rest, in transit)
- [ ] Secret management

### Data Requirements
- [ ] Database selection (SQL vs NoSQL)
- [ ] Data model and migrations
- [ ] Backup and recovery strategy
- [ ] Data retention policies
- [ ] GDPR/compliance considerations

## Architecture Patterns

### Decision: Service Architecture

| Pattern | When to Use | Pros | Cons |
|---------|-------------|------|------|
| **Monolith** | Small team, MVP, simple domain | Simple deployment, easy debugging | Scaling limits |
| **Modular Monolith** | Growing complexity, future splitting | Clear boundaries, simpler than micro | Discipline required |
| **Microservices** | Large team, complex domain, scale needs | Independent scaling/deployment | Operational complexity |
| **Serverless** | Event-driven, variable load | No infrastructure, pay-per-use | Cold starts, vendor lock |

### Layered Architecture (Recommended Default)

```
┌─────────────────────────────────────────────────┐
│              Presentation Layer                  │
│         (HTTP Handlers / Controllers)            │
├─────────────────────────────────────────────────┤
│              Application Layer                   │
│         (Use Cases / Application Services)       │
├─────────────────────────────────────────────────┤
│               Domain Layer                       │
│       (Entities / Business Logic / Rules)        │
├─────────────────────────────────────────────────┤
│            Infrastructure Layer                  │
│    (Repositories / External Services / DB)       │
└─────────────────────────────────────────────────┘
```

### API Design Principles

1. **Resource-Oriented**: Design around resources, not actions
2. **Consistent Naming**: Use plural nouns for collections
3. **Proper HTTP Methods**: GET (read), POST (create), PUT (replace), PATCH (update), DELETE (remove)
4. **Versioning**: URL path (`/v1/`) or header-based
5. **HATEOAS**: Include links for discoverability (optional)

## Interface Contracts

### REST API Standards

```yaml
# Standard response envelope
Success:
  data: [actual payload]
  meta: [pagination, timing]

Error:
  error:
    code: "ERROR_CODE"
    message: "Human readable message"
    details: [field-level errors]
    requestId: "for correlation"
```

### Standard Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check (for load balancers) |
| `/health/live` | GET | Liveness probe (is process running) |
| `/health/ready` | GET | Readiness probe (can serve traffic) |
| `/metrics` | GET | Prometheus metrics |
| `/api/v1/...` | * | Business endpoints |

### Pagination Pattern

```json
{
  "data": [...],
  "pagination": {
    "total": 100,
    "limit": 20,
    "offset": 0,
    "hasMore": true
  },
  "links": {
    "self": "/resources?limit=20&offset=0",
    "next": "/resources?limit=20&offset=20",
    "prev": null
  }
}
```

## Code Scaffolding

### Recommended Directory Structure

```
service/
├── cmd/
│   └── server/
│       └── main.go           # Entry point
├── internal/
│   ├── api/
│   │   ├── handlers/         # HTTP handlers
│   │   ├── middleware/       # HTTP middleware
│   │   └── routes.go         # Route definitions
│   ├── domain/
│   │   ├── entities/         # Domain entities
│   │   ├── services/         # Domain services
│   │   └── errors.go         # Domain errors
│   ├── repository/
│   │   ├── postgres/         # Postgres implementation
│   │   └── interfaces.go     # Repository interfaces
│   └── config/
│       └── config.go         # Configuration
├── pkg/                      # Public packages (if any)
├── migrations/               # Database migrations
├── scripts/                  # Utility scripts
├── deployments/
│   ├── Dockerfile
│   └── k8s/
├── tests/
│   ├── integration/
│   └── e2e/
├── go.mod
├── Makefile
└── README.md
```

## Testing Strategy

### Backend Test Pyramid

```
         /\
        /  \     E2E: API contract tests
       /----\    - Test full request/response cycle
      /      \
     /--------\  Integration: Database + external services
    /          \ - Test with real DB (testcontainers)
   /            \- Mock external APIs
  /--------------\
 /                \ Unit: Domain logic
/                  \- Pure functions, no I/O
/____________________\ - Mock all dependencies
```

### Key Test Patterns

**Repository Tests** (Integration):
```go
func TestUserRepository_Create(t *testing.T) {
    db := setupTestDB(t)
    defer db.Close()

    repo := NewUserRepository(db)
    user := &User{Email: "test@example.com"}

    err := repo.Create(ctx, user)

    assert.NoError(t, err)
    assert.NotEmpty(t, user.ID)
}
```

**Handler Tests** (Unit with mocks):
```go
func TestCreateUser_Success(t *testing.T) {
    mockService := new(MockUserService)
    mockService.On("Create", mock.Anything).Return(&User{ID: "123"}, nil)

    handler := NewUserHandler(mockService)

    req := httptest.NewRequest("POST", "/users", userJSON)
    rec := httptest.NewRecorder()

    handler.Create(rec, req)

    assert.Equal(t, 201, rec.Code)
    mockService.AssertExpectations(t)
}
```

**Contract Tests** (E2E):
```go
func TestAPI_CreateUser_Contract(t *testing.T) {
    app := setupTestApp(t)

    resp := app.POST("/api/v1/users").
        WithJSON(map[string]string{"email": "test@example.com"}).
        Expect()

    resp.Status(201)
    resp.JSON().Object().
        ContainsKey("id").
        ContainsKey("email").
        ContainsKey("createdAt")
}
```

## Deployment Considerations

### Health Checks
```go
// Liveness: Is the process healthy?
func (h *HealthHandler) Liveness(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(map[string]string{"status": "alive"})
}

// Readiness: Can the service handle traffic?
func (h *HealthHandler) Readiness(w http.ResponseWriter, r *http.Request) {
    if err := h.db.Ping(); err != nil {
        w.WriteHeader(http.StatusServiceUnavailable)
        return
    }
    w.WriteHeader(http.StatusOK)
}
```

### Graceful Shutdown
```go
func main() {
    server := &http.Server{...}

    go func() {
        if err := server.ListenAndServe(); err != http.ErrServerClosed {
            log.Fatal(err)
        }
    }()

    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    server.Shutdown(ctx)
}
```

### Observability
- **Logging**: Structured JSON logs with correlation IDs
- **Metrics**: Prometheus metrics (request count, latency, errors)
- **Tracing**: OpenTelemetry for distributed tracing
- **Alerting**: Define SLOs and alert on breaches

## Common Pitfalls to Avoid

1. **N+1 Queries**: Always check for eager loading
2. **Missing Input Validation**: Validate at API boundary
3. **Leaking Internal Errors**: Map to appropriate HTTP status
4. **No Rate Limiting**: Protect against abuse
5. **Synchronous External Calls**: Use timeouts and circuit breakers
6. **Missing Idempotency**: For non-idempotent operations
7. **Ignoring Graceful Shutdown**: Drain connections properly
