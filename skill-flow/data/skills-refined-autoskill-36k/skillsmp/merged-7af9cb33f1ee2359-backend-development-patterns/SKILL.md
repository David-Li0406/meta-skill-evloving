---
name: backend-development-patterns
description: Use this skill when building backend services, APIs, or microservices to implement best practices for error handling, logging, and caching.
---

# Backend Development Patterns

This skill provides best practices and patterns for backend service development, supporting language-specific loading as needed.

## Trigger Conditions

- Building backend services
- Designing service architecture
- Implementing business logic layers
- Configuring middleware
- Handling errors and logging

## Language-Specific Patterns

Load the corresponding language-specific files based on the project technology stack:

| Technology Stack      | Load File      | Frameworks                     |
|-----------------------|----------------|--------------------------------|
| Python                | `python.md`    | FastAPI, Django, Flask         |
| TypeScript/Node.js    | `typescript.md`| Express, NestJS, Fastify       |
| Java                  | `java.md`      | Spring Boot, Quarkus          |
| Go                    | `go.md`        | Gin, Echo, Fiber              |
| C#                    | `csharp.md`    | ASP.NET Core                  |

**Loading Method**: Detect the technology stack by checking files like `pyproject.toml`, `package.json`, `pom.xml`, or `go.mod`.

---

## General Architectural Patterns

### Layered Architecture

```
┌─────────────────────────────────────┐
│           Controller Layer           │  Handles HTTP requests/responses
├─────────────────────────────────────┤
│            Service Layer             │  Business logic
├─────────────────────────────────────┤
│          Repository Layer            │  Data access
├─────────────────────────────────────┤
│             Model Layer              │  Data models
└─────────────────────────────────────┘
```

### General Directory Structure

```
src/
├── controllers/          # Controllers (or routes/handlers)
├── services/             # Business logic
├── repositories/         # Data access (or dal/)
├── models/               # Data models (or entities/)
├── middlewares/          # Middleware
├── utils/                # Utility functions
├── config/               # Configuration
└── types/                # Type definitions (if applicable)
```

---

## General Best Practices

### 1. Error Handling Principles

```
┌─────────────────────────────────────────────────────┐
│                    Error Handling Pyramid           │
├─────────────────────────────────────────────────────┤
│  Business Errors (400-499)                          │
│  ├─ ValidationError (400)   Input validation failed │
│  ├─ UnauthorizedError (401) Not authenticated       │
│  ├─ ForbiddenError (403)    No permission           │
│  └─ NotFoundError (404)     Resource not found     │
├─────────────────────────────────────────────────────┤
│  System Errors (500-599)                            │
│  ├─ InternalError (500)     Internal server error   │
│  ├─ ServiceUnavailable (503) Service unavailable     │
│  └─ GatewayTimeout (504)    Gateway timeout        │
└─────────────────────────────────────────────────────┘
```

**Principles**:

- Custom error classes inherit from base errors
- Unified error response format
- Distinguish between actionable errors and program errors
- Log sufficient context for debugging

### 2. Logging Standards

**Log Levels**:
| Level | Purpose                     | Example                     |
|-------|-----------------------------|-----------------------------|
| ERROR | Errors needing immediate attention | Database connection failed  |
| WARN  | Potential issues            | Retry succeeded, fallback    |
| INFO  | Important business events    | User logged in, order created|
| DEBUG | Development debug information | Variable values, execution paths |

**Structured Log Fields**:

```json
{
  "timestamp": "2025-01-22T10:00:00Z",
  "level": "info",
  "message": "User logged in successfully",
  "requestId": "uuid",
  "userId": "123",
  "duration": 45
}
```

### 3. Caching Strategies

| Strategy        | Applicable Scenarios | Suggested TTL  |
|-----------------|----------------------|-----------------|
| Cache-Aside     | Read-heavy, write-light | 5-60 minutes   |
| Write-Through   | Strong consistency required | Short TTL      |
| Write-Behind    | Write-heavy, read-light | Based on business |

**Cache Key Naming**:

```
{service}:{entity}:{id}
{service}:{entity}:list:{hash}
```

### 4. API Design Principles

- **RESTful** resource-oriented
- **Versioning** `/api/v1/...`
- **Unified response format**
- **Idempotency** for PUT/DELETE operations
- **Pagination** for large list queries

### 5. Security Checklist

- [ ] Input validation (whitelist preferred)
- [ ] SQL/NoSQL injection protection
- [ ] Secure storage of authentication tokens
- [ ] Encryption of sensitive data
- [ ] Rate limiting
- [ ] CORS configuration

---

## General Code Patterns

### Unified Response Format

```
Successful Response:
{
  "success": true,
  "data": { ... },
  "meta": { "total": 100, "page": 1 }
}

Error Response:
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format"
  }
}
```

### Health Check Endpoint

```
GET /health

{
  "status": "ok",
  "timestamp": "2025-01-22T10:00:00Z",
  "services": {
    "database": { "status": "ok" },
    "redis": { "status": "ok" }
  }
}
```

### Graceful Shutdown

```
1. Receive SIGTERM signal
2. Stop accepting new requests
3. Wait for ongoing requests to complete (within timeout)
4. Close database connections
5. Close other resources
6. Exit process
```

---

## Language-Specific Content

For detailed language-specific implementations, please refer to:

- **Python**: [python.md](./python.md) - FastAPI/Django/Flask
- **TypeScript**: [typescript.md](./typescript.md) - Express/NestJS
- **Java**: [java.md](./java.md) - Spring Boot
- **Go**: [go.md](./go.md) - Gin/Echo
- **C#**: [csharp.md](./csharp.md) - ASP.NET Core

---

## Maintenance

- Sources: Official documentation for each language, 12-Factor App
- Last updated: 2025-01-22
- Pattern: General checklist + language-specific loading