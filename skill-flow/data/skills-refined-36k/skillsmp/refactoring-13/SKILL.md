---
name: refactoring
description: Execute a comprehensive 4-phase refactoring workflow (Analyze, Plan, Execute, Verify).
---

# Refactoring Workflow Skill

**Goal**: Pair programming partner for comprehensive module refactoring.

## Instructions

Follow this strict 4-phase sequence:

### Phase 1: Analyze

- Read code and explain what it does.
- Point out SOLID violations.
- Point out code duplication and potential bugs.

### Phase 2: Plan

- List valid refactoring plan using pseudocode.
- Explain *why* this is better (Performance, Readability, Maintainability).

### Phase 3: Execute

- Output the fully refactored code.
- Ensure necessary comments (JSDoc/DocString).
- Ensure descriptive variable names.

### Phase 4: Verify

- Generate a set of simple unit test cases to verify the logic.

## Appendix: Language-Specific Checks

**TypeScript/JavaScript**

- [ ] Abuse of `any`?
- [ ] Heavy logic in `useEffect`?
- [ ] Async functions using `try/catch`?

**Python**

- [ ] PEP8 compliance?
- [ ] Complex list comprehensions?
- [ ] Context managers (`with`) for resources?
