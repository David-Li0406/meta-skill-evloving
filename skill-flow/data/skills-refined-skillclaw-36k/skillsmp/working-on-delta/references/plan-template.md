# Implementation Plan Template

Use this template when creating implementation plans.

## Template

```markdown
# Implementation Plan: [FEATURE-ID]

**Feature Spec**: [../feature-specs/FEATURE-ID.md](../feature-specs/FEATURE-ID.md)
**Feature Design**: [../feature-designs/FEATURE-ID.md](../feature-designs/FEATURE-ID.md)
**Status**: Not Started | In Progress | Complete

## Pre-Implementation Checklist

- [ ] Read the spec
- [ ] Read the design
- [ ] Read dependency code: [list files]
- [ ] Review relevant ADRs: [list ADR-NNN]
- [ ] Review relevant design patterns: [list DES-NNN]

## Implementation Steps

### Step 1: [Description]

- Create/modify: `src/path/to/file`
- What to do: [specific instructions]
- Test: [how to verify this step]

### Step 2: [Description]

- Create/modify: `src/path/to/file`
- What to do: [specific instructions]
- Test: [how to verify this step]

### Step N: Verify Acceptance Criteria

- [ ] Run tests for each acceptance criterion
- [ ] Manual verification: [what to check]

## Files Changed

- [ ] `src/...` - [purpose of changes]
- [ ] `tests/...` - [purpose of changes]

## Notes

[Anything discovered during implementation, deviations from plan, learnings]
```

## Guidelines

### Pre-Implementation Checklist

List everything to read before coding:

**Required:**
- The spec (acceptance criteria to satisfy)
- The design (approach to follow)

**If applicable:**
- Dependency code (imports, interfaces to use)
- ADRs (architectural constraints)
- DES patterns (coding patterns to follow)

### Implementation Steps

Each step should be:
- **Atomic**: Independently verifiable
- **Ordered**: Dependencies come first
- **Specific**: Clear what to do
- **Testable**: How to verify success

#### Step Structure

```markdown
### Step N: [Verb-based description]

- Create/modify: `path/to/file`
- What to do: [specific, actionable instructions]
- Test: [how to verify this step works]
```

#### Ordering Principles

1. **Foundation first**: Core structures before dependent code
2. **Inside out**: Inner functions before outer wrappers
3. **Happy path first**: Success cases before error handling
4. **Tests alongside**: Write tests with implementation

#### Verification

Every step should have verification:
- Unit test to run
- Manual check to perform
- Expected output/behavior

### Mapping to Acceptance Criteria

Ensure coverage:

| Acceptance Criterion | Implementing Step(s) |
|---------------------|---------------------|
| Given X When Y Then Z | Step 2, Step 3 |
| Error case A | Step 5 |

If a criterion has no implementing step, add one.

### Files Changed

List all files that will be modified:
- Helps reviewer understand scope
- Ensures nothing is forgotten
- Groups related changes

### Common Step Patterns

**Core functionality:**
```markdown
### Step 1: Create core data structures
- Create: `src/models/entity.py`
- What to do: Define Entity class with fields X, Y, Z per design
- Test: Unit test instantiation and validation
```

**Error handling:**
```markdown
### Step 3: Add input validation
- Modify: `src/handlers/input.py`
- What to do: Add validation per spec error cases
- Test: Test each error case from spec
```

**Integration:**
```markdown
### Step 5: Wire up components
- Modify: `src/main.py`
- What to do: Connect Handler to Service following data flow
- Test: Integration test for end-to-end flow
```

### Notes Section

Use during implementation to record:
- Deviations from plan (with rationale)
- Issues encountered
- Learnings for future
- Patterns detected (candidates for DES)
