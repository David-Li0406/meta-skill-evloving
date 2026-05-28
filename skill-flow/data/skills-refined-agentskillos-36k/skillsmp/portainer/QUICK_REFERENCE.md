# Portainer Quick Reference

## Environment Setup

```bash
export PORTAINER_URL="https://your-portainer-instance.com"
export PORTAINER_TOKEN="ptr_YOUR_TOKEN_HERE"
```

## CLI Commands

The CLI script is located at `skills/portainer/portainer-cli.sh` within this plugin.

### List all stacks
```bash
./portainer-cli.sh list
```

### Check stack status
```bash
./portainer-cli.sh status my-stack
```

### Redeploy with fresh images
```bash
./portainer-cli.sh redeploy my-stack true
```

### View logs
```bash
./portainer-cli.sh logs my-stack backend 100
```

### Delete a stack
```bash
./portainer-cli.sh delete my-stack
```

## Direct API Calls

### Get endpoint ID
```bash
curl -s "$PORTAINER_URL/api/endpoints" -H "X-API-Key: $PORTAINER_TOKEN" | jq '.[0].Id'
```

### List stacks (JSON)
```bash
curl -s "$PORTAINER_URL/api/stacks" -H "X-API-Key: $PORTAINER_TOKEN" | jq .
```

### Get stack by name
```bash
curl -s "$PORTAINER_URL/api/stacks" -H "X-API-Key: $PORTAINER_TOKEN" | \
  jq '.[] | select(.Name=="my-stack")'
```

### Redeploy a stack
```bash
STACK_ID=1
ENDPOINT_ID=1
curl -X PUT "$PORTAINER_URL/api/stacks/$STACK_ID/git/redeploy?endpointId=$ENDPOINT_ID" \
  -H "X-API-Key: $PORTAINER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"pullImage": true, "prune": false}'
```

## Stack Configuration Template

```json
{
  "name": "my-stack",
  "repositoryURL": "https://github.com/user/repo.git",
  "repositoryReferenceName": "refs/heads/main",
  "composeFile": "docker-compose.yml",
  "repositoryAuthentication": true,
  "repositoryUsername": "github-username",
  "repositoryPassword": "ghp_token_here",
  "env": [
    {"name": "DATABASE_URL", "value": "postgresql://..."},
    {"name": "API_KEY", "value": "secret"}
  ],
  "autoUpdate": {
    "interval": "5m"
  }
}
```

## Getting a Portainer API Token

1. Log into your Portainer instance
2. Go to **My Account** (click your username)
3. Scroll to **Access Tokens**
4. Click **Add access token**
5. Give it a description and copy the token (starts with `ptr_`)

## Getting a GitHub Token (for private repos)

```bash
# If using GitHub CLI
gh auth token

# Or create a Personal Access Token at:
# https://github.com/settings/tokens
```
