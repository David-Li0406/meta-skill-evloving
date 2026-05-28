# n8n Workflow JSON Structure

## Complete Schema Overview

```json
{
  "name": "Workflow Name",
  "nodes": [...],
  "connections": {...},
  "pinData": {},
  "active": false,
  "settings": {
    "executionOrder": "v1"
  },
  "versionId": "uuid",
  "meta": {
    "templateCredsSetupCompleted": true,
    "instanceId": "instance-uuid"
  },
  "id": "workflow-id",
  "tags": [...]
}
```

---

## Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✓ | Workflow display name |
| `nodes` | array | ✓ | Array of node objects |
| `connections` | object | ✓ | Node connection mapping |
| `active` | boolean | | Enable automatic execution |
| `settings` | object | | Workflow settings |
| `pinData` | object | | Pinned test data |
| `id` | string | | Workflow ID (auto-generated) |
| `versionId` | string | | Version UUID |
| `meta` | object | | Metadata |
| `tags` | array | | Tag objects |

---

## Node Object

```json
{
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "position": [400, 200],
  "id": "unique-uuid-here",
  "name": "Descriptive Name",
  "parameters": { ... },
  "credentials": { ... },
  "webhookId": "...",
  "notes": "Node description",
  "notesInFlow": true,
  "disabled": false,
  "alwaysOutputData": true,
  "onError": "continueRegularOutput",
  "retryOnFail": true,
  "maxTries": 3
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Node type identifier |
| `typeVersion` | number | Node version |
| `position` | [x, y] | Canvas coordinates |
| `id` | string | Unique identifier |
| `name` | string | Display name (must be unique) |
| `parameters` | object | Node-specific configuration |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `credentials` | object | Referenced credentials |
| `webhookId` | string | For webhook nodes |
| `disabled` | boolean | Skip node execution |
| `notes` | string | Documentation text |
| `notesInFlow` | boolean | Show notes on canvas |
| `alwaysOutputData` | boolean | Output even if empty |
| `onError` | string | Error handling mode |
| `retryOnFail` | boolean | Retry on failure |
| `maxTries` | number | Max retry attempts |

### Error Handling Options

```json
"onError": "stopWorkflow"          // Default: halt execution
"onError": "continueRegularOutput" // Continue with empty output
"onError": "continueErrorOutput"   // Route to error output (index 1)
```

---

## Node Types

### Built-in Nodes
```
n8n-nodes-base.<nodeName>
```
Examples:
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.code`
- `n8n-nodes-base.if`
- `n8n-nodes-base.set`
- `n8n-nodes-base.merge`

### LangChain/AI Nodes
```
@n8n/n8n-nodes-langchain.<nodeName>
```
Examples:
- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatOpenRouter`
- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.toolCode`

---

## Connections Object

### Basic Connection
```json
"connections": {
  "Source Node Name": {
    "main": [
      [
        { "node": "Target Node Name", "type": "main", "index": 0 }
      ]
    ]
  }
}
```

### Multiple Outputs (IF/Switch)
```json
"IF Node": {
  "main": [
    [{ "node": "True Branch", "type": "main", "index": 0 }],
    [{ "node": "False Branch", "type": "main", "index": 0 }]
  ]
}
```

### Multiple Targets from Same Output
```json
"Trigger": {
  "main": [
    [
      { "node": "Path A", "type": "main", "index": 0 },
      { "node": "Path B", "type": "main", "index": 0 }
    ]
  ]
}
```

### AI Node Connections
```json
"AI Model": {
  "ai_languageModel": [
    [{ "node": "LLM Chain", "type": "ai_languageModel", "index": 0 }]
  ]
}
```

**AI Connection Types:**
- `ai_languageModel` - Language model connection
- `ai_memory` - Memory/context connection
- `ai_tool` - Tool for agents
- `ai_outputParser` - Output parser
- `ai_retriever` - RAG retriever
- `ai_document` - Document loader
- `ai_textSplitter` - Text splitter
- `ai_embedding` - Embedding model

---

## Credentials Reference

```json
"credentials": {
  "credentialType": {
    "id": "credential-uuid",
    "name": "Credential Display Name"
  }
}
```

Common credential types:
- `supabaseApi`
- `openRouterApi`
- `slackApi`
- `gmailOAuth2`
- `httpHeaderAuth`
- `httpBasicAuth`

---

## Settings Object

```json
"settings": {
  "executionOrder": "v1",
  "saveManualExecutions": true,
  "callerPolicy": "any",
  "errorWorkflow": "error-workflow-id",
  "timezone": "America/New_York"
}
```

---

## Tags

```json
"tags": [
  {
    "id": "tag-uuid",
    "name": "Production",
    "createdAt": "2024-01-01T00:00:00.000Z",
    "updatedAt": "2024-01-01T00:00:00.000Z"
  }
]
```

---

## Position Guidelines

Nodes are positioned using `[x, y]` coordinates:

- Start at `[0, 0]` for trigger
- Horizontal spacing: ~220px
- Vertical spacing: ~160px (for parallel branches)
- Grid alignment recommended

```
[0, 0]    → [220, 0]   → [440, 0]
                       ↘ [440, 160] (branch)
```

---

## Minimal Valid Workflow

```json
{
  "name": "Minimal Workflow",
  "nodes": [
    {
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [0, 0],
      "id": "1",
      "name": "Start",
      "parameters": {}
    }
  ],
  "connections": {},
  "active": false,
  "settings": { "executionOrder": "v1" }
}
```
