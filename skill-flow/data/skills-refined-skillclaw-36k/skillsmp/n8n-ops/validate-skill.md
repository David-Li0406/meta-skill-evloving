# n8n-ops Skill Validation

## Quick Validation Steps

### 1. List Workflows (READ)

```javascript
// Using MCP Hub tool
n8n_list_workflows({})
```

**Expected:** Array of workflow objects with `id`, `name`, `active` fields.

### 2. Create Test Workflow (CREATE)

```javascript
// Load test-workflow.json content
n8n_create_workflow({
  workflow: /* contents of test-workflow.json */
})
```

**Expected:** Created workflow with assigned `id`.

### 3. Get Workflow Details (READ)

```javascript
n8n_get_workflow({
  workflowId: "{id}"
})
```

**Expected:** Full workflow object with nodes, connections, settings.

### 4. Execute Workflow (EXECUTE)

```javascript
n8n_execute_workflow({
  workflowId: "{id}",
  payload: { test: true, message: "Skill validation" }
})
```

**Expected:** Response with `success: true` and echoed payload.

## Full Test Run

Run all steps in sequence. Capture workflow ID from step 2 for subsequent steps.

### Success Criteria

- [ ] List workflows returns array
- [ ] Create workflow returns ID
- [ ] Get workflow returns full details
- [ ] Execute returns expected response

## Troubleshooting

| Issue | Check |
|-------|-------|
| 401 errors | JWT token valid? n8n credentials configured? |
| 404 on workflow | ID correct? Workflow exists? |
| Execute fails | Workflow activated? Webhook node present? |
| Empty list | n8n running? N8N_* env vars set? |
| Connection refused | n8n service reachable from Hub? |
