---
name: tabz-terminals
description: Use this skill when you need to spawn and manage terminal tabs via the TabzChrome REST API, particularly for creating workers, setting up worktrees for parallel tasks, or crafting prompts for Claude workers.
---

# TabzChrome Terminal Management

Spawn terminals, manage workers, and orchestrate parallel Claude sessions.

## Spawn API

```bash
TOKEN=$(cat /tmp/tabz-auth-token)
curl -X POST http://localhost:8129/api/spawn \
  -H "Content-Type: application/json" \
  -H "X-Auth-Token: $TOKEN" \
  -d '{"name": "Worker", "workingDir": "~/projects", "command": "claude"}'
```

**Response:**
```json
{
  "success": true,
  "terminalId": "ctt-default-abc123",
  "tmuxSession": "ctt-default-abc123"
}
```

## Spawn Options

| Field      | Type   | Default            | Description                     |
|------------|--------|--------------------|---------------------------------|
| `name`     | string | "Claude Terminal"   | Tab display name                |
| `workingDir` | string | `$HOME`          | Starting directory              |
| `command`  | string | -                  | Command to run after spawn      |
| `profileId`| string | default            | Profile for appearance          |

## Parallel Workers with Worktrees

```bash
# Create isolated worktree (bd handles beads redirect automatically)
bd worktree create feature-branch

# Spawn worker there with BEADS_WORKING_DIR for MCP tools
PROJECT_DIR=$(pwd)
curl -X POST http://localhost:8129/api/spawn \
  -H "Content-Type: application/json" \
  -H "X-Auth-Token: $TOKEN" \
  -d "{\"name\": \"Feature Worker\", \"workingDir\": \"../feature-branch\", \"command\": \"BEADS_WORKING_DIR=$PROJECT_DIR claude\"}"
```

**Key:** `BEADS_WORKING_DIR` tells the beads MCP server where to find the database. Point it to the main repo, not the worktree.

## Worker Prompts

Keep prompts simple - workers are vanilla Claude:

```
Fix the pagination bug in useTerminalSessions.ts around line 200.
Run tests when done: npm test
Close the issue: bd close TabzChrome-abc --reason="done"
```

Avoid prescriptive step-by-step pipelines. Let Claude work naturally.

## Worker Management

### List Workers

```bash
curl -s http://localhost:8129/api/agents | jq '.data[]'
```

### Find by Name

```bash
curl -s http://localhost:8129/api/agents | jq -r '.data[] | select(.name == "V4V-ct9")'
```

### Get Session ID

```bash
SESSION=$(curl -s http://localhost:8129/api/agents | jq -r '.data[] | select(.name == "V4V-ct9") | .id')
```

### Kill Worker

```bash
curl -s -X DELETE "http://localhost:8129/api/agents/$SESSION" \
  -H "X-Auth-Token: $TOKEN"
```

### Send Prompt via tmux

```bash
# Example command to send a prompt to a tmux session
tmux send-keys -t ctt-default-abc123 "Your command here" C-m
```