---
name: portainer
description: Use this skill when managing Docker stack deployments via Portainer, including creating stacks from Git repositories, checking deployment status, and viewing logs.
---

# Portainer Deployment Management

Manage Docker stack deployments via Portainer API.

## Configuration

Before using, ensure these are available:
- **PORTAINER_URL**: Portainer instance URL (e.g., `https://portainer.example.com`)
- **PORTAINER_TOKEN**: API token from Portainer (User Settings > Access Tokens)

Store sensitive config in environment or prompt user when needed.

## Available Operations

### 1. List All Stacks

```bash
curl -s -X GET "$PORTAINER_URL/api/stacks" \
  -H "X-API-Key: $PORTAINER_TOKEN" | jq '.[] | {Id, Name, Status, CreationDate}'
```

Status codes: `1` = active, `2` = inactive

### 2. Check Stack Status

```bash
# Get specific stack by name
STACK_NAME="my-stack"
curl -s -X GET "$PORTAINER_URL/api/stacks" \
  -H "X-API-Key: $PORTAINER_TOKEN" | jq ".[] | select(.Name==\"$STACK_NAME\")"
```

### 3. Get Stack Containers/Services

```bash
STACK_ID=24
ENDPOINT_ID=1
curl -s -X GET "$PORTAINER_URL/api/endpoints/$ENDPOINT_ID/docker/containers/json?all=true" \
  -H "X-API-Key: $PORTAINER_TOKEN" | jq '.[] | select(.Labels["com.docker.compose.project"]=="STACK_NAME") | {Id: .Id[:12], Name: .Names[0], State, Status}'
```

### 4. Create Stack from Git Repository

Required parameters:
- `name`: Stack name (lowercase, hyphens allowed)
- `repositoryURL`: Git repo URL
- `repositoryReferenceName`: Branch (e.g., `refs/heads/main`)
- `composeFile`: Path to compose file in repo
- `env`: Array of environment variables

```bash
ENDPOINT_ID=$(curl -s "$PORTAINER_URL/api/endpoints" -H "X-API-Key: $PORTAINER_TOKEN" | jq '.[0].Id')

curl -X POST "$PORTAINER_URL/api/stacks/create/standalone/repository?endpointId=$ENDPOINT_ID" \
  -H "X-API-Key: $PORTAINER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-stack",
    "repositoryURL": "https://github.com/user/repo.git",
    "repositoryReferenceName": "refs/heads/main",
    "composeFile": "docker-compose.yml",
    "repositoryAuthentication": true,
    "repositoryUsername": "USERNAME",
    "repositoryPassword": "GITHUB_TOKEN",
    "env": [
      {"name": "VAR_NAME", "value": "value"}
    ],
    "autoUpdate": {
      "interval": "5m"
    }
  }'
```