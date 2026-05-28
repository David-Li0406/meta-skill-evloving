# Spawn Plan Executor Workflow

## Purpose

Spawn a **fresh subagent** to execute a single PLAN.md file using Claude Code's Task tool.

**CRITICAL**: This workflow creates a new agent with fresh 200k context at 0% usage. This is essential for maintaining quality across multiple plans.

## Why This Matters

```
Context degradation without fresh spawning:
Plan 1: 0-30% → good quality
Plan 2: 30-60% → degrading
Plan 3: 60-90% → poor quality

With fresh spawning (this workflow):
Plan 1: 0-30% (fresh) → peak quality
Plan 2: 0-30% (fresh) → peak quality
Plan 3: 0-30% (fresh) → peak quality
```

## Inputs

```typescript
interface SpawnExecutorInput {
  plan_path: string;        // Path to PLAN.md file
  plan_number: string;      // e.g., "02"
  task_group: string;       // e.g., "API Endpoints"
  state_path: string;       // Path to .long-run/ directory
  spec_path: string;        // Path to spec directory
  checkpoint?: Checkpoint;  // Optional checkpoint for resume
  resume_from_task?: number; // Task number to resume from (default: 1)
}
```

## Spawn Protocol

### Step 1: Read Plan Content

```typescript
const plan_content = read_file(input.plan_path);
```

### Step 2: Read Context Files

```typescript
const spec_content = read_file(`${input.spec_path}/spec.md`);
const requirements = read_file(`${input.spec_path}/planning/requirements.md`) || "";
```

### Step 3: Build Executor Prompt

```typescript
function buildExecutorPrompt(input: SpawnExecutorInput): string {
  const resume_from = input.resume_from_task || 1;
  const checkpoint_json = input.checkpoint
    ? JSON.stringify(input.checkpoint, null, 2)
    : "Starting fresh";

  return `
You are a long-run-executor subagent. Execute this plan with minimal stops.

## Plan to Execute

${plan_content}

## Context

### Spec
${spec_content}

### Requirements
${requirements}

## Paths

- tasks.md: ${input.spec_path}/tasks.md
- checkpoint: ${input.state_path}/plans/${input.plan_number}-CHECKPOINT.json
- issues: ${input.state_path}/ISSUES.md

## Resume State

${input.checkpoint ? `Resuming from Task ${resume_from}. Previous progress:\n${checkpoint_json}` : "Starting fresh from Task 1."}

## Instructions

1. Execute tasks sequentially starting from Task ${resume_from}
2. Apply deviation rules:
   - Rules 1-3: Auto-fix and continue (log what you fixed)
   - Rule 4: STOP immediately and return NEEDS_DECISION
   - Rule 5: Log to ISSUES.md, continue
3. After each task completes:
   - Stage ONLY files listed in <files>
   - Commit: "{type}(${input.plan_number}): {task-name}"
   - Update checkpoint at ${input.state_path}/plans/${input.plan_number}-CHECKPOINT.json
   - Mark complete in tasks.md
4. Output final status between OUTPUT_JSON_START/END markers

## Output Format

Your final output MUST include:

\`\`\`
OUTPUT_JSON_START
{
  "status": "COMPLETED" | "NEEDS_DECISION" | "NEEDS_ACTION" | "FAILED",
  ... status-specific fields (see long-run-executor agent for full schema)
}
OUTPUT_JSON_END
\`\`\`

Begin execution now.
`;
}
```

### Step 4: Invoke Task Tool (CRITICAL)

**This is where the fresh context is created.**

```typescript
// SPAWN FRESH SUBAGENT via Task tool
// This creates a NEW agent with fresh 200k context!
const result = Task({
  subagent_type: "general-purpose",
  description: `Execute plan ${input.plan_number}: ${input.task_group}`,
  prompt: buildExecutorPrompt(input)
});
```

### Step 5: Track Agent

Before waiting for result, track the spawned agent:

```typescript
// Update agent-history.json
const history = read_json(`${input.state_path}/agent-history.json`) || { agents: [] };
history.agents.push({
  agent_id: result.agent_id,
  task_description: `Execute plan ${input.plan_number}`,
  plan: input.plan_number,
  task_group: input.task_group,
  timestamp: new Date().toISOString(),
  status: "spawned"
});
write_json(`${input.state_path}/agent-history.json`, history);

// Write transient file for quick resume lookup
write_file(`${input.state_path}/current-agent-id.txt`, result.agent_id);
```

### Step 6: Wait for Completion

The Task tool is **synchronous** - it returns when the subagent completes or stops.

```typescript
// Task tool blocks until subagent finishes
const output = await result;

// Clean up transient file
delete_file(`${input.state_path}/current-agent-id.txt`);

// Parse and return result
return parseExecutorOutput(output);
```

## Output Parsing

```typescript
function parseExecutorOutput(output: string): ExecutorResult {
  // Extract JSON from markers
  const match = output.match(/OUTPUT_JSON_START\n([\s\S]*?)\nOUTPUT_JSON_END/);

  if (!match) {
    return {
      status: "unknown",
      raw_output: output,
      error: "Could not find OUTPUT_JSON_START/END markers"
    };
  }

  try {
    const data = JSON.parse(match[1]);

    switch (data.status) {
      case "COMPLETED":
        return {
          status: "completed",
          tasks_completed: data.tasks_completed,
          commits: data.commits,
          files_modified: data.files_modified,
          deviations: data.deviations || []
        };

      case "NEEDS_DECISION":
        return {
          status: "needs_decision",
          blocked_at: data.blocked_at,
          decision_needed: data.decision_needed,
          options: data.options,
          context: data.context
        };

      case "NEEDS_ACTION":
        return {
          status: "needs_action",
          blocked_at: data.blocked_at,
          action_needed: data.action_needed,
          instructions: data.instructions,
          verification: data.verification
        };

      case "FAILED":
        return {
          status: "failed",
          failed_at: data.failed_at,
          error: data.error,
          output: data.output,
          retry_count: data.retry_count,
          partial_commits: data.partial_commits || []
        };

      default:
        return {
          status: "unknown",
          raw_output: output,
          parsed_data: data
        };
    }
  } catch (e) {
    return {
      status: "unknown",
      raw_output: output,
      error: `JSON parse error: ${e.message}`
    };
  }
}
```

## Resume Capability

### Using Task Resume Parameter

If the Task tool supports resuming an interrupted agent:

```typescript
// Check for interrupted agent
const current_agent_file = `${input.state_path}/current-agent-id.txt`;
if (file_exists(current_agent_file)) {
  const interrupted_agent_id = read_file(current_agent_file).trim();

  // Try to resume
  const result = Task({
    resume: interrupted_agent_id,
    subagent_type: "general-purpose"
  });

  return parseExecutorOutput(await result);
}
```

### Fallback: Re-spawn with Checkpoint

If resume not supported or fails, re-spawn with checkpoint context:

```typescript
function respawnWithCheckpoint(input: SpawnExecutorInput): ExecutorResult {
  // Read checkpoint
  const checkpoint_path = `${input.state_path}/plans/${input.plan_number}-CHECKPOINT.json`;
  const checkpoint = read_json(checkpoint_path);

  // Spawn new agent with checkpoint context
  return spawnExecutor({
    ...input,
    checkpoint: checkpoint,
    resume_from_task: checkpoint.last_completed_task + 1
  });
}
```

## Error Handling

| Error | Action |
|-------|--------|
| Task tool unavailable | Return error, let orchestrator handle |
| Agent timeout | Return timeout status with partial progress |
| Network error | Retry spawn 3 times, then return error |
| Invalid output format | Return "unknown" status with raw output |

## Type Definitions

```typescript
interface ExecutorResult {
  status: "completed" | "needs_decision" | "needs_action" | "failed" | "unknown";

  // Completed
  tasks_completed?: string;
  commits?: string[];
  files_modified?: string[];
  deviations?: Array<{ rule: number; description: string }>;

  // Needs Decision
  blocked_at?: string;
  decision_needed?: string;
  options?: Array<{ key: string; description: string }>;
  context?: string;

  // Needs Action
  action_needed?: string;
  instructions?: string[];
  verification?: string;

  // Failed
  failed_at?: string;
  error?: string;
  output?: string;
  retry_count?: number;
  partial_commits?: string[];

  // Unknown
  raw_output?: string;
  parsed_data?: any;
}

interface Checkpoint {
  plan: string;
  last_completed_task: number;
  total_tasks: number;
  task_commits: Record<string, string>;
  files_modified: string[];
  updated_at: string;
}
```
