# API: <METHOD> <PATH>

## Summary

<What this endpoint does, in one sentence.>

## Auth

- Required: <Yes/No>
- Scheme: <Bearer token / API key / session cookie>
- Scopes/roles: <if applicable>

## Request

### Headers

| Name | Value | Required | Notes |
|------|-------|----------|-------|
| <header> | <value> | <yes/no> | <notes> |

### Query parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| <param> | <type> | <yes/no> | <description> |

### Path parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| <param> | <type> | yes | <description> |

### Request body (if applicable)

```json
{
  "<field>": "<value>"
}
```

## Response

### 200 OK (example)

```json
{
  "<field>": "<value>"
}
```

## Errors

| HTTP status | Error code | Meaning | How to fix |
|------------|------------|---------|------------|
| <status> | <code> | <meaning> | <fix> |

## Examples

### cURL

```bash
curl -X <METHOD> "<BASE_URL><PATH>" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '<JSON_BODY>'
```

### SDK (optional)

```ts
// <language-specific snippet>
```

## Notes (optional)

- Rate limits: <details>
- Idempotency: <details>
- Pagination: <details>
- Timeouts/retries: <details>

## Evidence

- Spec: `path/to/spec.ext:line` (or URL if applicable)
- Handler/controller: `path/to/file.ext:line`
- Tests: `path/to/test.ext:line`
