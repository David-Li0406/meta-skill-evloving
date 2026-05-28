---
name: tabz-terminal-management
description: Use this skill when you need to spawn and manage terminal tabs via the TabzChrome REST API for orchestrating parallel Claude sessions and managing workers.
---

# TabzChrome Terminal Management

Spawn terminals, manage workers, and orchestrate parallel Claude sessions.

## Spawn API

```bash
TOKEN=$(cat /tmp/tabz-auth-token)
curl -X POST http://localhost:8129/api/spawn \
  -H "Content-Type: application/json" \
  -H "X-Auth-Token: $TOKEN" \
  -d '{"name": "<worker_name>", "workingDir": "<working_directory>", "command": "<command_to_run>"}'
```

**Response:**
```json
{
  "success": true,
  "terminalId": "<terminal_id>",
  "tmuxSession": "<tmux_session>"
}
```

## Spawn Options

| Field      | Type   | Default               | Description                |
|------------|--------|-----------------------|----------------------------|
| `name`     | string | "Claude Terminal"     | Tab display name           |
| `workingDir` | string | `$HOME`             | Starting directory         |
| `command`  | string | -                     | Command to run after spawn |
| `profileId`| string | default               | Profile for appearance     |

## Parallel Workers with Worktrees

```bash
# Create isolated worktree (bd handles beads redirect automatically)
bd worktree create <feature_branch>

# Spawn worker there with BEADS_WORKING_DIR for MCP tools
PROJECT_DIR=$(pwd)
curl -X POST http://localhost:8129/api/spawn \
  -H "Content-Type: application/json" \
  -H "X-Auth-Token: $TOKEN" \
  -d "{\"name\": \"<feature_worker_name>\", \"workingDir\": \"../<feature_branch>\", \"command\": \"BEADS_WORKING_DIR=$PROJECT_DIR <command_to_run>\"}"
```

**Key:** `BEADS_WORKING_DIR` tells the beads MCP server where to find the database. Point it to the main repo, not the worktree.

## Worker Prompts

Keep prompts simple - workers are vanilla Claude:

```
<your_prompt_here>
```

Avoid prescriptive step-by-step pipelines. Let Claude work naturally.

## Worker Management

### List Workers

```bash
curl -s http://localhost:8129/api/agents | jq '.data[]'
```

### Find by Name

```bash
curl -s http://localhost:8129/api/agents | jq -r '.data[] | select(.name == "<worker_name>")'
```

### Get Session ID

```bash
SESSION=$(curl -s http://localhost:8129/api/agents | jq -r '.data[] | select(.name == "<worker_name>") | .id')
```

### Kill Worker

```bash
curl -s -X DELETE "http://localhost:8129/api/agents/$SESSION" \
  -H "X-Auth-Token: $TOKEN"
```

### Send Prompt via tmux

```bash
tmux send-keys -t "$SESSION" -l "<your_prompt_here>"
sleep 0.5
tmux send-keys -t "$SESSION" Enter
```

## References

See `references/` for details:
- `spawn-api.md` - Full API reference
- `worktree-setup.md` - Git worktree patterns
- `worker-prompts.md` - Prompt crafting guidelines