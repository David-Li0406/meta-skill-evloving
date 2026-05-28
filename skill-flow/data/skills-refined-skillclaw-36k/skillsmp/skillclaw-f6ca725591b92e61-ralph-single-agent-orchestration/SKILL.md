---
name: ralph-single-agent-orchestration
description: Use this skill when you need to manage a single-agent orchestration system, coordinating tasks and handoffs without polling.
---

# Ralph Single-Agent Orchestration

You are the **Coordinator** or **Worker Agent** in a single-agent Ralph Wiggum system. In this mode, you are the ONLY active agent, and you will output handoff phrases to transition tasks between yourself and other agents (Developer or QA) as needed.

## Key Differences from Polling Mode

| Aspect        | Polling Mode         | Single-Agent Mode        |
| ------------- | -------------------- | ------------------------ |
| Your role     | Poll continuously    | Work, then handoff       |
| Other agents  | Running in parallel  | Only started when needed |
| Communication | File polling         | Handoff phrases          |
| Your exit     | Never (poll forever) | Handoff to another agent |

## The Handoff Protocol

When you need another agent or complete your work, output:

```
HANDOFF:agent_name:base64_context
```

Refer to the handoff documentation for full protocol details.

## Coordinator Workflow

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
   | `task_assignment`    | Start working on the assigned task   |

## Worker Agent Workflow

### 1. Determine Your Role

Check the `--agent` argument:

- **`developer`**: Implement features, fix bugs, run feedback loops
- **`qa`**: Validate implementations, run tests, check quality

### 2. Receiving a Task

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

### 3. Implementation

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

### 4. Completion - Handoff to QA

When implementation is complete and feedback loops pass:

1. **Update `current-task.json`**:

   ```json
   {
     "status": "ready_for_qa",
     "completedAt": "{{ISO_TIMESTAMP}}"
   }
   ```

2. **Output the handoff** to QA:

   ```
   HANDOFF:qa:base64_context
   ```