# Phase 6: Implementation (Complex Path)

**Duration**: 4-8 hours (varies by complexity)
**Prerequisites**: Phases 2-5 complete (template, spec, design, wireframes) + audit passed
**Next Phase**: Phase 7 (QA & Testing)

---

## Overview

**Purpose**: Execute implementation with TDD and progressive delivery following SDD workflow

**Inputs**:
- `/docs/plan.md` (implementation plan from Phase 3)
- `/docs/tasks.md` (user-story-organized tasks from Phase 3)
- `/docs/design-system.md` (design system from Phase 4)
- `/docs/wireframes.md` (component mapping from Phase 5)
- Audit PASS status (required gate)

**Outputs**:
- Implemented Next.js application (all P1 stories minimum)
- Passing test suite (100% AC coverage)
- Verification reports per story
- Working MVP ready for QA

---

## SDD Workflow Integration

**CRITICAL**: This phase is executed via `/implement plan.md` command

### Automatic Workflow

**User invokes** (manual):
```bash
/implement plan.md
```

**implement-and-verify skill handles** (automatic):
1. Loads plan.md and tasks.md
2. Implements stories in priority order (P1 → P2 → P3)
3. Per story:
   - Writes tests for ACs FIRST
   - Runs tests (MUST fail - proves tests work)
   - Implements minimum code to pass tests
   - Runs tests again (MUST pass)
   - Invokes `/verify --story P1` (automatic)
   - Blocks next story until current passes
4. Progressive delivery: Each story independently validated

**Constitution Enforcement**:
- **Article III**: Test-First Imperative (TDD mandatory, no exceptions)
- **Article VII**: User-Story-Centric Organization (implement P1 completely before P2)
- **Article V**: Template-Driven Quality (verification-report.md per story)

---

## Workflow (CoD^Σ)

```
/implement plan.md → implement-and-verify_skill
  ↓
Tasks.md[P1] → Tests_First ∘ Red ∘ Green ∘ Refactor
  ↓
/verify --story P1 → AC_Validation
  ↓ [PASS]
Tasks.md[P2] → Tests_First ∘ Red ∘ Green ∘ Refactor
  ↓
/verify --story P2 → AC_Validation
  ↓ [PASS]
Tasks.md[P3] → Tests_First ∘ Red ∘ Green ∘ Refactor
  ↓
/verify --story P3 → AC_Validation
  ↓ [PASS]
Complete_Implementation → Phase_7_QA
```

**Key Principle**: Each story is independently testable and demonstrable. No "big bang" integration.

---

## Detailed Steps

### Step 1: Pre-Implementation Validation

**MANDATORY GATE**: Verify audit passed before proceeding

**Checklist**:
- [ ] `/audit` status: PASS (required)
- [ ] `plan.md` exists with tech stack defined
- [ ] `tasks.md` exists with user-story organization
- [ ] Design system finalized (`design-system.md`)
- [ ] Wireframes approved (`wireframes.md`)
- [ ] Template installed and running (from Phase 2)
- [ ] All dependencies installed (`package.json` up to date)

**If audit FAILED**:
```
STOP: Do not proceed with implementation.
Fix audit violations first, then re-run /audit.
Only proceed after PASS status.
```

### Step 2: Foundation Setup (Phase 1 Tasks)

**From tasks.md Phase 1: Setup**

**Infrastructure** (if not from template):
```bash
# Database setup (if Supabase)
npm install @supabase/supabase-js
# Create .env.local with keys

# Testing setup
npm install -D vitest @testing-library/react @testing-library/jest-dom
# Create vitest.config.ts

# Additional dependencies from plan.md
npm install [dependencies from plan.md tech stack]
```

**Verification**:
- [ ] Dev server runs without errors
- [ ] Database connection established (if applicable)
- [ ] Test runner configured and operational
- [ ] All imports resolve correctly

### Step 3: Foundational Tasks (Phase 2)

**From tasks.md Phase 2: Foundational**

**Common Foundational Tasks**:
- Database schema creation (if database project)
- Authentication flow setup (if auth required)
- Global layouts (root layout, error boundaries)
- Navigation components (header, sidebar, footer)
- Utility functions (cn, formatters, validators)

**TDD Workflow Example** (Database Schema):
```typescript
// 1. Write test FIRST (tests/db/user-schema.test.ts)
describe('User Schema', () => {
  it('should create user with email and password', async () => {
    const user = await db.user.create({
      email: 'test@example.com',
      password: 'hashed_password'
    })
    expect(user.id).toBeDefined()
    expect(user.email).toBe('test@example.com')
  })
})

// 2. Run test - MUST FAIL (red)
// $ npm test -- user-schema.test.ts
// FAIL: Cannot find module 'db'

// 3. Implement schema (lib/db/schema.ts)
export const userSchema = pgTable('users', {
  id: uuid('id').defaultRandom().primaryKey(),
  email: text('email').notNull().unique(),
  password: text('password').notNull(),
  createdAt: timestamp('created_at').defaultNow()
})

// 4. Run test - MUST PASS (green)
// $ npm test -- user-schema.test.ts
// PASS: User schema creates user correctly

// 5. Refactor if needed (extract validators, add indexes)
```

**Blocking Principle**: Foundational tasks MUST be complete and tested before any user story implementation.

### Step 4: User Story P1 Implementation

**From tasks.md Phase 3: User Story P1 - [Title]**

**Story-by-Story Workflow** (implement-and-verify skill enforces):

**Example: P1 - User Authentication**

**Tasks from tasks.md**:
```markdown
## Phase 3: User Story P1 - User Authentication

**User Story**:
As a user, I want to log in with email and password so that I can access my dashboard.

**Acceptance Criteria**:
- AC1: User can enter email and password
- AC2: Valid credentials show dashboard within 2 seconds
- AC3: Invalid credentials show error message
- AC4: Password is masked during entry

**Tasks**:
- [ ] T005: Write tests for P1 ACs (all 4 criteria)
- [ ] T006: [P] Implement login form component
- [ ] T007: [P] Implement authentication API route
- [ ] T008: Integrate form with API
- [ ] T009: Verify P1 (automatic via /verify)
```

**Implementation Sequence**:

**T005: Write Tests First**
```typescript
// tests/auth/login.test.tsx
describe('User Authentication (P1)', () => {
  it('AC1: User can enter email and password', () => {
    render(<LoginForm />)
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
  })

  it('AC2: Valid credentials show dashboard within 2s', async () => {
    render(<LoginForm />)
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@example.com' }
    })
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' }
    })

    const start = Date.now()
    fireEvent.click(screen.getByRole('button', { name: /log in/i }))

    await waitFor(() => {
      expect(screen.getByText(/dashboard/i)).toBeInTheDocument()
    }, { timeout: 2000 })

    const elapsed = Date.now() - start
    expect(elapsed).toBeLessThan(2000)
  })

  it('AC3: Invalid credentials show error', async () => {
    render(<LoginForm />)
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'wrong@example.com' }
    })
    fireEvent.click(screen.getByRole('button', { name: /log in/i }))

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument()
    })
  })

  it('AC4: Password is masked', () => {
    render(<LoginForm />)
    const passwordInput = screen.getByLabelText(/password/i)
    expect(passwordInput).toHaveAttribute('type', 'password')
  })
})
```

**Run tests - MUST FAIL (red)**:
```bash
$ npm test -- login.test.tsx
FAIL tests/auth/login.test.tsx
  ✕ AC1: User can enter email and password (Cannot find module 'LoginForm')
  ✕ AC2: Valid credentials show dashboard within 2s
  ✕ AC3: Invalid credentials show error
  ✕ AC4: Password is masked
```

**T006 & T007: Implement in Parallel** (marked with [P]):
```typescript
// components/auth/login-form.tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card } from '@/components/ui/card'

export function LoginForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })

    if (res.ok) {
      router.push('/dashboard')
    } else {
      setError('Invalid credentials')
    }
  }

  return (
    <Card className="p-6">
      <form onSubmit={handleSubmit}>
        <div className="space-y-4">
          <div>
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div>
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          {error && <p className="text-destructive">{error}</p>}
          <Button type="submit">Log In</Button>
        </div>
      </form>
    </Card>
  )
}
```

```typescript
// app/api/auth/login/route.ts
import { NextResponse } from 'next/server'
import { createClient } from '@/lib/supabase/server'

export async function POST(request: Request) {
  const { email, password } = await request.json()
  const supabase = createClient()

  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password
  })

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 401 })
  }

  return NextResponse.json({ user: data.user })
}
```

**T008: Integration** (sequential after T006/T007):
- Form component imports API route types
- Error handling integrated
- Loading states added

**Run tests - MUST PASS (green)**:
```bash
$ npm test -- login.test.tsx
PASS tests/auth/login.test.tsx
  ✓ AC1: User can enter email and password (45ms)
  ✓ AC2: Valid credentials show dashboard within 2s (1234ms)
  ✓ AC3: Invalid credentials show error (567ms)
  ✓ AC4: Password is masked (12ms)

Test Suites: 1 passed, 1 total
Tests:       4 passed, 4 total
```

**T009: Verify P1** (automatic):
```bash
# implement-and-verify skill invokes:
/verify --story P1

# Output:
✅ P1 - User Authentication: PASS
  ✅ AC1: User can enter email and password
  ✅ AC2: Valid credentials show dashboard within 2s
  ✅ AC3: Invalid credentials show error
  ✅ AC4: Password is masked

Independent Demo: ✅ Can log in and see dashboard
Dependencies: ✅ None (foundational complete)
Ready for Production: ✅ All ACs passing

Verification Report: /docs/verification-p1.md
```

**GATE**: P1 must PASS before proceeding to P2. If fails, fix P1 first.

### Step 5: User Stories P2, P3, ... (Progressive Delivery)

**Repeat Step 4 for each priority**:
- Implement P2 completely → verify → PASS → proceed
- Implement P3 completely → verify → PASS → proceed
- Continue until all priorities complete

**Independent Testing Per Story**:
```bash
# Each story can be tested independently
/verify --story P1  # Authentication works standalone
/verify --story P2  # Profile editing works standalone
/verify --story P3  # Settings works standalone

# No "big bang" integration - each story is MVP-capable
```

**Parallel Task Execution**:
- Tasks marked `[P]` can run in parallel
- Foundation tasks completed first (blocking)
- Story-level parallelization possible if no dependencies

### Step 6: Integration & Polish

**After all stories pass individual verification**:

**Cross-Story Integration**:
- Navigation between features
- Shared state management
- Global error handling
- Loading states and transitions

**Accessibility Validation**:
```bash
# Run accessibility tests
npm run test:a11y

# Check contrast ratios
# Verify keyboard navigation
# Test screen reader compatibility
```

**Performance Validation**:
```bash
# Run Lighthouse locally
npx lighthouse http://localhost:3000 --view

# Targets:
# - Performance: ≥90
# - Accessibility: 100
# - Best Practices: ≥90
# - SEO: ≥90
```

---

## Sub-Agents

**None required** - implement-and-verify skill handles execution

**Optional**: If complex debugging needed, dispatch code-analyzer agent

---

## Quality Checks

### Per-Story Checklist (Before /verify)
- [ ] All ACs have passing tests (100% coverage)
- [ ] No hardcoded values (use design system variables)
- [ ] Components installed from Shadcn (followed Search → View → Example → Install)
- [ ] Mobile responsive (tested at sm/md/lg breakpoints)
- [ ] Accessibility validated (keyboard nav, ARIA labels)
- [ ] Loading states implemented
- [ ] Error handling complete

### Integration Checklist
- [ ] All P1 stories passing independently
- [ ] Navigation between features working
- [ ] Shared state (if any) functioning correctly
- [ ] No console errors in browser
- [ ] No TypeScript errors
- [ ] Build succeeds (`npm run build`)

### Pre-QA Checklist
- [ ] All tests passing (`npm test`)
- [ ] Lint passing (`npm run lint`)
- [ ] Type-check passing (`npm run type-check`)
- [ ] Build optimized (`npm run build` no warnings)
- [ ] All verification reports generated (per story)
- [ ] MVP demonstrable (P1 stories functional)

---

## Outputs

### 1. Implemented Application
**Location**: Project root directory
**Status**: Running on http://localhost:3000
**Coverage**: All P1 stories minimum (P2/P3 optional)

### 2. Test Suite
**Location**: `/tests/` directory
**Coverage**: 100% AC coverage (all acceptance criteria tested)
**Status**: All tests passing

### 3. Verification Reports
**Location**: `/docs/verification-*.md` (per story)
**Content**: AC validation results, independent demo status
**Format**: Template from @.claude/templates/verification-report.md

### 4. Build Artifacts
**Location**: `/.next/` directory
**Status**: Production build successful
**Performance**: Lighthouse scores documented

---

## Next Phase Handover

**Prerequisites for Phase 7 (QA & Testing)**:
- ✅ All P1 stories implemented and verified
- ✅ Test suite passing (100% AC coverage)
- ✅ Build succeeds without errors
- ✅ Verification reports generated
- ✅ MVP demonstrable (P1 functional)

**Handover Context**:
- Working application on localhost:3000
- Test coverage report
- Known issues or limitations (if any)
- P2/P3 implementation status
- Performance baseline (Lighthouse scores)

**Continue with**: `phase-7-qa.md`

---

## Common Issues & Solutions

### Issue: Tests fail after implementation
**Cause**: Tests written incorrectly OR implementation doesn't match ACs
**Solution**: Review ACs in spec.md. Tests should validate ACs exactly, not implementation details. Fix tests if they test wrong thing, fix implementation if it doesn't meet ACs.

### Issue: P1 verification blocks on dependencies
**Cause**: P1 depends on incomplete foundational tasks
**Solution**: Complete Phase 2 (Foundational) fully before starting P1. Foundational tasks are blocking prerequisites.

### Issue: Cannot proceed to P2 (P1 verification fails)
**Cause**: Constitution Article VII enforcement - stories must pass independently
**Solution**: Fix P1 until all ACs pass. Do not skip to P2. Progressive delivery requires each story complete before next.

### Issue: Hardcoded colors in components
**Cause**: Not following design system from Phase 4
**Solution**: Replace all hardcoded colors with CSS variables (e.g., `text-primary` not `#000000`). Review design-system.md for variable names.

### Issue: Components don't render
**Cause**: Shadcn component not installed OR incorrect import path
**Solution**: Follow Shadcn workflow (Search → View → Example → Install). Verify component exists in components.json registry.

### Issue: Build fails with TypeScript errors
**Cause**: Missing types OR incorrect imports
**Solution**: Run `npm run type-check` to see all errors. Fix imports, add types, or update tsconfig.json if needed.

---

## Success Criteria

- ✅ All P1 stories implemented (MVP functional)
- ✅ Test suite passing (100% AC coverage per story)
- ✅ All verification reports PASS status
- ✅ Independent story demos working
- ✅ Build succeeds (`npm run build`)
- ✅ No TypeScript errors
- ✅ No console errors in browser
- ✅ Design system followed (no hardcoded colors)
- ✅ Accessibility validated (WCAG 2.1 AA minimum)
- ✅ Ready for comprehensive QA (Phase 7)

---

## Evidence Requirements (Constitution Article II)

**All implementations MUST document**:
- **AC mapping**: Every test traced to specific AC (tasks.md:line)
- **Test results**: Actual test output showing PASS status
- **Component usage**: Shadcn components used per wireframes.md
- **Design system compliance**: No hardcoded colors, all variables from globals.css

**Example Good Evidence**:
"P1 AC2 (tasks.md:line 67 - Dashboard load < 2s) verified via test (tests/auth/login.test.tsx:45-58) which measures elapsed time. Test PASSES at 1234ms < 2000ms threshold. Implementation uses Next.js App Router with server components for fast initial load."

---

## TDD Cycle Enforcement (Constitution Article III)

**MANDATORY SEQUENCE** (no exceptions):

1. **Write tests FIRST** - All ACs become tests before ANY implementation
2. **Run tests** - Tests MUST FAIL (proves tests work)
3. **Implement** - Minimum code to pass tests
4. **Run tests** - Tests MUST PASS (proves implementation works)
5. **Refactor** - Improve code while keeping tests green
6. **/verify** - Independent story validation (automatic)

**Violations**:
- Writing implementation before tests → STOP, write tests first
- Tests passing without implementation → STOP, tests are wrong
- Skipping test execution → STOP, run tests to prove they work
- Marking task complete without passing tests → STOP, fix tests first

**Rationale**: Tests are the specification in executable form. Code that passes tests meets requirements. Tests that don't run are worthless.

---

## Progressive Delivery Pattern (Constitution Article VII)

**Story-by-Story Delivery**:

```
P1 Complete → Demo → Ship → User Feedback
  ↓
P2 Complete → Demo → Ship → User Feedback
  ↓
P3 Complete → Demo → Ship → User Feedback
```

**Benefits**:
- Early user feedback (MVP after P1)
- Reduced risk (ship incrementally)
- Clear progress (each story is milestone)
- Parallel development possible (if stories independent)

**Anti-Pattern**:
```
❌ All stories 80% complete → Nothing shippable
✅ P1 100% complete → Ship MVP immediately
```

---

## Integration with SDD Workflow

**User Journey** (85% automated):

```
User: /feature "User authentication with email/password"
  ↓ (automatic)
specify-feature creates spec.md
  ↓ (automatic)
/plan creates plan.md + supporting docs
  ↓ (automatic)
generate-tasks creates tasks.md
  ↓ (automatic)
/audit validates consistency → PASS
  ↓ (manual)
User: /implement plan.md
  ↓ (automatic per story)
implement-and-verify implements P1 → /verify --story P1 → PASS
  ↓ (automatic)
implement-and-verify implements P2 → /verify --story P2 → PASS
  ↓ (automatic)
implement-and-verify implements P3 → /verify --story P3 → PASS
  ↓
Complete implementation ready for Phase 7 QA
```

**Total User Actions**: 2 manual steps (/feature, /implement)
**Automatic Steps**: 8+ (spec → plan → tasks → audit → P1 → P2 → P3 → verifications)

**This phase (Phase 6) IS the /implement command execution.**
