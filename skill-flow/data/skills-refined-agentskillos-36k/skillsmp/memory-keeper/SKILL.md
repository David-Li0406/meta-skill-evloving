---
name: memory-keeper
description: Manages project structure, auto-saves artifacts, and performs recovery protocols. Use this skill at the end of tasks or when encountering errors.
---

# Memory Keeper Skill

## Purpose
To ensure the `Structural Memory` of the agent is preserved, artifacts are backed up, and the agent can recover from context limits.

## Trigger Conditions
- Task completion (finishing a feature).
- User mentions `/retro` or "save memory".
- Agent encounters "Agent terminated due to error" or "Context Limit" errors.

## Workflow Rules

### 1. Structural Integrity Check
-   Verify `agent/rules/` exists.
-   Verify `docs/` exists.
-   Verify `.memory/` exists.
    -   *Action*: If missing, suggest running `init-project` or creating them.

### 2. Auto-Save Protocol
When a major task is done:
1.  **Format Timestamp**: `YYMMDD_HHMM`.
2.  **Target Directory**: `.memory/[Timestamp]_[TaskName]/`.
3.  **Action**: Copy key artifacts (`task.md`, `implementation_plan.md`, `spec.md`) to this folder.
    -   *Note*: Do not perform the copy yourself if it's too heavy. Just remind the user or create a script.

### 3. Recovery Protocol (Agent Terminated Handler)
If the Agent is slow, buggy, or hits token limits:
1.  **Advise User**: "I am hitting context limits. Recommendation: Factory Reset."
2.  **Command**: Suggest running:
    ```bash
    ./antigravity_toolkit.sh full
    ```
3.  **Post-Reset**: Remind user to:
    -   "Import rules and workflows" immediately after reset.
