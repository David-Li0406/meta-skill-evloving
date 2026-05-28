# Refactoring Checklists

Printable/copyable checklists for each refactoring phase.

---

## Pre-Refactor Assessment

Before starting any refactoring:

```markdown
## Pre-Refactor Checklist

### Understand the Code
- [ ] I understand what this code does
- [ ] I know why it exists (business purpose)
- [ ] I've identified the code's boundaries/scope

### Verify Safety Net
- [ ] Tests exist for this code
- [ ] Tests are passing
- [ ] I can run tests easily and quickly

### Define Scope
- [ ] Refactoring scope is clearly defined
- [ ] Target intensity level chosen: [ ] SMALL [ ] MEDIUM [ ] DEEP
- [ ] Files/modules to touch are identified

### Environment Ready
- [ ] Code is committed (clean working tree)
- [ ] Branch created if needed
- [ ] Can revert if something goes wrong
```

---

## Phase 1: SMALL (Safe)

```markdown
## Phase 1 Checklist (SMALL)

### Naming
- [ ] Variables have descriptive names
- [ ] Functions have verb-phrase names
- [ ] Booleans prefixed with is/has/should/can
- [ ] No abbreviations or single letters (except loop indices)
- [ ] Names reveal intent, not implementation

### Dead Code Removal
- [ ] Unused imports removed
- [ ] Commented-out code removed (or has ticket reference)
- [ ] Unreachable code removed
- [ ] Unused variables removed
- [ ] Unused functions removed (verified not called)

### Formatting
- [ ] Consistent indentation
- [ ] No trailing whitespace
- [ ] Consistent spacing around operators
- [ ] Line length within limits

### Magic Values
- [ ] Numbers extracted to named constants
- [ ] Repeated strings extracted to constants
- [ ] No magic boolean parameters

### Comments
- [ ] Stale/incorrect comments updated or removed
- [ ] Clarifying comments added where needed
- [ ] TODO comments have ticket references

### Completion
- [ ] All tests passing
- [ ] Changes committed
- [ ] Commit message follows convention
```

---

## Phase 2: MEDIUM (Standard)

```markdown
## Phase 2 Checklist (MEDIUM)

### Prerequisites
- [ ] Phase 1 (SMALL) complete
- [ ] Summary of planned changes prepared
- [ ] Approval received (if required)

### Function Extraction
- [ ] Large functions (>40 lines) identified
- [ ] Logical chunks extracted to named functions
- [ ] Duplicated logic extracted to helpers
- [ ] Each function does one thing

### Simplification
- [ ] Nested conditionals converted to guard clauses
- [ ] Complex boolean expressions simplified
- [ ] Callbacks converted to async/await (where applicable)
- [ ] Unnecessary abstractions inlined

### Organization
- [ ] Functions ordered: public first, helpers below
- [ ] Related functions grouped together
- [ ] Error handling consistent

### Quality Checks
- [ ] No function exceeds 40 lines
- [ ] No nesting deeper than 3 levels
- [ ] No function has more than 5 parameters
- [ ] Cyclomatic complexity reasonable (<10)

### Completion
- [ ] All tests passing
- [ ] Changes committed atomically
- [ ] Each commit message describes what and why
- [ ] Summary of changes documented
```

---

## Phase 3: DEEP (Aggressive)

```markdown
## Phase 3 Checklist (DEEP)

### Prerequisites
- [ ] Phase 1 (SMALL) complete
- [ ] Phase 2 (MEDIUM) complete
- [ ] Deep refactor plan drafted
- [ ] Plan includes:
  - [ ] Current state assessment
  - [ ] Proposed end state
  - [ ] Risk analysis
  - [ ] Migration strategy
  - [ ] Rollback plan
- [ ] Explicit approval received

### Execution Setup
- [ ] Working branch created
- [ ] Baseline commit identified for rollback
- [ ] Checkpoints defined

### Structural Changes
For each major change:
- [ ] Change implemented
- [ ] Tests updated if needed
- [ ] Tests passing
- [ ] Change committed with clear message
- [ ] Breaking changes documented

### Public API Changes
- [ ] All API changes identified
- [ ] Migration notes written
- [ ] Deprecation warnings added (if applicable)
- [ ] Consumers notified (if applicable)

### Documentation
- [ ] Breaking changes listed
- [ ] Migration instructions provided
- [ ] Architecture changes documented
- [ ] README updated if needed

### Final Verification
- [ ] Full test suite passing
- [ ] No regressions in functionality
- [ ] Code review complete (if applicable)
- [ ] Rollback tested or verified possible

### Completion
- [ ] Final commit/merge
- [ ] Summary report created
- [ ] Rollback point documented
```

---

## Post-Refactor Verification

After any refactoring:

```markdown
## Post-Refactor Checklist

### Functional Verification
- [ ] All tests passing
- [ ] Manual smoke test (if applicable)
- [ ] No console errors/warnings introduced

### Code Quality
- [ ] Code is more readable than before
- [ ] No new complexity introduced
- [ ] Follows established conventions

### Documentation
- [ ] Changes summarized
- [ ] Any follow-up work noted
- [ ] Technical debt tracked (if any deferred)

### Cleanup
- [ ] No temporary/debug code left behind
- [ ] No TODOs without ticket references
- [ ] Working tree clean
```

---

## Quick Decision Checklist

When unsure whether to make a change:

```markdown
## Should I Make This Change?

- [ ] Does it improve readability?
- [ ] Does it reduce complexity?
- [ ] Does it follow established patterns?
- [ ] Can I test that it doesn't break anything?
- [ ] Is it within my defined scope?
- [ ] Would another developer thank me for this?

If NO to any: reconsider or defer the change.
```
