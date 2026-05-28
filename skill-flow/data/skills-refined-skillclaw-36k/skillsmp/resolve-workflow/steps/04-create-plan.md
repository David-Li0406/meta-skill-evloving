---
name: create-plan
description: Generate implementation plan based on ticket and analysis
order: 4

skip_if:
  - flag: "--continue"
  - flag: "--refine-plan"

next:
  default: plan-validation

tools:
  - Read
  - Write
  - Task
---

# Step: Create Plan

<context>
This step generates an implementation plan based on the ticket content, complexity analysis,
and exploration findings. The plan format and detail level depend on the complexity.
</context>

## Instructions

<instructions>

### 1. Determine Planning Approach

Based on complexity level:

| Complexity | Approach |
|------------|----------|
| SIMPLE | Basic plan, 1-2 phases |
| MEDIUM | Standard plan, 2-4 phases |
| COMPLEX | Apply Architect skill for detailed plan |

### 2. Load Context

Read these files:
- `.claude/feature/{ticket-id}/ticket.md`
- `.claude/feature/{ticket-id}/analysis.md`
- `.claude/feature/{ticket-id}/status.json` (for user_context if present)

### 3. Generate Plan

For COMPLEX tickets, apply: `~/.claude/skills/architect/SKILL.md`

For all tickets, create plan with YAML frontmatter:

```markdown
---
feature: {ticket-id-slug}
ticket_id: {ticket-id}
created: {ISO timestamp}
status: pending
total_phases: {N}
---

# {ticket-id}: Implementation Plan - {title}

## Overview

{Brief description of what will be implemented}

---

## Phase 1: {Phase Title}

**Goal**: {What this phase accomplishes}

### Files to modify/create

- `path/to/file.ext` - Description of changes

### Implementation Details

{Specific implementation steps}

### Validation

```bash
{Command to validate: make test, phpunit, etc.}
```

### Commit message

```
{conventional commit message}
```

---

## Phase 2: ...
```

### 4. Include Visual Verification Checkpoints

If `figma_urls` exist in status.json, add visual verification to relevant phases:

```markdown
### Visual Verification

After this phase, verify against Figma designs:
- Screen: {description}
- Expected: {what should match}
```

### 5. Save Plan

Write to `.claude/feature/{ticket-id}/plan.md`

Update status: `phases.plan = "completed"`, `state = "planned"`

</instructions>

## Output

<output>
- File: `.claude/feature/{ticket-id}/plan.md`
- Status: `phases.plan = "completed"`, `state = "planned"`
</output>

## Plan Quality Checklist

<constraints>
The plan MUST include:
- [ ] Clear phase separation
- [ ] Specific files to modify
- [ ] Validation commands for each phase
- [ ] Commit messages following conventional commits
- [ ] Consider existing patterns from exploration
- [ ] Account for user_context if provided
</constraints>

## Auto Behavior

<auto_behavior>
- Generate plan without user interaction
- Use standard templates based on complexity
</auto_behavior>
