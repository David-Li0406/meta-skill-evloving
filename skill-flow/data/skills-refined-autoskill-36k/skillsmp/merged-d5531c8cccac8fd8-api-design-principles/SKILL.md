---
name: api-design-principles
description: Use this skill when designing, reviewing, or establishing standards for REST and GraphQL APIs to ensure they are intuitive, scalable, and maintainable.
---

# API Design Principles

Master REST and GraphQL API design principles to build intuitive, scalable, and maintainable APIs. This skill focuses on design theory and best practices for creating APIs that developers love.

## When to Use This Skill

- Designing new REST or GraphQL API contracts
- Reviewing API specifications before implementation
- Establishing API design standards for your team
- Planning API versioning and evolution strategy
- Creating developer-friendly API documentation

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

### 2. HTTP Methods Semantics

| Method | Purpose | Idempotent | Safe | Request Body |
|--------|---------|------------|------|--------------|
| `GET` | Retrieve resource(s) | Yes | Yes | No |
| `POST` | Create resource | No | No | Yes |
| `PUT` | Replace entire resource | Yes | No | Yes |
| `PATCH` | Partial update | Yes* | No | Yes |
| `DELETE` | Remove resource | Yes | No | No |

### 3. HTTP Status Codes

**Success (2xx)**:
| Code | Meaning | Use When |
|------|---------|----------|
| `200 OK` | Success | GET, PUT, PATCH succeeded |
| `201 Created` | Resource created | POST succeeded |
| `204 No Content` | Success, no body | DELETE succeeded |

**Client Errors (4xx)**:
| Code | Meaning | Use When |
|------|---------|----------|
| `400 Bad Request` | Malformed request | Invalid JSON, missing required headers |
| `401 Unauthorized` | Not authenticated | Missing or invalid token |
| `403 Forbidden` | Not authorized | Valid token, insufficient permissions |
| `404 Not Found` | Resource doesn't exist | ID not found |
| `409 Conflict` | State conflict | Duplicate email, version mismatch |
| `422 Unprocessable Entity` | Validation failed | Business rule violations |
| `429 Too Many Requests` | Rate limited | Exceeded request quota |

**Server Errors (5xx)**:
| Code | Meaning | Use When |
|------|---------|----------|
| `500 Internal Server Error` | Unexpected error | Unhandled exception |
| `503 Service Unavailable` | Temporarily down | Maintenance, overload |

## Design Patterns

### Pagination

**Always paginate collections** - Never return unbounded lists.

**Offset-Based** (simple, good for small datasets):
```
GET /api/v1/patients?page=2&pageSize=20
```

**Cursor-Based** (efficient for large datasets):
```
GET /api/v1/patients?cursor=eyJpZCI6MTIzfQ&limit=20
```

### Filtering and Sorting

**Query Parameters for Filtering**:
```
GET /api/v1/patients?status=active
GET /api/v1/patients?status=active&createdAfter=2025-01-01
```

**Sorting**:
```
GET /api/v1/patients?sorting=name
GET /api/v1/patients?sorting=createdAt desc
```

### Error Response Design

**Consistent Structure**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "One or more validation errors occurred.",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format."
      }
    ],
    "traceId": "00-abc123-def456-00"
  }
}
```

### Versioning Strategy

**URL Versioning** (Recommended):
```
/api/v1/patients
/api/v2/patients
```

## Quick Reference

### API Design Checklist

- [ ] Resources are nouns, not verbs
- [ ] Plural names for collections
- [ ] Consistent naming convention
- [ ] All CRUD mapped to correct HTTP methods
- [ ] All collections paginated
- [ ] Default and max page size defined
- [ ] Filter parameters documented
- [ ] Sorting parameters documented
- [ ] Consistent error response format
- [ ] OpenAPI/Swagger spec available
- [ ] All endpoints documented

---

*"The best API is invisible. Developers use it without thinking about it because it does what they expect."*