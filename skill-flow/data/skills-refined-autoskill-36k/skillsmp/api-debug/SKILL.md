---
name: api-debug
description: Query the PrdAgent API to fetch real data for debugging. Use when you need to investigate issues, verify data states, or understand system behavior by querying actual API endpoints.
---

# API Debug

Query the PrdAgent API using AI Access Key authentication to fetch real data for debugging and investigation.

## When to Use

This skill should be used when:
- Debugging issues that require checking actual data states
- Investigating user-reported problems
- Verifying API behavior or data consistency
- Understanding system state without guessing

## Configuration

The API uses AI Access Key authentication:
- **Environment Variable**: `AI_ACCESS_KEY` (configured on the server)
- **Request Headers**:
  - `X-AI-Access-Key: {key}` - The configured access key
  - `X-AI-Impersonate: {username}` - A valid username to impersonate (must exist in database)

## Base URL

```
http://[::1]:5000
```

## Common API Endpoints

### User Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | List all users |
| GET | `/api/users/{userId}` | Get user details |

### Authentication & Authorization
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/authz/users` | List users with permissions |
| GET | `/api/authz/roles` | List system roles |

### Projects & PRD
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/prd/projects` | List projects |
| GET | `/api/prd/projects/{id}` | Get project details |

### Model Groups
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/model-groups` | List model groups |

### System
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/init/status` | Get system initialization status |

## Execution Steps

1. **Identify the data needed**: Determine which API endpoint to query based on the debugging context.

2. **Execute the query**: Use curl with the AI Access Key headers:
   ```bash
   curl -s "http://[::1]:5000/api/{endpoint}" \
     -H "X-AI-Access-Key: 123" \
     -H "X-AI-Impersonate: admin"
   ```

3. **Parse the response**: The API returns JSON in this format:
   ```json
   {
     "success": true,
     "data": { ... },
     "error": null
   }
   ```

4. **Analyze the data**: Use the returned data to understand the system state and diagnose issues.

## Example Queries

### Get all users
```bash
curl -s "http://[::1]:5000/api/users" \
  -H "X-AI-Access-Key: 123" \
  -H "X-AI-Impersonate: admin" | jq
```

### Get specific user
```bash
curl -s "http://[::1]:5000/api/users/user1" \
  -H "X-AI-Access-Key: 123" \
  -H "X-AI-Impersonate: admin" | jq
```

### List projects with pagination
```bash
curl -s "http://[::1]:5000/api/prd/projects?page=1&pageSize=10" \
  -H "X-AI-Access-Key: 123" \
  -H "X-AI-Impersonate: admin" | jq
```

## Error Handling

- **401 Unauthorized**: Check that `AI_ACCESS_KEY` environment variable is set on the server
- **401 User not found**: The username in `X-AI-Impersonate` must exist in the database
- **403 Forbidden**: Should not happen with AI Access Key (has super permissions)
- **404 Not Found**: Check the endpoint path

## Security Notes

- This skill has super permissions and can access all data
- Use responsibly for debugging purposes only
- The access key should be kept secure and not logged
- All requests are logged on the server for audit purposes
