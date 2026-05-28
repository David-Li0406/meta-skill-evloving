# Anti-Patterns to Avoid

Common mistakes in TDD runbook creation and how to fix them.

---

| Anti-Pattern | Bad Example | Good Example |
|--------------|-------------|--------------|
| **Setup-only cycles** | `Cycle 1.1: Create test fixture` (no test, just fixture) | `Cycle 1.1: Test fixture works correctly` - RED: Fixture doesn't exist, GREEN: Create fixture, Verify: Fixture behaves as expected |
| **God cycles** | `Cycle 2.1: Implement entire auth system` - Tests login + logout + token refresh + password reset + 2FA | Split: `2.1: Basic login`, `2.2: Logout`, `2.3: Token refresh`, `2.4: Password reset`, `2.5: 2FA` |
| **Unclear RED** | `Expected failure: Something will fail` | `Expected failure: ModuleNotFoundError: No module named 'auth'` + Why: Auth module not created yet |
| **Missing regression** | `Verify GREEN: pytest tests/test_new.py` (stops here) | `Verify GREEN: pytest tests/test_new.py` (must pass) + `Verify no regression: pytest tests/` (all existing tests pass) |
| **Coupled cycles** | `3.1: Modify shared state`, `3.2: Test that state was modified` (implicit dependency) | `3.1: Test state modification [sets up state]`, `3.2: Test state query [DEPENDS: 3.1]` - Explicit dependency, clear order |

---
