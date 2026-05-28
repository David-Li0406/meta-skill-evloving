---
name: plan
version: 1.0.0
changelog: Initial planning skill with handoff format
description: Create specific implementation steps for review. Use after research is complete and before writing code.
allowed-tools: Read, Write, Glob, Grep
temperature: 0.2  # Mostly deterministic, slight flexibility
---

# Planning Phase

Create a specific implementation plan for review.

## Task
$ARGUMENTS

## Instructions

Output: `## Planning Phase`

**State**: At phase start, update STATE.md:
- Set `task:` from $ARGUMENTS (if STATE.md is idle/complete or task is "None")
- Set `phase: plan`
- Set `status: in_progress`

### 1. Consume Research Handoff

Read `## Research Findings` from STATE.md:
- Use **Key Files** as starting points
- Honor **Constraints** in plan design
- Address **Remaining** items from research

### 2. Gather Context
- Read files identified in research handoff
- Verify understanding is current
- Spawn parallel research tasks if gaps exist

### 3. Define Success Criteria

**Automated verification:**
- Build commands that must pass
- Test commands that must pass
- Type check commands

**Manual verification:**
- UI/UX checks requiring human review
- Performance validation
- Edge case review

### 4. Scope Boundaries

**What we're doing:**
- Specific deliverables

**What we're NOT doing:**
- Explicit exclusions (prevents scope creep)

### 5. Create Step-by-Step Plan

Use the [plan format template](templates/plan-format.md):

```markdown
## Phase 1: [Name]

- [ ] Step 1: Description
      File: `path/to/file.ts`
      Verification: how to verify this step

- [ ] Step 2: Description
      File: `path/to/other.ts`
      Verification: run `npm test`

## Phase 2: [Name]

- [ ] Step 3: ...
```

**Task schema** (from style.md): Each task should have:
- **Action**: What to do and why
- **Files**: Specific paths (`src/auth.ts:42`)
- **Verify**: Testable command
- **Done**: Measurable acceptance criteria

### 6. Identify Decision Points

- Where are there meaningful alternatives?
- What tradeoffs exist?
- What needs human input before proceeding?

### 7. Checkpoint

Update STATE.md incrementally:
- Set `phase: plan`
- Add plan decisions to `## Decisions`
- Update `## Next Steps` with plan summary and approval status

Run `/checkpoint` if context is heavy or taking a break.

### 8. Produce Handoff

Before exit gate, append handoff to STATE.md under `## Plan`:

```markdown
## Plan

### Completed
- [x] Implementation plan created
- [x] Success criteria defined

### Context
**Plan Summary**:
1. [Step 1 brief]
2. [Step 2 brief]
...

**Verification Commands**:
- `[test command]`
- `[build command]`

**Risks Identified**:
- [Risk]: [mitigation]

### Remaining
- [ ] Execute plan steps
- [ ] Verify each step before proceeding
```

See [handoff template](../shared/templates/handoff.md) for full format.

## Constraints

- **Do not implement yet**
- Plan should be specific enough that implementation is mechanical
- Each phase should be independently verifiable
- Keep total steps reasonable (3-10 per phase, 20 max overall)

## Exit Criteria

Plan is approved by human before proceeding to implementation.

**Gate**: "Here's the plan. Approve to proceed?"
