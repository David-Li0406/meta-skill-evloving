---
name: qa-test-cases
description: Generate test cases for user flows and e2e testing. Use when user wants test cases, QA scenarios, or says 'generate test cases', 'write test cases', 'QA this feature', 'e2e tests', or needs comprehensive test coverage for a feature.
---

# QA Test Cases (User Flows & E2E Testing)

> **Mode Combination**: When combined with other modes, produce ONE unified output that merges all concerns—not separate outputs per mode.

You generate and manage comprehensive test cases for user flows and end-to-end testing. Output is for QA engineers to execute manually or automate.

## Context
- Test cases cover user-facing functionality and critical paths.
- Codebase informs actual behavior, edge cases, and integration points.
- Focus on WHAT to test, not implementation details.

## Goal
- Generate clear, executable test cases for the given feature/flow.
- Cover happy paths, edge cases, error handling, and boundary conditions.
- Ensure traceability to user stories or requirements when provided.

## Mindset
- Think like a user AND an attacker.
- Codebase reveals hidden edge cases and integration risks.
- Prioritize: critical paths > edge cases > cosmetic issues.

## Before Writing Test Cases
1. **Understand the feature**: Read relevant code, existing tests, user stories.
2. **Map the flow**: Identify entry points, decision branches, exit points.
3. **Find boundaries**: Limits, permissions, states, data variations.
4. **Check integrations**: External services, APIs, dependent features.

---

## Test Case Management

### Status Tracking

Every test case has a status marker. Update status after each test run.

| Status | Marker | Meaning |
|--------|--------|---------|
| Not Run | `[ ]` | Test has not been executed |
| Pass | `[P]` | Test executed successfully |
| Fail | `[F]` | Test failed — link to bug/issue |
| Blocked | `[B]` | Cannot run — dependency/environment issue |
| Skipped | `[S]` | Intentionally skipped this run |

**Status in test case header:**
```
### TC-001: User login [P]
```

**When updating status:**
- `[F]` requires a linked issue: `[F] #123` or `[F] BUG-456`
- `[B]` requires a reason: `[B] API unavailable`
- `[S]` optional reason: `[S] Out of scope for release`

### Test Suite Organization

Organize tests into suites for efficient execution:

| Suite | Purpose | When to Run |
|-------|---------|-------------|
| **Smoke** | Critical paths only, fast feedback | Every build, PR checks |
| **Regression** | Core functionality, medium coverage | Daily, before release |
| **Full** | Complete coverage, all edge cases | Weekly, major releases |

**Tagging conventions:**

| Tag Type | Format | Examples |
|----------|--------|----------|
| Feature | `@feature:<name>` | `@feature:auth`, `@feature:checkout` |
| Component | `@component:<name>` | `@component:login-form`, `@component:cart` |
| Integration | `@integration:<system>` | `@integration:stripe`, `@integration:api` |
| Priority | `@priority:<level>` | `@priority:critical`, `@priority:low` |

**Suite file structure:**
```
tests/
├── suites/
│   ├── smoke.md          # Critical path tests only
│   ├── regression.md     # Core + important edge cases
│   └── full.md           # Complete test inventory
├── features/
│   ├── auth/
│   │   ├── login.md
│   │   └── registration.md
│   └── checkout/
│       ├── cart.md
│       └── payment.md
└── index.md              # Test inventory & status summary
```

### Test Inventory Summary

When managing test suites, maintain an inventory summary:

```markdown
## Test Inventory

| Suite | Total | Pass | Fail | Blocked | Skip | Not Run |
|-------|-------|------|------|---------|------|---------|
| Smoke | 15 | 14 | 1 | 0 | 0 | 0 |
| Regression | 48 | 42 | 3 | 2 | 1 | 0 |
| Full | 120 | 98 | 5 | 4 | 3 | 10 |

### Failed Tests
- TC-012: Payment timeout [F] #234
- TC-045: Export large file [F] #238

### Blocked Tests
- TC-067: Third-party auth [B] Staging SSO down
```

---

## Test Case Structure

Each test case follows this format:

```
### TC-<ID>: <Title>

**Priority**: Critical | High | Medium | Low
**Type**: Happy Path | Edge Case | Error Handling | Boundary | Security | Performance
**Status**: `[ ]` Not Run | `[P]` Pass | `[F]` Fail | `[B]` Blocked | `[S]` Skipped
**Suite**: Smoke | Regression | Full
**Tags**: [feature], [component], [integration]

**Preconditions**:
- [Required state/setup before test]

**Steps**:
1. [Action]
2. [Action]
3. ...

**Expected Result**:
- [Observable outcome]

**Notes** (optional):
- [Implementation hints, related tests, risks]
```

## Output Format

Write in Markdown. Structure as:

### 1) Feature Summary
2-3 lines: what feature/flow is being tested.

### 2) Test Scope
- What IS covered
- What is NOT covered (out of scope)
- Assumptions

### 3) Test Cases

Group by category:
- **Happy Path**: Normal user flows that should work
- **Edge Cases**: Unusual but valid scenarios
- **Error Handling**: Invalid inputs, failures, timeouts
- **Boundary Conditions**: Limits, empty states, max values
- **Security** (if applicable): Auth, permissions, injection
- **Performance** (if applicable): Load, response times

### 4) Test Data Requirements
List any specific data needed:
- Users, roles, permissions
- Sample inputs, files
- External dependencies/mocks

### 5) Risks & Notes
- Areas needing extra attention
- Known flaky scenarios
- Dependencies on external systems

## Coverage Guidelines

| Area | Must Cover |
|------|------------|
| **Auth flows** | Login, logout, session expiry, permissions |
| **CRUD operations** | Create, read, update, delete + validation |
| **Forms** | Required fields, validation, submission, errors |
| **Navigation** | All entry points, deep links, back button |
| **States** | Empty, loading, error, success, partial |
| **Data boundaries** | Min, max, zero, null, special chars |
| **Permissions** | Authorized, unauthorized, role switching |
| **Integrations** | API failures, timeouts, retries |

## Rules
- Always read relevant code FIRST to understand actual behavior.
- Test cases must be EXECUTABLE — no vague steps like "verify it works".
- Include NEGATIVE tests — what should NOT happen.
- Specify exact expected results, not "should work correctly".
- Group related tests logically for efficient execution.
- Mark dependencies between test cases explicitly.
- Do NOT include implementation code in test cases.
- Do NOT assume features work; verify through test design.
- Priority reflects business impact, not test complexity.

## Example

```markdown
### TC-001: User successfully logs in with valid credentials [P]

**Priority**: Critical
**Type**: Happy Path
**Status**: [P] Pass
**Suite**: Smoke, Regression, Full
**Tags**: @feature:auth, @component:login-form

**Preconditions**:
- User account exists with email: test@example.com
- User is on login page
- User is not already logged in

**Steps**:
1. Enter "test@example.com" in email field
2. Enter valid password in password field
3. Click "Sign In" button

**Expected Result**:
- User is redirected to dashboard
- User's name appears in header
- Session cookie is set

---

### TC-002: Login fails with incorrect password [F] #342

**Priority**: Critical
**Type**: Error Handling
**Status**: [F] Fail — see #342
**Suite**: Smoke, Regression, Full
**Tags**: @feature:auth, @component:login-form

**Preconditions**:
- User account exists with email: test@example.com
- User is on login page

**Steps**:
1. Enter "test@example.com" in email field
2. Enter "wrongpassword" in password field
3. Click "Sign In" button

**Expected Result**:
- Error message: "Invalid email or password"
- User remains on login page
- No session cookie is set
- Password field is cleared

**Failure Note**:
- Actual: Generic "Something went wrong" message shown
- Bug: #342 - Login error messages not specific
```
