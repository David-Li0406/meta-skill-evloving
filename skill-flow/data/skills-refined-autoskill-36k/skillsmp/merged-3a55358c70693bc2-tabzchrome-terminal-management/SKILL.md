---
name: tabzchrome-terminal-management
description: Use this skill when spawning and managing terminal tabs, creating workers, or setting up worktrees for parallel tasks via the TabzChrome REST API.
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

| Field      | Type   | Default               | Description                     |
|------------|--------|-----------------------|---------------------------------|
| `name`     | string | "Claude Terminal"     | Tab display name                |
| `workingDir` | string | `$HOME`             | Starting directory              |
| `command`  | string | -                     | Command to run after spawn      |
| `profileId`| string | default               | Profile for appearance          |

## Parallel Workers with Worktrees

```bash
# Create isolated worktree
bd worktree create <feature_branch>

# Spawn worker there with BEADS_WORKING_DIR for MCP tools
PROJECT_DIR=$(pwd)
curl -X POST http://localhost:8129/api/spawn \
  -H "Content-Type: application/json" \
  -H "X-Auth-Token: $TOKEN" \
  -d "{\"name\": \"<feature_worker_name>\", \"workingDir\": \"../<feature_branch>\", \"command\": \"BEADS_WORKING_DIR=$PROJECT_DIR <command_to_run>\"}"
```

**Key:** `BEADS_WORKING_DIR` tells the beads MCP server where to find the database. Point it to the main repo, not the worktree.

## Worker Management

### List Workers

```bash
curl -s http://localhost:8129/api/agents | jq '.data[]'
```

### Find Worker by Name

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

## Worker Prompts

Keep prompts simple - workers are vanilla Claude:

```
<your_task_description>
Run tests when done: npm test
Close the issue: bd close <issue_id> --reason="done"
```

Avoid prescriptive step-by-step pipelines. Let Claude work naturally.

## Git Worktrees

Worktrees enable parallel workers on the same repo.

```bash
# REQUIRED for beads projects - creates .beads/redirect for MCP tools
bd worktree create .worktrees/<issue_id> --branch feature/<issue_id>

# Remove
git worktree remove ".worktrees/<issue_id>" --force
git branch -d "feature/<issue_id>"
```

**Critical:** Always use `bd worktree create` for beads projects. It creates `.beads/redirect` which points MCP tools to the main database.

### Dependency Initialization

Worktrees share git but NOT node_modules. Initialize before spawning:

```bash
INIT_SCRIPT=$(find ~/plugins ~/.claude/plugins ~/projects/TabzChrome/plugins -name "init-worktree.sh" -path "*spawner*" 2>/dev/null | head -1)
$INIT_SCRIPT ".worktrees/<issue_id>"
```

| Detected            | Action                          |
|---------------------|---------------------------------|
| package.json        | npm ci / pnpm / yarn / bun     |
| pyproject.toml      | uv pip install -e .            |
| requirements.txt    | uv pip install -r               |
| Cargo.toml          | cargo fetch                     |
| go.mod              | go mod download                 |

## Dashboard

Monitor workers with tmuxplexer:

```bash
curl -s -X POST http://localhost:8129/api/spawn \
  -H "Content-Type: application/json" \
  -H "X-Auth-Token: $TOKEN" \
  -d '{
    "name": "Worker Dashboard",
    "workingDir": "<dashboard_working_directory>",
    "command": "./tmuxplexer --watcher"
  }'
```

Shows: status, context usage, working directory, git branch.

## References

- `spawn-api.md` - Full API reference
- `worktree-setup.md` - Git worktree patterns
- `worker-prompts.md` - Prompt crafting guidelines
- `handoff-format.md` - Worker handoff notes
- `model-routing.md` - Model selection