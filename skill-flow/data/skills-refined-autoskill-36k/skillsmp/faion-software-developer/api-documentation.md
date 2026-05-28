# API Documentation

**ID:** api-documentation

## Problem

Good API needs good documentation. Developers won't use what they don't understand.

## Framework

**Documentation Tools:**

| Tool | Type | Best For |
|------|------|----------|
| **Swagger UI** | Interactive | Try-it-out testing |
| **Redoc** | Reference | Clean, readable docs |
| **Stoplight** | Design-first | Visual API design |
| **Postman** | Testing + Docs | Team collaboration |
| **AsyncAPI** | Event-driven | WebSocket, Kafka |

## Swagger UI Setup

```python
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI(
    title="User Management API",
    description="""
    ## Overview

    This API provides user management capabilities.

    ## Authentication

    All endpoints require Bearer token authentication.

    ```
    Authorization: Bearer <your-token>
    ```

    ## Rate Limits

    - Free: 100 requests/hour
    - Pro: 10,000 requests/hour
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
```

## Documentation Structure

```markdown
# User Management API

## Overview
Brief description of what the API does.

## Quick Start
```bash
# Get your API key
curl -X POST https://api.example.com/auth/register

# Make your first request
curl -H "Authorization: Bearer YOUR_KEY" \
  https://api.example.com/users
```

## Authentication
How to authenticate with the API.

## Endpoints
### Users
- GET /users - List all users
- POST /users - Create a user
- GET /users/{id} - Get user by ID

## Error Codes
| Code | Meaning | Solution |
|------|---------|----------|
| 400 | Bad Request | Check request body |
| 401 | Unauthorized | Verify API key |

## SDKs
- JavaScript: `npm install @example/api-client`
- Python: `pip install example-api`

## Changelog
### v1.1.0 (2026-01-15)
- Added user search endpoint
- Fixed pagination bug
```

## Code Examples

```yaml
# OpenAPI with examples
paths:
  /users:
    post:
      summary: Create user
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUser'
            examples:
              basic:
                summary: Basic user
                value:
                  name: "John Doe"
                  email: "john@example.com"
              with-role:
                summary: User with admin role
                value:
                  name: "Admin User"
                  email: "admin@example.com"
                  role: "admin"
```

## Best Practices

- Include working code examples in multiple languages
- Provide copy-paste ready curl commands
- Document all error scenarios
- Keep examples up-to-date with tests
- Add changelog for version history
- Include rate limit information
- Show authentication flow
- Provide SDKs for popular languages

## Agent

faion-api-agent
