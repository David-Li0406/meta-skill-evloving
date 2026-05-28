---
name: test
description: Write tests that verify atomic spec acceptance criteria and requirements. Maps each AC to specific test cases, follows AAA pattern, ensures deterministic isolated tests. Use in parallel with implementation or after.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
user-invocable: true
---

# Test Writing Skill

## Purpose

Write tests that verify atomic spec requirements with full traceability to acceptance criteria. Tests serve as executable validation of the spec contract.

**Key Input**: Atomic specs from `.claude/specs/groups/<spec-group-id>/atomic/`

## Usage

```
/test <spec-group-id>                    # Write tests for all atomic specs
/test <spec-group-id> <atomic-spec-id>   # Write tests for specific atomic spec
/test <spec-group-id> --parallel         # Dispatch parallel test writers per atomic spec
```

## Prerequisites

Before using this skill, verify:

1. **Spec group exists** at `.claude/specs/groups/<spec-group-id>/`
2. **review_state** is `APPROVED` in manifest.json
3. **Atomic specs exist** in `atomic/` directory
4. **Enforcement passed** (`atomic_specs.enforcement_status: "passing"`)

If prerequisites not met → STOP and resolve before writing tests.

## Testing Philosophy

### Tests Verify Atomic Spec, Not Implementation
- Tests should validate **what** the system does (behavior)
- Not **how** it does it (implementation details)
- If implementation changes but behavior stays the same, tests should still pass

### One Test Per Acceptance Criterion (Minimum)
- Each AC in each atomic spec gets at least one test
- Complex ACs may need multiple tests
- Test name references atomic spec ID and AC for traceability

### AAA Pattern (Arrange-Act-Assert)
Always structure tests with comments:

```typescript
it("should clear token on logout (as-002 AC1)", () => {
  // Arrange
  const authService = new AuthService();
  authService.setToken("test-token");

  // Act
  authService.logout();

  // Assert
  expect(localStorage.getItem("auth_token")).toBeNull();
});
```

## Test Writing Process

### Step 1: Load and Verify Spec Group

```bash
# Load manifest
cat .claude/specs/groups/<spec-group-id>/manifest.json

# List atomic specs
ls .claude/specs/groups/<spec-group-id>/atomic/
```

Verify:
- `review_state` is `APPROVED`
- `atomic_specs.enforcement_status` is `passing`
- No blocking open questions

### Step 2: Map Atomic Specs to Test Files

For each atomic spec:

```bash
# Read atomic spec
cat .claude/specs/groups/<spec-group-id>/atomic/as-001-logout-button-ui.md
```

Extract from each atomic spec:
- Acceptance criteria (AC1, AC2, etc.)
- Test strategy section
- Edge cases
- Error conditions

Create test mapping:

```markdown
## Test Plan

| Atomic Spec | AC | Test File | Test Case |
|-------------|-----|-----------|-----------|
| as-001 | AC1 | user-menu.test.ts | "should render logout button" |
| as-002 | AC1 | auth-service.test.ts | "should clear token on logout" |
| as-003 | AC1 | auth-router.test.ts | "should redirect to /login" |
| as-004 | AC1 | auth-service.test.ts | "should show error on failure" |
| as-004 | AC2 | auth-service.test.ts | "should keep user logged in on error" |
```

### Step 3: Identify Test Locations

Determine where tests should live:

```bash
# Find existing test patterns
glob "**/*.test.ts"

# Check for related tests
grep -r "describe.*Auth" --include="*.test.ts"
```

Follow project conventions:
- Unit tests: `src/**/__tests__/*.test.ts` or co-located `*.test.ts`
- Integration tests: `tests/integration/*.test.ts`
- E2E tests: `tests/e2e/*.test.ts`

### Step 4: Review Existing Test Patterns

Study how tests are written in this codebase:

```bash
# Read a representative test file
cat src/services/__tests__/auth.test.ts
```

Note:
- Test framework (Jest, Vitest, Mocha)
- Assertion library (expect, assert)
- Mocking approach (jest.mock, vi.mock)
- Builder patterns or factories
- Setup/teardown patterns

### Step 5: Write Tests Per Atomic Spec

For each atomic spec, create tests for all ACs:

```typescript
// Reference atomic spec in describe block
describe("AuthService - as-002: Token Clearing", () => {
  describe("logout", () => {
    it("should clear authentication token (as-002 AC1)", () => {
      // Arrange - Set up test state
      const authService = new AuthService();
      localStorage.setItem("auth_token", "test-token");

      // Act - Execute the behavior
      await authService.logout();

      // Assert - Verify the outcome
      expect(localStorage.getItem("auth_token")).toBeNull();
    });
  });
});
```

### Step 6: Use Builders and Fakes

Prefer in-memory fakes over deep mocking:

**Builder pattern**:
```typescript
// test/builders/user.builder.ts
export class UserBuilder {
  private user: User = {
    id: "test-id",
    name: "Test User",
    email: "test@example.com"
  };

  withId(id: string): this {
    this.user.id = id;
    return this;
  }

  withEmail(email: string): this {
    this.user.email = email;
    return this;
  }

  build(): User {
    return { ...this.user };
  }
}

// In tests
const user = new UserBuilder()
  .withEmail("custom@example.com")
  .build();
```

**Fake implementation**:
```typescript
// test/fakes/fake-auth-api.ts
export class FakeAuthApi implements AuthApi {
  private shouldFail = false;

  async logout(): Promise<void> {
    if (this.shouldFail) {
      throw new Error("Network error");
    }
    // Success - no-op for fake
  }

  setFailure(shouldFail: boolean): void {
    this.shouldFail = shouldFail;
  }
}

// In tests
const fakeApi = new FakeAuthApi();
const authService = new AuthService(fakeApi);
```

### Step 7: Control External Boundaries

Make tests deterministic by controlling:

**Time**:
```typescript
beforeEach(() => {
  jest.useFakeTimers();
  jest.setSystemTime(new Date("2026-01-14T12:00:00Z"));
});

afterEach(() => {
  jest.useRealTimers();
});
```

**Randomness**:
```typescript
const mockRandom = jest.spyOn(Math, "random").mockReturnValue(0.5);
```

**Network**:
```typescript
// Use fakes or mock API responses
const mockFetch = jest.fn().mockResolvedValue({
  ok: true,
  json: async () => ({ success: true })
});
global.fetch = mockFetch;
```

### Step 8: Run Tests

```bash
# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test -- auth-service.test.ts
```

Verify:
- All tests passing
- Coverage meets project standards (typically 80%+)
- No flaky tests (run multiple times to confirm)

### Step 9: Fill Test Evidence in Atomic Specs

For each atomic spec, update its Test Evidence section:

```markdown
## Test Evidence

| AC | Test File | Line | Test Name | Status |
|----|-----------|------|-----------|--------|
| AC1 | src/services/__tests__/auth-service.test.ts | 24 | "should clear token on logout" | ✅ Pass |
| AC2 | src/services/__tests__/auth-service.test.ts | 35 | "should invalidate server session" | ✅ Pass |
```

Also add to the atomic spec's Decision Log:

```markdown
## Decision Log

- `2026-01-14T10:30:00Z`: Created from spec.md decomposition
- `2026-01-14T15:00:00Z`: Tests written - 2 tests covering AC1, AC2
```

### Step 10: Update Manifest

Update manifest.json with test completion:

```json
{
  "convergence": {
    "all_tests_written": true,
    "test_coverage": "94%"
  },
  "decision_log": [
    // ... existing entries ...
    {
      "timestamp": "<ISO timestamp>",
      "actor": "agent",
      "action": "tests_complete",
      "details": "8 tests written for 4 atomic specs, 100% AC coverage"
    }
  ]
}
```

### Step 11: Report Completion

```markdown
## Tests Complete ✅

**Spec Group**: <spec-group-id>
**Atomic Specs**: 4/4 tested

**Test Coverage by Atomic Spec**:
- as-001: 2 tests (AC1, AC2)
- as-002: 2 tests (AC1, AC2)
- as-003: 2 tests (AC1, AC2)
- as-004: 2 tests (AC1, AC2)

**Total Tests**: 8
**AC Coverage**: 100% (8/8 ACs tested)
**Line Coverage**: 94%

**Test Files**:
- src/services/__tests__/auth-service.test.ts (4 tests)
- src/components/__tests__/user-menu.test.ts (2 tests)
- src/router/__tests__/auth-router.test.ts (2 tests)

**Next Steps**:
1. Run `/unify <spec-group-id>` to validate convergence
```

## Testing Guidelines

### Unit Test Guidelines
Test individual units in isolation:

```typescript
// Good - Unit test for AuthService
it("should clear token on logout (as-002 AC1)", () => {
  const authService = new AuthService(fakeApi);
  authService.logout();
  expect(authService.getToken()).toBeNull();
});

// Bad - Integration test disguised as unit test
it("should clear token on logout", () => {
  const authService = new AuthService(); // Uses real API
  authService.logout(); // Makes real network call
  expect(authService.getToken()).toBeNull(); // Flaky!
});
```

### Integration Test Guidelines
Test interactions between units:

```typescript
// Integration test for full logout flow
it("should complete full logout flow (as-001 to as-004)", async () => {
  // Arrange - Real dependencies
  const api = new AuthApi(testConfig);
  const authService = new AuthService(api);
  const router = new Router();

  // Act
  await authService.logout();

  // Assert
  expect(router.currentRoute).toBe("/login");
  expect(authService.isAuthenticated()).toBe(false);
});
```

### Edge Case Testing
Cover edge cases from atomic spec:

```typescript
describe("edge cases", () => {
  it("should handle logout when already logged out (as-002 edge)", () => {
    // Arrange
    const authService = new AuthService();
    // User not logged in

    // Act & Assert - Should not throw
    expect(() => authService.logout()).not.toThrow();
  });

  it("should handle concurrent logout calls (as-002 edge)", async () => {
    // Arrange
    const authService = new AuthService();

    // Act - Multiple simultaneous logouts
    await Promise.all([
      authService.logout(),
      authService.logout(),
      authService.logout()
    ]);

    // Assert - Only one API call made
    expect(mockApi.post).toHaveBeenCalledTimes(1);
  });
});
```

### Error Path Testing
Test all error conditions per atomic spec:

```typescript
// Tests for as-004: Error Handling
describe("error handling (as-004)", () => {
  it("should handle network error (as-004 AC1)", async () => {
    // Arrange
    mockApi.post.mockRejectedValue({ code: "NETWORK_ERROR" });

    // Act & Assert
    await expect(authService.logout()).rejects.toThrow("Logout failed");
  });

  it("should keep user logged in on error (as-004 AC2)", async () => {
    // Arrange
    authService.setToken("test-token");
    mockApi.post.mockRejectedValue({ code: "NETWORK_ERROR" });

    // Act
    try {
      await authService.logout();
    } catch (e) {
      // Expected
    }

    // Assert - Token still present
    expect(authService.getToken()).toBe("test-token");
  });
});
```

## Parallel Execution with Implementation

Tests can be written in parallel with implementation.

### Approach: TDD-Style
1. Write tests first (they will fail)
2. Run implementer in parallel
3. Tests pass as implementation completes

```javascript
// Main agent dispatches both
Task({
  description: "Write tests for logout",
  prompt: `Write tests for all atomic specs in spec group sg-logout-button.

  Location: .claude/specs/groups/sg-logout-button/atomic/

  Do NOT implement - test-writer only writes tests.`,
  subagent_type: "test-writer"
});

Task({
  description: "Implement logout",
  prompt: `Implement all atomic specs in spec group sg-logout-button.

  Location: .claude/specs/groups/sg-logout-button/atomic/

  Do NOT write tests - implementer only writes implementation.`,
  subagent_type: "implementer"
});
```

### Synchronization Point
After both complete:
- Run tests to verify implementation
- Use `/unify` to validate alignment

## Test Anti-Patterns to Avoid

### Don't Test Implementation Details
```typescript
// Bad - Tests implementation
it("should call localStorage.removeItem", () => {
  authService.logout();
  expect(localStorage.removeItem).toHaveBeenCalledWith("auth_token");
});

// Good - Tests behavior
it("should clear token on logout (as-002 AC1)", () => {
  authService.logout();
  expect(authService.getToken()).toBeNull();
});
```

### Don't Use Deep Mocking
```typescript
// Bad - Deep mock
jest.mock("./auth-service", () => ({
  AuthService: jest.fn().mockImplementation(() => ({
    logout: jest.fn(),
    getToken: jest.fn()
  }))
}));

// Good - Fake implementation
class FakeAuthService implements AuthService {
  logout() { /* simple fake behavior */ }
  getToken() { return null; }
}
```

### Don't Write Brittle Tests
```typescript
// Bad - Brittle (breaks if message changes)
expect(error.message).toBe("Logout failed. Please try again.");

// Good - Flexible (tests intent)
expect(error.message).toMatch(/logout failed/i);
```

## Integration with Other Skills

After writing tests:
- Use `/implement` (if not run in parallel) to implement features
- Use `/unify` to validate spec-test-implementation alignment
- Tests become evidence in convergence validation

After unify passes, the review chain is:
1. `/code-review` - Code quality review
2. `/security` - Security review
3. `/browser-test` - UI validation (if UI changes)
4. `/docs` - Documentation generation (if public API)
5. Commit

## Examples

### Example 1: Unit Test for Atomic Spec as-002

**Atomic spec as-002-token-clearing.md**:
```markdown
## Acceptance Criteria
- AC1: When logout called, clear authentication token from localStorage
- AC2: When logout called, invalidate server session
```

**Test**:
```typescript
// src/services/__tests__/auth-service.test.ts
import { AuthService } from "../auth-service";
import { FakeAuthApi } from "../../test/fakes/fake-auth-api";

describe("AuthService - as-002: Token Clearing", () => {
  describe("logout", () => {
    it("should clear authentication token (as-002 AC1)", async () => {
      // Arrange
      const fakeApi = new FakeAuthApi();
      const authService = new AuthService(fakeApi);
      authService.setToken("test-token-123");

      // Act
      await authService.logout();

      // Assert
      expect(authService.getToken()).toBeNull();
    });

    it("should invalidate server session (as-002 AC2)", async () => {
      // Arrange
      const fakeApi = new FakeAuthApi();
      const authService = new AuthService(fakeApi);

      // Act
      await authService.logout();

      // Assert
      expect(fakeApi.wasLogoutCalled()).toBe(true);
    });
  });
});
```

### Example 2: Integration Test for Multiple Atomic Specs

**Test**:
```typescript
// tests/integration/logout-flow.test.ts
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { App } from "../../src/App";

describe("Logout flow integration (as-001 to as-003)", () => {
  it("should complete full logout flow", async () => {
    // Arrange
    render(<App initialRoute="/dashboard" />);

    // Act - as-001: Click logout button
    const logoutButton = screen.getByRole("button", { name: /logout/i });
    fireEvent.click(logoutButton);

    // Assert - as-002: Token cleared (implicit via auth state)
    // Assert - as-003: Redirect to login
    await waitFor(() => {
      expect(screen.getByRole("heading", { name: /login/i })).toBeInTheDocument();
    });
  });
});
```

### Example 3: Error Path Test

**Atomic spec as-004-error-handling.md**:
```markdown
## Acceptance Criteria
- AC1: When logout API call fails, display error message
- AC2: When logout fails, user remains logged in (token NOT cleared)
```

**Test**:
```typescript
describe("error handling (as-004)", () => {
  it("should display error message on network failure (as-004 AC1)", async () => {
    // Arrange
    const fakeApi = new FakeAuthApi();
    fakeApi.setFailure(true);
    const authService = new AuthService(fakeApi);

    // Act & Assert
    await expect(authService.logout()).rejects.toThrow(/logout failed/i);
  });

  it("should keep user logged in on error (as-004 AC2)", async () => {
    // Arrange
    const fakeApi = new FakeAuthApi();
    fakeApi.setFailure(true);
    const authService = new AuthService(fakeApi);
    authService.setToken("test-token");

    // Act
    try {
      await authService.logout();
    } catch (e) {
      // Expected
    }

    // Assert - Token still present
    expect(authService.getToken()).toBe("test-token");
  });
});
```
