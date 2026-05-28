---
name: swarm-coordination
description: Use this skill when working on complex tasks that benefit from parallelization and require coordination among multiple agents, ensuring efficient task decomposition and management.
---

# Swarm Coordination Skill

This skill provides guidance for effective multi-agent coordination in OpenCode swarm workflows.

## When to Use Swarm Coordination

**DO swarm when:**

- A task involves 3 or more files.
- There are natural parallel boundaries (e.g., frontend/backend/tests).
- Different specializations are needed for the task.
- Time-to-completion is critical.

**DON'T swarm when:**

- The task involves only 1-2 files.
- There are heavy sequential dependencies.
- The overhead of coordination exceeds the benefits.
- A tight feedback loop is required.

**Heuristic:** If you can describe the task in one sentence without "and", don't swarm.

## MANDATORY: Swarm Mail

**ALL coordination MUST use `swarmmail_*` tools.** This is non-negotiable. Swarm Mail provides:

- File reservations to prevent conflicts.
- Message passing between agents.
- Thread-based coordination tied to cells.

## Task Decomposition Strategy

1. **Analyze the Task**: Identify distinct units of work and determine which can run in parallel.
2. **Choose a Decomposition Strategy**:
   - **Parallel Strategy**: For independent subtasks.
   - **Sequential Strategy**: When order matters.

## Worker Protocol (High-Level)

1. **Initialize Swarm Mail**: 
   ```typescript
   swarmmail_init({
     project_path: "/abs/path/to/project",
     task_description: "bead-id: Task description"
   });
   ```
2. **Query Past Learnings**: 
   ```typescript
   hivemind_find({
     query: "task keywords domain",
     limit: 5
   });
   ```
3. **Load Skills**: 
   ```typescript
   skills_list();
   skills_use({ name: "relevant-skill" });
   ```
4. **Reserve Files**: 
   ```typescript
   swarmmail_reserve({
     paths: ["src/assigned/**"],
     reason: "bead-id: What I'm working on",
     ttl_seconds: 3600
   });
   ```
5. **Do Work**: Implement changes.
6. **Report Progress**: Use `swarm_progress` at 25%, 50%, and 75% completion.
7. **Complete Work**: 
   ```typescript
   swarm_complete();
   ```

## Coordinator Protocol (High-Level)

1. **Initialize Swarm Mail**.
2. **Query Past Learnings**.
3. **Decompose Tasks**: Use `swarm_plan_prompt` and `swarm_validate_decomposition`.
4. **Spawn Workers**: Assign explicit file lists.
5. **Review Worker Output**: Use `swarm_review` and `swarm_review_feedback`.
6. **Record Outcomes**: Use `swarm_complete`.
7. **Store Learnings**: Use `hivemind_store` after swarm completion.

## Tool Access

This skill is configured with `tools: ["*"]` per user choice. If you need curated access later, replace the wildcard with explicit tool lists.