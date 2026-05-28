---
name: prd-generator
description: >
  Generate comprehensive Product Requirements Documents (PRDs) for engineering teams,
  optimized for the Ralph autonomous coding loop. Use when user: (1) requests a PRD or
  product requirements document, (2) says "I want a PRD", "create requirements", or
  "write requirements", (3) mentions taskmaster or task-driven development, (4) asks
  to document product/feature requirements for engineering. Do NOT use for: code
  documentation, test specifications, project timelines without product context, or
  PDF document creation.
---

# PRD Generator

Create engineer-focused PRDs with checkbox tasks compatible with the Ralph loop.

## Principles

- **Quality over speed** - Planning is 95% of the work
- **Ralph-compatible** - All tasks use `[ ]` checkbox format
- **Validation-driven** - Run all checks before delivery

## Workflow

### 1. Discovery

Enter plan mode. Ask questions iteratively until all PRD sections can be filled:

**Vision**: Problem solved? Primary user? Success criteria?
**Scope**: MVP features? Explicitly out of scope? Integrations?
**Tech**: Stack? Existing patterns? Deployment constraints?
**User journeys**: Primary flows? Key actions? Feedback needed?
**Data**: What's stored? Key entities? External sources?
**Non-functional**: Performance? Security? Accessibility?
**Constraints**: Timeline? Team? Dependencies?
**Edge cases**: Error states? Recovery?

### 2. Generate PRD

Use the template in [references/prd-template.md](references/prd-template.md).

Key requirements:
- Executive summary: 2-3 sentences
- Out of scope: explicitly defined (never empty)
- Each user story: minimum 3 acceptance criteria
- All tasks: `[ ]` checkbox format
- Tasks: atomic, ordered by dependency, implementation-ready

### 3. Validate

Before delivery, verify:

| Check | Requirement |
|-------|-------------|
| Executive summary | 2-3 sentences exist |
| Out of scope | Explicitly defined |
| Acceptance criteria | 3+ per user story |
| Task format | All use `[ ]` checkboxes |
| Tech stack | Fully specified |
| Language | No "might", "could", "maybe", "TBD" |
| Criteria | All testable/verifiable |
| Data model | Covers all entities |
| Error handling | Approach defined |
| Env vars | Documented |

### 4. Deliver

1. Write PRD to `PRD.md` in project root
2. Create empty `progress.txt` for Ralph
3. Summarize: user stories count, tasks count, phases, open questions

## Ralph Integration

Ralph reads `PRD.md`, implements one `[ ]` task at a time, marks `[x]` only if tests pass, commits with `feat: [task]`. Tasks must be:

- **Self-contained** - Implementable without other incomplete tasks
- **Testable** - Clear pass/fail criteria
- **Ordered** - Dependencies first
- **Atomic** - One commit-sized change
