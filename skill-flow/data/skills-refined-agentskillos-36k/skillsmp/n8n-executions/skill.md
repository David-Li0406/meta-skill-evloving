---
name: n8n-executions
description: Fetch and display recent n8n workflow execution logs from the Railways-hosted instance.
user_invocable: true
---

# n8n Execution Logs

Fetch recent execution logs from the n8n instance to debug workflows and monitor execution status.

## When to Use This Skill (vs MCP)

Two ways to interact with n8n programmatically:

| Task | Use |
|------|-----|
| Find a workflow | MCP: `search_workflows` |
| View workflow nodes | MCP: `get_workflow_details` |
| Run a workflow | MCP: `execute_workflow` |
| Debug an execution | **This skill** or API: `GET /executions/{id}?includeData=true` |
| List recent failures | **This skill** with `status=error` |
| Retry a failed run | API: `POST /executions/{id}/retry` |

**MCP tools** have built-in authentication and work for workflow-level operations.
**REST API** (this skill) is required for execution data - MCP cannot fetch execution logs or outputs.

## Configuration

- **Environment file:** `.claude/n8n-api.env`
- **Variables:** `N8N_API_URL`, `N8N_API_KEY`

## Instructions

When this skill is invoked:

1. **Load environment variables** from `.claude/n8n-api.env`:
   ```bash
   source .claude/n8n-api.env
   ```

2. **Fetch executions** using curl:
   ```bash
   curl -s "$N8N_API_URL/api/v1/executions?limit=<LIMIT>" \
     -H "X-N8N-API-KEY: $N8N_API_KEY"
   ```

   Default limit is 3 unless the user specifies otherwise.

3. **Parse and display** the results in a readable format:

   For each execution, show:
   - **Execution ID**
   - **Workflow name** (fetch from workflow details if needed)
   - **Status** (success/error/running/waiting)
   - **Started at** (human-readable timestamp)
   - **Finished at** (if completed)
   - **Duration** (calculated)
   - **Error message** (if failed)
   - **Mode** (manual/trigger/webhook)

4. **Format output** as a table or structured list:

   ```
   ## Recent Executions

   | # | Workflow | Status | Started | Duration | Mode |
   |---|----------|--------|---------|----------|------|
   | 1 | workflow-name | Success | 2h ago | 1.2s | trigger |
   | 2 | workflow-name | Error | 5h ago | 0.3s | manual |
   ```

   For failed executions, include the error details below the table.

### Getting Execution Details by ID

To investigate a specific execution:

**Step 1: Identify the execution ID**
- In n8n UI: Executions sidebar shows IDs
- From workflow logs: Execution ID is logged on each run
- From error handler: Captures execution_id of failed runs

**Step 2: Fetch with full node data**
```bash
curl -s "$N8N_API_URL/api/v1/executions/<ID>?includeData=true" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
```

**Step 3: Understanding the response**

Basic fields:
```json
{
  "id": "36006",
  "finished": true,
  "mode": "manual",
  "status": "success",
  "workflowId": "S0hk9fjhB-itqaFkq9qnI",
  "startedAt": "2026-01-21T09:56:18.856Z",
  "stoppedAt": "2026-01-21T09:57:39.785Z"
}
```

With `?includeData=true`, the response includes `data.resultData.runData` containing each node's input/output.

## API Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/executions` | GET | List executions (with filters) |
| `/api/v1/executions/{id}` | GET | Get specific execution details |
| `/api/v1/executions/{id}/retry` | POST | Retry a failed execution |
| `/api/v1/workflows` | GET | List all workflows |
| `/api/v1/workflows/{id}` | GET | Get workflow details |
| `/api/v1/workflows/{id}/activate` | POST | Activate a workflow |
| `/api/v1/workflows/{id}/deactivate` | POST | Deactivate a workflow |

## Arguments

- `limit=N` - Number of executions to fetch (default: 3, max: 100)
- `workflow=ID` - Filter by specific workflow ID
- `status=success|error|waiting` - Filter by status

## Example Usage

```
/n8n-executions              # Last 3 executions
/n8n-executions limit=10     # Last 10 executions
/n8n-executions status=error # Recent failures only
```

## Error Handling

- If API returns 401: API key may be invalid or expired
- If API returns 404: Check the n8n instance URL
- If connection fails: Instance may be sleeping (Railways free tier) - retry in 30s
