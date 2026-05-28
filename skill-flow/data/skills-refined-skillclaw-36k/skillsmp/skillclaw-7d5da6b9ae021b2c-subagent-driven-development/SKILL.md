---
name: subagent-driven-development
description: Use this skill when executing implementation plans with independent tasks in the current session, dispatching fresh subagents for each task with code review between tasks to ensure fast iteration and maintain quality.
---

# Subagent-Driven Development

Execute a plan by dispatching a fresh subagent for each task, with code review after each to ensure quality and fast iteration.

**Core principle:** Fresh subagent per task + review between tasks = high quality, fast iteration.

## Overview

**vs. Executing Plans (parallel session):**
- Same session (no context switch)
- Fresh subagent per task (no context pollution)
- Code review after each task (catch issues early)
- Faster iteration (no human-in-loop between tasks)

**Works in main branch OR worktree (no preference)**

**When to use:**
- Staying in this session
- Tasks are mostly independent
- Want continuous progress with quality gates

**When NOT to use:**
- Need to review plan first (use executing-plans)
- Tasks are tightly coupled (manual execution better)
- Plan needs revision (brainstorm first)

## The Process

### 1. Load Plan

Read the plan file and create a TodoWrite with all tasks.

### 2. Execute Task with Subagent

For each task:

**Dispatch fresh subagent:**
```
Task tool (general-purpose):
  description: "Implement Task N: [task name]"
  prompt: |
    You are implementing Task N from [plan-file].

    Read that task carefully. Your job is to:
    1. Implement exactly what the task specifies
    2. Write tests (following TDD if task says to)
    3. Verify implementation works
    4. Commit your work
    5. Report back

    IMPORTANT: Create TDD Compliance Certification for each function you implement
    (format specified in test-driven-development skill). Include this in your report.

    Work from: [directory]

    Report: What you implemented, what you tested, test results, files changed,
    TDD Compliance Certification, any issues
```

**Subagent reports back** with a summary of work.

### 3. Review Subagent's Work

**Verify subagent provided TDD Compliance Certification:**
- If certification is missing or incomplete: Request it before proceeding to code review.
- Certification must have an entry for each new function.

**Dispatch code-reviewer subagent:**
```
Task tool (code-reviewer):
  Use template at requesting-code-review/code-reviewer.md

  WHAT_WAS_IMPLEMENTED: [from subagent's report]
  PLAN_OR_REQUIREMENTS: Task N from [plan-file]
  BASE_SHA: [commit before task]
  HEAD_SHA: [current commit]
  DESCRIPTION: [task summary]
```

**Code reviewer returns:** Strengths, Issues (Critical/Important/Minor), Assessment.

### 4. Apply Review Feedback

**If issues found:**
- Fix Critical issues immediately.
- Fix Important issues before the next task.
- Note Minor issues.

**Dispatch follow-up subagent if needed:**
```
"Fix issues from code review: [list issues]"
```

### 5. Mark Complete, Next Task

- Mark task as completed in TodoWrite.
- Move to the next task.
- Repeat steps 2-5.