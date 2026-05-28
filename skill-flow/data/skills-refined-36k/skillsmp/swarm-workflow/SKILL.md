---
name: swarm-workflow
description: Swarm-based parallel worker execution with automatic spawning, worktree isolation, and wave-based merge synchronization. Use for orchestrators managing teamwork projects with concurrent worker execution.
---

# Swarm Workflow

This skill provides the complete swarm orchestration workflow for teamwork projects. Use this to manage automatic worker spawning, worktree isolation, and merge synchronization across waves.

## When to Use This Skill

- Orchestrating teamwork projects with automatic worker spawning
- Managing git worktree isolation for parallel work
- Coordinating wave-based merges and conflict resolution
- Monitoring and restarting crashed workers
- Synchronizing worktrees across wave boundaries

## What is Swarm Mode?

Swarm mode automates worker spawning and coordination:

- **Automatic spawning**: Orchestrator creates workers in tmux panes
- **Worktree isolation**: Each worker operates in a separate git worktree
- **Wave-based merges**: All worktrees merge to main at wave completion
- **Conflict handling**: Automatic conflict detection and fix task creation
- **Health monitoring**: Detect and restart crashed workers

## Input Format

Your prompt includes:

```
TEAMWORK_DIR: {path to teamwork directory}
PROJECT: {project name}
SUB_TEAM: {sub-team name}
SCRIPTS_PATH: {path to scripts directory}

Options:
- workers: {count or role:count, optional}
- worktree: {true/false, default false}
```

---

## Swarm Spawn Decision

After task decomposition and wave calculation, decide whether to spawn workers automatically.

### Spawn Strategies

| Option | Behavior | Example |
|--------|----------|---------|
| (none) | Manual worker spawning | User runs `/teamwork-worker` manually |
| `--workers N` | Spawn N generic workers | `--workers 3` → 3 workers, any role |
| `--workers role:N` | Spawn N workers per role | `--workers backend:2,frontend:1` |
| `--worktree` | Enable worktree isolation | Each worker gets separate git worktree |

### Role-Based Auto Spawn

When no `--workers` specified, automatically determine worker count from task roles:

```javascript
// Pseudocode: Count unique roles in tasks
const taskRoles = tasks.map(t => t.role);
const uniqueRoles = [...new Set(taskRoles)];

// Spawn one worker per unique role
for (const role of uniqueRoles) {
  spawnWorker({ role, worktree: useWorktree });
}
```

### Spawn Command

```bash
# Basic spawn (manual mode, no swarm)
# User runs: /teamwork-worker --role backend

# Auto spawn with generic workers
bun "$SCRIPTS_PATH/swarm-spawn.js" \
  --project {PROJECT} \
  --team {SUB_TEAM} \
  --count 3 \
  --worktree false

# Auto spawn with role-specific workers
bun "$SCRIPTS_PATH/swarm-spawn.js" \
  --project {PROJECT} \
  --team {SUB_TEAM} \
  --roles backend,frontend,test \
  --worktree true

# Spawn specific worker count per role
bun "$SCRIPTS_PATH/swarm-spawn.js" \
  --project {PROJECT} \
  --team {SUB_TEAM} \
  --roles "backend:2,frontend:1,test:1" \
  --worktree true
```

**Expected output:**

```json
{
  "status": "success",
  "session": "teamwork-my-app",
  "workers": [
    {
      "id": "w1",
      "role": "backend",
      "pane": 1,
      "worktree": "~/.claude/teamwork/my-app/master/worktrees/w1",
      "branch": "worker-w1"
    },
    {
      "id": "w2",
      "role": "frontend",
      "pane": 2,
      "worktree": "~/.claude/teamwork/my-app/master/worktrees/w2",
      "branch": "worker-w2"
    }
  ]
}
```

---

## Worker Lifecycle

Workers run autonomously until project completion or manual stop.

### Worker States

| State | Description | Next State |
|-------|-------------|------------|
| `spawning` | Being created in tmux | `idle` or `error` |
| `idle` | Waiting for available tasks | `working` |
| `working` | Executing a task | `idle` or `crashed` |
| `paused` | Waiting for wave merge | `idle` |
| `crashed` | Process died unexpectedly | `spawning` (restart) |
| `stopped` | Manually terminated | (terminal) |

### Heartbeat Mechanism

Workers update heartbeat to signal liveness:

```bash
# Worker updates every 60 seconds
bun "$SCRIPTS_PATH/worker-heartbeat.js" \
  --project {PROJECT} \
  --team {SUB_TEAM} \
  --worker-id {WORKER_ID}
```

### Dead Worker Detection

Orchestrator checks for dead workers during monitoring loop:

```bash
# Get swarm status
SWARM_STATUS=$(bun "$SCRIPTS_PATH/swarm-status.js" \
  --project {PROJECT} \
  --team {SUB_TEAM} \
  --format json)

# Detect dead workers (no heartbeat > 3 minutes)
DEAD_WORKERS=$(echo $SWARM_STATUS | jq -r '.workers[] | select(.alive == false) | .id')

# Restart each dead worker
for WORKER_ID in $DEAD_WORKERS; do
  echo "⚠️  Worker $WORKER_ID crashed, restarting..."

  bun "$SCRIPTS_PATH/swarm-spawn.js" \
    --project {PROJECT} \
    --team {SUB_TEAM} \
    --worker-id $WORKER_ID \
    --role $(echo $SWARM_STATUS | jq -r ".workers[] | select(.id == \"$WORKER_ID\") | .role") \
    --worktree $(echo $SWARM_STATUS | jq -r ".workers[] | select(.id == \"$WORKER_ID\") | .worktree != null")
done
```

---

## Wave Completion Detection

Monitor wave status to detect when all tasks are resolved.

### Wave Completion Check

```bash
# Get wave status
WAVE_STATUS=$(bun "$SCRIPTS_PATH/wave-status.js" \
  --project {PROJECT} \
  --team {SUB_TEAM} \
  --format json)

# Extract current wave info
CURRENT_WAVE=$(echo $WAVE_STATUS | jq -r '.current_wave')
WAVE_TASKS=$(echo $WAVE_STATUS | jq -r ".waves[] | select(.id == $CURRENT_WAVE) | .tasks[]")

# Check if all tasks resolved
ALL_RESOLVED=true
for TASK_ID in $WAVE_TASKS; do
  TASK_STATUS=$(bun "$SCRIPTS_PATH/task-get.js" \
    --project {PROJECT} \
    --team {SUB_TEAM} \
    --id $TASK_ID \
    --field status)

  if [ "$TASK_STATUS" != "resolved" ]; then
    ALL_RESOLVED=false
    break
  fi
done

if [ "$ALL_RESOLVED" = "true" ]; then
  echo "✅ Wave $CURRENT_WAVE complete, triggering merge..."
  # Proceed to merge workflow
fi
```

---

## Merge/Sync Workflow

When a wave completes, merge all worktrees to main and sync.

### Step 1: Pause Workers

Signal all workers to stop claiming new tasks:

```bash
# Update swarm state to paused
bun "$SCRIPTS_PATH/swarm-pause.js" \
  --project {PROJECT} \
  --team {SUB_TEAM}

echo "⏸️  Workers paused, no new task claims until merge complete"
```

### Step 2: Merge Worktrees

Merge all worktrees sequentially to main:

```bash
# Merge all worktrees for current wave
MERGE_RESULT=$(bun "$SCRIPTS_PATH/swarm-merge.js" \
  --project {PROJECT} \
  --team {SUB_TEAM} \
  --wave $CURRENT_WAVE 2>&1)

MERGE_EXIT=$?
```

**Merge algorithm:**

1. For each worker worktree:
   - Checkout main branch
   - Pull latest changes
   - Merge worker branch
   - If conflict → stop and report
   - If success → continue to next worker

2. If any conflicts → return error with conflict details
3. If all success → return success

### Step 3: Handle Merge Conflicts

If merge fails, create fix tasks:

```bash
if [ $MERGE_EXIT -ne 0 ]; then
  echo "❌ Merge conflicts detected"

  # Parse conflict details
  CONFLICTS=$(echo $MERGE_RESULT | jq -r '.conflicts[]')

  # Create fix tasks
  for CONFLICT in $CONFLICTS; do
    FILE=$(echo $CONFLICT | jq -r '.file')
    WORKERS=$(echo $CONFLICT | jq -r '.workers | join(",")')

    # Get next task ID
    NEXT_ID=$(bun "$SCRIPTS_PATH/task-list.js" \
      --project {PROJECT} \
      --team {SUB_TEAM} \
      --format json | jq '.tasks | length + 1')

    # Create fix task
    bun "$SCRIPTS_PATH/task-create.js" \
      --project {PROJECT} \
      --team {SUB_TEAM} \
      --id "$NEXT_ID" \
      --title "Resolve merge conflict in $FILE" \
      --description "Merge conflict between workers $WORKERS in file $FILE. Review changes and resolve manually." \
      --role backend \
      --complexity standard
  done

  # Recalculate waves to include fix tasks
  bun "$SCRIPTS_PATH/wave-calculate.js" \
    --project {PROJECT} \
    --team {SUB_TEAM}

  echo "Created fix tasks, recalculated waves"
fi
```

### Step 4: Sync All Worktrees

After successful merge, sync all worktrees to latest main:

```bash
if [ $MERGE_EXIT -eq 0 ]; then
  # Sync all worktrees with updated main
  bun "$SCRIPTS_PATH/swarm-sync.js" \
    --project {PROJECT} \
    --team {SUB_TEAM}

  echo "✅ All worktrees synced with main"
fi
```

### Step 5: Resume Workers

Unpause workers to continue with next wave:

```bash
# Resume workers
bun "$SCRIPTS_PATH/swarm-resume.js" \
  --project {PROJECT} \
  --team {SUB_TEAM}

echo "▶️  Workers resumed, can claim tasks from Wave $(($CURRENT_WAVE + 1))"
```

---

## Error Handling

### Worker Crash Recovery

**Detection:**
- Heartbeat timeout (> 3 minutes)
- tmux pane status shows `pane_dead=1`

**Recovery:**
1. Log crash event
2. Restart worker in same role
3. Reuse existing worktree (if present)
4. Worker picks up from where it left off

```bash
# Restart crashed worker
echo "🔄 Restarting crashed worker $WORKER_ID"

bun "$SCRIPTS_PATH/swarm-spawn.js" \
  --project {PROJECT} \
  --team {SUB_TEAM} \
  --worker-id $WORKER_ID \
  --role $ROLE \
  --worktree $USE_WORKTREE
```

### Merge Conflict Recovery

**Detection:**
- `swarm-merge.js` exits with code 1
- Conflict details in stderr output

**Recovery:**
1. Parse conflict files and affected workers
2. Create fix task for each conflict
3. Add fix tasks to new wave
4. Recalculate waves
5. Resume monitoring with fix wave

**Example conflict:**

```json
{
  "file": "src/auth.ts",
  "workers": ["w1", "w2"],
  "severity": "critical",
  "description": "Both workers modified function authenticate()"
}
```

### Stuck Worker Recovery

**Detection:**
- Task claimed for > fresh-start interval (default: 1 hour)
- Task status still `in_progress`

**Recovery:**
1. Release task (reset claimed_by, claimed_at)
2. Log fresh start event
3. Worker or another worker can reclaim

```bash
# Orchestrator detects stuck task
STUCK_TASKS=$(bun "$SCRIPTS_PATH/task-list.js" \
  --project {PROJECT} \
  --team {SUB_TEAM} \
  --stuck-for 3600)  # 1 hour

# Release stuck tasks
for TASK_ID in $STUCK_TASKS; do
  bun "$SCRIPTS_PATH/task-update.js" \
    --project {PROJECT} \
    --team {SUB_TEAM} \
    --id $TASK_ID \
    --release

  echo "🔓 Released stuck task $TASK_ID"
done
```

### tmux Session Lost

**Detection:**
- `tmux has-session` returns error

**Recovery:**
1. Log session loss event
2. Recreate tmux session
3. Respawn all workers from swarm state
4. Workers reconnect to existing worktrees

```bash
# Check if tmux session exists
if ! tmux has-session -t teamwork-{PROJECT} 2>/dev/null; then
  echo "⚠️  tmux session lost, recreating..."

  # Read swarm state
  SWARM_STATE=$(cat {TEAMWORK_DIR}/swarm/swarm.json)

  # Recreate session and respawn workers
  bun "$SCRIPTS_PATH/swarm-spawn.js" \
    --project {PROJECT} \
    --team {SUB_TEAM} \
    --restore
fi
```

---

## Swarm Status Monitoring

Check swarm health in monitoring loop:

```bash
# Get comprehensive swarm status
SWARM_STATUS=$(bun "$SCRIPTS_PATH/swarm-status.js" \
  --project {PROJECT} \
  --team {SUB_TEAM} \
  --format json)

# Example status output
{
  "session": "teamwork-my-app",
  "status": "running",
  "paused": false,
  "workers": [
    {
      "id": "w1",
      "role": "backend",
      "pane": 1,
      "alive": true,
      "status": "working",
      "current_task": "3",
      "last_heartbeat": "2026-01-26T10:15:00Z",
      "worktree": "~/.claude/teamwork/my-app/master/worktrees/w1"
    },
    {
      "id": "w2",
      "role": "frontend",
      "pane": 2,
      "alive": false,
      "status": "crashed",
      "current_task": null,
      "last_heartbeat": "2026-01-26T10:10:00Z",
      "worktree": "~/.claude/teamwork/my-app/master/worktrees/w2"
    }
  ]
}
```

**Key metrics:**
- `alive`: Worker process running
- `status`: Current worker state
- `last_heartbeat`: Last activity timestamp
- `current_task`: Active task ID or null

---

## Swarm Cleanup

On project completion or manual stop:

```bash
# Stop all workers gracefully
bun "$SCRIPTS_PATH/swarm-stop.js" \
  --project {PROJECT} \
  --team {SUB_TEAM} \
  --all

# Cleanup worktrees
if [ "$USE_WORKTREE" = "true" ]; then
  for WORKER_ID in $(echo $SWARM_STATUS | jq -r '.workers[].id'); do
    bun "$SCRIPTS_PATH/worktree-remove.js" \
      --project {PROJECT} \
      --team {SUB_TEAM} \
      --worker-id $WORKER_ID
  done

  echo "🗑️  All worktrees cleaned up"
fi

# Remove swarm state
rm -rf {TEAMWORK_DIR}/swarm/

echo "✅ Swarm cleanup complete"
```

---

## Best Practices

### Spawn Strategy

- **Small projects (< 5 tasks)**: Manual workers, no swarm
- **Medium projects (5-20 tasks)**: Auto spawn by role
- **Large projects (> 20 tasks)**: Explicit `--workers` with worktree isolation

### Worktree Usage

- **Enable worktree** when:
  - Multiple workers may touch same files
  - High risk of merge conflicts
  - Need isolation for testing

- **Skip worktree** when:
  - Tasks are completely independent (e.g., different modules)
  - Single worker or manual coordination
  - Quick prototyping

### Conflict Prevention

- Design tasks to minimize file overlap
- Use fine-grained tasks (1-3 files per task)
- Assign clear ownership boundaries (e.g., backend vs frontend)
- Coordinate high-risk files (schema, configs) in separate waves

### Monitoring Frequency

- Check swarm status every 30 seconds
- Allow 3-minute heartbeat timeout before restart
- Log all worker state changes for debugging

---

## Notes

- Swarm mode is optional - manual workers still supported
- Worktree isolation requires git repository
- tmux is required for automatic spawning
- Workers can be added/removed dynamically during execution
- Merge conflicts are expected and handled gracefully
