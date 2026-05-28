---
name: restspace-api
description: Interact with Restspace Runtime servers. Use when you need to make HTTP requests to a Restspace instance for data, files, or other operations. Always discover services first via /.well-known/restspace/services.
allowed-tools: Bash, Read
---

# Restspace Runtime API

Interact with a running Restspace Runtime instance via HTTP.

## Key Concept: Dynamic Service Discovery

Restspace has **no fixed URLs** except for the discovery endpoint. Services are mounted at configurable paths, so you must **always discover services first** before performing operations.

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `RESTSPACE_URL` | No | Server URL (default: `http://localhost:3100`) |
| `RESTSPACE_EMAIL` | Yes | Login email address |
| `RESTSPACE_PASSWORD` | Yes | Login password |

## Workflow

### Step 1: Discover Available Services (ALWAYS DO THIS FIRST)

**IMPORTANT**: Always use `$RESTSPACE_URL` directly. Do NOT use intermediate variable assignments like `BASE_URL=...` as they can cause shell expansion issues on Windows.

```bash
# Get raw JSON (recommended - avoids jq piping issues)
curl -s "$RESTSPACE_URL/.well-known/restspace/services"

# Optional: pretty print with jq if needed
curl -s "$RESTSPACE_URL/.well-known/restspace/services" | jq '.'
```

If `RESTSPACE_URL` is not set, it defaults to `http://localhost:3100`.

Response shows services with their paths and types:
```json
{
  "/api/users": {
    "name": "User Data",
    "source": "./services/data.rsm.json",
    "apis": ["store"]
  },
  "/files": {
    "name": "File Storage",
    "source": "./services/file.rsm.json",
    "apis": ["store"]
  },
  "/auth": {
    "name": "Authentication",
    "source": "./services/auth.rsm.json",
    "apis": ["auth"]
  }
}
```

### Step 2: Find Services by Type

```bash
# Find data services
curl -s "$RESTSPACE_URL/.well-known/restspace/services" | \
  jq 'to_entries | map(select(.value.source | contains("data.rsm"))) | .[] | {path: .key, name: .value.name}'

# Find file services
curl -s "$RESTSPACE_URL/.well-known/restspace/services" | \
  jq 'to_entries | map(select(.value.source | contains("file.rsm"))) | .[] | {path: .key, name: .value.name}'

# Find auth service
curl -s "$RESTSPACE_URL/.well-known/restspace/services" | \
  jq 'to_entries | map(select(.value.source | contains("auth.rsm"))) | .[] | {path: .key, name: .value.name}'
```

### Step 3: Handle Multiple Services

If multiple services of the same type exist (e.g., multiple data services), **present them to the user and ask which to use**.

If the user specifies a URL path in their prompt, use that path directly.

### Step 4: Authenticate

See [AUTH.md](AUTH.md) for authentication patterns.

### Step 5: Perform Operations

Use the discovered service path for all operations. See:
- [AUTH.md](AUTH.md) - Authentication (login, logout, sessions)
- [DATA.md](DATA.md) - Data CRUD operations
- [FILES.md](FILES.md) - File operations
- [PIPELINES.md](PIPELINES.md) - Pipelines and transforms (compose services)

## Service Type Patterns

| Service Type | Source Pattern |
|--------------|----------------|
| Data (JSON store) | `./services/data.rsm.json` |
| File storage | `./services/file.rsm.json` |
| Authentication | `./services/auth.rsm.json` |
| Dataset (single) | `./services/dataset.rsm.json` |
| Template | `./services/template.rsm.json` |
| Pipeline | `./services/pipeline.rsm.json` |

## Common Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |

## Security Notes

- Never echo or log `$RESTSPACE_EMAIL` or `$RESTSPACE_PASSWORD`
- Use `-s` (silent) flag to suppress curl output
- Keep `cookies.txt` in a secure, non-committed location
