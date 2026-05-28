# Example: Feature Planning (OAuth Login)

**Purpose**: Complete walkthrough of planning process for a feature with multiple requirements.

---

## Input: feature-spec-oauth.md

```markdown
Requirements:
- REQ-001: Users can log in with Google OAuth
- REQ-002: Sessions persist for 7 days
- REQ-003: Users can log out

Constraints:
- Must integrate with existing authentication system
- No breaking changes to current login flow
- Timeline: 2 weeks
```

---

## Planning Process (CoD^Σ)

### Step 1: Load Specification

```markdown
→ LoadSpec
  ↳ Source: feature-spec-oauth.md
  ↳ Requirements: 3 (REQ-001, REQ-002, REQ-003)
  ↳ Constraints: Integration with existing auth, 2-week timeline
```

---

### Step 2: Intelligence Gathering

```markdown
⇄ IntelQuery("existing auth")
  ↳ Query: project-intel.mjs --search "auth|session" --type ts --json
  ↳ Data: Found src/auth/session.ts, src/auth/middleware.ts
  ↳ Evidence: session.ts:23-67 has JWT token management (can reuse)

⇄ IntelQuery("dependencies")
  ↳ Query: project-intel.mjs --dependencies src/auth/session.ts --direction upstream --json
  ↳ Data: Imports jsonwebtoken library, crypto stdlib
  ↳ Evidence: session.ts:5 imports jsonwebtoken (already configured)
```

---

### Step 3: Task Breakdown

```markdown
∘ BreakdownByLayer
  ↳ REQ-001 → Database + Backend + Frontend + Testing
  ↳ REQ-002 → Backend session logic
  ↳ REQ-003 → Backend endpoint + Frontend button
```

**Tasks Generated**:

```markdown
### Task 1: Add OAuth Database Schema
- **ID:** T1
- **Owner:** executor-agent
- **Estimated:** 2 hours
- **Dependencies:** None

**Acceptance Criteria:**
- [ ] AC1: users table has google_id VARCHAR(255) column
- [ ] AC2: Migration script runs without errors
- [ ] AC3: google_id is nullable (existing users don't have it)

### Task 2: Implement OAuth Flow
- **ID:** T2
- **Owner:** executor-agent
- **Estimated:** 6 hours
- **Dependencies:** T1

**Acceptance Criteria:**
- [ ] AC1: OAuth redirect returns HTTP 302 with Google authorization URL
- [ ] AC2: OAuth callback validates state parameter
- [ ] AC3: User profile data (email, name) stored correctly

### Task 3: Create Login UI
- **ID:** T3
- **Owner:** executor-agent
- **Estimated:** 4 hours
- **Dependencies:** T2

**Acceptance Criteria:**
- [ ] AC1: Button renders with "Log in with Google" text
- [ ] AC2: Button click triggers OAuth redirect
- [ ] AC3: Button shows loading spinner during authentication

### Task 4: Implement Session Management
- **ID:** T4
- **Owner:** executor-agent
- **Estimated:** 4 hours
- **Dependencies:** T1

**Acceptance Criteria:**
- [ ] AC1: Session tokens expire after exactly 7 days
- [ ] AC2: Session middleware validates unexpired tokens
- [ ] AC3: Expired tokens return 401 Unauthorized

### Task 5: Implement Logout
- **ID:** T5
- **Owner:** executor-agent
- **Estimated:** 3 hours
- **Dependencies:** T4

**Acceptance Criteria:**
- [ ] AC1: Logout endpoint returns 204 status code
- [ ] AC2: Logout clears session cookie
- [ ] AC3: Subsequent requests with cleared cookie return 401

### Task 6: E2E Test OAuth Flow
- **ID:** T6
- **Owner:** executor-agent
- **Estimated:** 5 hours
- **Dependencies:** T2, T3, T5

**Acceptance Criteria:**
- [ ] AC1: User can click button, complete OAuth, and reach dashboard
- [ ] AC2: User session persists across page reloads for 7 days
- [ ] AC3: User can log out and session is cleared
```

---

### Step 4: Define Dependencies

```markdown
→ AnalyzeDependencies
  ↳ T1 (DB schema) blocks T2, T4 (backend needs schema)
  ↳ T2 (OAuth flow) blocks T3 (UI needs working endpoint)
  ↳ T2, T3, T5 all block T6 (E2E needs full flow)
```

**Dependency Graph**:
```
T1 (DB)
 ├→ T2 (OAuth) ─→ T3 (UI) ─→ T6 (E2E test)
 └→ T4 (Session) ─→ T5 (Logout) ─┘
```

**Parallel Opportunities**:
- T2 and T4 can run in parallel after T1 completes
- T3 and T5 can run in parallel after T2 and T4 complete

---

### Step 5: Validate Requirements Coverage

```markdown
∘ Validate
  ↳ REQ-001 (OAuth login) → T1, T2, T3 ✓
  ↳ REQ-002 (Session persistence) → T4, T5 ✓
  ↳ REQ-003 (Logout) → T6, T7 ✓
  ↳ All requirements covered ✓
  ↳ All tasks have ≥2 ACs ✓
```

---

## Output: plan.md

**File Generated**: `20251023-1430-plan-oauth-login.md`

```markdown
---
plan-id: oauth-login
created: 2025-10-23
status: Draft
---

# Implementation Plan: OAuth Login with Google

## Summary

Add Google OAuth login to existing authentication system, with 7-day session persistence and logout functionality. Integrates with current JWT-based auth infrastructure (src/auth/session.ts:23).

## Requirements

- REQ-001: Users can log in with Google OAuth
- REQ-002: Sessions persist for 7 days
- REQ-003: Users can log out

## Tasks

[T1-T6 as defined above]

## Dependencies

Task Graph:
```
T1 (DB)
 ├→ T2 (OAuth) ─→ T3 (UI) ─→ T6 (E2E test)
 └→ T4 (Session) ─→ T5 (Logout) ─┘
```

Critical Path: T1 → T2 → T3 → T6 (17 hours)
Parallel Work: (T2, T4) after T1; (T3, T5) after (T2, T4)

## Estimates

Total: 24 hours
Critical Path: 17 hours (T1, T2, T3, T6)
With Parallelization: ~19 hours (T2||T4 save 4h, T3||T5 save 3h)

## Risks

- Google OAuth API changes (mitigation: use official SDK)
- Session management complexity (mitigation: reuse existing JWT code)
- E2E test flakiness (mitigation: mock OAuth in tests)

## Verification

Plan meets quality gates:
- [x] 100% requirement coverage (3/3)
- [x] All tasks have ≥2 ACs (6/6)
- [x] Dependencies valid, no cycles
- [x] Estimates realistic (2-8h per task)
- [x] Intelligence queries executed (session.ts:23 evidence)

## CoD^Σ Evidence Trace

Intelligence Queries:
- project-intel.mjs --search "auth" --json → src/auth/session.ts:23-67
- project-intel.mjs --dependencies session.ts → jsonwebtoken (lib)

Reusable Patterns:
- JWT token management (session.ts:23-67)
- Middleware authentication (middleware.ts:15-42)

Assumptions:
- [ASSUMPTION: Google OAuth returns email and name in profile]
- [ASSUMPTION: Existing JWT infrastructure supports OAuth tokens]

## Next Steps

1. Review plan for completeness
2. Run `/tasks plan.md` to generate task breakdown
3. Run `/audit oauth-login` to validate consistency
4. If audit passes, run `/implement plan.md`
```

---

## Success Metrics

**Plan Quality**:
- Requirements coverage: 3/3 = 100% ✓
- Tasks with ≥2 ACs: 6/6 = 100% ✓
- Dependencies valid: No cycles ✓

**Estimating Quality**:
- Tasks sized 2-8h: 6/6 ✓
- Critical path: 17 hours
- Total time: 24 hours
- With parallelization: ~19 hours

**Constitutional Compliance**:
- Article I: Intelligence queries executed ✓
- Article II: CoD^Σ traces with evidence ✓
- Article III: Test-first ACs (≥2 per task) ✓
- Article IV: Derived from spec.md ✓
- Article V: Follows plan.md template ✓
