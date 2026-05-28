# Design Phase

> **STOP. Do not write implementation code until this phase is complete.**

## Core Insight: Tests Are Design

Writing tests is not verification — it's **specification**. When you write a test, you are:
- Defining expected behavior
- Clarifying edge cases
- Designing the interface

If you can't write a test, you don't understand the requirement yet.

## Design Checklist

Before any implementation, complete these steps:

### 1. Define Behavior (Required)

- [ ] **What** does this feature/fix do? (1-2 sentences)
- [ ] **How** will users interact with it? (input → output)
- [ ] **What** should NOT change? (side effects to avoid)

### 2. Identify Test Cases (Required)

| Case Type | Questions to Answer |
|-----------|---------------------|
| Happy path | What's the normal successful flow? |
| Edge cases | Empty input? Max values? Concurrent access? |
| Error cases | What should fail? How should it fail? |
| Regression | What existing behavior must NOT break? |

### 3. Write Tests First (Required)

```
# Workflow
1. Write test → it fails (no implementation yet)
2. Write minimal code → test passes
3. Refactor → tests still pass
```

**Do not proceed to implementation until you have at least:**
- 1 happy path test
- 1 edge case test (if applicable)
- 1 error case test (if applicable)

## Test Requirements by Change Type

| Change Type | Minimum Tests |
|-------------|---------------|
| New feature | Happy path + edge cases + error handling |
| Bug fix | Test that reproduces the bug + regression test |
| API/IO change | Integration test with mocked externals |
| Refactor | See below |

### Refactor: Test Requirements

Refactoring means **no behavior change**. Test requirements depend on existing coverage:

| Existing Test Coverage | Action Required |
|------------------------|-----------------|
| Good coverage exists | Existing tests must pass; no new tests needed |
| Coverage is insufficient | **Add tests BEFORE refactoring** |
| Touching concurrency/state/resources | Add stress/boundary tests regardless |

> **Rule:** If you're not confident existing tests catch regressions, you don't have permission to refactor yet.

## When Design Is Complete

You should be able to answer:
1. What tests will I write?
2. What behavior do they verify?
3. What's the minimal code to make them pass?

---

**→ Next:** Load `references/implementation.md` to write code.
