---
name: api-design
description: Design resource-oriented APIs following patterns from "API Design Patterns" by JJ Geewax (Google)
---

# API Design Patterns Skill

This skill helps you design consistent, scalable, and flexible APIs following the patterns from **"API Design Patterns" by JJ Geewax** and Google's API Improvement Proposals (AIP).

## Additional Resources

- **patterns-reference.md** - Deep dives into each pattern with trade-offs and implementation details
- **templates/openapi-template.yaml** - OpenAPI 3.1 template following these patterns
- **examples/task-management-api.yaml** - Complete example API design

---

## Core Philosophy

**Resource-Oriented Design**: APIs are built around resources (nouns), not actions (verbs). A small set of standard methods operate on these resources.

> "The fundamental building blocks of an API are individually-named resources and the relationships and hierarchy that exist between them."

---

## Part 1: Design Principles

### 1.1 Naming Conventions

**Resources (Nouns)**
- Use plural nouns for collections: `/users`, `/orders`, `/products`
- Use singular nouns for singletons: `/users/{id}/profile`
- Use lowercase with hyphens: `/user-accounts` not `/userAccounts`
- Be consistent and predictable across the entire API

**Fields**
- Use `snake_case` for JSON field names: `created_at`, `user_id`
- Use clear, unambiguous names: `email_address` not just `email`
- Avoid abbreviations: `configuration` not `config`

**Methods**
- Standard methods use HTTP verbs (GET, POST, PUT, PATCH, DELETE)
- Custom methods use POST with verb suffix: `POST /orders/{id}:cancel`

### 1.2 Resource Scope and Hierarchy

**Hierarchy Rules**
- Model resources as trees with parent-child relationships
- Maximum recommended depth: 3-4 levels
- Resources must form a Directed Acyclic Graph (no circular references)

**Example Structure**
```
/projects/{project_id}
/projects/{project_id}/databases/{database_id}
/projects/{project_id}/databases/{database_id}/tables/{table_id}
```

**Resource Names**
- Full resource name: `projects/my-project/databases/main/tables/users`
- Relative resource name: `databases/main/tables/users`

### 1.3 Data Types and Defaults

**Standard Field Types**
| Type | Format | Example |
|------|--------|---------|
| Timestamps | RFC 3339 | `2024-01-15T10:30:00Z` |
| Durations | Seconds with 's' suffix | `3600s` |
| Money | Object with currency | `{"amount": "10.00", "currency": "USD"}` |
| Bytes | Base64 encoded | `SGVsbG8gV29ybGQ=` |

**Default Values**
- Booleans default to `false`
- Numbers default to `0`
- Strings default to empty string `""`
- Arrays default to empty array `[]`
- Never use `null` as a meaningful default

---

## Part 2: Fundamentals

### 2.1 Resource Identification

**Resource IDs**
- Use opaque, unique identifiers: UUIDs or custom IDs
- IDs should be URL-safe: alphanumeric, hyphens, underscores
- Consider client-provided IDs for idempotency

```json
{
  "name": "projects/my-project/users/abc123",
  "id": "abc123",
  "display_name": "John Doe"
}
```

### 2.2 Standard Methods

| Method | HTTP | Request Body | Response | Idempotent |
|--------|------|--------------|----------|------------|
| List | GET | None | Collection | Yes |
| Get | GET | None | Resource | Yes |
| Create | POST | Resource | Resource | No* |
| Update | PUT/PATCH | Resource | Resource | Yes |
| Delete | DELETE | None | Empty | Yes |

*Create can be idempotent with client-provided IDs

**List Method**
```http
GET /users?page_size=25&page_token=xyz
```
Response:
```json
{
  "users": [...],
  "next_page_token": "abc"
}
```

**Get Method**
```http
GET /users/123
```

**Create Method**
```http
POST /users
Content-Type: application/json

{
  "display_name": "Jane Doe",
  "email": "jane@example.com"
}
```

**Update Method (Full)**
```http
PUT /users/123
Content-Type: application/json

{
  "display_name": "Jane Smith",
  "email": "jane.smith@example.com"
}
```

**Delete Method**
```http
DELETE /users/123
```

### 2.3 Partial Updates and Retrievals

**Partial Update (PATCH)**
Use field masks to specify which fields to update:
```http
PATCH /users/123?update_mask=display_name,email
Content-Type: application/json

{
  "display_name": "New Name",
  "email": "new@example.com"
}
```

**Partial Retrieval**
Use field masks to limit response fields:
```http
GET /users/123?read_mask=display_name,email
```

### 2.4 Custom Methods

For operations that don't map to standard CRUD:
```http
POST /orders/123:cancel
POST /documents/456:publish
POST /emails/789:send
POST /users/123:deactivate
```

**Custom Method Rules**
- Use POST (sometimes GET for read-only)
- Append colon + verb to resource name
- Keep the set of custom methods small
- Prefer standard methods when possible

### 2.5 Long-Running Operations

For operations that take significant time:

**Initial Request**
```http
POST /databases/123:backup
```

**Response (Operation)**
```json
{
  "name": "operations/backup-xyz",
  "done": false,
  "metadata": {
    "@type": "type.googleapis.com/BackupMetadata",
    "progress_percent": 0
  }
}
```

**Poll for Status**
```http
GET /operations/backup-xyz
```

**Completed Response**
```json
{
  "name": "operations/backup-xyz",
  "done": true,
  "response": {
    "@type": "type.googleapis.com/Backup",
    "name": "backups/backup-123"
  }
}
```

### 2.6 Rerunnable Jobs

For repeated scheduled operations:
```json
{
  "name": "jobs/nightly-backup",
  "schedule": "0 0 * * *",
  "job_config": {
    "backup_type": "FULL"
  },
  "last_run": {...},
  "next_run_time": "2024-01-16T00:00:00Z"
}
```

**Execute immediately**
```http
POST /jobs/nightly-backup:run
```

---

## Part 3: Resource Relationships

### 3.1 Singleton Sub-Resources

For resources that exist exactly once per parent:
```
/users/123/profile        (not /users/123/profiles)
/users/123/settings
/projects/456/config
```

### 3.2 Cross References

Reference resources by their full name:
```json
{
  "name": "orders/123",
  "customer": "users/456",
  "items": [
    {"product": "products/789", "quantity": 2}
  ]
}
```

### 3.3 Association Resources

For many-to-many relationships with metadata:
```
/groups/123/memberships/456
```
```json
{
  "name": "groups/123/memberships/456",
  "user": "users/789",
  "role": "ADMIN",
  "joined_at": "2024-01-01T00:00:00Z"
}
```

### 3.4 Add/Remove Custom Methods

For simple many-to-many without metadata:
```http
POST /groups/123:addMember
{
  "user": "users/789"
}

POST /groups/123:removeMember
{
  "user": "users/789"
}
```

### 3.5 Polymorphism

Handle dynamic types with discriminators:
```json
{
  "name": "notifications/123",
  "type": "EMAIL",
  "email_config": {
    "recipient": "user@example.com",
    "subject": "Hello"
  }
}
```

Or using `@type` field:
```json
{
  "@type": "type.googleapis.com/EmailNotification",
  "recipient": "user@example.com"
}
```

---

## Part 4: Collective Operations

### 4.1 Copy and Move

```http
POST /files/123:copy
{
  "destination_parent": "folders/456"
}

POST /files/123:move
{
  "destination_parent": "folders/789"
}
```

### 4.2 Batch Operations

**Batch Get**
```http
GET /users:batchGet?ids=123,456,789
```

**Batch Create/Update/Delete**
```http
POST /users:batchCreate
{
  "requests": [
    {"user": {"display_name": "User 1"}},
    {"user": {"display_name": "User 2"}}
  ]
}
```

**Atomicity**: Batch operations should be atomic (all succeed or all fail).

### 4.3 Criteria-Based Deletion

Delete multiple resources matching criteria:
```http
POST /logs:purge
{
  "filter": "timestamp < '2023-01-01'"
}
```

Returns a long-running operation for tracking.

### 4.4 Anonymous Writes

For high-volume data ingestion without addressing:
```http
POST /metrics:write
{
  "entries": [
    {"name": "cpu_usage", "value": 0.75},
    {"name": "memory_usage", "value": 0.60}
  ]
}
```

### 4.5 Pagination

**Request**
```http
GET /users?page_size=25&page_token=eyJvZmZzZXQiOjI1fQ
```

**Response**
```json
{
  "users": [...],
  "next_page_token": "eyJvZmZzZXQiOjUwfQ",
  "total_size": 150
}
```

**Rules**
- Use opaque page tokens (not page numbers)
- Default page size: 25-100
- Maximum page size: 1000
- Include `total_size` when feasible

### 4.6 Filtering

```http
GET /users?filter=status="ACTIVE" AND created_at>"2024-01-01"
```

**Filter Syntax**
- Comparisons: `=`, `!=`, `<`, `>`, `<=`, `>=`
- Logical: `AND`, `OR`, `NOT`
- Functions: `has()`, `contains()`
- Wildcards: `*` for partial matching

### 4.7 Importing and Exporting

**Export**
```http
POST /databases/123:export
{
  "destination": "gs://bucket/exports/",
  "format": "CSV"
}
```

**Import**
```http
POST /databases/123:import
{
  "source": "gs://bucket/data.csv",
  "format": "CSV"
}
```

Both return long-running operations.

---

## Part 5: Safety and Security

### 5.1 Versioning and Compatibility

**URL Versioning**
```
/v1/users
/v2/users
```

**Header Versioning**
```http
GET /users
API-Version: 2024-01-01
```

**Compatibility Rules**
- Adding fields is backward compatible
- Removing fields is NOT backward compatible
- Changing field types is NOT backward compatible
- Use deprecation notices before removal

### 5.2 Soft Deletion

```json
{
  "name": "users/123",
  "display_name": "John Doe",
  "delete_time": "2024-01-15T10:00:00Z",
  "expire_time": "2024-02-15T10:00:00Z"
}
```

**Restore**
```http
POST /users/123:undelete
```

### 5.3 Request Deduplication

Use client-provided request IDs:
```http
POST /orders
X-Request-Id: unique-request-123
Content-Type: application/json

{...}
```

Server stores request ID and returns cached response on retry.

### 5.4 Request Validation

Dry-run mode for validation without execution:
```http
POST /users?validate_only=true
{
  "display_name": "Test User"
}
```

Returns validation errors without creating the resource.

### 5.5 Resource Revisions

Track change history:
```http
GET /documents/123/revisions
GET /documents/123@revision=5
```

```json
{
  "name": "documents/123",
  "revision_id": "5",
  "revision_create_time": "2024-01-15T10:00:00Z",
  "content": "..."
}
```

### 5.6 Request Retrial

**Idempotency Keys**
```http
POST /payments
Idempotency-Key: payment-abc-123
```

**Retry Strategies**
- Exponential backoff with jitter
- Maximum retry attempts
- Circuit breaker pattern

### 5.7 Request Authentication

**API Keys**
```http
GET /users
X-API-Key: your-api-key
```

**Bearer Tokens (OAuth 2.0)**
```http
GET /users
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
```

**Request Signing**
For sensitive operations, sign requests with timestamps to prevent replay attacks.

---

## Quick Reference: HTTP Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST creating resource |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid request syntax |
| 401 | Unauthorized | Missing/invalid authentication |
| 403 | Forbidden | Valid auth but no permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource state conflict |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Error | Server-side failure |
| 503 | Service Unavailable | Temporary overload |

---

## Error Response Format

```json
{
  "error": {
    "code": 400,
    "status": "INVALID_ARGUMENT",
    "message": "Display name is required",
    "details": [
      {
        "@type": "type.googleapis.com/FieldViolation",
        "field": "display_name",
        "description": "Field is required"
      }
    ]
  }
}
```

---

## Checklist: API Design Review

- [ ] Resources are nouns, not verbs
- [ ] Standard methods (CRUD) are used where possible
- [ ] Custom methods are minimized and use `:verb` syntax
- [ ] Resource hierarchy is logical and not too deep
- [ ] Naming is consistent (snake_case, plural collections)
- [ ] Pagination is implemented for list operations
- [ ] Filtering uses a consistent syntax
- [ ] Errors include actionable messages
- [ ] Versioning strategy is defined
- [ ] Authentication/authorization is implemented
- [ ] Idempotency is considered for mutations
- [ ] Long-running operations return operation resources

---

## Usage Examples

**Design a new API**
```
/api-design
Help me design an API for a task management system with users, projects, and tasks.
```

**Review existing API**
```
/api-design
Review this API endpoint design and suggest improvements following best practices.
```

**Add a feature to existing API**
```
/api-design
How should I add soft deletion to my existing users API?
```

---

## References

- "API Design Patterns" by JJ Geewax (Manning, 2021)
- Google API Improvement Proposals: https://google.aip.dev/
- Google Cloud API Design Guide: https://cloud.google.com/apis/design
