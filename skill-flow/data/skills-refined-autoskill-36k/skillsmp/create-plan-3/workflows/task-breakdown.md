# Phase 2: Task Breakdown with Acceptance Criteria

**Purpose**: Break requirements into implementable tasks with minimum 2 testable acceptance criteria each (Article III).

---

## Step 2.1: Decompose Requirements into Tasks

**Task Sizing Guidelines**:
- **Ideal**: 2-8 hours per task
- **Too large**: "Implement authentication system" (several days)
- **Too small**: "Add comment" (15 minutes, not worth tracking)
- **Just right**: "Add google_id column to users table" (2-4 hours)

**Decomposition Strategy**:
```
Requirement → Multiple Tasks (by layer or phase)

Example:
REQ-001: Users can log in with Google OAuth
  ↓
T1: Add OAuth database schema (DB layer)
T2: Implement OAuth flow (backend)
T3: Create login UI components (frontend)
T4: Write E2E test (testing)
```

---

## Step 2.2: Define Acceptance Criteria (CRITICAL)

**Article III Requirement**: **Minimum 2 testable ACs per task**

**AC Format**:
```markdown
**Acceptance Criteria:**
- [ ] AC1: [Testable condition with pass/fail clarity]
- [ ] AC2: [Independent verification without implementation knowledge]
- [ ] AC3: [Optional third AC for complex tasks]
```

**Testable AC Examples**:

**✓ Good ACs** (objectively verifiable):
- "users table has google_id VARCHAR(255) column"
- "OAuth redirect returns HTTP 302 with Google authorization URL"
- "Session token expires after exactly 7 days"
- "Logout endpoint returns 204 and clears cookies"

**❌ Bad ACs** (vague, unverifiable):
- "OAuth works"
- "System is secure"
- "Login looks good"
- "Performance is acceptable"

---

## Step 2.3: CoD^Σ Task Breakdown Process

**Systematic Decomposition**:

```markdown
Step 1: → LoadRequirement
  ↳ Source: REQ-001 (Users can log in with Google OAuth)
  ↳ Constraints: Must use existing auth infrastructure

Step 2: ⇄ IntelQuery("existing auth")
  ↳ Query: project-intel.mjs --search "auth|session" --type ts --json
  ↳ Data: Found src/auth/session.ts:23, src/auth/middleware.ts:15

Step 3: ∘ BreakdownByLayer
  ↳ Database: T1 (add google_id column)
  ↳ Backend: T2 (OAuth flow), T3 (session management)
  ↳ Frontend: T4 (login button), T5 (callback handler)
  ↳ Testing: T6 (E2E test OAuth flow)

Step 4: → DefineACs
  ↳ T1-AC1: google_id column added
  ↳ T1-AC2: Migration runs successfully
  ↳ T1-AC3: google_id is nullable (existing users don't have it)
  ↳ T2-AC1: OAuth redirect works (302 with correct URL)
  ↳ T2-AC2: Google token validates
  ↳ T2-AC3: User profile data stored correctly
  ↳ ... (2-3 ACs per task)

Step 5: → ValidateACs
  ↳ Each AC is independently testable ✓
  ↳ Each AC has pass/fail clarity ✓
  ↳ Minimum 2 ACs per task ✓
```

---

## Step 2.4: Task Format

**Required Fields**:
- **ID**: T1, T2, T3, etc. (sequential)
- **Title**: Brief, specific description
- **Owner**: Which agent handles this (executor-agent, analyzer-agent, etc.)
- **Estimated Time**: 2-8 hours
- **Dependencies**: Which tasks must complete first
- **Acceptance Criteria**: Minimum 2 testable ACs

**Example Task**:
```markdown
### Task 1: Add OAuth Database Schema
- **ID:** T1
- **Owner:** executor-agent
- **Estimated:** 2 hours
- **Dependencies:** None

**Acceptance Criteria:**
- [ ] AC1: users table has google_id VARCHAR(255) column
- [ ] AC2: Migration script runs without errors
- [ ] AC3: google_id is nullable (existing users don't have google_id = NULL)

**Notes:**
- Use existing migration framework
- Reference: src/migrations/001_create_users.sql
```

---

## Step 2.5: Requirement Coverage Check

**Validation**:
```markdown
Requirements:
- REQ-001: OAuth login → T1, T2, T3 ✓
- REQ-002: Session persistence → T4, T5 ✓
- REQ-003: Logout → T6, T7 ✓

Coverage: 100% ✓
```

**Enforcement**:
- [ ] Every requirement has at least 1 task
- [ ] Every task maps to a requirement
- [ ] No orphaned tasks (tasks not tied to requirements)

---

## Step 2.6: AC Quality Enforcement

**Checklist for Every AC**:
- [ ] Pass/fail is objectively verifiable (no interpretation needed)
- [ ] Can be tested without knowing implementation details
- [ ] Specific enough to guide implementation
- [ ] Technology-agnostic where possible (focus on behavior, not HOW)

**Example Review**:

**AC1**: "OAuth works"
- ❌ Fails: Not objectively verifiable, vague

**AC1 (revised)**: "OAuth redirect returns HTTP 302 with location header pointing to Google authorization URL"
- ✓ Pass: Specific HTTP status, header, URL check
- ✓ Pass: Can verify with curl or test framework
- ✓ Pass: No interpretation needed

---

## Common AC Anti-Patterns

| Anti-Pattern | Why Bad | Fix |
|-------------|---------|-----|
| "Feature works" | Vague, untestable | Specify exact behavior to verify |
| "System is fast" | Subjective | Define specific latency threshold |
| "UI looks good" | Opinion-based | Define specific UI elements present |
| "Code is clean" | Subjective | Define specific linting/quality checks |

---

## Output of Phase 2

**Data Structure**:
```
Tasks: [T1, T2, T3, ..., TN]
Each Task:
  - ID: T<N>
  - Title: <specific description>
  - Owner: <agent>
  - Estimated: <2-8 hours>
  - Dependencies: [T<M>, ...]
  - ACs: [AC1, AC2, AC3, ...]  # Minimum 2

Requirement Coverage: 100% ✓
All Tasks Have ≥2 ACs: ✓
```

**Article III Compliance**:
- ✓ Every task has minimum 2 testable ACs
- ✓ Each AC is independently verifiable
- ✓ Pass/fail criteria clear

**Proceed to Phase 3**: Identify Dependencies
