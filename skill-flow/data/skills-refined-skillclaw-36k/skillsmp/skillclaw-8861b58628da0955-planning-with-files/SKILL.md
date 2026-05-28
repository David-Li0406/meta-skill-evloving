---
name: planning-with-files
description: Use this skill when starting complex tasks, multi-step projects, or research tasks to track progress, store findings, and maintain context using persistent markdown files.
---

# Planning with Files

Work like Manus: Use persistent markdown files as your "working memory on disk."

## Quick Start

Before ANY complex task:

1. **Create `task_plan.md`** in the working directory.
2. **Define phases** with checkboxes.
3. **Update after each phase** - mark [x] and change status.
4. **Read before deciding** - refresh goals in attention window.

## The 3-File Pattern

For every non-trivial task, create THREE files:

| File | Purpose | When to Update |
|------|---------|----------------|
| `task_plan.md` | Track phases and progress | After each phase |
| `notes.md` | Store findings and research | During research |
| `[deliverable].md` | Final output | At completion |

## Core Workflow

1. **Create `task_plan.md`** with goal and phases.
2. **Research** → save to `notes.md` → update `task_plan.md`.
3. **Read `notes.md`** → create deliverable → update `task_plan.md`.
4. **Deliver final output**.

### The Loop in Detail

**Before each major action:**
```bash
Read task_plan.md  # Refresh goals in attention window
```

**After each phase:**
```bash
Edit task_plan.md  # Mark [x], update status
```

**When storing information:**
```bash
Write notes.md     # Don't stuff context, store in file
```

## Templates

### task_plan.md Template
Create this file FIRST for any complex task:
```markdown
# Task Plan: [Brief Description]

## Goal
[One sentence describing the end state]

## Phases
- [ ] Phase 1: Plan and setup
- [ ] Phase 2: Research/gather information
- [ ] Phase 3: Execute/build
- [ ] Phase 4: Review and deliver

## Key Questions
1. [Question to answer]
2. [Question to answer]

## Decisions Made
- [Decision]: [Rationale]

## Errors Encountered
- [Error]: [Resolution]

## Status
**Currently in Phase X** - [What I'm doing now]
```

### notes.md Template
For research and findings:
```markdown
# Notes: [Topic]

## Sources

### Source 1: [Name]
- URL: [link]
- Key points:
  - [Finding]
  - [Finding]

## Synthesized Findings

### [Category]
- [Finding]
- [Finding]
```

## Critical Rules

1. **ALWAYS Create Plan First**: Never start a complex task without `task_plan.md`. This is non-negotiable.
2. **Read Before Decide**: Before any major action, refresh your goals by reading `task_plan.md`.