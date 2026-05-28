---
name: planning-with-files
description: Use this skill for complex tasks to implement a Manus-style workflow with persistent markdown files for planning, progress tracking, and knowledge storage.
---

# Planning with Files

Work like Manus: Use persistent markdown files as your "working memory on disk."

## Quick Start

Before any complex task:

1. **Create `task_plan.md`** in the working directory.
2. **Define phases** with checkboxes.
3. **Update after each phase** - mark [x] and change status.
4. **Read before deciding** - refresh goals in attention window.

## The 3-File Pattern

For every non-trivial task, create THREE files:

| File              | Purpose                               | When to Update               |
|-------------------|---------------------------------------|------------------------------|
| `task_plan.md`    | Track phases and progress             | After each phase             |
| `findings.md`     | Store research and findings           | During research              |
| `progress.md`     | Log actions taken and results         | After each session           |

## Core Workflow

```
1. Create task_plan.md with goal and phases
2. Research → save to findings.md → update task_plan.md
3. Read findings.md → create deliverable → update task_plan.md
4. Deliver final output
```

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
Write findings.md  # Don't stuff context, store in file
```

## Templates

### task_plan.md Template
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

### findings.md Template
```markdown
# Findings & Knowledge

## Key Decisions
- [Date] [Decision]: [Rationale]

## Technical Learnings
- [Tool/Library]: [How to use it / Gotchas]
- [Architecture]: [Description]

## Unresolved Questions
- [ ] [Question]?
```

### progress.md Template
```markdown
# Progress Log

## [YYYY-MM-DD HH:MM] Session Start
- Goal: [Goal for this session]

### [HH:MM] Action
- executed: `command`
- result: success/fail
- thoughts: ...
```

## Critical Rules

1. **ALWAYS Create Plan First**: Never start a complex task without `task_plan.md`.
2. **Read Before Decide**: Before any major decision, read the plan file.
3. **Update After Act**: After completing any phase, immediately update the plan file.
4. **Store, Don't Stuff**: Large outputs go to files, not context.
5. **Log All Errors**: Every error goes in the "Errors Encountered" section.

## When to Use This Pattern

**Use this pattern for:**
- Multi-step tasks (3+ steps)
- Research tasks
- Building/creating something
- Tasks spanning multiple tool calls
- Anything requiring organization

**Skip for:**
- Simple questions
- Single-file edits
- Quick lookups

## Anti-Patterns to Avoid

| Don't | Do Instead |
|-------|------------|
| Use TodoWrite for persistence | Create `task_plan.md` file |
| State goals once and forget | Re-read plan before each decision |
| Hide errors and retry | Log errors to plan file |
| Stuff everything in context | Store large content in files |
| Start executing immediately | Create plan file FIRST |

## Advanced Patterns

For advanced techniques, refer to:
- Attention manipulation techniques
- Error recovery patterns
- Context optimization from Manus

## Example

**You:** "Research the benefits of TypeScript and write a summary"

**Claude creates:**

```markdown
# Task Plan: TypeScript Benefits Research

## Goal
Create a research summary on TypeScript benefits.

## Phases
- [x] Phase 1: Create plan ✓
- [ ] Phase 2: Research and gather sources (CURRENT)
- [ ] Phase 3: Synthesize findings
- [ ] Phase 4: Deliver summary

## Status
**Currently in Phase 2** - Searching for sources
```

## Links

- [GitHub Repository](https://github.com/OthmanAdi/planning-with-files)
- [Context Engineering for AI Agents](https://manus.im/de/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)