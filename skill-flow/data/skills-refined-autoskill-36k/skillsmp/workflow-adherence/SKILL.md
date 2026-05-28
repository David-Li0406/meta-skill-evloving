---
name: Workflow Adherence
description: Essential rules for ensuring agents complete full multi-step workflows without stopping prematurely.
---

# Workflow Adherence Skill

Agents often stop after a single tool call or partial completion. This skill enforces **autonomous persistence**.

## 1. The Rule of Continuity

**YOU MUST NOT STOP** until the entire task as defined in your instructions or the active plan is COMPLETE.

- **Bad**: Executing Step 1, then waiting for the user.
- **Good**: Executing Step 1, verifying it, executing Step 2, verifying it... until the end.

## 2. Handling Workflow Files (*.workflow.md)

If you are executing a Workflow:
1.  **Read the whole file**: Understand the full sequence.
2.  **Iterate**: Execute the current phase completely.
3.  **Handoff**: If the workflow specifies a handoff (e.g., "Passed to Analyst"), you MUST use the appropriate tool or instruction to trigger that handoff (or notify the Orchestrator/User to do so).
4.  **Do not halt** between steps of the *same* phase.

## 3. Handling Plans (Implementing/Planning)

If you are following a numbered list (e.g., a Plan or Checklist):
- **Batching**: You may batch multiple small tool calls (e.g., creating 3 files) if safe.
- **Verification Loop**: After every major action, verify success. If it fails, **fix it immediately**. Do not stop and report failure unless you are stuck after retries.
- **Completion**: Only output "Task Complete" or similar status when **ALL** items are checked off.

## 4. Anti-Stalling Triggers

If you feel the urge to stop and ask "What next?", **CHECK YOUR INSTRUCTIONS FIRST**.
- Is there a next step in the Plan? -> **DO IT.**
- Is there a next phase in the Workflow? -> **DO IT.**
- Are there unresolved questions? -> **Resolve them yourself** (if possible) using research tools.

## 5. Explicit Stop Conditions

ONLY stop if:
1.  You need **User Approval** (e.g., Critical Plan Change, Deployment).
2.  You are **Technically Blocked** (e.g., Missing credentials, severe error).
3.  The Task is **Fully Complete** (All deliverables created and verified).
