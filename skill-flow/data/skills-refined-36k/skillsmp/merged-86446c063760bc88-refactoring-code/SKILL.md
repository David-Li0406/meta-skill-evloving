---
name: refactoring-code
description: Use this skill to improve code structure while preserving behavior through systematic refactoring and test verification.
---

# Refactoring Code

You are following a systematic refactoring methodology that improves code quality, maintainability, and simplicity while **preserving existing behavior**.

**Core Principle:** Refactoring changes structure, not functionality. Safety and clarity are more important than elegance.

## The Iron Law

```
BEHAVIOR MUST BE PRESERVED
Tests must verify behavior, not implementation
```

If you change what the code does (not just how it does it), you're not refactoring—you're rewriting.

## Prerequisites

- Access to codebase for pattern research
- **Behavior-driven tests** that verify current functionality
- Understanding of project conventions

## Core Responsibilities

1. **Simplify Complex Code** - Break down complex functions, reduce nesting, improve readability.
2. **Extract Patterns** - Identify and extract reusable components, hooks, utilities.
3. **Eliminate Duplication** - Apply DRY principles while avoiding premature abstraction.
4. **Improve Type Safety** - Strengthen TypeScript usage, eliminate `any` types when possible.
5. **Performance Optimization** - Identify unnecessary re-renders, optimize data structures.
6. **Align with Standards** - Ensure code follows project patterns and conventions.

## The Five-Phase Refactoring Process

You MUST complete each phase before proceeding to the next.

Copy this checklist and track your progress:

```
Refactoring Progress:
- [ ] Phase 1: Understand Current Behavior
  - [ ] Read existing code thoroughly
  - [ ] Check usage across codebase
  - [ ] Document current behavior
- [ ] Phase 2: Verify Test Coverage (CRITICAL)
  - [ ] Behavior-driven tests exist and pass
  - [ ] Tests cover main workflows and edge cases
  - [ ] Tests don't depend on implementation details
- [ ] Phase 3: Identify Issues
  - [ ] Issues documented with locations
  - [ ] Issues categorized by type and severity
  - [ ] Root cause understood for each issue
- [ ] Phase 4: Plan Refactoring
  - [ ] Broken into small, verifiable steps
  - [ ] Each step has verification criteria
  - [ ] Dependencies between steps identified
- [ ] Phase 5: Execute & Verify
  - [ ] All planned changes implemented
  - [ ] All tests pass
  - [ ] No new type errors or warnings
  - [ ] Behavior verified unchanged
```

### Phase 1: Understand Current Behavior

**Objective:** Know exactly what the code does before changing how it does it.

1. **Read existing code thoroughly**
   - Understand the purpose, not just the implementation.
   - Identify inputs, outputs, and side effects.
   - Note any edge cases or error handling.

2. **Check usage across codebase**
   - Use Grep to find all call sites.
   - Understand how consumers depend on this code.
   - Identify any public APIs that must remain stable.

3. **Document current behavior**
   - List what the code accomplishes.
   - Note any implicit contracts or assumptions.
   - Identify performance characteristics if relevant.

**Phase 1 Complete When:**
- [ ] You can explain what the code does in plain language.
- [ ] All call sites and dependencies are identified.
- [ ] Current behavior is documented.

### Phase 2: Verify Test Coverage (CRITICAL)

**Objective:** Ensure behavior-driven tests exist that will catch regressions.

**BEFORE refactoring, ensure tests verify BEHAVIOR (what users see/do), NOT implementation:**

✅ **Good - Behavior-driven tests:**
```typescript
// Tests user-observable behavior
test('displays error message when API returns 404', async () => {
  server.use(
    http.get('/api/users', () => new HttpResponse(null, { status: 404 }))
  );
  render(<UserList />);
  expect(await screen.findByText(/user not found/i)).toBeInTheDocument();
});
```

❌ **Bad - Implementation-detail tests:**
```typescript
// Tests internal state/functions - breaks during refactoring
test('sets error state when fetch fails', () => {
  const wrapper = shallow(<UserList />);
  wrapper.instance().handleError(new Error('404'));
  expect(wrapper.state('error')).toBe('404');
});
```

**Test Quality Checklist:**
- [ ] Tests verify user workflows, not function calls.
- [ ] Tests use real dependencies (not mocks of components).
- [ ] Tests query by role/label/text, not internal state.
- [ ] Tests will survive refactoring when behavior unchanged.

**If tests are missing or test implementation details:**

1. **Add behavior-driven tests first.**
2. Focus on user workflows, loading/error states, interactions.
3. Ensure new tests are passing before refactoring.

**Phase 2 Complete When:**
- [ ] Behavior-driven tests exist and pass.
- [ ] Tests cover main workflows and edge cases.
- [ ] Tests don't depend on implementation details.

### Phase 3: Identify Issues

**Objective:** Systematically catalog what needs improvement.

**Common refactoring opportunities:**

| Issue Type | Indicators | Impact |
|------------|-----------|---------|
| **Complexity** | Deep nesting (>3 levels), long functions (>50 lines), many parameters (>4) | Hard to understand, error-prone |
| **Duplication** | Copy-pasted code, repeated patterns, similar logic in multiple places | Maintenance burden, inconsistent fixes |
| **Poor Naming** | Unclear variables (`x`, `data`, `temp`), misleading names, inconsistent terminology | Cognitive overhead |
| **Type Safety Gaps** | `any` types, missing types, type assertions, implicit any | Runtime errors, poor IDE support |
| **Performance Issues** | Unnecessary re-renders, inefficient algorithms (O(n²) when O(n) possible), large bundle size | Slow UX, high resource usage |
| **Pattern Violations** | Inconsistent with project conventions, outdated patterns | Team confusion, tech debt |

**Analysis checklist:**
- [ ] Identify specific complexity hotspots.
- [ ] Catalog duplicated code blocks.
- [ ] List unclear or misleading names.
- [ ] Find type safety vulnerabilities.
- [ ] Measure performance bottlenecks (if applicable).
- [ ] Check against project conventions.

**Phase 3 Complete When:**
- [ ] All issues are documented with locations.
- [ ] Issues are categorized by type and severity.
- [ ] You understand the root cause of each issue.

### Phase 4: Plan Refactoring

**Objective:** Create a safe, incremental execution plan.

1. **Create todo list for multi-step refactorings.**
   - Break large refactorings into small, verifiable steps.
   - Each step should be independently testable.

2. **Prioritize changes by impact and risk.**
   - High impact, low risk first (e.g., rename variables).
   - Defer high-risk changes (e.g., algorithm rewrites).

3. **Consider backward compatibility.**
   - If this is a public API, can we deprecate gradually?
   - Do we need to support both old and new interfaces temporarily?

4. **Plan verification steps.**
   - What will you check after each change?
   - Which tests must pass?

**Phase 4 Complete When:**
- [ ] Refactoring is broken into small steps.
- [ ] Each step has clear verification criteria.
- [ ] Dependencies between steps are identified.
- [ ] Risk mitigation strategies are planned.

### Phase 5: Execute & Verify

**Objective:** Make changes safely with continuous verification.

**Execution principles:**

1. **Make one change at a time.**
   - Single responsibility per edit.
   - Commit frequently if using git.

2. **Run tests after each change.**
   - Don't accumulate untested changes.
   - Catch regressions immediately.

3. **Check TypeScript compilation.**
   - `tsc --noEmit` or equivalent.
   - Fix type errors before proceeding.

4. **Verify behavior unchanged.**
   - Run the application manually if needed.
   - Confirm user-facing behavior is identical.

**Phase 5 Complete When:**
- [ ] All planned changes are implemented.
- [ ] All tests pass.
- [ ] No new type errors or warnings.
- [ ] Code follows project conventions.
- [ ] Behavior is verified unchanged.

## Red Flags - STOP and Reassess

If you catch yourself:

- **Changing behavior while refactoring** → You're rewriting, not refactoring. Separate behavior changes from refactoring.
- **"I'll just skip the tests this time"** → Tests are your safety net. No tests = no safe refactoring.
- **Adding complexity to remove complexity** → Over-engineering. Simpler solution probably exists.
- **"This is clever!"** → Code should be clear, not clever. Clever code is hard to maintain.
- **Removing comments that explained context** → Comments explaining "why" are valuable. Keep them.
- **Breaking existing APIs without considering consumers** → Check all call sites. Plan deprecation if needed.
- **Abstracting before seeing pattern 3 times** → Rule of Three: Don't abstract until you see the pattern repeated three times.

**ALL of these mean: STOP. Reassess your approach.**

## Key Principles Summary

1. **Preserve behavior** - Tests must verify same outcomes before and after.
2. **Test first** - Behavior-driven tests are your safety net.
3. **Small steps** - One change at a time, verify continuously.
4. **Clarity over cleverness** - Code should be obvious, not impressive.
5. **Rule of Three** - Don't abstract until you see the pattern three times.
6. **Safety over elegance** - Working code is better than beautiful code.

**Remember:** The goal of refactoring is to make future changes easier, not to make code perfect.