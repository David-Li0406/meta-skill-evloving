---
name: api-design-principles
description: Master REST and GraphQL API design principles to build intuitive, scalable, and maintainable APIs. Use when designing new APIs, reviewing API specifications, or establishing API design standards.
---

# API Design Principles

Master REST and GraphQL API design principles to build intuitive, scalable, and maintainable APIs. This skill focuses on **design theory** - for implementation patterns, see related skills.

## When to Use This Skill

- Designing new API contracts
- Reviewing API specifications before implementation
- Establishing API design standards for your team
- Planning API versioning and evolution strategy
- Creating developer-friendly API documentation

## Audience

- **Backend Architects** - API contract design
- **Tech Leads** - Standards and review
- **Business Analysts** - Understanding API capabilities

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

---

## Design Patterns

### Pagination

**Always paginate collections** - Never return unbounded lists.

**Offset-Based**:
```
GET /api/v1/patients?page=2&pageSize=20
```

**Cursor-Based**:
```
GET /api/v1/patients?cursor=eyJpZCI6MTIzfQ&limit=20
```

### Filtering and Sorting

**Query Parameters for Filtering**:
```
GET /api/v1/patients?status=active
```

**Sorting**:
```
GET /api/v1/patients?sorting=name
```

### Error Response Design

**Consistent Structure**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "One or more validation errors occurred.",
    "details": []
  }
}
```

### Versioning Strategy

**URL Versioning**:
```
/api/v1/patients
```

---

## API Contract Checklist

### Resource Design
- [ ] Resources are nouns, not verbs
- [ ] Plural names for collections
- [ ] Consistent naming convention
- [ ] Max 2 levels of nesting
- [ ] All CRUD mapped to correct HTTP methods

### Request/Response
- [ ] All collections paginated
- [ ] Default and max page size defined
- [ ] Filter parameters documented
- [ ] Sorting parameters documented
- [ ] Consistent error response format

### Security
- [ ] Authentication method defined
- [ ] Authorization on all mutating endpoints
- [ ] Rate limiting configured
- [ ] Sensitive data not in URLs
- [ ] CORS configured

### Documentation
- [ ] OpenAPI/Swagger spec
- [ ] All endpoints documented
- [ ] Request/response examples
- [ ] Error responses documented

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Verb endpoints | `POST /createPatient` | `POST /patients` |
| Ignoring HTTP methods | Using POST for everything | Use appropriate method |
| No pagination | Returning 10,000 items | Always paginate |
| Inconsistent errors | Different formats per endpoint | Standardize error structure |
| Exposing internals | Database columns in API | Design API contract separately |
| No versioning | Breaking changes break clients | Version from day one |
| Deep nesting | `/a/{id}/b/{id}/c/{id}/d` | Flatten, max 2 levels |

---

## Integration with Other Skills

| Need | Skill |
|------|-------|
| **AppService implementation** | Related skills |
| **Response wrappers** | Related skills |
| **Input validation** | Related skills |
| **Query optimization** | Related skills |
| **Technical design docs** | Related skills |

---

## References

- `references/rest-best-practices.md` - Detailed REST patterns
- `assets/api-design-checklist.md` - Pre-implementation checklist