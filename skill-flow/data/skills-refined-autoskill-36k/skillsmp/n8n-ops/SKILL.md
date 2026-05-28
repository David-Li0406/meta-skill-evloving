---
name: n8n-ops
permissionMode: bypassPermissions
description: n8n Workflow Operations - List, trigger, create, deploy workflows. Full lifecycle via MCP Hub or Direct API.
---

# n8n Ops

> **Operations skill for n8n workflows.**

## Quick Start: What Do You Need?

| Task | Action |
|------|--------|
| **List/trigger existing workflows** | Use MCP Hub invoke (see below) |
| **Create new workflow** | Use create_workflow tool |
| **Edit workflow JSON** | Edit in n8n-workflows/ and deploy |
| **Deploy from repo** | Use import script |

## Quick Commands

```bash
# ═══════════════════════════════════════════════════════════════════
# WORKFLOW LOCATION
# ═══════════════════════════════════════════════════════════════════
# Workflows stored in: n8n-workflows/

# ═══════════════════════════════════════════════════════════════════
# DEPLOY WORKFLOW (GitOps)
# ═══════════════════════════════════════════════════════════════════

# Set your n8n URL and API key
export N8N_BASE_URL="https://your-n8n-instance.com"
export N8N_API_KEY="your-api-key"

# Deploy workflow
./scripts/import-n8n-workflow.sh n8n-workflows/my-workflow.json

# ═══════════════════════════════════════════════════════════════════
# MCP HUB OPERATIONS (runtime)
# ═══════════════════════════════════════════════════════════════════

# List workflows
mcp__hub__invoke({ service: 'n8n', method: 'GET', path: 'workflows' })

# Trigger workflow
mcp__hub__invoke({ service: 'n8n', method: 'POST', path: 'workflows/{id}/trigger', body: { payload: {...} } })

# Activate workflow
mcp__hub__invoke({ service: 'n8n', method: 'POST', path: 'workflows/{id}/activate' })
```

## Scope

| Capability | Covered |
|------------|---------|
| MCP Hub Operations (CRUD, Control) | ✅ |
| Direct n8n API Access (workaround) | ✅ |
| GitOps Flow (Repo → Deploy) | ✅ |
| Workflow Development | ✅ |

---

## Architecture

```
Claude → MCP Hub → n8n API
              │
              └── /n8n/workflows/*
                  /n8n/variables/*
```

## Available Operations

### Workflow CRUD

| Operation | Method | Path | Description |
|-----------|--------|------|-------------|
| List | GET | `/n8n/workflows` | Get all workflows |
| Get | GET | `/n8n/workflows/:id` | Get single workflow |
| Create | POST | `/n8n/workflows` | Create new workflow |
| Update | PATCH | `/n8n/workflows/:id` | Update workflow (merge) |
| Delete | DELETE | `/n8n/workflows/:id` | Delete workflow |

### Workflow Control

| Operation | Method | Path | Description |
|-----------|--------|------|-------------|
| Activate | POST | `/n8n/workflows/:id/activate` | Activate workflow |
| Deactivate | POST | `/n8n/workflows/:id/deactivate` | Deactivate workflow |
| Execute | POST | `/n8n/workflows/:id/execute` | Execute workflow immediately |
| Trigger | POST | `/n8n/workflows/:id/trigger` | Trigger via webhook |
| Get Webhook URL | GET | `/n8n/workflows/:id/webhook-url` | Get webhook URLs |

### Variables

| Operation | Method | Path | Description |
|-----------|--------|------|-------------|
| List | GET | `/n8n/variables` | List all variables |
| Set | POST | `/n8n/variables` | Create/update variable |

## MCP Hub Invocation

### Via invoke Tool

```javascript
// List all workflows
mcp__hub__invoke({
  service: 'n8n',
  method: 'GET',
  path: 'workflows'
})

// Get specific workflow
mcp__hub__invoke({
  service: 'n8n',
  method: 'GET',
  path: 'workflows/abc123'
})

// Activate workflow
mcp__hub__invoke({
  service: 'n8n',
  method: 'POST',
  path: 'workflows/abc123/activate'
})

// Execute workflow with data
mcp__hub__invoke({
  service: 'n8n',
  method: 'POST',
  path: 'workflows/abc123/execute',
  body: {
    data: { key: 'value' }
  }
})

// Trigger via webhook
mcp__hub__invoke({
  service: 'n8n',
  method: 'POST',
  path: 'workflows/abc123/trigger',
  body: {
    payload: { message: 'Hello from Claude' }
  }
})
```

## Direct API Fallback

For operations requiring full workflow JSON, use n8n API directly:

### 1. Set API Key

```bash
# From environment or 1Password
N8N_API_KEY="your-api-key-here"
```

### 2. Direct API Calls

```bash
# Get full workflow with all nodes
curl -s "${N8N_BASE_URL}/api/v1/workflows/{id}" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" | jq

# List all workflows with full details
curl -s "${N8N_BASE_URL}/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" | jq

# Get workflow executions
curl -s "${N8N_BASE_URL}/api/v1/executions?workflowId={id}" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" | jq
```

## Examples

### 1. List Active Workflows

```javascript
const result = await mcp__hub__invoke({
  service: 'n8n',
  method: 'GET',
  path: 'workflows'
});

// Filter active
const active = result.data.filter(w => w.active);
console.log(`${active.length} active workflows`);
```

### 2. Create Simple Webhook Workflow

```javascript
const workflow = {
  name: 'Test Webhook Handler',
  nodes: [
    {
      parameters: {
        httpMethod: 'POST',
        path: 'test-webhook'
      },
      name: 'Webhook',
      type: 'n8n-nodes-base.webhook',
      typeVersion: 1,
      position: [250, 300]
    },
    {
      parameters: {},
      name: 'Respond to Webhook',
      type: 'n8n-nodes-base.respondToWebhook',
      typeVersion: 1,
      position: [450, 300]
    }
  ],
  connections: {
    'Webhook': {
      main: [[{ node: 'Respond to Webhook', type: 'main', index: 0 }]]
    }
  },
  settings: {
    executionOrder: 'v1'
  }
};

await mcp__hub__invoke({
  service: 'n8n',
  method: 'POST',
  path: 'workflows',
  body: workflow
});
```

### 3. Update Workflow Settings

```javascript
// PATCH merges with existing workflow
await mcp__hub__invoke({
  service: 'n8n',
  method: 'PATCH',
  path: 'workflows/abc123',
  body: {
    settings: {
      errorWorkflow: 'error-handler-workflow-id',
      timezone: 'Europe/Berlin'
    }
  }
});
```

### 4. Get Webhook URLs

```javascript
const urls = await mcp__hub__invoke({
  service: 'n8n',
  method: 'GET',
  path: 'workflows/abc123/webhook-url'
});

// Returns:
// {
//   production: 'https://your-n8n.com/webhook/...',
//   test: 'https://your-n8n.com/webhook-test/...'
// }
```

## Workflow Node Types

### Native Node Preference

**ALWAYS prefer native n8n nodes over HTTP Request where available.** Native nodes provide:
- Built-in authentication handling
- Better error messages
- Automatic retries
- Type-safe parameters

**Common Native Nodes:**

| Service | Native Node | Type |
|---------|-------------|------|
| Notion | Yes | `n8n-nodes-base.notion` |
| Slack | Yes | `n8n-nodes-base.slack` |
| GitHub | Yes | `n8n-nodes-base.github` |
| Jina AI | Yes | `n8n-nodes-base.jinaAi` |

### Common Node Types

| Type | Purpose |
|------|---------|
| `n8n-nodes-base.webhook` | HTTP Webhook Trigger |
| `n8n-nodes-base.respondToWebhook` | Webhook Response |
| `n8n-nodes-base.httpRequest` | External API calls (fallback) |
| `n8n-nodes-base.code` | JavaScript/Python Code |
| `n8n-nodes-base.if` | Conditional branching |
| `n8n-nodes-base.set` | Set/transform data |
| `n8n-nodes-base.slack` | Slack integration |
| `n8n-nodes-base.notion` | Notion integration |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid/missing API key | Check N8N_API_KEY |
| 404 Not Found | Invalid workflow ID | Verify ID via list operation |
| 409 Conflict | Workflow name exists | Use unique name |
| 500 Server Error | n8n API error | Check n8n logs |

## Best Practices

1. **Workflow Naming**: Use descriptive names with prefix (e.g., `MyApp-Webhook-Handler`)
2. **Error Workflows**: Configure `errorWorkflow` in settings
3. **Webhooks**: Use unique paths, prefer production over test URLs
4. **Variables**: Store secrets in n8n Variables, not in workflow JSON
5. **Activation**: Test with `execute` before `activate`

## Workflow GitOps (Repo → n8n)

**Workflows managed in repo and deployed to n8n.**

### Development Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  1. EDIT                                                        │
│  ────────────────────────────────────────────────────────────── │
│  Edit workflow JSON in repo:                                    │
│  - New: Create `n8n-workflows/{workflow-name}.json`             │
│  - Existing: Edit JSON directly or export from n8n UI           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. COMMIT                                                      │
│  ────────────────────────────────────────────────────────────── │
│  git add n8n-workflows/my-workflow.json                         │
│  git commit -m "feat(n8n): Add my-workflow"                     │
│  git push origin main                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. DEPLOY                                                      │
│  ────────────────────────────────────────────────────────────── │
│  Option A: Via Script                                           │
│  ./scripts/import-n8n-workflow.sh n8n-workflows/my-workflow.json│
│                                                                 │
│  Option B: Via MCP Hub                                          │
│  mcp__hub__invoke({                                             │
│    service: 'n8n', method: 'POST', path: 'workflows',           │
│    body: <workflow-json>                                        │
│  })                                                             │
│                                                                 │
│  Option C: Via n8n UI                                           │
│  Import JSON in n8n Editor → Settings → Import from File        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. ACTIVATE & TEST                                             │
│  ────────────────────────────────────────────────────────────── │
│  - Test with webhook-test URL first                             │
│  - Activate via API or UI                                       │
│  - Verify with production webhook                               │
└─────────────────────────────────────────────────────────────────┘
```

### Import Script

```bash
#!/bin/bash
# scripts/import-n8n-workflow.sh

WORKFLOW_FILE=$1
N8N_API_KEY=${N8N_API_KEY:-"your-api-key"}
N8N_BASE_URL=${N8N_BASE_URL:-"https://your-n8n.com"}

# Check if workflow exists (by name)
WORKFLOW_NAME=$(jq -r '.name' "$WORKFLOW_FILE")
EXISTING_ID=$(curl -s "${N8N_BASE_URL}/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" | \
  jq -r ".data[] | select(.name==\"$WORKFLOW_NAME\") | .id")

if [ -n "$EXISTING_ID" ]; then
  echo "Updating existing workflow: $EXISTING_ID"
  curl -X PATCH "${N8N_BASE_URL}/api/v1/workflows/$EXISTING_ID" \
    -H "X-N8N-API-KEY: $N8N_API_KEY" \
    -H "Content-Type: application/json" \
    -d @"$WORKFLOW_FILE"
else
  echo "Creating new workflow: $WORKFLOW_NAME"
  curl -X POST "${N8N_BASE_URL}/api/v1/workflows" \
    -H "X-N8N-API-KEY: $N8N_API_KEY" \
    -H "Content-Type: application/json" \
    -d @"$WORKFLOW_FILE"
fi
```

## Debugging

```bash
# Check n8n health
curl ${N8N_BASE_URL}/healthz

# Test webhook directly
curl -X POST ${N8N_BASE_URL}/webhook-test/path \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `notion-spec` | Tasks können n8n Workflows triggern |
| `notion-issue` | Issue-Erstellung kann Notification Workflow triggern |
