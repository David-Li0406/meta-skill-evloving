---
name: Test Automation Suite
description: Unified runner for smoke tests, visual regression checks, and reliability reporting.
---

# 🧪 Test Automation Suite Skill

This skill powers the **QA Agent**. It provides a reliable way to run critical test paths and verify "Does it actually work?" before pushing.

## 🎯 When to Use
- **After Logic Changes**: Run smoke tests.
- **Before Committing**: Mandatory check.
- **New Feature**: **MUST** add a corresponding test.

## 🛠️ Toolbelt

### 1. The Runner (Automated)
Executes the critical path checks.

```bash
# Fast Smoke Tests (Critical Paths Only)
node .agent/skills/test-automation/scripts/run-smoke-tests.js

# Full Suite (Nightly/Deep)
npx playwright test
```

### 2. Flakiness Patrol (Best Practices)
Avoid these anti-patterns to keep tests green.

| Anti-Pattern | Why it breaks | The Reliable Fix |
|:---:|:---:|:---:|
| `waitForTimeout(1000)` | Random failures | `waitForSelector('data-testid=x')` |
| `.class-name` selectors | Fragile CSS | `getByTestId('submit-btn')` |
| Testing too much | Slow | Test the **user flow**, not every prop. |

## 🚀 Workflows

### Workflow A: The "Green Light" Check
Use this before every `git push`.

1. **Run**: `run-smoke-tests.js`.
2. **Fail?**: **Do not push.** Fix the code, not the test (usually).
3. **Pass?**: You are safe to proceed.

### Workflow B: Adding Coverage
Use this when adding a new feature (e.g., "Gift Wrapping").

1. **Scaffold**: Create `tests/gift-wrapping.spec.ts`.
2. **Select**: Use the codified `data-testid` convention (`gift-wrap-checkbox`).
3. **Assert**: distinct state change (e.g., "Total price increased").
4. **Register**: Add to smoke config if it's a critical path.

## 🧠 Testing Pyramid
1.  **Unit**: (Fastest) Logic only. Jest/Vitest.
2.  **Integration**: Components working together.
3.  **E2E (Smoke)**: (Slowest/Most Important) Does the user succeed? **Focus here.**
