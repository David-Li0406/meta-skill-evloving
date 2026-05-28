# Detect Resume State

## Purpose
Check for interrupted execution and determine resume point.

## Inputs
- `spec_path`: Path to spec folder
- `state_path`: Path to .long-run/ directory

## Workflow

### Step 1: Check for Active Agent
```
IF {state_path}/current-agent-id.txt exists:
  agent_id = read file
  history = read agent-history.json
  entry = find entry by agent_id

  Return {
    interrupted: true,
    type: "active_agent",
    agent_id: agent_id,
    plan: entry.plan,
    status: entry.status,
    timestamp: entry.timestamp
  }
```

### Step 2: Check for Checkpoint
```
FOR each plan in {state_path}/plans/:
  checkpoint_path = {plan_number}-CHECKPOINT.json
  IF checkpoint exists:
    checkpoint = read JSON
    IF checkpoint.last_completed_task < checkpoint.total_tasks:
      Return {
        interrupted: true,
        type: "partial_plan",
        plan: checkpoint.plan,
        completed_tasks: checkpoint.last_completed_task,
        total_tasks: checkpoint.total_tasks,
        last_commit: checkpoint.task_commits[checkpoint.last_completed_task]
      }
```

### Step 3: Check STATE.md Status
```
state = read STATE.md
IF state.status != "Complete":
  current_plan = state.current_position.plan

  # Find last completed plan
  completed_plans = list {state_path}/summaries/*-SUMMARY.md
  last_completed = max(completed_plans by number) or 0

  IF current_plan > last_completed:
    Return {
      interrupted: true,
      type: "between_plans",
      resume_from: current_plan,
      last_completed: last_completed
    }
```

### Step 4: Check for Pending Clarification
```
IF {state_path}/clarifications.md exists:
  clarifications = parse file
  pending = filter(status == "pending")

  IF pending.length > 0:
    Return {
      interrupted: true,
      type: "pending_clarification",
      task_group: pending[0].task_group,
      question: pending[0].question
    }
```

### Step 5: No Interruption Found
```
Return {
  interrupted: false,
  completed_plans: count summaries,
  total_plans: count plans
}
```

## Resume Options

### For Active Agent
```
"Found interrupted execution of Plan {plan}.
Agent {agent_id} was spawned at {timestamp}.

Options:
1. Resume agent (if Task resume supported)
2. Re-spawn with checkpoint context
3. Skip to next plan
4. Start fresh (clear all state)"
```

### For Partial Plan
```
"Plan {plan} was interrupted after Task {completed}/{total}.
Commits made: {commits}

Options:
1. Resume from Task {completed + 1}
2. Restart plan from beginning
3. Skip to next plan
4. Start fresh"
```

### For Pending Clarification
```
"Execution paused waiting for clarification on Task Group {N}.

[Original question]

Options:
1. Answer now
2. Skip this task group
3. Start fresh"
```

## Output

```typescript
interface ResumeState {
  interrupted: boolean;
  type?: "active_agent" | "partial_plan" | "between_plans" | "pending_clarification";
  // Type-specific fields
  agent_id?: string;
  plan?: string;
  completed_tasks?: number;
  total_tasks?: number;
  last_commit?: string;
  resume_from?: number;
  question?: string;
}
```
