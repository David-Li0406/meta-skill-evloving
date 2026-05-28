---
name: shipbox-sandbox
description: Develop code using Shipbox sandboxes with real Cloudflare containers. Use when the user wants to run code in a sandbox, test in isolation, or deploy workers.
---

# Shipbox Sandbox Development

This skill enables development using Shipbox sandboxes - isolated Cloudflare containers running the OpenCode agent.

## Available MCP Tools

When this skill is active, you have access to these tools via the `shipbox-sandbox` MCP server:

### opencode_run_task
Execute a coding task in a sandbox.

**Parameters:**
- `task` (required): The coding task to execute
- `sessionId` (optional): Continue an existing session
- `repository` (optional): Git repository URL to clone
- `branch` (optional): Branch name (default: main)
- `model` (optional): Claude model to use
- `title` (optional): Task title

**Returns:**
- `runId`: Use to poll for results
- `sessionId`: Use to continue this session
- `webUiUrl`: Share with user for real-time progress

### opencode_get_result
Get status and result of a task run.

**Parameters:**
- `runId` (required): The run ID from opencode_run_task

**Returns:**
- `status`: started | running | completed | failed
- `result`: Final output when completed

### opencode_list_runs
List past task runs.

**Parameters:**
- `sessionId` (optional): Filter by session
- `status` (optional): Filter by status
- `limit` (optional): Max results (default 10)
- `before` (optional): Pagination cursor

### opencode_preview_worker
Start a miniflare development server.

**Parameters:**
- `sessionId` (required): Active session ID
- `workerPath` (optional): Path to worker entry point
- `port` (optional): Port number (default 8787)

**Returns:**
- `previewUrl`: URL to test the worker

### opencode_deploy_worker
Deploy a worker to production.

**Parameters:**
- `sessionId` (required): Active session ID
- `workerPath` (optional): Path to worker entry point
- `name` (optional): Worker name

**Returns:**
- `url`: Production URL

## Workflow

1. **Start a task**: Use `opencode_run_task` with your task description
2. **Monitor progress**: Share the `webUiUrl` and poll `opencode_get_result`
3. **Continue work**: Use the same `sessionId` for follow-up tasks
4. **Preview**: Use `opencode_preview_worker` to test workers
5. **Deploy**: Use `opencode_deploy_worker` for production

## Example Session

```
User: Create a simple Cloudflare Worker that returns "Hello World"

1. Call opencode_run_task with task="Create a Cloudflare Worker that returns Hello World on all requests"
2. Share the webUiUrl with the user
3. Poll opencode_get_result until completed
4. Call opencode_preview_worker to start local preview
5. Share the previewUrl for testing
6. When ready, call opencode_deploy_worker
```

## Tips

- Always share the `webUiUrl` so users can watch agent progress in real-time
- Poll every 10-30 seconds for task completion
- Reuse `sessionId` for related tasks to maintain workspace state
- The sandbox persists files between tasks in the same session
