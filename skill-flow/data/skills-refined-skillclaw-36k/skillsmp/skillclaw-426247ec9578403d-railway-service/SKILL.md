---
name: railway-service
description: Use this skill when you need to check service status, rename services, change service icons, link services, or create services with Docker images.
---

# Railway Service Management

Check status, update properties, and advanced service creation.

## When to Use

- User asks about service status, health, or deployments
- User asks "is my service deployed?"
- User wants to rename a service or change service icon
- User wants to link a different service
- User wants to deploy a Docker image as a new service (advanced)

**Note:** For creating services with local code (the common case), prefer the `railway-new` skill which handles project setup, scaffolding, and service creation together.

**For GitHub repo sources:** Use `railway-new` skill to create an empty service, then `railway-environment` skill to configure the source.

## Create Service

Create a new service via GraphQL API. There is no CLI command for this.

### Get Context

```bash
railway status --json
```

Extract:
- `project.id` - for creating the service
- `environment.id` - for staging the instance config

### Create Service Mutation

```graphql
mutation serviceCreate($input: ServiceCreateInput!) {
  serviceCreate(input: $input) {
    id
    name
  }
}
```

### ServiceCreateInput Fields

| Field | Type | Description |
|-------|------|-------------|
| `projectId` | String! | Project ID (required) |
| `name` | String | Service name (auto-generated if omitted) |
| `source.image` | String | Docker image (e.g., `nginx:latest`) |
| `source.repo` | String | GitHub repo (e.g., `user/repo`) |
| `branch` | String | Git branch for repo source |
| `environmentId` | String | If set and is a fork, only creates in that env |

### Example: Create empty service

```bash
bash <<'SCRIPT'
railway-api.sh \
  'mutation createService($input: ServiceCreateInput!) {
    serviceCreate(input: $input) { id name }
  }' \
  '{"input": {"projectId": "PROJECT_ID"}}'
SCRIPT
```

### Example: Create service with image

```bash
bash <<'SCRIPT'
railway-api.sh \
  'mutation createService($input: ServiceCreateInput!) {
    serviceCreate(input: $input) { id name }
  }' \
  '{"input": {"projectId": "PROJECT_ID", "name": "my-service", "source": {"image": "nginx:latest"}}}'
SCRIPT
```