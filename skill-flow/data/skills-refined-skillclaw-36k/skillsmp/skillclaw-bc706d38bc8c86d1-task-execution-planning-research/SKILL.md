---
name: task-execution-planning-research
description: Use this skill when you need to systematically execute tasks based on structured planning and thorough research, ensuring quality and tracking changes throughout the process.
---

# Skill body

## When to Use This Skill

Use this skill when you need to:
- Execute tasks based on a structured plan.
- Conduct thorough research before planning and implementation.
- Track changes and maintain quality thresholds throughout the execution process.

## Core Principles

### Research First

- Verify that research documents exist and are complete before planning.
- If research is missing or needs updates, use the task-research skill immediately.

### Plan-Driven Execution

- Implementation must correspond to specific tasks from the plan.
- Update the plan checklist upon completion of each task.

### Continuous Tracking

- Update the changes file after every task completion.
- Document reasons for any divergence from the plan.

## Pre-Execution Checklist (Hard Gate)

You MUST verify before starting:

- [ ] All prerequisite tasks completed.
- [ ] Required tools and packages installed.
- [ ] Planning documents available:
  - [ ] Research: `.copilot-tracking/research/*.md`
  - [ ] Plan: `.copilot-tracking/plans/*.plan.instructions.md`
  - [ ] Details: `.copilot-tracking/details/*.details.md`
- [ ] Understanding confirmed:
  - [ ] Task objectives clear.
  - [ ] Success criteria clear.
  - [ ] Implementation approach defined.

## Execution Workflow

### Step 1: Research Planning and Discovery

1. Analyze the research scope and use all available tools to conduct a thorough investigation.
2. Collect evidence from multiple sources to establish a complete understanding.

### Step 2: Planning File Creation

1. Create planning documents in the following format:
   - Plan: `YYYYMMDD-##-task-description-plan.instructions.md` in `plans/`
   - Details: `YYYYMMDD-##-task-description-details.md` in `details/`
   - Prompt: `implement-##-task-description.prompt.md` in `prompts/`

### Step 3: Initialize

1. Read implementation prompt: `.copilot-tracking/prompts/implement-*.prompt.md`
2. Create changes file if not exists: `.copilot-tracking/changes/YYYYMMDD-##-task-changes.md`
3. Review all linked planning documents (plan/details/research).
4. Confirm scope and success criteria.

### Step 4: Implement by Phase

For each Phase in the plan, execute in order:

1. Read Phase objectives and tasks.
2. Reference details/research for implementation specifics.
3. Implement completely (follow NO LAZY CODING).
4. Write/update unit tests.
5. Update plan checklist: `[ ]` → `[x]`.
6. Record changes to changes file.
7. Report Phase completion status.

**Phase Stop**: If `phaseStop=true`, pause after each Phase for user review.

### Step 5: Verify and Finalize

1. Execute build command (e.g., `dotnet build`, `npm run build`).
2. Execute test command (e.g., `dotnet test`, `npm run test`).
3. Verify all success criteria achieved.
4. Update all plan items.