---
name: backend-patterns
description: Use this skill when building backend services, APIs, or microservices to implement best practices for error handling, logging, and caching.
---

# Skill body

This skill provides best practices and patterns for backend service development, supporting multi-language loading as needed.

## Trigger Conditions

- Building backend services
- Designing service architecture
- Implementing business logic layer
- Configuring middleware
- Handling errors and logging

## Language-Specific Patterns

Load the corresponding language-specific files based on the project tech stack:

| Tech Stack             | Load File        | Frameworks                     |
| ---------------------- | ---------------- | ------------------------------- |
| Python                 | `python.md`      | FastAPI, Django, Flask         |
| TypeScript/Node.js     | `typescript.md`  | Express, NestJS, Fastify       |
| Java                   | `java.md`        | Spring Boot, Quarkus          |
| Go                     | `go.md`          | Gin, Echo, Fiber              |
| C#                     | `csharp.md`      | ASP.NET Core                   |

**Loading Method**: Detect the tech stack by checking for files like `pyproject.toml`, `package.json`, `pom.xml`, `go.mod`, etc.

---

## General Architecture Patterns

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
│  └─ NotFoundError (404)     Resource not found      │
├─────────────────────────────────────────────────────┤
│  System Errors (500-599)                            │
│  ├─ InternalError (500)     Internal server error   │
│  ├─ ServiceUnavailable (503) Service unavailable     │
│  └─ GatewayTimeout (504)    Gateway timeout         │
└─────────────────────────────────────────────────────┘
```

**Principles**:

- Custom error classes inherit from base error
- Unified error response format
- Distinguish between actionable errors and system errors