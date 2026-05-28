# Canonical Plan Template

The standard output structure for all planning tasks. This format is task-type agnostic.

## Plan Output Structure

```markdown
# Plan: [Task Title]

## A) Goal & Acceptance Criteria

### Goal
[What success looks like - observable outcome]

### Constraints
- Time: [if applicable]
- Scope: [boundaries]
- Compatibility: [requirements]

### Acceptance Criteria
- [ ] [Criterion 1 - measurable]
- [ ] [Criterion 2 - measurable]
- [ ] [Criterion 3 - measurable]

---

## B) Context Pack Summary

*From Explorer agent*

### Entry Points
- [file:line] - [description]

### Key Conventions
- [convention 1]
- [convention 2]

### Commands
- Tests: `[command]`
- Lint: `[command]`
- Build: `[command]`

### Touch Set
Files to modify:
- [file1]
- [file2]

---

## C) Proposed Approach

### Strategy
[1-2 paragraph description of the approach]

### Key Design Choices
| Decision | Choice | Rationale |
|----------|--------|-----------|
| [decision 1] | [choice] | [why] |
| [decision 2] | [choice] | [why] |

### Alternatives Considered
1. [Alternative 1] - rejected because [reason]
2. [Alternative 2] - rejected because [reason]

---

## D) Step Plan (Checkpointed)

### Step 1: [Title]
**Edit Set**: [files to modify]
**Action**: [what to do]
**Behavior Change**: [what changes]
**Verify**: `[command]`
**Stop If**: [failure condition]

### Step 2: [Title]
**Edit Set**: [files to modify]
**Action**: [what to do]
**Behavior Change**: [what changes]
**Verify**: `[command]`
**Stop If**: [failure condition]

### Step 3: [Title]
...

---

## E) Test Plan

*From Test Planner agent (if applicable)*

### New Tests
| Test | Location | Purpose |
|------|----------|---------|
| [test 1] | [path] | [what it verifies] |
| [test 2] | [path] | [what it verifies] |

### Key Test Cases
- Happy path: [description]
- Edge case: [description]
- Error case: [description]

### Regression Guard
[The specific test that prevents this issue from recurring]

---

## F) Risk Register

*From Reviewer agent*

### Identified Risks
| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| [risk 1] | High | Medium | [mitigation] |
| [risk 2] | Medium | Low | [mitigation] |

### Must Address
- [ ] [Critical item 1]
- [ ] [Critical item 2]

### Monitor After Deploy
- [Metric/behavior to watch]

---

## G) Definition of Done

### Required
- [ ] All tests pass
- [ ] Lint/format clean
- [ ] Code review approved
- [ ] No blocking risks remain

### Verification Commands
```bash
[test command]
[lint command]
[build command]
```

### Sign-off
- [ ] Reviewer verdict: PROCEED
- [ ] Acceptance criteria met
```

---

## Compact Variant (for Simple Tasks)

For straightforward tasks, use this shortened format:

```markdown
# Plan: [Task Title]

## Goal
[Observable outcome]

## Context
- Entry: [main file]
- Tests: `[command]`
- Touch: [files]

## Steps
1. [Action] → verify with `[command]`
2. [Action] → verify with `[command]`
3. [Action] → verify with `[command]`

## Risks
- [Top risk + mitigation]

## Done When
- [ ] Tests pass
- [ ] [Acceptance criterion]
```

---

## Advisory Panel Addendum (When Used)

When Advisory Panel is consulted, append:

```markdown
---

## H) Advisory Panel Input

### Pragmatist Recommendation
[Summary of ship-it path]

### Purist Recommendation
[Summary of ideal approach]

### Skeptic Concerns
[Summary of risks and failure modes]

### Synthesis
**Chosen approach**: [which recommendation]
**Accepted tradeoff**: [what we're giving up]
**Risk mitigation**: [how we address skeptic concerns]
```

---

## Architect Addendum (When Used)

When Architect is consulted, append:

```markdown
---

## I) Architecture Assessment

### Architecture Impact
[Summary of system-level changes]

### Interface Changes
| Interface | Change | Impact |
|-----------|--------|--------|
| [name] | [type] | [consumers affected] |

### Decision Record
**Decision**: [what was decided]
**Context**: [why this decision was needed]
**Consequences**: [implications]
```
