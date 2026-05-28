# Update State Workflow

## Purpose

Update STATE.md after a plan completes to reflect current progress, metrics, and accumulated context.

## Inputs

```typescript
interface UpdateStateInput {
  state_path: string;          // Path to .long-run/ directory
  plan_number: string;         // Just completed plan (e.g., "02")
  plan_result: {
    status: 'completed' | 'failed' | 'partial' | 'skipped';
    tasks_completed: number;
    tasks_total: number;
    commits: string[];
    duration_minutes: number;
    decisions?: Decision[];
    issues_logged?: string[];  // ISS-XXX IDs
  };
  total_plans: number;         // Total plans in this run
}
```

## Workflow Steps

### Step 1: Read Current STATE.md

```typescript
function readState(state_path: string): StateData {
  const content = read_file(`${state_path}/STATE.md`);
  return parseStateMarkdown(content);
}

interface StateData {
  spec_reference: {
    spec: string;
    tasks: string;
    started: string;
  };
  current_position: {
    plan: number;
    total_plans: number;
    task_group: string;
    status: string;
    last_activity: string;
    progress: number;  // 0-100
  };
  execution_metrics: {
    plans_completed: number;
    tasks_completed: number;
    total_commits: number;
    duration: string;  // "X hours Y minutes"
  };
  accumulated_context: {
    decisions: Decision[];
    deferred_issues: string[];
    blockers: string[];
  };
  session_continuity: {
    last_session: string;
    stopped_at: string;
    resume_agent: string;
  };
  rollback_reference: {
    start_commit: string;
  };
}
```

### Step 2: Calculate New Metrics

```typescript
function updateMetrics(current: StateData, plan_result: PlanResult): StateData {
  // Increment counters
  const plans_completed = current.execution_metrics.plans_completed +
    (plan_result.status === 'completed' ? 1 : 0);

  const tasks_completed = current.execution_metrics.tasks_completed +
    plan_result.tasks_completed;

  const total_commits = current.execution_metrics.total_commits +
    plan_result.commits.length;

  // Calculate total duration
  const current_minutes = parseDuration(current.execution_metrics.duration);
  const new_total_minutes = current_minutes + plan_result.duration_minutes;
  const duration = formatDuration(new_total_minutes);

  return {
    ...current,
    execution_metrics: {
      plans_completed,
      tasks_completed,
      total_commits,
      duration
    }
  };
}

function formatDuration(minutes: number): string {
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  if (hours > 0) {
    return `${hours} hours ${mins} minutes`;
  }
  return `${mins} minutes`;
}
```

### Step 3: Update Progress Bar

```typescript
function calculateProgress(plans_completed: number, total_plans: number): string {
  const percent = Math.round((plans_completed / total_plans) * 100);
  const filled = Math.round(percent / 10);
  const empty = 10 - filled;

  const bar = '█'.repeat(filled) + '░'.repeat(empty);
  return `[${bar}] ${percent}%`;
}

// Examples:
// 0/5 plans  → [░░░░░░░░░░] 0%
// 2/5 plans  → [████░░░░░░] 40%
// 5/5 plans  → [██████████] 100%
```

### Step 4: Update Current Position

```typescript
function updatePosition(
  current: StateData,
  plan_number: string,
  plan_result: PlanResult,
  total_plans: number
): StateData {
  const next_plan = parseInt(plan_number) + 1;
  const all_done = next_plan > total_plans;

  return {
    ...current,
    current_position: {
      plan: all_done ? total_plans : next_plan,
      total_plans: total_plans,
      task_group: all_done ? "All Complete" : `Plan ${next_plan}`,
      status: all_done ? "Complete" : "Executing",
      last_activity: `${new Date().toISOString().split('T')[0]} - Completed Plan ${plan_number}`,
      progress: calculateProgress(
        current.execution_metrics.plans_completed + (plan_result.status === 'completed' ? 1 : 0),
        total_plans
      )
    }
  };
}
```

### Step 5: Accumulate Context

```typescript
function accumulateContext(
  current: StateData,
  plan_result: PlanResult,
  plan_number: string
): StateData {
  // Add any new decisions
  const decisions = [...current.accumulated_context.decisions];
  if (plan_result.decisions) {
    decisions.push(...plan_result.decisions.map(d => ({
      ...d,
      plan: plan_number
    })));
  }

  // Add any new deferred issues
  const deferred_issues = [...current.accumulated_context.deferred_issues];
  if (plan_result.issues_logged) {
    deferred_issues.push(
      ...plan_result.issues_logged.map(id => `${id} (Plan ${plan_number})`)
    );
  }

  return {
    ...current,
    accumulated_context: {
      decisions,
      deferred_issues,
      blockers: current.accumulated_context.blockers // Preserved unless resolved
    }
  };
}
```

### Step 6: Update Session Continuity

```typescript
function updateSession(current: StateData, plan_number: string): StateData {
  return {
    ...current,
    session_continuity: {
      last_session: new Date().toISOString().replace('T', ' ').substring(0, 16),
      stopped_at: `Completed Plan ${plan_number}`,
      resume_agent: "None"  // Clear after successful completion
    }
  };
}
```

### Step 7: Generate Updated Markdown

```typescript
function generateStateMarkdown(state: StateData): string {
  return `# Long-Run Implementation State

## Spec Reference
Spec: ${state.spec_reference.spec}
Tasks: ${state.spec_reference.tasks}
Started: ${state.spec_reference.started}

## Current Position
Plan: ${state.current_position.plan} of ${state.current_position.total_plans}
Task Group: ${state.current_position.task_group}
Status: ${state.current_position.status}
Last activity: ${state.current_position.last_activity}
Progress: ${state.current_position.progress}

## Execution Metrics
Plans completed: ${state.execution_metrics.plans_completed}
Tasks completed: ${state.execution_metrics.tasks_completed}
Total commits: ${state.execution_metrics.total_commits}
Duration: ${state.execution_metrics.duration}

## Accumulated Context

### Decisions Made
${formatDecisionsTable(state.accumulated_context.decisions)}

### Deferred Issues
${formatDeferredIssues(state.accumulated_context.deferred_issues)}

### Blockers
${state.accumulated_context.blockers.length > 0
  ? state.accumulated_context.blockers.map(b => `- ${b}`).join('\n')
  : 'None.'}

## Session Continuity
Last session: ${state.session_continuity.last_session}
Stopped at: ${state.session_continuity.stopped_at}
Resume agent: ${state.session_continuity.resume_agent}

## Rollback Reference
start_commit: ${state.rollback_reference.start_commit}
`;
}
```

### Step 8: Write Atomically

```typescript
function writeState(state_path: string, state: StateData): void {
  const content = generateStateMarkdown(state);
  const target = `${state_path}/STATE.md`;

  // Use atomic write pattern
  write_atomic(target, content);
}
```

## Complete Update Flow

```typescript
async function updateState(input: UpdateStateInput): Promise<void> {
  // 1. Read current state
  let state = readState(input.state_path);

  // 2. Update metrics
  state = updateMetrics(state, input.plan_result);

  // 3. Update position and progress
  state = updatePosition(state, input.plan_number, input.plan_result, input.total_plans);

  // 4. Accumulate context
  state = accumulateContext(state, input.plan_result, input.plan_number);

  // 5. Update session info
  state = updateSession(state, input.plan_number);

  // 6. Write atomically
  writeState(input.state_path, state);
}
```

## Error Handling

| Error | Action |
|-------|--------|
| STATE.md missing | Create from template, log warning |
| Parse error | Attempt recovery from backup, fail if none |
| Write failure | Retry atomic write, abort run if persists |
| Invalid plan_result | Skip update, log to ISSUES.md |

## State Transitions

```
Initializing → Transforming → Executing → Complete
     ↓              ↓            ↓
   (error)       (error)     (partial)
     ↓              ↓            ↓
   Failed        Failed       Failed
```

Each state update moves through these transitions based on plan results.
