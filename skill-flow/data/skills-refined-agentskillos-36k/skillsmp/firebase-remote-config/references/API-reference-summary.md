# Firebase Remote Config REST API Summary

Base: <https://firebaseremoteconfig.googleapis.com/v1>

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/projects/{project}/remoteConfig` | Fetch default (client) template |
| GET | `/projects/{project}/namespaces/{namespace}/remoteConfig` | Fetch template for specific namespace |
| PUT | `/projects/{project}/remoteConfig` | Publish default template (with If-Match ETag) |
| PUT | `/projects/{project}/namespaces/{namespace}/remoteConfig` | Publish template to specific namespace |
| POST | `/projects/{project}/remoteConfig:rollback` | Rollback default template |
| POST | `/projects/{project}/namespaces/{namespace}/remoteConfig:rollback` | Rollback namespace template |

## Namespaces

- `firebase` - Client-side Remote Config (default, can omit from path)
- `firebase-server` - Server-side Remote Config (must use `/namespaces/firebase-server/` in path)

## Authentication

Requires OAuth2 Bearer token with `cloudconfig.admin` IAM role.

**Required Headers:**

- `Authorization: Bearer {token}`
- `X-Goog-User-Project: {project_id}` - Required when using Application Default Credentials

## Template Structure

```json
{
  "parameters": {
    "parameter_key": {
      "defaultValue": {
        "value": "string"
      },
      "conditionalValues": {
        "condition_name": {
          "value": "string"
        }
      },
      "description": "string"
    }
  },
  "conditions": [
    {
      "name": "string",
      "expression": "string",
      "tagColor": "BLUE|GREEN|ORANGE|PINK|PURPLE|TEAL|CYAN|BROWN"
    }
  ],
  "version": {
    "versionNumber": "string",
    "updateTime": "timestamp",
    "updateUser": {
      "email": "string"
    }
  }
}
```

## ETag Handling

**Important:** Firebase Remote Config API does NOT return ETag as an HTTP header. The version information in the response body serves as the implicit ETag.

### Publishing Templates

**Recommended approach:**

1. Remove the `version` field from template before publishing (Firebase auto-generates it)
2. Use `If-Match: *` header to force update

```bash
# Remove version field
jq 'del(.version)' template.json > template-publish.json

# Publish with force update
curl -X PUT \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Goog-User-Project: {project_id}" \
  -H "If-Match: *" \
  -H "Content-Type: application/json" \
  "https://firebaseremoteconfig.googleapis.com/v1/projects/{project_id}/remoteConfig" \
  --data-binary @template-publish.json
```

## References

- Remote Config Conditional Expression Reference — Official syntax, elements, and operators for condition expressions. <https://firebase.google.com/docs/remote-config/condition-reference>
- Remote Config REST API — Schema and field definitions for Remote Config templates (conditions, parameters, parameterGroups, value types). <https://firebase.google.com/docs/reference/remote-config/rest/v1/RemoteConfig>

**Note:** Using `If-Match: *` forces an update and bypasses concurrency checks. Use with caution in production environments where multiple users might be editing simultaneously.
