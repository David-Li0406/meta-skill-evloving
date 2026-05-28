---
name: prd
description: Create Product Requirements Documents (PRDs) that define the end state of a feature. Use when planning new features, migrations, or refactors. Generates structured PRDs with acceptance criteria.
---

# PRD Creation Skill

Create Product Requirements Documents suitable for RFC review by Principal Engineers, Designers, and Product Owners.

The PRD describes WHAT to build and WHY, not HOW or in WHAT ORDER.

## Beads-Native Output (Recommended)

When you are working on a Beads task (you have a bead id like `bd-...`), the PRD should live with the task artifacts:

- Write PRD to: `.beads/artifacts/<bead-id>/prd.md`

This keeps requirements + execution tasks colocated with the bead.

If no bead id exists, fall back to writing `prd-<feature-name>.md` in the project root.

## Workflow

1. Confirm if the user has an existing bead id.
   - If yes: use `.beads/artifacts/<bead-id>/prd.md`
   - If no: write `prd-<feature-name>.md` in project root
2. Ask clarifying questions (5–7 max).
3. Explore codebase patterns and constraints.
4. Write a PRD that includes a machine-convertible `## Tasks` section (see below).

## Clarifying Questions

### Problem & Motivation

- What problem does this solve? Who experiences it?
- What's the cost of NOT solving this? (user pain, revenue, tech debt)
- Why now? What triggered this work?

### Users & Stakeholders

- Who are the primary users? Secondary users?

### End State & Success

- What does "done" look like? How will users interact with it?

### Scope & Boundaries

- What's explicitly OUT of scope?
- What's deferred to future iterations?
- Are there adjacent features that must NOT be affected?

### Constraints & Requirements

- Performance requirements?
- Security requirements? (auth, data sensitivity, compliance)
- Compatibility requirements? (browsers, versions, APIs)
- Accessibility requirements? (WCAG level, screen readers)

### Risks & Dependencies

- What could go wrong? Technical risks?
- External service dependencies?
- What decisions are still open/contentious?

## Output Format

Write a PRD in markdown using this structure.

IMPORTANT: include a `## Tasks` section that `prd-task` can convert.

```markdown
# PRD: <Feature Name>

**Bead:** <bd-...>  
**Date:** <YYYY-MM-DD>

---

## Problem Statement

### What problem are we solving?

Clear description of the problem. Include user impact and business impact.

### Why now?

What triggered this work? Cost of inaction?

### Who is affected?

- **Primary users:** Description
- **Secondary users:** Description

---

## Proposed Solution

### Overview

One paragraph describing what this feature does when complete.

### User Experience (if applicable)

How will users interact with this feature? Include user flows for primary scenarios.

---

## End State

When this PRD is complete, the following will be true:

- [ ] Capability 1 exists and works
- [ ] Capability 2 exists and works
- [ ] All acceptance criteria pass
- [ ] Tests cover the new functionality
- [ ] Documentation is updated

---

## Success Metrics

### Quantitative

| Metric   | Current | Target | Measurement Method |
| -------- | ------- | ------ | ------------------ |
| Metric 1 | X       | Y      | How measured       |

### Qualitative

- User feedback criteria
- Team/process improvements expected

---

## Acceptance Criteria

### Feature: <Name>

- [ ] Criterion 1
- [ ] Criterion 2

---

## Technical Context

### Existing Patterns

- Pattern 1: `src/path/to/example.ts` - Why relevant

### Key Files

- `src/relevant/file.ts` - Description of relevance

---

## Risks & Mitigations

| Risk   | Likelihood   | Impact       | Mitigation      |
| ------ | ------------ | ------------ | --------------- |
| Risk 1 | High/Med/Low | High/Med/Low | How to mitigate |

---

## Non-Goals (v1)

Explicitly out of scope:

- Thing we're not building - why deferred

---

## Tasks

Each task must be written like:

### <Task Title> [category]

One sentence describing the end state.

**Verification:**

- A command or manual check that proves it works
- Another check

Example:

### Registration API [api]

Users can register with email/password.

**Verification:**

- `curl -X POST /api/auth/register ...` returns 201
- Duplicate email returns 409

---

## Open Questions

| Question   | Owner | Due Date | Status        |
| ---------- | ----- | -------- | ------------- |
| Question 1 | Name  | Date     | Open/Resolved |
```

## Key Principles

- Problem Before Solution
- Define End State, Not Process
- Technical Context Enables Autonomy
- Non-Goals Prevent Scope Creep
- Risks & Alternatives Show Rigor
