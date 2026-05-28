# API Versioning Documentation

Patterns for documenting API versioning strategies.

## Versioning Strategies

### URL Path Versioning (Recommended)

```
https://api.example.com/v1/orders
https://api.example.com/v2/orders
```

**Documentation:**

```markdown
## API Versioning

The API version is included in the URL path. Always use the latest stable version for new integrations.

| Version | Status | Base URL |
|---------|--------|----------|
| v2 | **Current** | `https://api.example.com/v2` |
| v1 | Deprecated | `https://api.example.com/v1` |

### Version Selection
- New applications should use **v2**
- Existing v1 applications should migrate before the sunset date
```

### Header Versioning

```
GET /orders
Accept: application/vnd.example.v2+json
```

**Documentation:**

```markdown
## API Versioning

Specify the API version in the `Accept` header:

```bash
curl https://api.example.com/orders \
  -H "Accept: application/vnd.example.v2+json"
```

| Version | Accept Header |
|---------|---------------|
| v2 | `application/vnd.example.v2+json` |
| v1 | `application/vnd.example.v1+json` |

If no version is specified, the API defaults to the latest stable version.
```

### Query Parameter Versioning

```
https://api.example.com/orders?api_version=2024-01-15
```

**Documentation:**

```markdown
## API Versioning

Include the API version as a query parameter or header:

```bash
# Query parameter
curl "https://api.example.com/orders?api_version=2024-01-15"

# Header
curl https://api.example.com/orders \
  -H "API-Version: 2024-01-15"
```

| Version | Date | Status |
|---------|------|--------|
| 2024-01-15 | Current | Stable |
| 2023-06-01 | Previous | Deprecated |
```

## Version Lifecycle Documentation

### Version Status Definitions

```markdown
## Version Lifecycle

### Status Definitions

| Status | Description |
|--------|-------------|
| **Preview** | Early access, may change without notice |
| **Current** | Recommended for production use |
| **Deprecated** | Still works, but will be removed |
| **Sunset** | No longer available |

### Version Timeline

```
Preview → Current → Deprecated → Sunset
   │          │          │          │
   └──────────┴──────────┴──────────┘
        Active support period
```

### Support Policy

- **Current versions**: Full support, bug fixes, security patches
- **Deprecated versions**: Security patches only, 12-month notice before sunset
- **Preview versions**: No guaranteed support, may change at any time
```

### Migration Timeline

```markdown
## v1 to v2 Migration

### Timeline

| Date | Event |
|------|-------|
| 2024-01-15 | v2 released |
| 2024-03-01 | v1 deprecated (warnings enabled) |
| 2024-12-31 | v1 sunset |

### Deprecation Warnings

After March 1, 2024, v1 responses include deprecation headers:

```http
HTTP/1.1 200 OK
Deprecation: true
Sunset: Tue, 31 Dec 2024 23:59:59 GMT
Link: <https://api.example.com/v2/orders>; rel="successor-version"
```
```

## Breaking Changes Documentation

### What Constitutes a Breaking Change

```markdown
## Breaking Changes Policy

### Breaking Changes (Require New Version)

- Removing an endpoint
- Removing a required field from responses
- Adding a new required field to requests
- Changing field types (string → integer)
- Changing authentication requirements
- Changing error response formats
- Renaming fields

### Non-Breaking Changes (Same Version)

- Adding new endpoints
- Adding optional request fields
- Adding new response fields
- Adding new enum values
- Adding new error codes
- Performance improvements
- Bug fixes
```

### Documenting Changes

```markdown
## v2 Changelog

### 2024-01-15: v2.0.0 (Current)

#### Breaking Changes from v1

| Change | v1 | v2 | Migration |
|--------|----|----|-----------|
| User ID format | integer | string (prefixed) | See [ID Migration](#id-migration) |
| Pagination | offset-based | cursor-based | See [Pagination Migration](#pagination) |
| Error format | `{error: string}` | `{error: {code, message}}` | See [Error Migration](#errors) |

#### New Features

- Webhook support for all events
- Batch operations (up to 100 items)
- Field filtering with `?fields=id,name,email`

#### Removed Features

- XML response format (use JSON)
- Legacy authentication tokens
```

## Migration Guides

### Comprehensive Migration Guide

```markdown
## Migrating from v1 to v2

### Overview

This guide helps you migrate from API v1 to v2. The migration involves:

1. Updating endpoint URLs
2. Handling new ID formats
3. Updating pagination logic
4. Updating error handling

**Estimated effort**: 2-4 hours for typical integrations

### Step 1: Update Base URL

```diff
- https://api.example.com/v1
+ https://api.example.com/v2
```

### Step 2: Update ID Handling

v2 uses prefixed string IDs instead of integers:

```diff
- user_id: 12345
+ user_id: "usr_7k9m2n4p5q"
```

**Code change:**

```python
# v1
user_id = response['user_id']  # int
url = f"/users/{user_id}"

# v2
user_id = response['user_id']  # str
url = f"/users/{user_id}"  # Works the same, but type is different
```

### Step 3: Update Pagination

v2 uses cursor-based pagination:

```diff
# v1 - Offset pagination
- GET /orders?page=2&per_page=20

# v2 - Cursor pagination
+ GET /orders?cursor=eyJpZCI6MTAwfQ&limit=20
```

**Code change:**

```python
# v1
def fetch_all_orders():
    page = 1
    while True:
        response = api.get(f'/orders?page={page}')
        yield from response['data']
        if page >= response['total_pages']:
            break
        page += 1

# v2
def fetch_all_orders():
    cursor = None
    while True:
        params = {'limit': 100}
        if cursor:
            params['cursor'] = cursor
        response = api.get('/orders', params=params)
        yield from response['data']
        if not response['has_more']:
            break
        cursor = response['next_cursor']
```

### Step 4: Update Error Handling

v2 has structured error responses:

```diff
# v1
- {"error": "User not found"}

# v2
+ {
+   "error": {
+     "code": "not_found",
+     "message": "User not found",
+     "request_id": "req_abc123"
+   }
+ }
```

**Code change:**

```python
# v1
if response.status_code >= 400:
    error_message = response.json()['error']

# v2
if response.status_code >= 400:
    error = response.json()['error']
    error_code = error['code']
    error_message = error['message']
```

### Verification Checklist

After migration, verify:

- [ ] All endpoints return 200/201 status
- [ ] Pagination works correctly
- [ ] Error handling catches all error codes
- [ ] Webhook signatures validate
- [ ] Rate limits are respected
```

## Dual-Version Support Documentation

```markdown
## Running Both Versions

During migration, you may need to support both API versions:

### SDK Configuration

```python
# Python SDK
from example_api import Client

# v1 (deprecated)
v1_client = Client(api_key="...", version="v1")

# v2 (current)
v2_client = Client(api_key="...", version="v2")
```

### Feature Flags

Use feature flags to gradually migrate:

```python
if feature_flags.use_v2_api:
    response = v2_client.create_order(order_data)
else:
    response = v1_client.create_order(order_data)
```

### Testing Both Versions

Run integration tests against both:

```bash
API_VERSION=v1 pytest tests/integration/
API_VERSION=v2 pytest tests/integration/
```
```
