---
name: planning-with-files
description: Use this skill for complex tasks to track progress, store findings, and maintain context across sessions using a persistent markdown file workflow.
---

# Planning with Files

> "Work like Manus" — This skill implements a persistent memory workflow using three markdown files for planning, progress tracking, and knowledge storage.

## The 3-File Pattern

For every complex task, create and maintain these three files:

| File               | Purpose                                   | When to Update                     |
|--------------------|-------------------------------------------|------------------------------------|
| `task_plan.md`     | Track phases and progress                 | After each phase                   |
| `findings.md`      | Store research, decisions, and learnings  | During research and decision-making |
| `progress.md`      | Log actions taken and results observed    | After each session or action       |

## Core Workflow

1. **Initialization**: At the start of a task, check if the files exist. If not, create them using the templates below.
2. **Execution Loop**:
   - Before running tools, update `progress.md` with the actions you are about to take.
   - After completing a sub-task, mark it as completed in `task_plan.md`.
   - Record any discoveries or decisions in `findings.md`.
3. **Context Management**: Regularly read the files to keep track of goals, findings, and progress.

## Templates

### task_plan.md Template
```markdown
# Task Plan: [Task Name]

## Goal
[One sentence describing the end state]

## Phases
- [ ] Phase 1: [Name]
- [ ] Phase 2: [Name]

## Key Questions
1. [Question to answer]
2. [Question to answer]

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

## When to Use This Skill

**Use this pattern for:**
- Multi-step tasks (3+ steps)
- Research projects
- Building/creating something
- Tasks requiring organization across multiple tool calls

**Skip for:**
- Simple questions
- Single-file edits
- Quick lookups

## Critical Rules

1. **Always Create Plan First**: Never start a complex task without `task_plan.md`.
2. **Read Before Deciding**: Refresh goals by reading the plan before any major decision.
3. **Update After Action**: Immediately update the plan file after completing any phase.
4. **Store, Don't Stuff**: Keep large outputs in files, not in context.
5. **Log All Errors**: Document every error in the "Errors Encountered" section of `task_plan.md`.

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