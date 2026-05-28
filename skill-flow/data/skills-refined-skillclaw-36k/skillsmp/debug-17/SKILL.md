---
name: debug
version: 1.0.0
changelog: Initial debug skill with systematic diagnosis
description: Diagnose bugs systematically before proposing fixes. Use when something is broken, failing, erroring, or not working as expected.
allowed-tools: Read, Grep, Glob, Bash, Task
temperature: 0.2  # Mostly systematic, slight exploration
---

# Debug Phase

Diagnose systematically before proposing fixes.

## Task
$ARGUMENTS

## Instructions

Output: `## Debug Phase`

**State**: At phase start, update STATE.md:
- Set `task:` from $ARGUMENTS (if STATE.md is idle/complete or task is "None")
- Set `phase: debug`
- Set `status: in_progress`

### 1. Reproduce
- Confirm the failure exists
- Identify exact error message/behavior
- Note environment conditions (versions, config, state)

### 2. Isolate
- Narrow to smallest reproducible case
- Identify which component fails
- Trace information flow to failure point
- Use targeted reads/greps, not broad exploration

### 3. Hypothesize
- List possible causes (most likely first)
- For each: what evidence would confirm/reject?
- Consider: recent changes, dependencies, environment

### 4. Test Hypotheses
- Gather evidence systematically
- Update hypothesis ranking as evidence arrives
- Stop when root cause is confirmed

### 5. Produce Diagnosis

Use the [diagnosis template](templates/diagnosis.md):

```markdown
## Symptom
[What's failing — exact error or behavior]

## Root Cause
[Why it's failing — the actual problem]

## Evidence
- `file:line` — observation
- Command output — what it showed

## Fix Options
1. Option A: [approach] — tradeoffs
2. Option B: [approach] — tradeoffs

## Recommended
[Which option and why]
```

## Context Budget

- Target: complete diagnosis under 30% context
- Use subagents for exploration if needed
- Keep evidence concise — excerpts, not full files

### 6. Checkpoint

Update STATE.md incrementally:
- Set `phase: debug`
- Add root cause and fix decision to `## Decisions`
- Add investigated files to `## Key Files`
- Update `## Next Steps` with recommended fix

Run `/checkpoint` if context is heavy or taking a break.

## Constraints

- **Do not fix yet** — diagnosis first
- If fix is obvious (<5 lines, isolated), may proceed with approval
- Otherwise, get approval before implementing
- Don't guess — verify with evidence

## Exit Criteria

Root cause identified with evidence. Fix approach clear and approved.

**Gate**: "Here's the diagnosis. Approve fix approach?"
