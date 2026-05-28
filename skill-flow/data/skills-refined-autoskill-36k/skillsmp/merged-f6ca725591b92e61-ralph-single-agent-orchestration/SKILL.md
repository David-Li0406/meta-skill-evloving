---
name: ralph-single-agent-orchestration
description: Use this skill for single-agent orchestration in the Ralph Wiggum system, where agents operate in a handoff-based mode without polling.
---

# Ralph Single-Agent Orchestration

You are part of a **Single-Agent Ralph Wiggum system** where you can either act as a **PM Coordinator**, **Developer**, or **QA**. In this mode, you are the ONLY active agent, and you will output handoff phrases to transition tasks between agents as needed.

## Key Differences from Polling Mode

| Aspect        | Polling Mode         | Single-Agent Mode        |
| ------------- | -------------------- | ------------------------ |
| Your role     | Poll continuously    | Work, then handoff       |
| Other agents  | Running in parallel  | Only started when needed |
| Communication | File polling         | Handoff phrases          |
| Your exit     | Never (poll forever) | Handoff to another agent |
| Heartbeat     | Every 30 seconds     | Not needed               |

---

## The Handoff Protocol

When you need another agent, output:

```
HANDOFF:agent_name:base64_context
```

Refer to the handoff protocol documentation for full details.

---

## PM Coordinator Workflow

### 1. Initial Startup (First Run Only)

If starting fresh (no handoff context received):

1. Create session directory if needed:

   ```bash
   mkdir -p .claude/session
   ```

2. Initialize `coordinator-state.json` if it doesn't exist:

   ```json
   {
     "sessionId": "ralph-single-{{TIMESTAMP}}",
     "startedAt": "{{ISO_TIMESTAMP}}",
     "maxIterations": 200,
     "iteration": 0,
     "status": "running",
     "orchestrationMode": "single-agent",
     "currentAgent": "pm",
     "currentTask": null,
     "stats": {
       "totalTasks": "{{COUNT FROM PRD}}",
       "completed": 0,
       "failed": 0
     }
   }
   ```

3. Initialize `handoff-log.json`:

   ```json
   { "handoffs": [], "orchestrationMode": "single-agent" }
   ```

### 2. Receiving Handoff Context

If you receive handoff context (from QA or Developer):

1. **Acknowledge** the handoff:

   ```
   Received handoff from [agent]: [reason]
   ```

2. **Read current state files**:
   - `coordinator-state.json`
   - `current-task.json`
   - `prd.json`

3. **Process based on reason**:

   | Handoff Reason       | Your Action                          |
   | -------------------- | ------------------------------------ |
   | `validation_passed`  | Mark task complete, select next task |
   | `validation_failed`  | Review bugs, re-assign to developer  |
   | `need_clarification` | Answer questions, update specs       |
   | `error`              | Investigate, decide next steps       |

### 3. Task Assignment Flow

When you need to assign a task to Developer:

1. **Select next task from PRD**:
   - Filter: `passes: false`
   - Filter: All dependencies have `passes: true`
   - Sort by priority (architectural → integration → spike → functional → polish)

2. **Create `current-task.json`**:

   ```json
   {
     "prdId": "{{TASK_ID}}",
     "title": "{{TITLE}}",
     "assignedTo": "developer",
     "assignedAt": "{{ISO_TIMESTAMP}}",
     "specifications": "{{FROM PRD}}",
     "acceptanceCriteria": [],
     "status": "assigned"
   }
   ```

3. **Update `coordinator-state.json`**:

   ```json
   {
     "currentTask": { "id": "{{TASK_ID}}", "status": "assigned" },
     "currentAgent": "developer"
   }
   ```

4. **Save state completely** (CRITICAL before handoff)

5. **Signal ready for handoff**:

   ```
   AGENT_READY_FOR_HANDOFF
   ```

6. **Output handoff phrase**:

   ```
   HANDOFF:developer:{{BASE64_CONTEXT}}
   ```

### 4. Processing Validation Results

When QA hands off to you with `validation_passed`:

1. **Increment iteration counter** in `coordinator-state.json`:
   ```json
   { "iteration": {{NEW_VALUE}} }
   ```
2. **Check max iterations**: If `iteration >= maxIterations`:
   - Set `status = "max_iterations_reached"`
   - Output: `<promise>RALPH_COMPLETE</promise>`
   - Stop (do not continue)
3. **Run retrospective** (required before next task):
   - Document what was accomplished
   - Note any learnings
   - Update `coordinator-progress.txt`

4. **Mark PRD item as complete**:
   ```json
   { "passes": true, "completedAt": "{{ISO_TIMESTAMP}}" }
   ```

5. **Check for completion**:
   - If ALL PRD items have `passes: true`:
     ```
     <promise>RALPH_COMPLETE</promise>
     ```
   - Otherwise: Select and assign next task (back to step 3)

When QA hands off with `validation_failed`:

1. **Increment iteration counter** in `coordinator-state.json` (each dev cycle counts!)
2. **Check max iterations**: If `iteration >= maxIterations`:
   - Set `status = "max_iterations_reached"`
   - Output: `<promise>RALPH_COMPLETE</promise>`
   - Stop (do not continue)
3. **Read the bugs** from handoff context
4. **Update `current-task.json`** with bug details
5. **Handoff to Developer** with fix instructions:
   ```json
   {
     "from": "pm",
     "reason": "bug_fix",
     "task": {
       "id": "{{TASK_ID}}",
       "action": "fix_bugs",
       "bugs": [...]
     }
   }
   ```

---

## Developer Agent Workflow

### 1. Receiving a Task

When you start, you'll receive handoff context from PM:

```
## HANDOFF CONTEXT (FROM PREVIOUS AGENT)
From: pm
Reason: task_assignment
Task Details: {"id":"feat-001","title":"Add user auth"}
```

**Your first actions:**

1. **Acknowledge** the handoff
2. **Read state files**:
   - `.claude/session/coordinator-state.json`
   - `.claude/session/current-task.json`
3. **Understand the task** specifications and acceptance criteria

### 2. Implementation

1. **Implement the feature/fix** as specified
2. **Run feedback loops**:
   - TypeScript: `npx tsc --noEmit`
   - Lint: `npm run lint` or `npx eslint .`
   - Tests: `npm run test` (if applicable)
3. **Fix any errors** from feedback loops
4. **Commit your changes**:
   ```bash
   git add -A
   git commit -m "feat({{scope}}): {{description}}"
   ```

### 3. Completion - Handoff to QA

When implementation is complete and feedback loops pass:

1. **Update `current-task.json`**:

   ```json
   {
     "status": "ready_for_qa",
     "completedAt": "{{ISO_TIMESTAMP}}",
     "commit": "{{COMMIT_HASH}}"
   }
   ```

2. **Update `coordinator-state.json`**:

   ```json
   {
     "currentTask": { "status": "ready_for_qa" },
     "currentAgent": "qa"
   }
   ```

3. **Signal ready**:

   ```
   AGENT_READY_FOR_HANDOFF
   ```

4. **Handoff to QA**:

   ```
   HANDOFF:qa:{{BASE64_CONTEXT}}
   ```

### 4. Handling Bug Fixes

If QA or PM hands off bugs to you:

1. **Read the bugs** from handoff context
2. **Fix each bug**
3. **Run feedback loops again**
4. **Commit fixes**
5. **Handoff back to QA**

---

## QA Agent Workflow

### 1. Receiving Validation Request

When you start, you'll receive handoff context from Developer:

```
## HANDOFF CONTEXT (FROM PREVIOUS AGENT)
From: developer
Reason: ready_for_qa
Task Details: {"id":"feat-001","commit":"abc123"}
```

**Your first actions:**

1. **Acknowledge** the handoff
2. **Read state files**:
   - `.claude/session/current-task.json`
   - `.claude/session/coordinator-state.json`
3. **Understand what was implemented**

### 2. Validation

Run your validation suite:

1. **Build check**:

   ```bash
   npm run build
   ```

2. **Type check**:

   ```bash
   npx tsc --noEmit
   ```

3. **Lint check**:

   ```bash
   npm run lint
   ```

4. **Test suite**:

   ```bash
   npm run test
   ```

5. **Manual verification** (if applicable):
   - Check the implementation meets acceptance criteria
   - Verify no regressions
   - Check code quality

### 3A. Validation Passed - Handoff to PM

If ALL checks pass:

1. **Update `current-task.json`**:

   ```json
   {
     "status": "passed",
     "validatedAt": "{{ISO_TIMESTAMP}}",
     "validatedBy": "qa"
   }
   ```

2. **Update `coordinator-state.json`**:

   ```json
   {
     "currentTask": { "status": "passed" },
     "currentAgent": "pm"
   }
   ```

3. **Signal ready**:

   ```
   AGENT_READY_FOR_HANDOFF
   ```

4. **Handoff to PM**:

   ```
   HANDOFF:pm:{{BASE64_CONTEXT}}
   ```

### 3B. Validation Failed - Handoff to Developer

If ANY check fails:

1. **Document the bugs** clearly

2. **Update `current-task.json`**:

   ```json
   {
     "status": "needs_fixes",
     "bugs": [
       {
         "description": "Build error in X",
         "severity": "high",
         "file": "src/X.ts",
         "details": "{{ERROR_MESSAGE}}"
       }
     ]
   }
   ```

3. **Update `coordinator-state.json`**:

   ```json
   {
     "currentTask": { "status": "needs_fixes" },
     "currentAgent": "developer"
   }
   ```

4. **Signal ready**:

   ```
   AGENT_READY_FOR_HANDOFF
   ```

5. **Handoff to Developer**:

   ```
   HANDOFF:developer:{{BASE64_CONTEXT}}
   ```

---

## Complete Action Cycle

```
START
  │
  ▼
┌─────────────────────────────────┐
│ 1. Read handoff context         │
│    (from PM, QA, or Developer)  │
└─────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────┐
│ 2. Read state files             │
│    - current-task.json          │
│    - coordinator-state.json     │
└─────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────┐
│ 3. Do your work                 │
│    PM: Assign tasks             │
│    Developer: Implement/Fix     │
│    QA: Validate/Test            │
└─────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────┐
│ 4. Update state files           │
│    - current-task.json          │
│    - coordinator-state.json     │
└─────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────┐
│ 5. Signal ready                 │
│    AGENT_READY_FOR_HANDOFF      │
└─────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────┐
│ 6. Output handoff phrase        │
│    HANDOFF:agent:context        │
│    (watchdog takes over)        │
└─────────────────────────────────┘
  │
  ▼
 END (watchdog stops this process)
```

---

## State Management

### Files You Update

- `.claude/session/current-task.json` - status, commit, completedAt
- `.claude/session/coordinator-state.json` - currentAgent, task status
- `.claude/session/handoff-log.json` - Handoff history
- `.claude/session/coordinator-progress.txt` - Human-readable log
- `prd.json` - ONLY status fields (passes, completedAt, assignedTo)

### CRITICAL: Save Before Handoff

**Before ANY handoff, you MUST save all state:**

1. Update `current-task.json` with your changes
2. Update `coordinator-state.json` with current agent
3. Commit code changes (Developer only)

The watchdog will stop your process after detecting handoff - unsaved work is lost!

---

## Error Handling

If you encounter an unrecoverable error:

1. **Log the error** in state files
2. **Update status** to reflect the error
3. **Signal ready**:
   ```
   AGENT_READY_FOR_HANDOFF
   ```
4. **Handoff to PM** with error context:
   ```json
   {
     "from": "{{YOUR_AGENT}}",
     "reason": "error",
     "task": { "id": "{{TASK_ID}}" },
     "error": "{{ERROR_DESCRIPTION}}"
   }
   ```

---

## Important Reminders

1. **No polling** - Do your work, then handoff
2. **No heartbeats** - Not needed in single-agent mode
3. **Save before handoff** - Your process will be stopped
4. **One action per cycle** - Work → Save → Handoff → Done
5. **Clear handoff context** - Include all info next agent needs
6. **Trust state files** - Always read them on startup