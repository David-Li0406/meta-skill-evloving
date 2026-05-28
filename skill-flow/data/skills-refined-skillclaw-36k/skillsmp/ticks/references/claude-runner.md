# Claude Code Native Runner

Run Ticks epics using Claude Code's native Task tool for parallel subagent orchestration.

## When to Use This

- You're already in a Claude Code session
- Tasks are fairly independent and benefit from parallelization
- Epic doesn't require heavy human intervention mid-execution
- You want direct visibility into agent spawning

For rich monitoring, HITL workflows, or cost tracking, use `tk run` instead.

## Overview

```
1. Get MAX_AGENTS from user (1-10)
2. Run: tk graph <epic> --json
3. Parse waves from the graph
4. For each wave:
   a. Launch up to MAX_AGENTS Task agents in background
   b. Poll for completion (avoid blocking hangs)
   c. Sync results back to ticks
   d. Proceed to next wave
```

## Task Tool Reference

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | string | Full task instructions for the agent |
| `description` | string | Short (3-5 word) summary shown in UI |
| `subagent_type` | string | Use `"general-purpose"` for implementation |

### Key Optional Parameters

| Parameter | Type | Recommendation |
|-----------|------|----------------|
| `run_in_background` | boolean | `true` - enables parallel execution |
| `mode` | string | `"bypassPermissions"` for autonomous work |
| `model` | string | `"sonnet"` for most tasks, `"opus"` for complex |
| `name` | string | See naming conventions below |

## Naming Conventions

Use consistent naming for traceability.

### Available Identifiers

| Entity | ID | Title |
|--------|-----|-------|
| Epic | 3-letter (e.g., `x7k`) | e.g., "Authentication" |
| Tick | 3-letter (e.g., `abc`) | e.g., "Add JWT tokens" |

### Agent Name Pattern

Use a readable format: `<epic-slug>-w<wave>-<tick-id>`

Where `<epic-slug>` is a short lowercase version of the epic title (or the epic ID if title is long/unclear).

**Examples:**
- `auth-w1-abc` - Epic "Authentication", wave 1, tick abc
- `api-w2-def` - Epic "API Endpoints", wave 2, tick def
- `x7k-w1-ghi` - Epic with unclear title, using ID instead

### Why Naming Matters

- Distinguishes agents in logs and UI
- Enables filtering/searching by epic or wave
- Helps debug when things go wrong

## Orchestration Algorithm

### Step 1: Gather Context

```bash
# Get the dependency graph
tk graph <epic-id> --json

# Get tick details including HITL flags
tk list --parent <epic-id> --json

# Get project identifier for metadata
git remote get-url origin 2>/dev/null | sed 's/.*github.com[:/]\(.*\)\.git/\1/' || basename $(pwd)
```

### Step 2: Parse Waves

The `tk graph --json` output includes waves - groups of tasks that can run in parallel:

```json
{
  "waves": [
    [{"id": "abc", "title": "First task", "blocked_by": []}],
    [{"id": "def", ...}, {"id": "ghi", ...}],
    [{"id": "jkl", "blocked_by": ["def", "ghi"]}]
  ],
  "max_parallel": 2,
  "critical_path": 3
}
```

### Step 3: Filter HITL Tasks

Before launching, identify tasks that need special handling:

| Tick Flag | Action |
|-----------|--------|
| `--awaiting work` | **Skip** - human must do this |
| `--awaiting input` | **Skip** - needs human input first |
| `--requires approval/review/content` | **Include** - but transition to awaiting state after |

### Step 4: Execute Waves

For each wave, launch agents up to MAX_AGENTS:

```
For wave in waves:
    agents = []

    For tick in wave (up to MAX_AGENTS):
        if tick has --awaiting work or --awaiting input:
            skip  # Human task

        # Mark tick as in progress before launching agent
        run: tk update <tick-id> --status in_progress

        agent = Task(
            subagent_type: "general-purpose",
            name: "<epic-id>-w<wave-num>-<tick-id>",
            description: "Implement <tick-title>",
            prompt: <see prompt template below>,
            run_in_background: true,
            mode: "bypassPermissions"
        )
        agents.append(agent)

    # Wait for all agents in wave to complete
    For agent in agents:
        poll_until_complete(agent)  # See polling strategy below

    # Sync completed ticks
    For tick in completed:
        sync_to_ticks(tick)  # See HITL-aware sync below
```

### Step 5: HITL-Aware Sync

After each agent completes, update the tick based on its HITL requirements:

```bash
# No approval gates - close it
tk close <tick-id> --reason "Completed via Claude runner"

# Has approval gate - transition to awaiting
tk update <tick-id> --awaiting approval   # or review, content
```

### Step 6: Epic Closure

After all waves complete:

```bash
# Check if any ticks still open
tk list --parent <epic-id> --status open

# If all closed, close the epic
tk close <epic-id> --reason "All tasks completed via Claude runner"

# If some awaiting human, notify user
tk list --parent <epic-id> --awaiting
```

## Agent Prompt Template

Each spawned agent should receive a comprehensive prompt:

```
You are implementing a task from the Ticks issue tracker.

## Task
Title: <tick-title>
ID: <tick-id>
Epic: <epic-title> (<epic-id>)

## Description
<tick-description>

## Acceptance Criteria
<tick-acceptance>

## Instructions
1. Read and understand the existing codebase relevant to this task
2. Implement the feature/fix as described
3. Write tests that verify the acceptance criteria
4. Ensure all tests pass before completing

## Completion
When done, provide a summary of:
- Files changed
- Tests added/modified
- Any notes for the next task

Do NOT run `tk close` - the orchestrator will handle tick state.
```

## Avoiding Hangs: Polling Strategy

**Problem**: Using `TaskOutput(block=true)` can cause apparent hangs if agents take longer than the timeout (default 30s).

**Solution**: Poll with `block=false` and longer intervals:

```
poll_until_complete(agent):
    while true:
        result = TaskOutput(
            task_id: agent.id,
            block: false,      # Non-blocking check
            timeout: 5000      # Quick check
        )

        if result.status == "completed":
            return result

        if result.status == "failed":
            handle_failure(agent)
            return

        # Still running - wait before next poll
        sleep(10 seconds)
```

**Alternative**: Use `block=true` with longer timeout:

```
TaskOutput(
    task_id: agent.id,
    block: true,
    timeout: 600000    # 10 minutes max
)
```

The non-blocking poll approach gives better visibility into progress.

## Error Handling

### Agent Failure

If an agent fails:
1. Log the failure with tick ID
2. Add a note to the tick: `tk note <id> "Agent failed: <reason>"`
3. Continue with remaining agents in wave
4. Report failures to user at end

### Partial Wave Completion

If some agents in a wave succeed and others fail:
1. Sync successful ticks
2. Blocked tasks in next wave may still be blocked
3. User can retry failed ticks or handle manually

## Example Session

```
User: Run the auth epic with Claude

Claude: I'll run epic `auth` using Claude Code native orchestration.

> tk graph auth --json
Shows 3 waves, max parallel 2

How many parallel agents? (1-10, recommend 2 based on graph)

User: 2

Claude: Starting wave 1 (1 task)...
  Launching: auth-w1-abc "Add JWT token generation"
  [waiting...]
  Completed: abc

Starting wave 2 (2 tasks)...
  Launching: auth-w2-def "Add login endpoint"
  Launching: auth-w2-ghi "Add logout endpoint"
  [waiting...]
  Completed: def, ghi

Starting wave 3 (1 task)...
  Launching: auth-w3-jkl "Add auth middleware"
  [waiting...]
  Completed: jkl

All waves complete. Syncing to ticks...
  Closed: abc, def, ghi, jkl
  Closed epic: auth

Done! All 4 tasks completed.
```

## Comparison with tk run

| Aspect | `tk run` | Claude Native |
|--------|----------|---------------|
| Monitoring | Tickboard (local + remote) | Claude Code UI |
| HITL | Rich (approvals, checkpoints) | Basic (conversation) |
| Parallelization | Git worktrees | Task subagents |
| File isolation | Worktrees (proven) | Shared workspace |
| State persistence | Tick files (survives crashes) | Session-bound |
| Cost tracking | Built-in (`--max-cost`) | Manual |
| Best for | Production, HITL workflows | Quick parallel execution |

## Limitations

- **Shared workspace**: Unlike `tk run --worktree`, agents share the same working directory. Conflicts possible if tasks touch same files.
- **Session-bound**: If Claude session ends, orchestration stops. Use `tk run` for long-running epics.
- **No cost limits**: Can't set `--max-cost` like with `tk run`.
