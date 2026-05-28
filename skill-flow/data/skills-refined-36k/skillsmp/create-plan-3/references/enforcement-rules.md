# Enforcement Rules and Common Pitfalls

**Purpose**: Quality gates ensuring plan meets constitutional requirements.

---

## Rule 1: Minimum 2 ACs Per Task

**Article III Requirement**: Test-First Imperative mandates ≥2 testable acceptance criteria per task.

**❌ Violation**:
```markdown
### Task: Add login button
**Acceptance Criteria:**
- Button exists
```

**✓ Correct**:
```markdown
### Task: Add login button
**Acceptance Criteria:**
- [ ] AC1: Button renders with "Log in with Google" text
- [ ] AC2: Button click triggers OAuth redirect to Google
- [ ] AC3: Button shows loading state during authentication
```

**Why 2+ ACs**:
- Single AC often tests just "it compiles" or basic presence
- Multiple ACs ensure behavior verification from multiple angles
- Prevents trivial "tests" that don't actually validate functionality

**Enforcement**: Review plan, count ACs per task. If any task has <2 ACs, add more or reject plan.

---

## Rule 2: All Requirements → Tasks

**Complete Coverage Requirement**: Every spec requirement must map to at least one task.

**❌ Violation**:
```markdown
Requirements: REQ-001, REQ-002, REQ-003
Tasks: T1 (for REQ-001), T2 (for REQ-001)
# Missing REQ-002 and REQ-003!
```

**✓ Correct**:
```markdown
Requirements: REQ-001, REQ-002, REQ-003
Tasks:
- T1, T2 (REQ-001)
- T3, T4 (REQ-002)
- T5 (REQ-003)
Coverage: 100% ✓
```

**Enforcement**:
1. List all spec requirements
2. Map each requirement to tasks
3. Verify no requirements orphaned
4. Verify no tasks orphaned (unmapped)

**Matrix Format**:
```markdown
| Requirement | Tasks | Status |
|------------|-------|--------|
| REQ-001 | T1, T2 | ✓ Covered |
| REQ-002 | T3, T4 | ✓ Covered |
| REQ-003 | T5 | ✓ Covered |

Coverage: 3/3 = 100% ✓
```

---

## Rule 3: No Vague Tasks

**Specificity Requirement**: Task descriptions must be specific enough to guide implementation.

**❌ Violation**:
```markdown
### Task: Fix the auth system
### Task: Make it work
### Task: Improve performance
```

**✓ Correct**:
```markdown
### Task: Add missing setState dependency to useEffect
### Task: Validate OAuth token expiry before refresh
### Task: Replace N+1 query with single JOIN query
```

**Vague Patterns to Avoid**:
- "Fix X" → Specify exact fix
- "Improve X" → Specify exact improvement metric
- "Make X work" → Specify what "working" means
- "Handle X" → Specify exact handling behavior

**Enforcement**:
- Review task titles for vague language
- Ensure task title alone suggests clear implementation
- If unclear, ACs should clarify specific behavior

---

## Common Pitfalls

| Pitfall | Impact | Solution |
|---------|--------|----------|
| **Tasks too large** | Can't estimate accurately, hard to verify completion | Break into 2-8 hour chunks |
| **Vague ACs** | Can't objectively verify completion | Make testable (pass/fail clear) |
| **Missing dependencies** | Tasks blocked unexpectedly | Use project-intel.mjs to find dependencies |
| **No requirement coverage** | Incomplete implementation | Validate 100% requirement-to-task mapping |
| **Circular dependencies** | Cannot determine task order | Detect cycles, break by restructuring |
| **No parallel work identified** | Sequential execution when parallel possible | Mark independent tasks with [P] |
| **Estimates missing or unrealistic** | Poor sprint planning | 2-8 hour estimates per task |
| **No CoD^Σ evidence** | Claims without backing | Add file:line references, save intel queries |
| **Tasks not independently testable** | Integration dependencies | Restructure for independent verification |
| **Missing edge cases in ACs** | Bugs slip through | Add AC for boundary conditions |

---

## Anti-Patterns

### Anti-Pattern 1: Layer-First Organization

**Problem**: Organizing tasks by technical layer instead of user story.

**Bad**:
```
Phase 1: All Database Changes
  - T1: Create users table
  - T2: Create sessions table
  - T3: Create orders table

Phase 2: All Backend APIs
  - T4: Create user endpoints
  - T5: Create session endpoints
  - T6: Create order endpoints

Phase 3: All Frontend Components
  - T7: User management UI
  - T8: Session management UI
  - T9: Order management UI
```

**Good** (Article VII: User-Story-Centric):
```
Phase 1: Setup (shared infrastructure)

Phase 2: User Story P1 - User Registration (MVP)
  - T1: Create users table
  - T2: Create user registration endpoint
  - T3: Create registration form UI
  - T4: Test: User can register

Phase 3: User Story P2 - User Login (MVP)
  - T5: Create sessions table
  - T6: Create login endpoint
  - T7: Create login form UI
  - T8: Test: User can log in

Phase 4: User Story P3 - Order Placement
  - T9: Create orders table
  - T10: Create order endpoint
  - T11: Create order form UI
  - T12: Test: User can place order
```

**Why Bad**: Layer-first prevents shipping working features until ALL layers done. Story-first enables progressive delivery (ship P1, then P2, then P3).

---

### Anti-Pattern 2: No Acceptance Criteria

**Problem**: Tasks without testable ACs.

**Bad**:
```markdown
### Task 3: Add OAuth support
```

**Good**:
```markdown
### Task 3: Add OAuth support
**Acceptance Criteria:**
- [ ] AC1: OAuth redirect returns 302 with Google authorization URL
- [ ] AC2: OAuth callback validates state parameter
- [ ] AC3: User profile data stored correctly after OAuth success
```

---

### Anti-Pattern 3: Undocumented Assumptions

**Problem**: Making architectural decisions without evidence.

**Bad**:
```markdown
We'll use OAuth 2.0 for authentication.
```

**Good** (Article II: Evidence-Based):
```markdown
We'll use OAuth 2.0 for authentication.

**Evidence**:
- ⇄ IntelQuery("existing auth") → found src/auth/session.ts:23 uses JWT
- ⇄ MCPQuery(Ref, "OAuth 2.0 best practices") → Google recommends PKCE flow
- File: src/auth/session.ts:23 already has token validation logic we can reuse

**Assumption**: OAuth flow will integrate with existing session management.
**Justification**: Existing JWT infrastructure (session.ts:23-67) supports token storage.
```

---

### Anti-Pattern 4: Big-Bang Planning

**Problem**: Planning entire system at once instead of incrementally.

**Bad**:
```
- T1: Implement entire authentication system
- T2: Implement entire API layer
- T3: Implement entire frontend
```

**Good**:
```
Phase 1: MVP (basic login)
  - T1: Add auth schema
  - T2: Basic login endpoint
  - T3: Login form
  - T4: Test login works

Phase 2: Enhancement (OAuth)
  - T5: Add OAuth schema
  - T6: OAuth flow
  - T7: OAuth button
  - T8: Test OAuth works
```

**Why Good**: Progressive delivery enables early feedback and course correction.

---

## Validation Checklist

Before finalizing plan:

**Content Quality**:
- [ ] Every task has ≥2 testable ACs
- [ ] Task titles specific (no vague language)
- [ ] 100% requirement coverage
- [ ] Dependencies identified and valid
- [ ] Estimates realistic (2-8h per task)

**Constitutional Compliance**:
- [ ] Article I: Intelligence queries executed, evidence saved
- [ ] Article II: CoD^Σ traces with file:line references
- [ ] Article III: Test-first ACs defined (≥2 per task)
- [ ] Article IV: Derived from spec.md, not invented
- [ ] Article V: Follows plan.md template
- [ ] Article VI: Complexity justified (if >3 layers)
- [ ] Article VII: User-story organization (not layer-first)
- [ ] Article VIII: Parallel work marked [P]

**Organization Quality**:
- [ ] Critical path identified
- [ ] Parallel opportunities marked
- [ ] Blockers documented
- [ ] Risks identified
