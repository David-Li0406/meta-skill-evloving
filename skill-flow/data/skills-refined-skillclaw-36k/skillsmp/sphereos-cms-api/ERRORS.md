# Error Handling

## Error Response Format

```json
{
  "errors": [
    {
      "message": "Organization with slug 'existing-slug' already exists",
      "extensions": {
        "code": "CONFLICT",
        "statusCode": 409
      },
      "path": ["createOrganization"]
    }
  ],
  "data": null
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `BAD_REQUEST` | 400 | Invalid input (validation failed) |
| `UNAUTHENTICATED` | 401 | Missing or invalid token |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Resource already exists (duplicate slug) |
| `INTERNAL_SERVER_ERROR` | 500 | Unexpected server error |

## Validation Error

```json
{
  "errors": [
    {
      "message": "Slug must be lowercase alphanumeric with hyphens",
      "extensions": {
        "code": "BAD_REQUEST",
        "statusCode": 400,
        "field": "slug"
      }
    }
  ]
}
```

## Authentication Error

```json
{
  "errors": [
    {
      "message": "Invalid or expired token",
      "extensions": {
        "code": "UNAUTHENTICATED",
        "statusCode": 401
      }
    }
  ]
}
```

## Not Found Error

```json
{
  "errors": [
    {
      "message": "Content entry with ID 'entry_xyz' not found",
      "extensions": {
        "code": "NOT_FOUND",
        "statusCode": 404
      }
    }
  ]
}
```

## Conflict Error

```json
{
  "errors": [
    {
      "message": "Organization with slug 'existing-slug' already exists",
      "extensions": {
        "code": "CONFLICT",
        "statusCode": 409
      }
    }
  ]
}
```

## Handling Errors in Code

```typescript
try {
  const { data, errors } = await client.mutate({
    mutation: CREATE_CONTENT_ENTRY,
    variables: { input },
  });

  if (errors) {
    const error = errors[0];
    const code = error.extensions?.code;

    switch (code) {
      case 'CONFLICT':
        console.error('Entry already exists:', error.message);
        break;
      case 'BAD_REQUEST':
        console.error('Validation error:', error.message);
        break;
      case 'UNAUTHENTICATED':
        // Refresh token and retry
        break;
      default:
        console.error('API error:', error.message);
    }
  }
} catch (networkError) {
  console.error('Network error:', networkError);
}
```
