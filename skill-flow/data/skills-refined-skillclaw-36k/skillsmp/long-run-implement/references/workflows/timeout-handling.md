# Timeout Handling Workflow

## Purpose

Handle subagent execution timeouts to prevent indefinitely running plans.

## Configuration

Located in STATE.md:

```markdown
## Configuration
timeout_per_plan_minutes: 30
timeout_action: prompt
```

| Setting | Values | Default | Description |
|---------|--------|---------|-------------|
| `timeout_per_plan_minutes` | 1-120 | 30 | Max minutes per plan execution |
| `timeout_action` | prompt, skip, fail | prompt | What to do on timeout |

## Timeout Detection

```typescript
interface TimeoutContext {
  plan_number: string;
  start_time: Date;
  timeout_minutes: number;
  timeout_action: 'prompt' | 'skip' | 'fail';
}

function checkTimeout(ctx: TimeoutContext): boolean {
  const elapsed_minutes = (Date.now() - ctx.start_time.getTime()) / 60000;
  return elapsed_minutes > ctx.timeout_minutes;
}
```

## Timeout Actions

### Action: `prompt` (Default)

Present options to user and wait for decision.

**Prompt Template:**
```
⏱️ TIMEOUT: Plan ${plan_number} has exceeded ${timeout_minutes} minutes.

Elapsed time: ${elapsed_minutes} minutes
Current task: ${current_task || "Unknown"}

Options:
1. Extend (+15 minutes) - Give the plan more time
2. Check status - See what the agent is currently doing
3. Kill and skip - Stop this plan, continue to next
4. Kill and abort - Stop entire long-run session

Select option [1-4]:
```

**Option Handlers:**

```typescript
async function handleTimeoutPrompt(ctx: TimeoutContext, choice: number): Promise<void> {
  switch (choice) {
    case 1: // Extend
      ctx.timeout_minutes += 15;
      console.log(`Timeout extended to ${ctx.timeout_minutes} minutes`);
      // Continue waiting
      break;

    case 2: // Check status
      const checkpoint = readCheckpoint(ctx.state_path);
      console.log(`
Current Status:
  Tasks completed: ${checkpoint.tasks_completed}/${checkpoint.tasks_total}
  Current task: ${checkpoint.current_task}
  Last activity: ${checkpoint.last_activity}

Agent appears to be: ${checkpoint.last_activity_age > 5 ? 'STUCK' : 'WORKING'}
      `);
      // Re-prompt
      break;

    case 3: // Kill and skip
      await killAgent(ctx.agent_id);
      await createTimeoutSummary(ctx);
      await trackComplete(ctx.agent_id, ctx.state_path, 'timeout');
      // Continue to next plan
      break;

    case 4: // Kill and abort
      await killAgent(ctx.agent_id);
      await trackComplete(ctx.agent_id, ctx.state_path, 'timeout');
      throw new Error('User aborted after timeout');
  }
}
```

### Action: `skip`

Automatically skip to next plan on timeout.

```typescript
async function handleTimeoutSkip(ctx: TimeoutContext): Promise<void> {
  console.log(`
⏱️ TIMEOUT: Plan ${ctx.plan_number} exceeded ${ctx.timeout_minutes} minutes.
Action: Automatic skip (configured timeout_action: skip)

Killing agent and creating timeout summary...
  `);

  await killAgent(ctx.agent_id);
  await createTimeoutSummary(ctx);
  await trackComplete(ctx.agent_id, ctx.state_path, 'timeout');

  console.log(`Plan ${ctx.plan_number} marked as timeout. Continuing to next plan.`);
}
```

### Action: `fail`

Abort entire long-run session on timeout.

```typescript
async function handleTimeoutFail(ctx: TimeoutContext): Promise<void> {
  console.log(`
⏱️ TIMEOUT: Plan ${ctx.plan_number} exceeded ${ctx.timeout_minutes} minutes.
Action: Abort run (configured timeout_action: fail)
  `);

  await killAgent(ctx.agent_id);
  await createTimeoutSummary(ctx);
  await trackComplete(ctx.agent_id, ctx.state_path, 'timeout');

  throw new Error(`Plan ${ctx.plan_number} timed out. Run aborted per configuration.`);
}
```

## Timeout Summary Generation

Create a SUMMARY.md for timed-out plans:

```typescript
async function createTimeoutSummary(ctx: TimeoutContext): Promise<void> {
  const checkpoint = readCheckpoint(ctx.state_path);

  const summary = `---
version: "1.0"
plan: ${ctx.plan_number}
task_group: ${ctx.task_group}
status: timeout
completed_at: ${new Date().toISOString()}
duration_minutes: ${ctx.timeout_minutes}
---

# Plan ${ctx.plan_number}: ${ctx.task_group} Summary

**Status:** Timeout after ${ctx.timeout_minutes} minutes

## Tasks Completed Before Timeout

${checkpoint.completed_tasks.map(t => `- [x] ${t.name} - commit ${t.commit}`).join('\n')}

## Tasks Not Completed

${checkpoint.remaining_tasks.map(t => `- [ ] ${t.name} - not started`).join('\n')}

## Partial Work

${checkpoint.partial_commits.length > 0
  ? `Commits made:\n${checkpoint.partial_commits.map(c => `  ${c}`).join('\n')}`
  : 'No commits made before timeout.'}

## Timeout Details

- Configured timeout: ${ctx.timeout_minutes} minutes
- Actual elapsed: ${ctx.elapsed_minutes} minutes
- Last known activity: ${checkpoint.last_activity}

## Recovery Options

1. **Resume:** Run \`/long-run-implement --resume\` to retry this plan
2. **Skip:** The orchestrator will continue to the next plan
3. **Investigate:** Check logs for what caused the delay

## Next Steps

- Review what was blocking progress
- Consider increasing timeout if tasks are legitimately slow
- Check for infinite loops or hung operations
`;

  write_atomic(
    `${ctx.state_path}/summaries/${ctx.plan_number}-SUMMARY.md`,
    summary
  );
}
```

## Checkpoint Reading for Status

```typescript
interface Checkpoint {
  plan_number: string;
  tasks_total: number;
  tasks_completed: number;
  current_task: string;
  completed_tasks: { name: string; commit: string }[];
  remaining_tasks: { name: string }[];
  partial_commits: string[];
  last_activity: string;
  last_activity_age: number;  // minutes since last activity
}

function readCheckpoint(state_path: string): Checkpoint {
  const checkpoint_path = `${state_path}/checkpoint.json`;

  if (!file_exists(checkpoint_path)) {
    return {
      plan_number: "unknown",
      tasks_total: 0,
      tasks_completed: 0,
      current_task: "Unknown",
      completed_tasks: [],
      remaining_tasks: [],
      partial_commits: [],
      last_activity: "Unknown",
      last_activity_age: 999
    };
  }

  const data = JSON.parse(read_file(checkpoint_path));
  const last_time = new Date(data.last_activity_timestamp);
  const age_minutes = (Date.now() - last_time.getTime()) / 60000;

  return {
    ...data,
    last_activity_age: Math.round(age_minutes)
  };
}
```

## Integration with Phase 3

In `3-execute.md`, timeout handling is integrated:

```typescript
async function executePlanWithTimeout(input: ExecutePlanInput): Promise<ExecutionResult> {
  const ctx: TimeoutContext = {
    plan_number: input.plan_number,
    start_time: new Date(),
    timeout_minutes: input.config.timeout_per_plan_minutes,
    timeout_action: input.config.timeout_action,
    state_path: input.state_path,
    agent_id: null
  };

  // Spawn agent
  const spawn_result = await spawnPlanExecutor(input);
  ctx.agent_id = spawn_result.agent_id;

  // Wait with timeout check
  while (true) {
    // Check if agent completed
    const status = await checkAgentStatus(ctx.agent_id);
    if (status.done) {
      return status.result;
    }

    // Check timeout
    if (checkTimeout(ctx)) {
      return await handleTimeout(ctx);
    }

    // Brief sleep before next check
    await sleep(5000);  // 5 seconds
  }
}

async function handleTimeout(ctx: TimeoutContext): Promise<ExecutionResult> {
  switch (ctx.timeout_action) {
    case 'prompt':
      return await handleTimeoutPrompt(ctx);
    case 'skip':
      await handleTimeoutSkip(ctx);
      return { status: 'timeout', continue: true };
    case 'fail':
      await handleTimeoutFail(ctx);
      return { status: 'timeout', continue: false };
  }
}
```

## Error Handling

| Error | Action |
|-------|--------|
| Cannot kill agent | Log warning, mark as zombie, continue |
| Checkpoint unreadable | Use defaults, note in summary |
| Summary write fails | Retry, log to STATE.md if persists |
| Invalid timeout_action | Default to 'prompt' |
