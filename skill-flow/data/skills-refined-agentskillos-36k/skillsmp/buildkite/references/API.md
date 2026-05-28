# Buildkite API Reference

## Authentication

### Token Creation

Create at `https://buildkite.com/user/api-access-tokens`.

### Token Scopes

| Scope | Permission |
|-------|------------|
| `read_builds` | List builds |
| `write_builds` | Create, cancel builds |
| `read_pipelines` | List pipelines |
| `write_pipelines` | Create, update pipelines |
| `read_agents` | List agents |
| `write_agents` | Stop agents |
| `read_artifacts` | Download artifacts |
| `write_artifacts` | Delete artifacts |
| `read_job_env` | Read job environment |
| `read_user` | Read user info |

### Request Format

```bash
curl -H "Authorization: Bearer $BUILDKITE_TOKEN" \
  "https://api.buildkite.com/v2/..."
```

## REST API

Base URL: `https://api.buildkite.com/v2`

### Builds

```bash
# List builds
GET /organizations/{org}/pipelines/{pipeline}/builds
GET /organizations/{org}/pipelines/{pipeline}/builds?branch=main&state=passed

# Get build
GET /organizations/{org}/pipelines/{pipeline}/builds/{number}

# Create build
POST /organizations/{org}/pipelines/{pipeline}/builds
{
  "commit": "HEAD",
  "branch": "main",
  "message": "Deploy :rocket:",
  "env": {
    "DEPLOY_ENV": "production"
  },
  "meta_data": {
    "release": "v1.2.3"
  }
}

# Cancel build
PUT /organizations/{org}/pipelines/{pipeline}/builds/{number}/cancel

# Rebuild
PUT /organizations/{org}/pipelines/{pipeline}/builds/{number}/rebuild
```

### Pipelines

```bash
# List pipelines
GET /organizations/{org}/pipelines

# Get pipeline
GET /organizations/{org}/pipelines/{slug}

# Create pipeline
POST /organizations/{org}/pipelines
{
  "name": "My Pipeline",
  "repository": "git@github.com:org/repo.git",
  "steps": [
    {
      "type": "script",
      "name": "Build",
      "command": "make build"
    }
  ]
}

# Update pipeline
PATCH /organizations/{org}/pipelines/{slug}
{
  "description": "Updated description"
}

# Delete pipeline
DELETE /organizations/{org}/pipelines/{slug}
```

### Jobs

```bash
# List jobs for build
GET /organizations/{org}/pipelines/{pipeline}/builds/{number}/jobs

# Get job
GET /organizations/{org}/pipelines/{pipeline}/builds/{number}/jobs/{job_id}

# Get job log
GET /organizations/{org}/pipelines/{pipeline}/builds/{number}/jobs/{job_id}/log

# Retry job
PUT /organizations/{org}/pipelines/{pipeline}/builds/{number}/jobs/{job_id}/retry

# Unblock job
PUT /organizations/{org}/pipelines/{pipeline}/builds/{number}/jobs/{job_id}/unblock
{
  "fields": {
    "env": "production"
  }
}
```

### Artifacts

```bash
# List artifacts for build
GET /organizations/{org}/pipelines/{pipeline}/builds/{number}/artifacts

# List artifacts for job
GET /organizations/{org}/pipelines/{pipeline}/builds/{number}/jobs/{job_id}/artifacts

# Get artifact
GET /organizations/{org}/pipelines/{pipeline}/builds/{number}/jobs/{job_id}/artifacts/{id}

# Download artifact (returns 302 redirect)
GET /organizations/{org}/pipelines/{pipeline}/builds/{number}/jobs/{job_id}/artifacts/{id}/download

# Delete artifact
DELETE /organizations/{org}/pipelines/{pipeline}/builds/{number}/jobs/{job_id}/artifacts/{id}
```

### Agents

```bash
# List agents
GET /organizations/{org}/agents
GET /organizations/{org}/agents?name=prod-*

# Get agent
GET /organizations/{org}/agents/{id}

# Stop agent
PUT /organizations/{org}/agents/{id}/stop
{
  "force": false
}
```

### Annotations

```bash
# List annotations
GET /organizations/{org}/pipelines/{pipeline}/builds/{number}/annotations

# Create annotation
POST /organizations/{org}/pipelines/{pipeline}/builds/{number}/annotations
{
  "body": "Deployment complete!",
  "style": "success",
  "context": "deploy"
}

# Delete annotation
DELETE /organizations/{org}/pipelines/{pipeline}/builds/{number}/annotations/{context}
```

### Meta-data

```bash
# List meta-data
GET /organizations/{org}/pipelines/{pipeline}/builds/{number}/meta-data

# Get meta-data
GET /organizations/{org}/pipelines/{pipeline}/builds/{number}/meta-data/{key}

# Set meta-data
POST /organizations/{org}/pipelines/{pipeline}/builds/{number}/meta-data
{
  "key": "version",
  "value": "1.2.3"
}
```

## Rate Limits

- **200 requests/minute** per organization
- Headers: `RateLimit-Remaining`, `RateLimit-Reset`
- 429 response when exceeded

## Pagination

```bash
# Query params
?page=2&per_page=100  # max 100

# Link header
Link: <https://api.buildkite.com/v2/...?page=2>; rel="next",
      <https://api.buildkite.com/v2/...?page=5>; rel="last"
```

## GraphQL API

Endpoint: `https://graphql.buildkite.com/v1`

Use GraphQL when you need:
- Nested data in single request
- Build lookup by UUID
- Job environment variables
- Complex filtering

### Authentication

```bash
curl -X POST https://graphql.buildkite.com/v1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "..."}'
```

### Common Queries

```graphql
# Get build by UUID
query GetBuild($uuid: ID!) {
  build(uuid: $uuid) {
    number
    state
    branch
    commit
    message
    createdAt
    startedAt
    finishedAt
    jobs(first: 50) {
      edges {
        node {
          ... on JobTypeCommand {
            uuid
            label
            state
            exitStatus
            env  # Only available in GraphQL
          }
        }
      }
    }
  }
}

# List pipelines with recent builds
query ListPipelines($org: ID!) {
  organization(slug: $org) {
    pipelines(first: 20) {
      edges {
        node {
          name
          slug
          builds(first: 5) {
            edges {
              node {
                number
                state
                branch
              }
            }
          }
        }
      }
    }
  }
}

# Search builds
query SearchBuilds($org: ID!, $pipeline: ID!) {
  pipeline(slug: $pipeline) {
    builds(
      first: 10
      branch: "main"
      state: [PASSED, FAILED]
    ) {
      edges {
        node {
          number
          state
          createdAt
        }
      }
    }
  }
}
```

### Mutations

```graphql
# Create build
mutation CreateBuild($input: BuildCreateInput!) {
  buildCreate(input: $input) {
    build {
      uuid
      number
      url
    }
  }
}

# Variables:
{
  "input": {
    "pipelineID": "UGlwZWxpbmUtLi4u",
    "commit": "HEAD",
    "branch": "main",
    "message": "Triggered via API"
  }
}

# Cancel build
mutation CancelBuild($id: ID!) {
  buildCancel(input: { id: $id }) {
    build {
      state
    }
  }
}
```

### Rate Limits

- **20,000 complexity points** per 2 minutes
- Each field has a cost
- Pagination connections have higher costs

## Webhooks

### Event Types

| Event | Description |
|-------|-------------|
| `build.scheduled` | Build created |
| `build.running` | Build started |
| `build.finished` | Build completed |
| `job.scheduled` | Job queued |
| `job.started` | Job running |
| `job.finished` | Job completed |
| `agent.connected` | Agent online |
| `agent.disconnected` | Agent offline |

### Payload Example

```json
{
  "event": "build.finished",
  "build": {
    "id": "uuid",
    "number": 123,
    "state": "passed",
    "branch": "main",
    "commit": "abc123",
    "message": "Fix bug",
    "created_at": "2024-01-15T10:00:00Z",
    "started_at": "2024-01-15T10:00:05Z",
    "finished_at": "2024-01-15T10:05:00Z"
  },
  "pipeline": {
    "slug": "my-pipeline"
  },
  "sender": {
    "name": "John Doe"
  }
}
```

### Webhook Signature

Verify with `X-Buildkite-Signature` header:

```python
import hmac
import hashlib

def verify_webhook(payload, signature, token):
    expected = hmac.new(
        token.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

## Code Examples

### Trigger Build (Python)

```python
import requests

def trigger_build(org, pipeline, branch="main", env=None):
    url = f"https://api.buildkite.com/v2/organizations/{org}/pipelines/{pipeline}/builds"
    headers = {"Authorization": f"Bearer {BUILDKITE_TOKEN}"}
    data = {
        "commit": "HEAD",
        "branch": branch,
        "env": env or {}
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
```

### Wait for Build (Python)

```python
import time

def wait_for_build(org, pipeline, build_number, timeout=600):
    url = f"https://api.buildkite.com/v2/organizations/{org}/pipelines/{pipeline}/builds/{build_number}"
    headers = {"Authorization": f"Bearer {BUILDKITE_TOKEN}"}
    
    start = time.time()
    while time.time() - start < timeout:
        response = requests.get(url, headers=headers)
        build = response.json()
        
        if build["state"] in ["passed", "failed", "canceled"]:
            return build
        
        time.sleep(10)
    
    raise TimeoutError(f"Build {build_number} did not complete")
```

### Download Artifacts (Python)

```python
def download_artifacts(org, pipeline, build_number, pattern="*"):
    url = f"https://api.buildkite.com/v2/organizations/{org}/pipelines/{pipeline}/builds/{build_number}/artifacts"
    headers = {"Authorization": f"Bearer {BUILDKITE_TOKEN}"}
    
    response = requests.get(url, headers=headers)
    artifacts = response.json()
    
    for artifact in artifacts:
        if fnmatch.fnmatch(artifact["filename"], pattern):
            download_url = artifact["download_url"]
            r = requests.get(download_url, headers=headers, allow_redirects=True)
            with open(artifact["filename"], "wb") as f:
                f.write(r.content)
```

### GraphQL Client (Python)

```python
def graphql_query(query, variables=None):
    url = "https://graphql.buildkite.com/v1"
    headers = {
        "Authorization": f"Bearer {BUILDKITE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"query": query, "variables": variables or {}}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
```
