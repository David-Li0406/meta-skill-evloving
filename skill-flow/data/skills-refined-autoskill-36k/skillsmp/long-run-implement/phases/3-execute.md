# Phase 3: Execute

## Purpose

Execute PLAN.md files by **spawning a fresh subagent for each plan** via the Task tool.

**CRITICAL**: Each plan MUST execute in a fresh context to prevent quality degradation.

## Why Fresh Contexts

```
WITHOUT fresh contexts (BAD):
Plan 1: 0-30% context → good
Plan 2: 30-60% context → degrading
Plan 3: 60-90% context → poor quality

WITH fresh contexts (GOOD):
Plan 1: fresh subagent (0-30%) → peak quality
Plan 2: fresh subagent (0-30%) → peak quality
Plan 3: fresh subagent (0-30%) → peak quality
```

## Inputs (from Phase 2)

- `plans`: Array of plan paths sorted by number
- `dependencies`: Dependency graph
- `spec_path`: Path to spec folder
- `state_path`: Path to .long-run/ directory

## Workflow

### Step 1: Execution Loop

```
FOR each plan_path in plans (sorted by number):
  plan_number = extract from filename (e.g., "01" from "01-PLAN.md")

  # Check if already completed
  IF {state_path}/summaries/{plan_number}-SUMMARY.md exists:
    summary = read summary
    IF summary.status == "completed":
      Log: "Plan {plan_number} already completed, skipping"
      CONTINUE to next plan

  # Check for checkpoint (partial completion)
  checkpoint_path = {state_path}/plans/{plan_number}-CHECKPOINT.json
  IF checkpoint exists:
    checkpoint = read checkpoint
    resume_from_task = checkpoint.last_completed_task + 1
  ELSE:
    resume_from_task = 1

  # Validate dependencies
  validation = {{workflows/long-run/validate-dependencies}}
    plan_path: plan_path
    state_path: state_path

  IF not validation.valid:
    Handle dependency issue (see Step 4)
    Continue or stop based on user choice

  # Execute plan in fresh context
  GOTO Step 2: Spawn Fresh Subagent
```

### Step 2: Spawn Fresh Subagent (CRITICAL)

**This is where quality is preserved - each plan gets fresh 200k context.**

```typescript
// 1. Read plan content
const plan_content = read_file(plan_path);

// 2. Read context files
const spec_content = read_file(`${spec_path}/spec.md`);
const requirements = read_file(`${spec_path}/planning/requirements.md`) || "";

// 3. Read checkpoint if exists
const checkpoint = file_exists(checkpoint_path)
  ? read_file(checkpoint_path)
  : null;

// 4. Build executor prompt (see template below)
const prompt = buildExecutorPrompt({
  plan_content,
  plan_number,
  checkpoint,
  spec_content,
  requirements,
  state_path,
  tasks_md_path: `${spec_path}/tasks.md`,
  resume_from_task
});

// 5. SPAWN FRESH SUBAGENT via Task tool
//    This creates a NEW agent with fresh 200k context!
const result = Task({
  subagent_type: "general-purpose",
  description: `Execute plan ${plan_number}: ${task_group_name}`,
  prompt: prompt
});

// 6. Track the spawned agent
track_agent({
  agent_id: result.agent_id,
  plan: plan_number,
  timestamp: new Date().toISOString(),
  status: "spawned"
});

// 7. Write transient file for resume lookup
write_file(`${state_path}/current-agent-id.txt`, result.agent_id);

// 8. Wait for completion (Task tool is synchronous)
const output = await result;

// 9. Parse and handle response
GOTO Step 3: Handle Response
```

### Step 3: Handle Subagent Response

Parse the `OUTPUT_JSON_START`/`OUTPUT_JSON_END` block from subagent output:

```
// Extract JSON from output
const json_match = output.match(/OUTPUT_JSON_START\n([\s\S]*?)\nOUTPUT_JSON_END/);
const response = JSON.parse(json_match[1]);

SWITCH response.status:

  CASE "COMPLETED":
    # Success path
    - Update agent-history.json: status = "completed"
    - Delete current-agent-id.txt
    - Create {plan_number}-SUMMARY.md from response:
      - tasks_completed
      - commits
      - files_modified
      - deviations applied
    - Update STATE.md progress
    - CONTINUE to next plan

  CASE "NEEDS_DECISION":
    # Rule 4 architectural decision
    - Present decision to user:
      "Architectural decision required at {response.blocked_at}

       {response.decision_needed}

       Options:
       1. {option1.key}: {option1.description}
       2. {option2.key}: {option2.description}
       3. {option3.key}: {option3.description}

       Context: {response.context}

       Select (1-N):"

    - Wait for user choice
    - IF user chooses "defer":
        Log to ISSUES.md
        Create skipped summary
        CONTINUE to next plan
    - ELSE:
        Re-spawn subagent with decision context
        (Include: "User decided: {choice}. Continue from {blocked_at}.")

  CASE "NEEDS_ACTION":
    # External action required (email verification, etc.)
    - Present instructions:
      "External action required at {response.blocked_at}

       {response.action_needed}

       Steps:
       {numbered instructions}

       Type 'done' when complete:"

    - Wait for user confirmation
    - Re-spawn subagent to verify action completed
      (Include: "User completed action. Verify and continue.")

  CASE "FAILED":
    # Execution error after retries
    - Present error:
      "Plan {plan_number} failed at {response.failed_at}

       Error: {response.error}
       Output: {response.output}
       Retry count: {response.retry_count}
       Partial commits: {response.partial_commits}

       Options:
       1. Retry from failed task
       2. Skip to next plan
       3. Abort execution"

    - Handle user choice:
      - Retry: Re-spawn subagent from failed task
      - Skip: Create failed/skipped summary, continue
      - Abort: Save state, exit
```

### Step 4: Dependency Issue Handling

```
IF validation.status in ["failed", "partial", "skipped", "timeout"]:
  Present options from validation.options

  SWITCH user_choice:
    CASE "skip":
      Create skipped SUMMARY for current plan
      CONTINUE to next plan

    CASE "retry" | "resume":
      Set current plan to dependency
      Restart execution from dependency

    CASE "ignore":
      Log warning in STATE.md
      Proceed with execution

    CASE "cascade":
      Create skipped SUMMARY
      CONTINUE to next plan

    CASE "clarify":
      Load clarification for skipped dependency
      Present to user
      On response, retry from dependency
```

### Step 5: Update Progress

After each plan:

```
completed = count summaries with status "completed"
total = count plans
percentage = (completed / total) * 100

Update STATE.md:
  ## Current Position
  - Current plan: {next_plan_number}
  - Plans completed: {completed}/{total}
  - Progress: [████████░░] {percentage}%
```

### Step 6: Completion

When all plans processed:

```
Pass to Phase 4:
  - completed_plans: count
  - failed_plans: list with reasons
  - skipped_plans: list with reasons
  - total_commits: sum from all summaries
  - total_files: unique files from all summaries
```

## Executor Prompt Template

```markdown
You are a long-run-executor subagent. Execute this plan with minimal stops.

## Plan to Execute

{plan_content}

## Context

### Spec
{spec_content}

### Requirements
{requirements}

## Paths

- tasks.md: {tasks_md_path}
- checkpoint: {state_path}/plans/{plan_number}-CHECKPOINT.json
- issues: {state_path}/ISSUES.md

## Resume State

{IF checkpoint exists}
Resuming from checkpoint. Skip to Task {resume_from_task}.
Previous progress:
{checkpoint JSON}
{ELSE}
Starting fresh from Task 1.
{ENDIF}

## Instructions

1. Execute tasks sequentially starting from Task {resume_from_task}
2. Apply deviation rules:
   - Rules 1-3: Auto-fix and continue (log what you fixed)
   - Rule 4: STOP immediately and return NEEDS_DECISION
   - Rule 5: Log to ISSUES.md, continue
3. After each task completes:
   - Stage ONLY files listed in <files>
   - Commit: "{type}({plan_number}): {task-name}"
   - Update checkpoint file at {checkpoint_path}
   - Mark complete in tasks.md
4. On completion or stop, output status between OUTPUT_JSON_START/END markers

## Output Format

Your final output MUST include:

\`\`\`
OUTPUT_JSON_START
{
  "status": "COMPLETED" | "NEEDS_DECISION" | "NEEDS_ACTION" | "FAILED",
  ... status-specific fields
}
OUTPUT_JSON_END
\`\`\`

Begin execution now.
```

## Error Handling

```
ON Task tool failure:
  Log error to STATE.md
  Offer retry to user
  If retry fails 3 times, abort with state saved

ON subagent timeout:
  Check timeout_action from STATE.md config:
    IF "prompt": Present timeout options to user
    IF "skip": Mark as timeout, create summary, continue
    IF "fail": Abort execution with state saved

ON invalid JSON output:
  Treat as unknown status
  Show raw output to user
  Ask: "How should we proceed?"

ON network/system error:
  Save current state
  Log error
  Offer retry
```

## Key Principle

**NEVER execute plan tasks in the orchestrator's context.**

Always use the Task tool to spawn a fresh subagent. This is non-negotiable for quality preservation.
