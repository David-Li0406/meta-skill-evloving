---
name: implementation-planner
description: Creates detailed implementation plans after requirements are clarified. Use when user says "plan this", "how should I implement", or after requirements-clarifier skill has gathered context. Breaks down work into steps with dependencies and complexity estimates.
user-invocable: true
disable-model-invocation: false
---

# Implementation Planner

Create structured implementation plans that guide development from requirements to working code.

## When to Use

Activate when:
- User says "plan this" or "create a plan"
- Requirements have been clarified
- Complex tasks need decomposition
- User asks "how should I implement this?"
- Before starting multi-file or multi-step work

## Prerequisites

**Don't plan until**:
- ✅ Requirements are clear (problem, users, success criteria)
- ✅ Constraints are known (timeline, scope, tech choices)
- ✅ Edge cases are identified
- ✅ Dependencies are understood

**If requirements unclear**, activate requirements-clarifier skill first.

## Planning Framework

### Step 1: Define Success Criteria

```
Clear success criteria:

1. What does "done" look like?
2. How will we verify it works?
3. What are the acceptance criteria?
```

**Example**:
```
Success Criteria:
- User can authenticate with email/password
- JWT tokens expire after 24 hours
- Refresh tokens work for 30 days
- All tests pass
- No security vulnerabilities detected
```

### Step 2: Identify Components

```
Identify what needs to be created/modified:

Files:
- src/auth/auth.service.ts (new)
- src/auth/auth.controller.ts (new)
- src/auth/jwt.strategy.ts (new)
- src/auth/refresh-token.strategy.ts (new)
- src/main.ts (modify - add auth module)

Dependencies:
- @nestjs/jwt, @nestjs/passport, passport-jwt
```

### Step 3: Break Down Tasks

```
Create ordered task list:

Phase 1: Foundation (30 min)
├─ [1.1] Install dependencies (5 min)
├─ [1.2] Create auth module structure (10 min)
└─ [1.3] Configure JWT module (15 min)

Phase 2: Core Authentication (45 min)
├─ [2.1] Implement auth service (20 min)
├─ [2.2] Create JWT strategy (15 min)
└─ [2.3] Add refresh token logic (10 min)

Phase 3: API Endpoints (30 min)
├─ [3.1] Create auth controller (20 min)
└─ [3.2] Add validation (10 min)

Phase 4: Testing & Verification (30 min)
├─ [4.1] Write unit tests (15 min)
├─ [4.2] Test authentication flow (10 min)
└─ [4.3] Security review (5 min)

Total estimated time: 2 hours 15 min
```

### Step 4: Identify Dependencies

```
Task dependencies:

1.2 depends on 1.1 (need dependencies installed)
2.1 depends on 1.3 (need JWT configured)
3.1 depends on 2.1 and 2.2 (need service + strategy)
4.1 depends on 3.1 (need controller to test)
```

### Step 5: Identify Risks & Edge Cases

```
Potential risks:

Risk: JWT secret management
Mitigation: Use environment variables, document setup

Risk: Token expiration timing
Mitigation: Implement refresh token rotation

Edge cases:
- User logs out before token expires
- Token stolen mid-session
- Refresh token expires during active session
```

### Step 6: Define Verification Steps

```
How to verify completion:

✅ Tests pass: npm test
✅ Can authenticate: curl /auth/login
✅ Token validates: JWT decodes correctly
✅ Refresh works: Can get new access token
✅ No security issues: Run security scan
```

## Plan Template

Use this structure for all plans:

```markdown
# Implementation Plan: [Feature Name]

## Overview
[Brief description of what we're building and why]

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Components
| File | Type | Purpose |
|------|------|---------|
| path/to/file | New/Modify | Description |

## Tasks

### Phase 1: [Phase Name] (Estimated: XX min)
- [1.1] Task description
- [1.2] Task description

### Phase 2: [Phase Name] (Estimated: XX min)
- [2.1] Task description (depends on 1.x)
- [2.2] Task description

## Dependencies
- Task 1.2 depends on 1.1
- Task 2.1 depends on 1.3
- [Full dependency graph]

## Risks & Mitigations
| Risk | Mitigation |
|------|-----------|
| Risk description | Mitigation strategy |

## Verification
- [ ] Test 1
- [ ] Test 2
- [ ] Manual verification step

## Notes
[Additional context, considerations, alternatives]
```

## Complexity Indicators

When estimating complexity, consider:

| Factor | Simple | Complex |
|--------|--------|---------|
| **Files** | 1-2 files | 5+ files or multiple directories |
| **Dependencies** | No new deps | New packages, external APIs |
| **Integration** | Standalone | Integrates with existing system |
| **Data** | No persistence | Database, state management |
| **Testing** | Obvious behavior | Edge cases, error scenarios |
| **Security** | No security concerns | Auth, permissions, sensitive data |

## Integration with Requirements Clarifier

**Workflow**:

```
1. User makes vague request
   ↓
2. requirements-clarifier activates
   ↓
3. Questions asked, requirements gathered
   ↓
4. implementation-planner activates
   ↓
5. Detailed plan created
   ↓
6. User approves plan
   ↓
7. Implementation begins
```

**Example conversation**:

```
User: "Add user authentication"

Claude (requirements-clarifier):
I want to make sure I implement the right solution:
1. What auth methods? (email/password, OAuth?)
2. Security requirements? (JWT, sessions?)
3. Existing auth system?

User: "Email/password, JWT tokens, new system"

Claude (implementation-planner):
Great, I'll create a plan:

[Detailed plan with phases, tasks, estimates]

Does this plan look good? I can adjust if you'd prefer different approach.
```

## Anti-Patterns

### Don't

- ❌ Plan without clarifying requirements first
- ❌ Create overly detailed plans (analysis paralysis)
- ❌ Ignore time estimates
- ❌ Skip risk identification
- ❌ Plan in isolation (incorporate user feedback)

### Do

- ✅ Clarify before planning
- ✅ Focus on structure, not every line of code
- ✅ Provide time estimates
- ✅ Identify risks early
- ✅ Get user approval on plan
- ✅ Leave room for adjustments during implementation

## Quick Reference

**Prerequisites**: Requirements clear, constraints known
**Structure**: Success criteria → Components → Tasks → Dependencies → Risks → Verification
**Format**: Markdown checklist with phases
**Estimation**: Consider files, dependencies, integration, data, testing, security
**Next step**: Get user approval, then implement

---

**Note**: This skill works best after requirements-clarifier. Always clarify requirements first, then plan.
