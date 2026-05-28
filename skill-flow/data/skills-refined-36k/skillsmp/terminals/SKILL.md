---
name: terminals
description: |
  TabzChrome terminal spawning and worker management patterns.
  Use when spawning workers, managing terminals, or setting up worktrees.
  Trigger with "spawn worker", "create terminal", "worktree setup".
model: haiku
allowed-tools: Bash, Read, mcp__tabz__*
---

# Terminals - Worker Spawning

Spawn and manage Claude workers via TabzChrome API.

## MCP Tools (Preferred)

| Tool | Purpose |
|------|---------|
| `tabz_spawn_profile` | Spawn using saved profile |
| `tabz_list_profiles` | List available profiles |
| `tabz_list_categories` | List profile categories |

```python
# Spawn worker with profile
tabz_spawn_profile(
    profileId="claude-worker",
    workingDir="~/projects/.worktrees/ISSUE-ID",
    name="ISSUE-ID"
)
```

## REST API

### Spawn Terminal

```bash
TOKEN=$(cat /tmp/tabz-auth-token)
PROJECT_DIR="/home/user/projects/myapp"  # Main repo path
curl -X POST http://localhost:8129/api/spawn \
  -H "Content-Type: application/json" \
  -H "X-Auth-Token: $TOKEN" \
  -d "{
    \"name\": \"ISSUE-ID\",
    \"workingDir\": \"$PROJECT_DIR/.worktrees/ISSUE-ID\",
    \"command\": \"BEADS_WORKING_DIR=$PROJECT_DIR claude\"
  }"
```

### Find Worker

```bash
# By name
curl -s http://localhost:8129/api/agents | jq -r '.data[] | select(.name == "ISSUE-ID")'

# Get session ID
SESSION=$(curl -s http://localhost:8129/api/agents | jq -r '.data[] | select(.name == "ISSUE-ID") | .id')
```

### Kill Worker

```bash
curl -s -X DELETE "http://localhost:8129/api/agents/$SESSION" \
  -H "X-Auth-Token: $TOKEN"
```

## Git Worktrees

Worktrees enable parallel workers on same repo.

```bash
# REQUIRED for beads projects - creates .beads/redirect for MCP tools
bd worktree create .worktrees/ISSUE-ID --branch feature/ISSUE-ID

# Remove
git worktree remove ".worktrees/ISSUE-ID" --force
git branch -d "feature/ISSUE-ID"
```

**Critical:** Always use `bd worktree create` for beads projects. It creates `.beads/redirect` which points MCP tools to the main database. Without this file, MCP tools fail silently and workers must use CLI only.

Fallback (non-beads projects only):
```bash
git worktree add ".worktrees/ISSUE-ID" -b "feature/ISSUE-ID"
```

### Dependency Initialization

Worktrees share git but NOT node_modules. Initialize before spawning:

```bash
INIT_SCRIPT=$(find ~/plugins ~/.claude/plugins ~/projects/TabzChrome/plugins -name "init-worktree.sh" -path "*spawner*" 2>/dev/null | head -1)
$INIT_SCRIPT ".worktrees/ISSUE-ID"
```

| Detected | Action |
|----------|--------|
| package.json | npm ci / pnpm / yarn / bun |
| pyproject.toml | uv pip install -e . |
| requirements.txt | uv pip install -r |
| Cargo.toml | cargo fetch |
| go.mod | go mod download |

## Sending Prompts

Wait for Claude to boot (8+ seconds), then use the `tabz_send_keys` MCP tool:

```python
tabz_send_keys(
    terminal="BD-xyz",  # Terminal name or ID
    text="Complete beads issue BD-xyz. Run: bd show BD-xyz --json",
    delay=600  # ms before Enter (increase for long prompts)
)
```

Or via mcp-cli:
```bash
mcp-cli call plugin_tabz_tabz/tabz_send_keys '{"terminal": "BD-xyz", "text": "Your prompt here", "delay": 600}'
```

## Worker Naming

**Use issue ID as terminal name:**
- Easy lookup via `/api/agents`
- Clear dashboard display
- Correlation: terminal = issue = branch = worktree

## Critical Settings

| Setting | Value | Why |
|---------|-------|-----|
| `BEADS_WORKING_DIR` | Main repo path | Beads MCP finds database |
| Wait time | 8+ seconds | Claude boot time |

## Dashboard

Monitor workers with tmuxplexer:

```bash
curl -s -X POST http://localhost:8129/api/spawn \
  -H "Content-Type: application/json" \
  -H "X-Auth-Token: $TOKEN" \
  -d '{
    "name": "Worker Dashboard",
    "workingDir": "~/projects/tmuxplexer",
    "command": "./tmuxplexer --watcher"
  }'
```

Shows: status, context usage, working directory, git branch.

## References

- [handoff-format.md](references/handoff-format.md) - Worker handoff notes
- [model-routing.md](references/model-routing.md) - Model selection
