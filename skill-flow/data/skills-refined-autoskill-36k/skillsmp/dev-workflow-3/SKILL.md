---
name: dev-workflow
description: Task-driven development workflow with TODO tracking. Use when user says "dev", "dev-workflow", or asks to work on tasks, develop features, or proceed with implementation.
---

# Dev Workflow

Implements the Development Flow from AGENTS.md with detailed steps and TODO tracking.

## Auto-Start

When this skill is loaded, IMMEDIATELY begin Phase 1. Do NOT wait for user confirmation.

---

## TODOs

Register ALL TODOs at once when starting Phase 1:

```
# Phase 1: Setup
- [ ] Read docs/README.md, core-concepts.md, architecture.md
- [ ] Check current task with `crew list` and `crew show <id>`
- [ ] Ensure on feature branch
# Phase 2: Implementation
- [ ] Plan implementation and update TODOs (add specific steps here)
# Phase 3: Wrap-up
- [ ] Run final CI check
- [ ] Check test coverage for new code
- [ ] Commit changes (no user confirmation needed)
- [ ] Run `crew complete <id>` to merge and close task
- [ ] Summary report (findings, retrospective)
```

---

## Rules

1. **Start immediately** - Begin Phase 1 upon skill load
2. **Register ALL TODOs at once** - Include all phases when starting Phase 1
3. **Update TODOs in real-time** - Mark in_progress/completed as you work
4. **One item in progress at a time** - Focus and complete before moving on
5. **Add implementation steps** - When reaching "Plan implementation and update TODOs", add specific steps

---

## Reference: Phase Details

### Phase 1: Setup

**Goal**: Understand context and prepare workspace.

1. **Read project docs** (skip if already familiar from this session)
   - **MUST read ALL docs**:
     - docs/README.md - Project overview
     - docs/core-concepts.md - Design principles
     - docs/architecture.md - Code structure

2. **Check current task**
   - **MUST execute** `crew list` to see all tasks
   - **MUST execute** `crew show <id>` to view task details
   - If `crew` is not available or returns error, ask the user which task to work on
   - Do NOT look for TASKS.md - this project uses git-crew for task management

3. **Ensure feature branch**
   - Check current branch: `git branch --show-current`
   - If on `main`: create feature branch `git checkout -b feature/<task-description>`
   - If already on `feature/*`: continue on current branch

### Phase 2: Implementation

**Goal**: Complete the task with quality.

1. **Plan implementation**
   - Break down the task into specific TODOs
   - Each TODO should be a single, verifiable step

2. **Implement incrementally**
   - Work on ONE TODO at a time
   - Mark TODO as `in_progress` when starting
   - Mark TODO as `completed` immediately when done

3. **Run CI frequently**
   - Run `mise run ci` after significant changes
   - Fix any issues before proceeding

4. **Update task status**
   - Use `crew edit <id> --status <status>` to update task status as you progress

### Phase 3: Wrap-up

**Goal**: Finalize changes and reflect on the session.

1. **Final CI check**
   - Run `mise run ci` one last time
   - Ensure all tests pass

2. **Check test coverage**
   - Run `mise run test:cover`
   - Review coverage: `go tool cover -func=coverage.out | grep -E "(total|<new-package>)"`
   - Add tests if coverage is insufficient

3. **Commit changes** (no user confirmation needed)
   - Stage and commit with clear message
   - Follow commit message format from AGENTS.md

4. **Complete task**
   - Run `crew complete <id>` to merge to main and close task

5. **Summary report**
   - Output a consolidated report with the following sections:

   ```
   ## Summary

   ### What was done
   - Brief description of implemented changes

   ### Technical findings (if any)
   - Concerns, ambiguities, or potential issues discovered
   - Spec interpretation questions
   - Edge cases not covered by specs
   - Design decisions that might need confirmation

   ### Retrospective (if any)
   - Patterns suggesting AGENTS.md or docs/ improvements
   - Friction with specs in docs/ → append to DESIGN_FEEDBACK.md
   ```
