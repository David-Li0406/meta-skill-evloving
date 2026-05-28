---
name: plan
description: Create implementation plans following project conventions. Use when planning new features, refactors, or significant changes.
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*), Bash(git log:*), Bash(git branch:*)
---

# Planning Skill

Plan the requested feature or change using the project's planning conventions.

## Process

1. **Invoke the Plan subagent** using the Task tool with `subagent_type=Plan` to thoroughly research the codebase and design an implementation approach. The prompt should include the user's feature request and ask for a complete implementation plan. **Capture the `agentId`** from the Task result - this allows resuming the planning agent for additional context.

2. **After planning is complete**, save the plan to the project's plans directory:
   - Find the next plan number by checking both `plans/` and `plans/archive/` for the highest `NNNN-*` prefix
   - Create `plans/NNNN-feature-name/` directory (use lowercase kebab-case)
   - Write `implementation-plan.md` with the full plan
   - Write `task-list.md` with checkboxes for each task
   - Write `.plan-state.json` with initial state (see format below)

3. **Use this format for implementation-plan.md:**
   ```markdown
   # Feature Name Implementation Plan

   ## Status: 🚧 IN PROGRESS

   ## Overview
   [Brief description of the feature]

   ## Current State
   [Analysis of existing code]

   ## Implementation Approach
   [Detailed plan with phases]

   ## Files to Modify/Create
   [List of files with descriptions]

   ## Testing Strategy
   [How to test the changes]
   ```

4. **Use this format for task-list.md:**
   ```markdown
   # Feature Name Task List

   ## Status: 🚧 IN PROGRESS

   ## Phase 1: Description
   - [ ] **1.1** Task description
   - [ ] **1.2** Another task

   ## Phase 2: Description
   - [ ] **2.1** Task description

   ## Progress Tracking

   | Phase          | Status      | Notes |
   | -------------- | ----------- | ----- |
   | 1 - Phase Name | Not Started |       |
   | 2 - Phase Name | Not Started |       |
   ```

5. **Use this format for .plan-state.json:**
   ```json
   {
     "status": "in_progress",
     "created_at": "2026-01-24T10:30:00Z",
     "updated_at": "2026-01-24T10:30:00Z",
     "planning_agent_id": "abc-123-def",
     "current_task": null,
     "last_session_notes": null,
     "progress": {
       "total": 12,
       "completed": 0
     },
     "commits": []
   }
   ```
   - `status` is always `"in_progress"` for new plans
   - Use the current UTC timestamp for `created_at` and `updated_at`
   - Set `planning_agent_id` to the agentId from the Plan subagent Task result
   - Set `total` to the actual number of tasks in task-list.md
   - `current_task` and `last_session_notes` start as null
   - `commits` is an array that will accumulate commit SHAs as phases complete

6. **Do not commit the plan files**

7. **Present the plan** to the user for approval before any implementation begins

8. **Provide enhanced continuation output** after saving the plan:

   Output format:
   ```
   **Plan saved to:** `plans/NNNN-feature-name/`
   **Created:** YYYY-MM-DD HH:MM UTC
   **Tasks:** 0/N complete
   **Planning agent:** `{agentId}` (resume for additional context)

   **First tasks:**
   - [ ] **1.1** First task description
   - [ ] **1.2** Second task description
   - [ ] **1.3** Third task description

   To continue with implementation, run `/clear` then paste:

   [continuation prompt code block]

   *Plan summary: Brief description of what the plan is about*
   ```

9. **Use this continuation prompt template:**
   ````
   Continue implementing the plan in plans/NNNN-feature-name/

   Read the implementation-plan.md and task-list.md files, then begin with the first incomplete task.

   As you work:
   - Update task-list.md checkboxes (change `- [ ]` to `- [x]`) when completing tasks
   - Update .plan-state.json with current_task and progress.completed count

   When completing a phase:
   - Create a commit with message: "feat(plan-NNNN): Phase N - <phase description>"
   - Add the commit SHA to the `commits` array in .plan-state.json

   Before ending the session, update .plan-state.json with last_session_notes about progress and next steps.

   If you need additional context from the original planning discussion, the planning agent ID is stored in .plan-state.json and can be resumed.
   ````

## Example Output

---

**Plan saved to:** `plans/0006-rust-parser/`
**Created:** 2026-01-24 10:30 UTC
**Tasks:** 0/12 complete
**Planning agent:** `a1b2c3d4-e5f6-7890-abcd-ef1234567890` (resume for additional context)

**First tasks:**
- [ ] **1.1** Create RustParser struct implementing ErrorParser trait
- [ ] **1.2** Add Rust variant to Language enum
- [ ] **1.3** Implement panic message regex patterns

To continue with implementation, run `/clear` and then `/resume` or paste:

```
Continue implementing the plan in plans/0006-rust-parser/

Read the implementation-plan.md and task-list.md files, then begin with the first incomplete task.

As you work:
- Update task-list.md checkboxes (change `- [ ]` to `- [x]`) when completing tasks
- Update .plan-state.json with current_task and progress.completed count

When completing a phase:
- Create a commit with message: "feat(plan-0006): Phase N - <phase description>"
- Add the commit SHA to the `commits` array in .plan-state.json

Before ending the session, update .plan-state.json with last_session_notes about progress and next steps.

If you need additional context from the original planning discussion, the planning agent ID is stored in .plan-state.json and can be resumed.
```

*Plan summary: Add support for parsing Rust panic stack traces*

---
