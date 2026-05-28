# Prevention Patterns

Best practices for preventing session crashes and ensuring recoverable state.

## Why Sessions Crash

Common causes of Claude Code session crashes:

| Cause | Description | Prevention |
|-------|-------------|------------|
| Context exhaustion | Too much data in context window | Smaller batches, background execution |
| Parallel overload | Too many concurrent agents | Limit to 3-4 per batch |
| No checkpointing | Progress not saved between tasks | Update after each completion |
| Long operations | Extended running without status | Use timeouts and heartbeats |
| Memory issues | Large file operations | Stream processing, chunking |

## Pattern 1: Batch Size Limits

### Problem

Launching many parallel agents exhausts context and resources.

```javascript
// RISKY: 6+ parallel agents
const allTasks = [...]; // 10 tasks
await Promise.all(allTasks.map(t => Task(t.agent, t.prompt)));
```

### Solution

Limit batch size to 3-4 agents:

```javascript
// SAFE: Batched execution
const BATCH_SIZE = 3;

for (let i = 0; i < allTasks.length; i += BATCH_SIZE) {
  const batch = allTasks.slice(i, i + BATCH_SIZE);

  // Execute batch
  await Promise.all(batch.map(t => Task(t.agent, t.prompt)));

  // Checkpoint after batch
  await updateProgressFile(batch);

  // Brief pause between batches
  await sleep(1000);
}
```

### Configuration

Add to progress file YAML:

```yaml
parallelization:
  max_batch_size: 3
  batch_1: ["TASK-1.1", "TASK-1.2", "TASK-1.3"]
  batch_2: ["TASK-2.1", "TASK-2.2"]
```

## Pattern 2: Checkpointing

### Problem

Progress not saved between tasks - crash loses all state.

```javascript
// RISKY: No checkpointing
for (const task of tasks) {
  await executeTask(task);
}
// All progress lost if crash here
await updateProgressFile(tasks);
```

### Solution

Update progress after each task:

```javascript
// SAFE: Checkpoint after each task
for (const task of tasks) {
  // Mark as in_progress
  await updateProgressFile({ [task.id]: 'in_progress' });

  // Execute
  const result = await executeTask(task);

  // Mark as complete immediately
  await updateProgressFile({
    [task.id]: 'complete',
    commit: result.commit,
    files: result.files
  });
}
```

### Progress File Updates

```yaml
# Before task
tasks:
  - id: "TASK-1.1"
    status: "in_progress"
    started_at: "2025-12-23T10:30:00Z"

# After task
tasks:
  - id: "TASK-1.1"
    status: "complete"
    completed_at: "2025-12-23T10:45:00Z"
    commit: "abc1234"
    agent_id: "a91845a"  # For recovery correlation
```

## Pattern 3: Session Tracking

### Problem

Can't correlate crashed agents with tasks.

### Solution

Record agent IDs in progress files:

```yaml
session_tracking:
  session_start: "2025-12-23T10:00:00Z"
  last_checkpoint: "2025-12-23T10:30:00Z"
  active_agents: ["a91845a", "abec615"]
  batch_in_progress: 2

tasks:
  - id: "TASK-2.1"
    status: "in_progress"
    agent_id: "a91845a"  # Links task to agent log
```

### Implementation

```javascript
// When launching agent
const agentResult = await Task(agent, prompt);
const agentId = extractAgentId(agentResult);

// Update progress with agent ID
await updateProgressFile({
  taskId: task.id,
  agentId: agentId,
  status: 'in_progress'
});
```

## Pattern 4: Background Execution with Monitoring

### Problem

Long-running tasks without status updates appear hung.

```javascript
// RISKY: No monitoring
await Task(agent, longRunningPrompt);
// No visibility into progress
```

### Solution

Use background execution with periodic status checks:

```javascript
// SAFE: Background with monitoring
const task = await Task(agent, prompt, { run_in_background: true });

// Monitor with timeout
const TIMEOUT = 10 * 60 * 1000; // 10 minutes
const CHECK_INTERVAL = 60 * 1000; // 1 minute
const startTime = Date.now();

while (Date.now() - startTime < TIMEOUT) {
  const status = await TaskOutput(task.id, { block: false });

  if (status.complete) {
    return status.result;
  }

  // Log heartbeat
  console.log(`Task ${task.id} still running...`);
  await sleep(CHECK_INTERVAL);
}

// Timeout - task may have stalled
console.warn(`Task ${task.id} timed out`);
```

## Pattern 5: Heartbeat Updates

### Problem

No indication of progress during long operations.

### Solution

Emit periodic status updates:

```javascript
// In long-running task
async function executeWithHeartbeat(task, interval = 5 * 60 * 1000) {
  const heartbeat = setInterval(async () => {
    await appendToProgressFile({
      timestamp: new Date().toISOString(),
      taskId: task.id,
      status: 'active',
      lastOperation: getCurrentOperation()
    });
  }, interval);

  try {
    return await executeTask(task);
  } finally {
    clearInterval(heartbeat);
  }
}
```

### Progress File Heartbeat Section

```yaml
heartbeats:
  - timestamp: "2025-12-23T10:30:00Z"
    task: "TASK-2.1"
    operation: "Writing component tests"
  - timestamp: "2025-12-23T10:35:00Z"
    task: "TASK-2.1"
    operation: "Running test suite"
```

## Pattern 6: Sequential Critical Paths

### Problem

Parallelizing dependent tasks causes race conditions.

```javascript
// RISKY: Parallel dependent tasks
await Promise.all([
  Task('backend', 'Create API endpoint'),
  Task('frontend', 'Consume API endpoint')  // May fail if API not ready
]);
```

### Solution

Sequential execution for dependencies:

```javascript
// SAFE: Sequential for dependencies
// Batch 1: Independent tasks
await Promise.all([
  Task('backend', 'Create models'),
  Task('backend', 'Create schemas')
]);

// Batch 2: Depends on Batch 1
const apiResult = await Task('backend', 'Create API endpoint');

// Batch 3: Depends on Batch 2
await Task('frontend', 'Consume API endpoint');
```

### Dependency Declaration

```yaml
tasks:
  - id: "TASK-1.1"
    dependencies: []  # Can run immediately
  - id: "TASK-2.1"
    dependencies: ["TASK-1.1"]  # Must wait for 1.1
  - id: "TASK-3.1"
    dependencies: ["TASK-2.1"]  # Must wait for 2.1

parallelization:
  batch_1: ["TASK-1.1", "TASK-1.2"]  # Parallel
  batch_2: ["TASK-2.1"]              # Sequential
  batch_3: ["TASK-3.1", "TASK-3.2"]  # Parallel after 2.1
```

## Pattern 7: Graceful Degradation

### Problem

One failed task crashes entire batch.

```javascript
// RISKY: All-or-nothing
await Promise.all(tasks.map(t => executeTask(t)));
// Single failure crashes everything
```

### Solution

Handle failures gracefully:

```javascript
// SAFE: Graceful failure handling
const results = await Promise.allSettled(
  tasks.map(t => executeTask(t))
);

for (let i = 0; i < results.length; i++) {
  const task = tasks[i];
  const result = results[i];

  if (result.status === 'fulfilled') {
    await updateProgress(task.id, 'complete', result.value);
  } else {
    await updateProgress(task.id, 'failed', result.reason);
    // Continue with remaining tasks
  }
}
```

## Pattern 8: Pre-Flight Checks

### Problem

Starting tasks that will obviously fail.

### Solution

Validate before execution:

```javascript
// Pre-flight validation
async function validateTask(task) {
  // Check required files exist
  for (const file of task.requiredFiles) {
    if (!await fileExists(file)) {
      throw new Error(`Required file missing: ${file}`);
    }
  }

  // Check dependencies complete
  for (const dep of task.dependencies) {
    const status = await getTaskStatus(dep);
    if (status !== 'complete') {
      throw new Error(`Dependency not met: ${dep}`);
    }
  }

  return true;
}

// Execute with validation
for (const task of tasks) {
  try {
    await validateTask(task);
    await executeTask(task);
  } catch (e) {
    await updateProgress(task.id, 'blocked', e.message);
    continue; // Try next task
  }
}
```

## execute-phase Command Updates

Recommended improvements to `/dev:execute-phase`:

### Current (Risky)

```javascript
// Execute all parallel tasks at once
await Promise.all(batch.map(t => Task(t.agent, t.prompt)));
```

### Recommended

```javascript
// 1. Limit batch size
const MAX_BATCH = 3;
const batches = chunk(tasks, MAX_BATCH);

for (const batch of batches) {
  // 2. Track agent IDs
  const agents = batch.map(t => ({
    task: t,
    agent: Task(t.agent, t.prompt, { run_in_background: true })
  }));

  // 3. Monitor with timeout
  const results = await monitorAgents(agents, { timeout: 600000 });

  // 4. Checkpoint immediately
  for (const result of results) {
    await updateProgress(result.task.id, result.status, {
      agentId: result.agentId,
      commit: result.commit
    });
  }

  // 5. Brief pause between batches
  await sleep(1000);
}
```

## CLAUDE.md Recovery Guidance

Add to project CLAUDE.md:

```markdown
## Session Recovery

If session crashes during parallel execution:

1. Invoke `/recovering-sessions` skill
2. Review generated recovery report
3. Commit completed work
4. Resume interrupted tasks

### Prevention Practices

- Keep parallel batches small (3-4 agents max)
- Use background execution with timeout monitoring
- Update progress tracking after each task completion
- Prefer sequential execution for critical paths
- Track agent IDs in progress file YAML
```

## Artifact Tracking Enhancements

### Enhanced YAML Frontmatter

```yaml
---
type: progress
prd: "feature-name"
phase: 2
status: in_progress

session_tracking:
  session_start: "2025-12-23T10:00:00Z"
  last_checkpoint: "2025-12-23T10:30:00Z"
  active_agents: ["a91845a", "abec615"]
  batch_in_progress: 2

tasks:
  - id: "TASK-2.1"
    status: "complete"
    completed_at: "2025-12-23T10:35:00Z"
    agent_id: "a91845a"
    commit: "abc1234"
  - id: "TASK-2.2"
    status: "in_progress"
    started_at: "2025-12-23T10:40:00Z"
    agent_id: "abec615"

parallelization:
  max_batch_size: 3
  batch_1: ["TASK-1.1", "TASK-1.2"]
  batch_2: ["TASK-2.1", "TASK-2.2", "TASK-2.3"]
  current_batch: 2
---
```

## Summary

| Pattern | Purpose | Key Benefit |
|---------|---------|-------------|
| Batch Size Limits | Prevent overload | Reduce crash risk |
| Checkpointing | Save progress | Recoverable state |
| Session Tracking | Correlate agents | Fast recovery |
| Background Monitoring | Visibility | Detect hangs |
| Heartbeat Updates | Progress indicator | Know what's running |
| Sequential Dependencies | Avoid races | Correct ordering |
| Graceful Degradation | Isolate failures | Continue on error |
| Pre-Flight Checks | Early validation | Fail fast |

Implementing these patterns significantly reduces crash frequency and improves recovery speed when crashes do occur.
