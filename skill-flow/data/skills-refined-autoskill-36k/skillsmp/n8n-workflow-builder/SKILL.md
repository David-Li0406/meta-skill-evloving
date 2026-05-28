---
name: n8n-workflow-builder
description: n8n v2.0 workflow design patterns and best practices. Use when building new workflows, debugging IF/Merge issues, fixing execution order problems, or modernizing legacy workflows. Covers conditional logic, parallel execution, error handling, and v2.0 breaking changes. Complementary to n8n-ops (operations/deployment).
---

# n8n Workflow Builder

Design patterns and best practices for n8n v2.0.

**For operations** (CRUD, deploy, trigger) see `n8n-ops` skill.

## Quick Diagnostic

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| IF node fires both outputs | v0 execution order | Set `executionOrder: 'v1'` |
| Merge doesn't wait | Wrong mode or inputs | Use Append + correct `numberInputs` |
| Code node can't read ENV | v2.0 default blocks it | Use credentials or `$env` |
| Workflow saves but not live | v2.0 Save ≠ Publish | Click Publish after Save |

## Execution Order (Critical)

**The #1 cause of mysterious workflow bugs.**

### Check Current Setting

```javascript
// In workflow JSON:
{
  "settings": {
    "executionOrder": "v0"  // ❌ Legacy - causes IF+Merge bug
    // or missing entirely    // ❌ Defaults to v0 for old workflows
  }
}
```

### Fix

```javascript
{
  "settings": {
    "executionOrder": "v1"  // ✅ Required for correct behavior
  }
}
```

**UI:** Workflow Settings → Execution Order → "v1 (recommended)"

### Why This Matters

| v0 (Legacy) | v1 (Modern) |
|-------------|-------------|
| Breadth-first: all first nodes, then all second | Depth-first: complete each branch |
| IF + Merge bug: both outputs fire | Only triggered output fires |
| Default for workflows created before n8n 1.0 | Default for new workflows |

## Conditional Logic

### IF Node (2 outputs)

```javascript
{
  "name": "Check Status",
  "type": "n8n-nodes-base.if",
  "typeVersion": 2,
  "parameters": {
    "conditions": {
      "conditions": [{
        "leftValue": "={{ $json.status }}",
        "rightValue": "active",
        "operator": { "type": "string", "operation": "equals" }
      }],
      "combinator": "and"
    }
  }
}
// Output 0 = TRUE, Output 1 = FALSE
```

### Switch Node (n outputs)

For more than 2 routing options:

```javascript
{
  "name": "Route by Type",
  "type": "n8n-nodes-base.switch",
  "typeVersion": 3,
  "parameters": {
    "mode": "rules",
    "rules": {
      "rules": [
        { "conditions": { "conditions": [{ "leftValue": "={{ $json.type }}", "rightValue": "order" }]}},
        { "conditions": { "conditions": [{ "leftValue": "={{ $json.type }}", "rightValue": "refund" }]}},
        { "conditions": { "conditions": [{ "leftValue": "={{ $json.type }}", "rightValue": "inquiry" }]}}
      ]
    }
  }
}
```

## Merging Patterns

### Append Mode (Wait for All)

```javascript
{
  "name": "Merge Results",
  "type": "n8n-nodes-base.merge",
  "typeVersion": 3,
  "parameters": {
    "mode": "append",
    "numberInputs": 3  // Must match connected inputs!
  }
}
```

### Combine Mode (Join)

```javascript
{
  "parameters": {
    "mode": "combine",
    "combineBy": "combineByFields",
    "fields": ["id"],
    "joinMode": "enrichInput1"  // Left join
  }
}
```

## Parallel Execution

### Pattern: Split Branches

```
Trigger ──┬── API 1 ──┐
          ├── API 2 ──┼── Merge (Append, numberInputs: 3)
          └── API 3 ──┘
```

Branches from same node run in parallel.

## Error Handling

### Node-Level

```javascript
{
  "name": "API Call",
  "onError": "continueRegularOutput",  // Don't stop workflow
  "parameters": { ... }
}
// Options: stopWorkflow, continueRegularOutput, continueErrorOutput
```

### Error Workflow

```javascript
{ "settings": { "errorWorkflow": "error-handler-id" } }
```

## n8n v2.0 Changes

### Code Node ENV Blocked

```javascript
// ❌ Blocked by default in v2.0
process.env.API_KEY  // undefined

// ✅ Use $env instead
$env.API_KEY

// ✅ Or use credential nodes
```
#### credential nodes are preferred, ask user before falling back to env for credentials!

### Save vs Publish

```
v1.x: Save = immediately live
v2.0: Save = saved locally, Publish = live
```

### Removed: Start Node

```javascript
// ❌ Removed
{ "type": "n8n-nodes-base.start" }

// ✅ Use instead
{ "type": "n8n-nodes-base.manualTrigger" }
{ "type": "n8n-nodes-base.executeWorkflowTrigger" }
```

## Node Types Reference

### Native Nodes (Always Prefer)

| Service | Type | Credential |
|---------|------|------------|
| Notion | `n8n-nodes-base.notion` | `notionApi` |
| Slack | `n8n-nodes-base.slack` | `slackApi` |
| GitHub | `n8n-nodes-base.github` | `githubApi` |

### Core Nodes

| Type | Purpose |
|------|---------|
| `n8n-nodes-base.webhook` | HTTP trigger |
| `n8n-nodes-base.respondToWebhook` | HTTP response |
| `n8n-nodes-base.code` | JS/Python |
| `n8n-nodes-base.if` | 2-way conditional |
| `n8n-nodes-base.switch` | N-way conditional |
| `n8n-nodes-base.merge` | Combine branches |
| `n8n-nodes-base.httpRequest` | Generic API (fallback) |

## Minimal Workflow Template

```javascript
{
  "name": "My Workflow",
  "nodes": [
    { "id": "1", "name": "Webhook", "type": "n8n-nodes-base.webhook",
      "typeVersion": 2, "position": [250, 300],
      "parameters": { "httpMethod": "POST", "path": "my-path", "responseMode": "responseNode" }},
    { "id": "2", "name": "Respond", "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1, "position": [450, 300],
      "parameters": { "respondWith": "json", "responseBody": "={{ $json }}" }}
  ],
  "connections": { "Webhook": { "main": [[{ "node": "Respond", "type": "main", "index": 0 }]] }},
  "settings": { "executionOrder": "v1" }
}
```

## Delegation

| Task | Skill |
|------|-------|
| Deploy/trigger workflow | `n8n-ops` |
| Document workflow | `notion-capture` |
