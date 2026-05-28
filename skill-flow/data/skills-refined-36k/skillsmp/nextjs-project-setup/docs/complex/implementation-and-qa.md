# Phases 6-7: Implementation & Quality Assurance (Complex Path)

**Duration**: 6-12 hours total (4-8 hours implementation + 2-4 hours QA)
**Prerequisites**: Phases 2-5 complete (template, spec, design, wireframes) + audit passed
**Next Phase**: Phase 8 (Documentation)

---

## Overview

This combined phase executes implementation using test-driven development (TDD) with progressive delivery, followed by comprehensive quality assurance across all dimensions. These phases flow together naturally: implementation creates working features with tests, QA validates quality meets production standards.

**What You'll Accomplish**:
1. Implement all user stories with tests-first approach
2. Verify each story independently (progressive delivery)
3. Execute comprehensive QA (functionality, accessibility, performance, security, compatibility)
4. Remediate blocking issues and document findings
5. Obtain production readiness sign-off

**Outputs**:
- Implemented Next.js application (all P1 stories minimum)
- Passing test suite (100% AC coverage)
- Verification reports per story
- QA report with findings and resolutions
- Performance baseline and accessibility audit
- Production readiness checklist

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
5. Comprehensive QA after all stories complete

**Constitution Enforcement**:
- **Article III**: Test-First Imperative (TDD mandatory, no exceptions)
- **Article VII**: User-Story-Centric Organization (implement P1 completely before P2)
- **Article V**: Template-Driven Quality (verification-report.md per story)

---

## Workflow (CoD^Σ)

```
/implement plan.md → implement-and-verify_skill
  ↓
Pre_Implementation_Validation → Foundation_Setup
  ↓
Tasks.md[P1] → Tests_First ∘ Red ∘ Green ∘ Refactor
  ↓
/verify --story P1 → AC_Validation → [PASS]
  ↓
Tasks.md[P2] → Tests_First ∘ Red ∘ Green ∘ Refactor
  ↓
/verify --story P2 → AC_Validation → [PASS]
  ↓
Tasks.md[P3] → Tests_First ∘ Red ∘ Green ∘ Refactor
  ↓
/verify --story P3 → AC_Validation → [PASS]
  ↓
Complete_Implementation → Comprehensive_QA
  ↓
{Automated_Tests, Accessibility, Performance, Security, Compatibility} ∥
  ↓
Findings_Report → Remediation ⇄ Retest
  ↓
QA_Sign_Off → Phase_8_Documentation
```

**Key Principle**: Each story is independently testable and demonstrable. No "big bang" integration.

---

## Phase 6: Implementation (4-8 hours)

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

### Step 4: User Story Implementation (P1, P2, P3...)

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

### Step 5: Progressive Delivery (P2, P3, ...)

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

**Pre-QA Checklist**:
- [ ] All tests passing (`npm test`)
- [ ] Lint passing (`npm run lint`)
- [ ] Type-check passing (`npm run type-check`)
- [ ] Build succeeds (`npm run build`)
- [ ] All verification reports generated (per story)
- [ ] MVP demonstrable (P1 stories functional)

---

## Phase 7: Quality Assurance (2-4 hours)

### QA Philosophy

**Quality Gates** (Constitution-enforced):
- ✅ **Functional**: All ACs passing (Article III - TDD)
- ✅ **Accessible**: WCAG 2.1 AA minimum
- ✅ **Performant**: Lighthouse ≥90 performance score
- ✅ **Secure**: No critical vulnerabilities
- ✅ **Compatible**: Works across modern browsers

**Gate Enforcement**:
- Each gate MUST pass before production deployment
- Failures documented with severity (CRITICAL/HIGH/MEDIUM/LOW)
- CRITICAL and HIGH severity blocks deployment
- MEDIUM and LOW severity can be tracked as technical debt

### Step 7: Automated Testing Suite

**Unit Tests** (already passing from Phase 6):
```bash
# Run all unit tests
npm test

# Coverage report
npm test -- --coverage

# Target: 100% AC coverage (minimum)
```

**Integration Tests**:
```bash
# Test API routes
npm test -- --grep "API"

# Test database operations
npm test -- --grep "Database"

# Test authentication flow end-to-end
npm test -- --grep "Auth Flow"
```

**E2E Tests via Chrome MCP**:
```typescript
// tests/e2e/user-journey.spec.ts
import { test, expect } from '@playwright/test'

test('User can sign up, log in, and access dashboard', async ({ page }) => {
  // Sign up
  await page.goto('http://localhost:3000/auth/signup')
  await page.fill('[name="email"]', 'test@example.com')
  await page.fill('[name="password"]', 'SecurePassword123!')
  await page.click('button:has-text("Sign Up")')
  await expect(page).toHaveURL(/\/dashboard/)

  // Log out
  await page.click('[aria-label="User menu"]')
  await page.click('text=Log Out')
  await expect(page).toHaveURL(/\/auth\/login/)

  // Log in
  await page.fill('[name="email"]', 'test@example.com')
  await page.fill('[name="password"]', 'SecurePassword123!')
  await page.click('button:has-text("Log In")')
  await expect(page).toHaveURL(/\/dashboard/)

  // Verify dashboard loads within 2s (AC from P1)
  const start = Date.now()
  await page.waitForSelector('h1:has-text("Dashboard")')
  const elapsed = Date.now() - start
  expect(elapsed).toBeLessThan(2000)
})
```

**Automated Test Checklist**:
- [ ] All unit tests passing (100% AC coverage)
- [ ] All integration tests passing (API, DB, Auth)
- [ ] All E2E tests passing (critical user journeys)
- [ ] Test coverage report generated
- [ ] No flaky tests (tests pass consistently)

### Step 8: Accessibility Audit

**Automated Accessibility Scan**:
```bash
# Install axe-core
npm install -D @axe-core/playwright

# Run accessibility tests
npm run test:a11y
```

**Manual Accessibility Checks** (WCAG 2.1 AA):

**Keyboard Navigation**:
- [ ] Tab order logical (follows visual layout)
- [ ] All interactive elements keyboard accessible
- [ ] Focus indicators visible (outline or custom style)
- [ ] Skip navigation link present (for screen readers)
- [ ] Modal/dialog traps focus correctly
- [ ] Escape key closes modals

**Screen Reader Compatibility**:
- [ ] All images have alt text
- [ ] Form inputs have associated labels
- [ ] ARIA labels present where needed
- [ ] Heading hierarchy logical (h1 → h2 → h3)
- [ ] Button text descriptive ("Submit" not "Click here")

**Color Contrast** (4.5:1 minimum):
```bash
# Use Chrome DevTools Lighthouse
# Navigate to page
# Open DevTools → Lighthouse → Accessibility

# Or use WebAIM contrast checker
# https://webaim.org/resources/contrastchecker/
```

**Verify Contrast**:
- [ ] Text on background: ≥4.5:1
- [ ] Large text (18pt+): ≥3:1
- [ ] UI components: ≥3:1 (buttons, inputs)
- [ ] Dark mode contrast also compliant

### Step 9: Performance Audit

**Lighthouse Performance Scan**:
```bash
# Run Lighthouse locally
npx lighthouse http://localhost:3000 --view

# Or use Chrome DevTools
# DevTools → Lighthouse → Performance + Best Practices
```

**Target Scores**:
- **Performance**: ≥90
- **Accessibility**: 100
- **Best Practices**: ≥90
- **SEO**: ≥90

**Core Web Vitals** (measure on real device):
- **LCP** (Largest Contentful Paint): <2.5s (good), <4s (needs improvement)
- **FID** (First Input Delay): <100ms (good), <300ms (needs improvement)
- **CLS** (Cumulative Layout Shift): <0.1 (good), <0.25 (needs improvement)

**Performance Optimization Checklist**:
- [ ] Images optimized (Next.js Image component with priority)
- [ ] Fonts loaded efficiently (next/font)
- [ ] No render-blocking resources
- [ ] Code splitting enabled (automatic with App Router)
- [ ] API responses cached appropriately
- [ ] Static pages generated at build time
- [ ] Bundle size reasonable (<200KB initial JS)

### Step 10: Security Audit

**Automated Security Scan**:
```bash
# Run npm audit
npm audit

# Fix vulnerabilities
npm audit fix

# Target: 0 critical/high vulnerabilities
```

**Manual Security Checks**:

**Authentication & Authorization**:
- [ ] Passwords hashed (bcrypt/argon2, never plaintext)
- [ ] Session tokens secure (HttpOnly, Secure, SameSite)
- [ ] JWT validated on server (not just client)
- [ ] Protected routes enforce authentication
- [ ] Role-based access control (if applicable)

**Data Validation**:
- [ ] Server-side validation (never trust client)
- [ ] SQL injection prevented (parameterized queries/ORM)
- [ ] XSS prevented (React escapes by default, verify dangerouslySetInnerHTML)
- [ ] CSRF tokens implemented (if using forms)
- [ ] File upload validation (type, size, malware scan if applicable)

**Environment & Secrets**:
- [ ] .env.local in .gitignore (secrets not committed)
- [ ] API keys not exposed to client (NEXT_PUBLIC_ only for public keys)
- [ ] Database credentials not hardcoded
- [ ] Sensitive data encrypted at rest (if applicable)

**API Security**:
- [ ] Rate limiting implemented (prevent brute force)
- [ ] CORS configured correctly (not allow *)
- [ ] Error messages don't leak sensitive info
- [ ] API authentication required (no open endpoints)

### Step 11: Browser Compatibility Testing

**Modern Browser Support** (target):
- Chrome/Edge: Last 2 versions
- Firefox: Last 2 versions
- Safari: Last 2 versions
- Mobile Safari: iOS 15+
- Mobile Chrome: Android 10+

**Testing Strategy**:

**Local Testing** (primary browsers):
- [ ] Chrome (desktop + mobile emulation)
- [ ] Firefox (desktop)
- [ ] Safari (if on macOS)

**Browser Compatibility Matrix**:
```markdown
| Browser           | Version | Status | Issues |
|-------------------|---------|--------|--------|
| Chrome (Desktop)  | 120     | ✅ PASS | None   |
| Chrome (Mobile)   | 120     | ✅ PASS | None   |
| Firefox (Desktop) | 121     | ✅ PASS | None   |
| Safari (Desktop)  | 17      | ⚠️ PARTIAL | Button hover state not working |
| Safari (iOS)      | 17      | ✅ PASS | None   |
| Edge (Desktop)    | 120     | ✅ PASS | None   |
```

### Step 12: Mobile Responsiveness Testing

**Viewport Testing** (real devices or Chrome DevTools):
- [ ] iPhone SE (375px)
- [ ] iPhone 14 Pro (390px)
- [ ] Pixel 5 (393px)
- [ ] iPad Mini (768px)
- [ ] iPad Pro (1024px)

**Mobile-Specific Checks**:
- [ ] Text readable without zoom (min 16px font)
- [ ] Touch targets ≥44x44px (WCAG)
- [ ] Horizontal scrolling absent (width: 100vw issues)
- [ ] Fixed elements don't overlap content
- [ ] Landscape orientation works (if applicable)
- [ ] Forms keyboard-friendly (no zoom on focus)

### Step 13: Manual Exploratory Testing

**User Journey Testing** (critical paths):

**Journey 1: New User Sign Up**:
1. Visit landing page
2. Click "Sign Up" CTA
3. Fill registration form
4. Submit form
5. Verify email (if applicable)
6. Access dashboard
7. Complete onboarding (if applicable)

**Expected**: Smooth flow, no errors, <30 seconds to dashboard

**Journey 2: Returning User Login**:
1. Visit /auth/login
2. Enter credentials
3. Submit form
4. Dashboard loads within 2s (AC)
5. Navigate to profile
6. Update profile
7. Changes persist after refresh

**Expected**: Fast login, data persistence, no errors

**Edge Case Testing**:
- [ ] Offline behavior (show offline indicator)
- [ ] Slow network (loading states visible)
- [ ] Invalid data (error messages clear)
- [ ] Empty states (no data scenarios handled)
- [ ] Long content (pagination or scrolling)
- [ ] Special characters (email with +, unicode names)

### Step 14: Remediation & Retesting

**Bug Tracking**:
```markdown
| ID | Severity | Description | Status | Fix |
|----|----------|-------------|--------|-----|
| BUG-001 | HIGH | Rate limiting not implemented | OPEN | Add Upstash rate limiter |
| BUG-002 | SERIOUS | Missing alt text on hero image | FIXED | Added alt="..." |
| BUG-003 | MEDIUM | Safari button hover not working | OPEN | Add -webkit-appearance |
| BUG-004 | MEDIUM | Unclear error message for duplicate email | OPEN | Update error text |
| BUG-005 | LOW | Loading state missing on profile save | OPEN | Add spinner |
```

**Remediation Process**:
1. Prioritize by severity (CRITICAL → HIGH → MEDIUM → LOW)
2. Fix blocking issues (CRITICAL, HIGH, SERIOUS) first
3. Retest after each fix
4. Update bug tracker status
5. Re-run affected tests (automated + manual)

**Retest Checklist**:
- [ ] All CRITICAL and HIGH bugs fixed and retested
- [ ] Regression testing (ensure fixes don't break other features)
- [ ] Automated tests still passing
- [ ] Performance/accessibility scores maintained

### Step 15: QA Sign-Off

**Final QA Checklist**:
- [ ] All automated tests passing (unit, integration, E2E)
- [ ] Accessibility: WCAG 2.1 AA compliant (100 score)
- [ ] Performance: Lighthouse ≥90 (all categories)
- [ ] Security: No critical/high vulnerabilities
- [ ] Browser compatibility: All target browsers working
- [ ] Mobile responsive: All breakpoints tested
- [ ] All CRITICAL and HIGH bugs resolved
- [ ] MEDIUM and LOW bugs tracked (can defer)

**Production Readiness Gate**:
```
IF (all_tests_passing AND
    accessibility_score == 100 AND
    lighthouse_performance >= 90 AND
    critical_bugs == 0 AND
    high_bugs == 0)
THEN
  Status := READY_FOR_PRODUCTION
ELSE
  Status := BLOCKED (fix issues first)
```

---

## Quality Checks

### Per-Story Checklist (Implementation - Before /verify)
- [ ] All ACs have passing tests (100% coverage)
- [ ] No hardcoded values (use design system variables)
- [ ] Components installed from Shadcn (followed Search → View → Example → Install)
- [ ] Mobile responsive (tested at sm/md/lg breakpoints)
- [ ] Accessibility validated (keyboard nav, ARIA labels)
- [ ] Loading states implemented
- [ ] Error handling complete

### Pre-QA Checklist (After Implementation)
- [ ] All P1 stories passing independently
- [ ] Navigation between features working
- [ ] Shared state (if any) functioning correctly
- [ ] No console errors in browser
- [ ] No TypeScript errors
- [ ] Build succeeds (`npm run build`)
- [ ] All verification reports generated (per story)

### QA Validation Checklist
- [ ] All quality gates passed (functional, accessible, performant, secure, compatible)
- [ ] QA report generated with findings
- [ ] All blocking issues resolved
- [ ] Regression testing complete
- [ ] Performance baseline documented

---

## Outputs

### Implementation Outputs

**1. Implemented Application**
- **Location**: Project root directory
- **Status**: Running on http://localhost:3000
- **Coverage**: All P1 stories minimum (P2/P3 optional)

**2. Test Suite**
- **Location**: `/tests/` directory
- **Coverage**: 100% AC coverage (all acceptance criteria tested)
- **Status**: All tests passing

**3. Verification Reports**
- **Location**: `/docs/verification-*.md` (per story)
- **Content**: AC validation results, independent demo status
- **Format**: Template from @.claude/templates/verification-report.md

**4. Build Artifacts**
- **Location**: `/.next/` directory
- **Status**: Production build successful
- **Performance**: Ready for QA validation

### QA Outputs

**5. QA Report**
- **Location**: `/docs/qa-report.md`
- **Content**: Comprehensive findings across all quality dimensions
- **Format**: Issues with severity, status, remediation steps

**6. Performance Baseline**
- **Location**: `/docs/performance-baseline.md`
- **Content**: Lighthouse scores, Core Web Vitals, bundle analysis
- **Usage**: Compare against future deployments (no regression)

**7. Accessibility Audit**
- **Location**: `/docs/accessibility-audit.md`
- **Content**: WCAG compliance results, manual checks, remediation
- **Status**: PASS (100 score) or BLOCKED with issues

**8. Browser Compatibility Matrix**
- **Location**: `/docs/browser-compatibility.md`
- **Content**: Tested browsers with versions and status
- **Format**: Table with PASS/FAIL/PARTIAL per browser

**9. Bug Tracker**
- **Location**: `/docs/bug-tracker.md` (or issue tracker)
- **Content**: All bugs with severity, status, assignments
- **Updated**: Throughout remediation process

---

## Next Phase Handover

**Prerequisites for Phase 8 (Documentation)**:
- ✅ All P1 stories implemented and verified
- ✅ Test suite passing (100% AC coverage)
- ✅ Build succeeds without errors
- ✅ QA report complete
- ✅ All blocking bugs resolved (CRITICAL, HIGH)
- ✅ Performance baseline documented
- ✅ Accessibility audit PASS
- ✅ Production readiness sign-off

**Handover Context**:
- Working application on localhost:3000
- Test coverage report
- QA report with all findings
- Known issues (MEDIUM, LOW) for documentation
- Performance targets for monitoring
- Browser support matrix for user guidance
- Verification reports per story

**Continue with**: `documentation.md`

---

## Common Issues & Solutions

### Implementation Issues

**Issue**: Tests fail after implementation
- **Cause**: Tests written incorrectly OR implementation doesn't match ACs
- **Solution**: Review ACs in spec.md. Tests should validate ACs exactly, not implementation details. Fix tests if they test wrong thing, fix implementation if it doesn't meet ACs.

**Issue**: P1 verification blocks on dependencies
- **Cause**: P1 depends on incomplete foundational tasks
- **Solution**: Complete Phase 2 (Foundational) fully before starting P1. Foundational tasks are blocking prerequisites.

**Issue**: Cannot proceed to P2 (P1 verification fails)
- **Cause**: Constitution Article VII enforcement - stories must pass independently
- **Solution**: Fix P1 until all ACs pass. Do not skip to P2. Progressive delivery requires each story complete before next.

**Issue**: Hardcoded colors in components
- **Cause**: Not following design system from Phase 4
- **Solution**: Replace all hardcoded colors with CSS variables (e.g., `text-primary` not `#000000`). Review design-system.md for variable names.

**Issue**: Components don't render
- **Cause**: Shadcn component not installed OR incorrect import path
- **Solution**: Follow Shadcn workflow (Search → View → Example → Install). Verify component exists in components.json registry.

**Issue**: Build fails with TypeScript errors
- **Cause**: Missing types OR incorrect imports
- **Solution**: Run `npm run type-check` to see all errors. Fix imports, add types, or update tsconfig.json if needed.

### QA Issues

**Issue**: Lighthouse score drops after fixes
- **Cause**: New code added without optimization
- **Solution**: Re-run bundle analyzer, optimize images, check for render-blocking resources

**Issue**: Accessibility score failing on contrast
- **Cause**: Design system colors don't meet 4.5:1 ratio
- **Solution**: Adjust CSS variables in globals.css, verify with contrast checker

**Issue**: Tests passing locally but failing in CI
- **Cause**: Environment differences, timing issues, missing dependencies
- **Solution**: Use fixed test data, add explicit waits, ensure CI has all dependencies

**Issue**: Mobile testing reveals layout issues
- **Cause**: Fixed widths, missing responsive classes
- **Solution**: Use responsive Tailwind classes (sm:, md:, lg:), test at breakpoints

---

## Success Criteria

### Implementation Success Criteria
- ✅ All P1 stories implemented (MVP functional)
- ✅ Test suite passing (100% AC coverage per story)
- ✅ All verification reports PASS status
- ✅ Independent story demos working
- ✅ Build succeeds (`npm run build`)
- ✅ No TypeScript errors
- ✅ No console errors in browser
- ✅ Design system followed (no hardcoded colors)

### QA Success Criteria
- ✅ All automated tests passing (100% AC coverage)
- ✅ Accessibility: WCAG 2.1 AA (score 100)
- ✅ Performance: Lighthouse ≥90 all categories
- ✅ Security: 0 critical/high vulnerabilities
- ✅ Browser compatibility: All target browsers working
- ✅ Mobile responsive: All breakpoints tested
- ✅ All blocking bugs resolved
- ✅ QA report generated
- ✅ Production readiness sign-off complete
- ✅ Ready for comprehensive documentation (Phase 8)

---

## Evidence Requirements (Constitution Article II)

**Implementation Evidence**:
- **AC mapping**: Every test traced to specific AC (tasks.md:line)
- **Test results**: Actual test output showing PASS status
- **Component usage**: Shadcn components used per wireframes.md
- **Design system compliance**: No hardcoded colors, all variables from globals.css

**QA Evidence**:
- **Test results**: Actual output from test runs (pass/fail)
- **Lighthouse scores**: Screenshot or JSON output with scores
- **Accessibility violations**: Specific elements with file:line references
- **Browser screenshots**: Visual proof of compatibility issues
- **Performance metrics**: Core Web Vitals with measurement timestamps

**Example Good Evidence**:
"P1 AC2 (tasks.md:line 67 - Dashboard load < 2s) verified via test (tests/auth/login.test.tsx:45-58) which measures elapsed time. Test PASSES at 1234ms < 2000ms threshold. Implementation uses Next.js App Router with server components for fast initial load. Lighthouse confirms LCP: 1.8s (target: <2.5s). QA audit PASS."

---

## TDD Cycle Enforcement (Constitution Article III)

**MANDATORY SEQUENCE** (no exceptions):

1. **Write tests FIRST** - All ACs become tests before ANY implementation
2. **Run tests** - Tests MUST FAIL (proves tests work)
3. **Implement** - Minimum code to pass tests
4. **Run tests** - Tests MUST PASS (proves implementation works)
5. **Refactor** - Improve code while keeping tests green
6. **/verify** - Independent story validation (automatic)
7. **QA** - Comprehensive quality validation

**Violations**:
- Writing implementation before tests → STOP, write tests first
- Tests passing without implementation → STOP, tests are wrong
- Skipping test execution → STOP, run tests to prove they work
- Marking task complete without passing tests → STOP, fix tests first

**Rationale**: Tests are the specification in executable form. Code that passes tests meets requirements. Tests that don't run are worthless. QA validates quality beyond functional correctness.

---

## Progressive Delivery Pattern (Constitution Article VII)

**Story-by-Story Delivery**:

```
P1 Complete → Demo → Ship → User Feedback → QA Validation
  ↓
P2 Complete → Demo → Ship → User Feedback → QA Validation
  ↓
P3 Complete → Demo → Ship → User Feedback → QA Validation
  ↓
Comprehensive QA → Production Readiness
```

**Benefits**:
- Early user feedback (MVP after P1)
- Reduced risk (ship incrementally)
- Clear progress (each story is milestone)
- Parallel development possible (if stories independent)
- Quality validated throughout (not just at end)

**Anti-Pattern**:
```
❌ All stories 80% complete → Nothing shippable
✅ P1 100% complete → Ship MVP immediately → QA validated
```

---

## Tools Required

**Implementation Tools**:
- Vitest (unit test runner)
- Testing Library (component testing)
- TypeScript (type checking)
- ESLint (linting)
- Shadcn MCP (component installation)
- Supabase MCP (database operations, if applicable)

**QA Tools**:
- Chrome MCP (E2E testing, performance profiling, accessibility audits)
- Lighthouse (performance and best practices scoring)
- Axe (accessibility violation detection)
- npm audit (security vulnerability scanning)
- Browser Stack (optional - cross-browser testing)

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
  ↓ (automatic)
Comprehensive QA validation → Production readiness
  ↓
Complete implementation ready for Phase 8 Documentation
```

**Total User Actions**: 2 manual steps (/feature, /implement)
**Automatic Steps**: 8+ (spec → plan → tasks → audit → P1 → P2 → P3 → verifications → QA)

**This phase (Phases 6-7) IS the /implement command execution with comprehensive QA validation.**
