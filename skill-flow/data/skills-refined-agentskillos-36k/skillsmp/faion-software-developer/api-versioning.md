# API Versioning

**ID:** api-versioning

## Problem

APIs evolve, but breaking changes break clients. Need backward compatibility strategy.

## Framework

**Strategy Comparison:**

| Strategy | Example | Pros | Cons |
|----------|---------|------|------|
| **URL Path** | `/v1/users` | Clear, cacheable | URL pollution |
| **Query Param** | `/users?version=1` | Easy to add | Caching issues |
| **Header** | `Accept-Version: v1` | Clean URLs | Less visible |
| **Content-Type** | `Accept: application/vnd.api+json;v=1` | Standards-based | Complex |

## URL Path Versioning (Recommended)

```
/api/v1/users
/api/v2/users
```

**Implementation:**

```python
# Django/FastAPI
from fastapi import APIRouter

v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")

@v1_router.get("/users")
async def get_users_v1():
    return {"format": "v1", "users": [...]}

@v2_router.get("/users")
async def get_users_v2():
    return {"data": {"users": [...]}, "meta": {...}}
```

## Header Versioning

```http
GET /users HTTP/1.1
Host: api.example.com
Accept-Version: v2
```

```python
from fastapi import Header

@app.get("/users")
async def get_users(accept_version: str = Header("v1")):
    if accept_version == "v2":
        return v2_response()
    return v1_response()
```

## Deprecation Strategy

```http
HTTP/1.1 200 OK
Deprecation: Sun, 01 Jan 2026 00:00:00 GMT
Sunset: Sun, 01 Jul 2026 00:00:00 GMT
Link: </api/v2/users>; rel="successor-version"
```

**Response Warning:**

```json
{
  "data": [...],
  "_warnings": [
    {
      "code": "DEPRECATED_API",
      "message": "v1 API deprecated. Migrate to v2 by 2026-07-01",
      "documentation": "https://api.example.com/docs/migration"
    }
  ]
}
```

## Best Practices

- Default to latest stable version
- Support at least 2 versions simultaneously
- Announce deprecation 6+ months ahead
- Provide migration guides
- Log version usage for sunset planning
- Use feature flags for gradual rollout

## Agent

faion-api-agent
