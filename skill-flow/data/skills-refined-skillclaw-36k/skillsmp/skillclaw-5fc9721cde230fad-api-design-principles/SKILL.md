---
name: api-design-principles
description: Use this skill when designing new APIs, reviewing API specifications, or establishing API design standards to create intuitive, scalable, and maintainable APIs.
---

# API Design Principles

Master REST and GraphQL API design principles to build intuitive, scalable, and maintainable APIs. This skill focuses on **design theory** - for implementation patterns, see `abp-api-implementation` or `abp-service-patterns`.

## When to Use This Skill

- Designing new API contracts (REST or GraphQL)
- Reviewing API specifications before implementation
- Establishing API design standards for your team
- Planning API versioning and evolution strategy
- Creating developer-friendly API documentation

## Audience

- **Backend Architects** - API contract design
- **Tech Leads** - Standards and review
- **Business Analysts** - Understanding API capabilities

> **For Implementation**: Use `abp-service-patterns` for AppService code, `api-response-patterns` for response wrappers, `fluentvalidation-patterns` for validation.

---

## Core Principles

### 1. Resource-Oriented Design

APIs expose **resources** (nouns), not **actions** (verbs).

| Concept | Good | Bad |
|---------|------|-----|
| Resource naming | `/patients`, `/appointments` | `/getPatients`, `/createAppointment` |
| Actions via HTTP methods | `POST /patients` | `POST /createPatient` |
| Plural for collections | `/patients` | `/patient` |
| Consistent casing | `kebab-case` or `camelCase` | Mixed styles |

**Resource Hierarchy**:
```
/api/v1/patients                    # Collection
/api/v1/patients/{id}               # Single resource
/api/v1/patients/{id}/appointments  # Nested collection
/api/v1/appointments/{id}           # Direct access to nested resource
```

**Avoid Deep Nesting** (max 2 levels):
```
# Good - Shallow
GET /api/v1/patients/{id}/appointments
GET /api/v1/appointments/{id}

# Bad - Too deep
GET /api/v1/clinics/{id}/doctors/{id}/patients/{id}/appointments/{id}
```

### 2. HTTP Methods Semantics

| Method | Purpose | Idempotent | Safe | Request Body |
|--------|---------|------------|------|--------------|
| `GET` | Retrieve resource(s) | Yes | Yes | No |
| `POST` | Create resource | No | No | Yes |
| `PUT` | Update resource | Yes | No | Yes |
| `DELETE` | Remove resource | Yes | No | No |

### 3. Versioning Strategies

- **URI Versioning**: `/api/v1/patients`
- **Header Versioning**: `Accept: application/vnd.yourapi.v1+json`
- **Query Parameter Versioning**: `/api/patients?version=1`

### 4. Pagination and Filtering

- Use query parameters for pagination: `GET /patients?page=1&limit=10`
- Support filtering: `GET /patients?status=active`

### 5. Status Codes

Use appropriate HTTP status codes to indicate the result of API requests:
- `200 OK` - Successful GET
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Client error
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

By adhering to these principles, you can create APIs that are not only functional but also user-friendly and maintainable.