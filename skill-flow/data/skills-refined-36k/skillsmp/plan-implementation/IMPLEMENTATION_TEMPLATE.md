# [Feature Name] - Implementation Plan

## Overview

**Feature**: [Link to feature spec in /docs/features/]
**Approach**: TDD with Vertical Slices
**Total Phases**: [N]

## Summary

[2-3 sentences describing the implementation approach and key decisions]

---

## Phase 1: [Phase Name]

**Goal**: [One sentence describing what this phase delivers]

**Vertical Slice**: [What end-to-end capability does this enable?]

### RED - Write Failing Tests

**Test File**: `[path/to/test/file.cs]`

- [ ] Test: [Test case with Given/When/Then]
- [ ] Test: [Edge case]
- [ ] Test: [Error case]

### GREEN - Make Tests Pass

**Files to Create**:
- `[path/to/file.cs]` - [Purpose]

**Files to Modify**:
- `[path/to/file.cs]` - [What changes]

**Tasks**:
- [ ] Create `[ClassName]` with [key properties]
- [ ] Implement `[MethodName]()` to [what it does]
- [ ] Wire up [integration point]

### REFACTOR - Clean Up

- [ ] Extract [what] for [reason]
- [ ] Remove duplication in [where]

### Acceptance Criteria

- [ ] All tests pass
- [ ] [Observable behavior works]
- [ ] No regressions

**Deliverable**: [Concrete working functionality]

---

## Phase 2: [Phase Name]

[Same structure as Phase 1]

---

## Phase 3: [Phase Name]

[Same structure as Phase 1]

---

## Files Summary

### New Files
- `[path]` - [Purpose]

### Modified Files
- `[path]` - [What changes]

---

## Milestones

| Milestone | After Phase | What's Working |
|-----------|-------------|----------------|
| [Name] | Phase N | [Observable functionality] |
| Feature Complete | Final | Full feature working |

---

## Risks

| Risk | Mitigation | Phase |
|------|------------|-------|
| [Description] | [How addressed] | N |

---

## Success Criteria

- [ ] All phases implemented
- [ ] All tests passing
- [ ] No regressions
- [ ] Code coverage ≥ 80% for new code
