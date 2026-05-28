---
name: code-review
description: "Review code and suggest improvements, refactors, and clarifications"
allowed-tools: Read, Grep, Glob
---

# Code Review Patterns

## Overview

Code reviews catch bugs before they ship.
Clean code and good architecture is easier for both humans and agents to understand, and therefore to modify.

## Quick Review Checklist (Reference Pattern)

**For rapid reviews, check these 8 items:**

- [ ] Code is simple and readable
- [ ] Functions and variables have clear semantic names
- [ ] No duplicated code without reason
- [ ] Proper error handling and clear error messages
- [ ] No exposed secrets or API keys
- [ ] Input validation implemented
- [ ] Good test coverage
- [ ] Performance considerations addressed
- [ ] API design is "deep", minimal API surface with maximal functionality

---

## Extended Review Rubric

Examine each of the principles below and document violations, categorizing them according to severity.

### Depth over Decomposition
- **Problem**: System split into many small modules that expose logic to callers.
- **Why it’s bad**: Complexity is distributed; callers pay cognitive cost; changes ripple.
- **Smells**:
  - Many tiny classes/functions with minimal behavior.
  - Callers contain orchestration, conditionals, or policy.
  - Excessive “glue code.”
- **Fixes**:
  - Merge shallow modules.
  - Pull logic and policy downward.
  - Prefer fewer, deeper abstractions.

### Interfaces Simple Relative to Power
- **Problem**: Interfaces force callers to manage many details.
- **Why it’s bad**: High recall cost; increased coupling.
- **Smells**:
  - Many parameters or flags.
  - Config objects with many rarely-used fields.
  - Repeated argument combinations.
- **Fixes**:
  - Replace flags with semantic operations.
  - Strong defaults.
  - Collapse parameters into intent-level APIs.

### Caller Shouldn’t Know Implementation Details
- **Problem**: Interfaces leak internal representation or mechanisms.
- **Why it’s bad**: Tight coupling; high change amplification.
- **Smells**:
  - Getters/setters everywhere.
  - Params like `useRedis`, `bufferSize`, `offset`.
  - Callers mutating internal data structures.
- **Fixes**:
  - Hide data structures.
  - Expose operations, not state.
  - Rename APIs in terms of *what*, not *how*.

### Centralize Complexity
- **Problem**: Same logic reimplemented locally in multiple places.
- **Why it’s bad**: Inconsistency; subtle bugs; impossible global fixes.
- **Smells**:
  - Multiple `toCamelCase`, `debounce`, `retry`, formatting helpers.
  - Slightly different copies of the same logic.
- **Fixes**:
  - Choose a canonical implementation.
  - Centralize behind a single abstraction.
  - Test it; block new copies.

### Optimize for Cognitive Load, Not Line Count
- **Problem**: Code optimized for brevity or cleverness.
- **Why it’s bad**: Harder reasoning; higher bug risk.
- **Smells**:
  - Dense one-liners.
  - Clever functional chains.
  - Non-obvious control flow.
- **Fixes**:
  - Prefer obvious over clever.
  - Name intermediate steps.
  - Make invariants explicit.

### Slight Generality, Not Over-Abstraction
- **Problem**: Code is hyper-specific or prematurely generic.
- **Why it’s bad**: Duplication or needless complexity.
- **Smells**:
  - Parameterized functions used once.
  - “For future use” abstractions.
- **Fixes**:
  - Design for current use + one plausible variation.
  - Abstract only after duplication appears.
  - Pull complexity downward when abstracting.

### Policy Belongs Inside the Module
- **Problem**: Callers decide formatting, retry, debounce semantics.
- **Why it’s bad**: Inconsistent behavior across the system.
- **Smells**:
  - Repeated conditionals around the same operation.
  - Same utility used with different flags everywhere.
- **Fixes**:
  - Define canonical policies (`formatCurrency`, `debounceSearchInput`).
  - Expose policy-level APIs.

### Tests Are the Price of Centralization
- **Problem**: Shared utilities without clear guarantees.
- **Why it’s bad**: Centralized bugs with large blast radius.
- **Smells**:
  - Untested shared helpers.
  - Fear of modifying shared code.
- **Fixes**:
  - Table-driven tests for edge cases.
  - Explicit semantic guarantees.
  - Fewer, better-tested utilities.

### Judge Design by Change Cost
- **Problem**: Design judged by structure or style instead of change impact.
- **Why it’s bad**: Misses real complexity.
- **Smells**:
  - Small changes touch many files.
  - Defensive edits.
- **Fixes**:
  - Ask “where does complexity live?”
  - Refactor so future changes touch one module.

### Naming Should Encode Intent
- **Problem**: Names are vague, generic, or misleading.
- **Why it’s bad**: Increases cognitive load; obscures abstraction.
- **Smells**:
  - Names like `calc`, `doStuff`, `handle`.
  - Overuse of `Manager`, `Helper`, `Util`.
- **Fixes**:
  - Use precise, domain-relevant names.
  - Prefer verbs for actions, nouns for concepts.
  - Rename when abstraction changes.

### Functions Should Do One Coherent Thing
- **Problem**: Functions have multiple responsibilities.
- **Why it’s bad**: Hard to reason about; hard to reuse or test.
- **Smells**:
  - Long functions.
  - Multiple unrelated conditionals.
- **Fixes**:
  - Split by responsibility *inside* the module.
  - Extract helpers that hide detail, not expose it.
- **BUT**: remember optimize for cognitive load, not line count

### Control Flow Should Be Obvious
- **Problem**: Logic is deeply nested or tangled.
- **Why it’s bad**: High cognitive load; error-prone.
- **Smells**:
  - Deeply nested `if/else` or `try/catch`.
  - Multiple exit paths with unclear invariants.
- **Fixes**:
  - Early returns.
  - Extract helper functions.
  - Flatten control flow.

### Explicit Error Handling
- **Problem**: Errors are swallowed or ignored.
- **Why it’s bad**: Silent failures; undefined states.
- **Smells**:
  - Empty `catch` blocks.
  - Logging and continuing blindly.
- **Fixes**:
  - Propagate errors or handle explicitly.
  - Define clear failure semantics.
  - Prefer failing fast to hiding errors.

### Avoid Implicit Coupling
- **Problem**: Code relies on hidden globals, env, or order dependence.
- **Why it’s bad**: Non-local reasoning; fragile behavior.
- **Smells**:
  - Hidden globals or shared mutable state.
  - Functions that “just assume” setup.
- **Fixes**:
  - Make dependencies explicit.
  - Pass dependencies in.
  - Reduce shared state.

### Performance: Eliminate Structural Inefficiencies
- **Problem**: Inefficient patterns baked into design.
- **Why it’s bad**: Performance fixes become invasive or impossible.
- **Smells**:
  - N+1 queries.
  - Repeated expensive operations.
  - Sync blocking on hot paths.
- **Fixes**:
  - Batch operations.
  - Cache where appropriate.
  - Use async/non-blocking patterns.

### Resource Lifetime Must Be Explicit
- **Problem**: Resources are allocated but not released.
- **Why it’s bad**: Memory leaks; degraded performance.
- **Smells**:
  - Objects never cleaned up.
  - Long-lived references.
- **Fixes**:
  - Explicit cleanup/dispose.
  - Tie lifetime to clear ownership.

### Configuration Should Not Be Control Flow
- **Problem**: Behavior controlled by many flags or env vars.
- **Why it’s bad**: Combinatorial complexity; hard reasoning.
- **Smells**:
  - Many boolean flags.
  - Env vars altering core logic.
- **Fixes**:
  - Consolidate configuration.
  - Define explicit modes or profiles.
  - Replace flags with separate APIs.

### Maintain Clear Module Boundaries
- **Problem**: Modules change for unrelated reasons.
- **Why it’s bad**: High churn; unclear ownership.
- **Smells**:
  - Frequent unrelated edits to same files.
  - “God modules.”
- **Fixes**:
  - Enforce single-responsibility boundaries.
  - Split by reason-to-change.

### Enforce Invariants in Code, Not Comments
- **Problem**: Correctness relies on discipline or documentation.
- **Why it’s bad**: Invariants drift; bugs creep in.
- **Smells**:
  - Comments explaining required call order.
  - “Must be called before…” notes.
- **Fixes**:
  - Encode invariants in types and structure.
  - Make invalid states unrepresentable.

### UI: Make States Explicit
- **Problem**: UI doesn’t represent all system states.
- **Why it’s bad**: Confusing UX; hidden failures.
- **Smells**:
  - No loading, empty, or error states.
- **Fixes**:
  - Explicit loading, error, empty, and success states.
  - Inline validation and feedback.

### Accessibility Is Part of Design
- **Problem**: UI only works for ideal users.
- **Why it’s bad**: Excludes users; legal and ethical risk.
- **Smells**:
  - Non-semantic HTML.
  - Mouse-only interactions.
  - Poor contrast.
- **Fixes**:
  - Semantic elements.
  - Keyboard accessibility.
  - Visible focus, sufficient contrast.
  - Screen-reader-friendly labels.

## Spiritual/Moral Coherence of Code
- **Problem**: Some solutions violate spiritual principles of the Dao
- **Why it's bad**: Dehumanizing, possible eternal consquences
- **Smells**:
  - Convenience at all costs
  - Features that serve Landlords and not Workers
  - Canned food is ultimately very damaging to the soul
- **Fixes**:
  - Exorcism
  - Two-weeks' notice
  - Doing it better

## Severity Classification

| Severity | Definition | Action |
|----------|------------|--------|
| **CRITICAL** | Security vulnerability or blocks functionality | Must fix before merge |
| **MAJOR** | Affects functionality or significant quality issue | Should fix before merge |
| **MINOR** | Style issues, small improvements | Can merge, fix later |
| **NIT** | Purely stylistic preferences | Optional |

## Priority Output Format (Feedback Grouping)

**Organize feedback by priority (from reference pattern):**

```markdown
## Code Review Feedback

### Critical (must fix before merge)
- [95] SQL injection at `src/api/users.ts:45`
  → Fix: Use parameterized query `db.query('SELECT...', [userId])`

### Warnings (should fix)
- [85] N+1 query at `src/services/posts.ts:23`
  → Fix: Batch query with WHERE IN clause

### Suggestions (consider improving)
- [70] Function `calc()` could be renamed to `calculateTotal()`
  → More descriptive naming
```

**ALWAYS include specific examples of how to fix each issue.**
Don't just say "this is wrong" - show the correct approach.

## Red Flags - STOP and Re-review

If you find yourself:

- Reviewing code style before checking functionality
- Not running the tests
- Skipping the security checklist
- Giving generic feedback ("looks good")
- Not providing file:line citations
- Not explaining WHY something is wrong
- Not providing fix recommendations

**STOP. Start over with Stage 1.**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Tests pass so it's fine" | Tests can miss requirements. Check spec compliance. |
| "Code looks clean" | Clean code can still be wrong. Verify functionality. |
| "I trust this developer" | Trust but verify. Everyone makes mistakes. |
| "It's a small change" | Small changes cause big bugs. Review thoroughly. |
| "No time for full review" | Bugs take more time than reviews. Do it properly. |
| "Security is overkill" | One vulnerability can sink the company. Check it. |

## Output Format

```markdown
## Code Review: [PR Title/Component]

**Security:**
- [CRITICAL] Issue at `file:line` - Fix: [recommendation]
- No issues found ✅

**Performance:**
- [MAJOR] N+1 query at `file:line` - Fix: Use batch query
- No issues found ✅

**Quality:**
- [MINOR] Unclear naming at `file:line` - Suggestion: rename to X
- No issues found ✅

**UX/A11y:** (if UI code)
- [MAJOR] Missing loading state - Fix: Add spinner
- No issues found ✅

---

### Summary

**Decision:** Approve / Request Changes

**Critical:** [count]
**Major:** [count]
**Minor:** [count]

**Required fixes before merge:**
1. [Most important fix]
2. [Second fix]
```

## Review Loop Protocol

After requesting changes:

1. **Wait for fixes** - Developer addresses issues
2. **Re-review** - Check that fixes actually fix the issues
3. **Verify no regressions** - Run tests again
4. **Approve or request more changes** - Repeat if needed

**Never approve without verifying fixes work.**

## Final Check

Before approving:

- [ ] All critical/major issues addressed
- [ ] Tests pass
- [ ] No regressions introduced
- [ ] Evidence captured for each claim

