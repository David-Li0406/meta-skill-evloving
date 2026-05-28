# Phase 7: Quality Assurance & Testing (Complex Path)

**Duration**: 2-4 hours
**Prerequisites**: Phase 6 (Implementation complete, all P1 stories verified)
**Next Phase**: Phase 8 (Documentation)

---

## Overview

**Purpose**: Comprehensive quality validation across functionality, accessibility, performance, security, and compatibility

**Inputs**:
- Implemented application (from Phase 6)
- Passing unit/integration tests (100% AC coverage)
- Verification reports (per story)
- Wireframes and design system (Phases 4-5)

**Outputs**:
- QA report with findings and resolutions
- Performance baseline (Lighthouse scores)
- Accessibility audit results (WCAG 2.1 AA)
- Browser compatibility matrix
- Bug tracker (if issues found)
- Production readiness checklist

---

## QA Philosophy

**Quality Gates** (Constitution-enforced):
- ✅ **Functional**: All ACs passing (Article III - TDD)
- ✅ **Accessible**: WCAG 2.1 AA minimum (Article VI - Simplicity)
- ✅ **Performant**: Lighthouse ≥90 performance score
- ✅ **Secure**: No critical vulnerabilities
- ✅ **Compatible**: Works across modern browsers

**Gate Enforcement**:
- Each gate MUST pass before production deployment
- Failures documented with severity (CRITICAL/HIGH/MEDIUM/LOW)
- CRITICAL and HIGH severity blocks deployment
- MEDIUM and LOW severity can be tracked as technical debt

---

## Tools Required

- **Chrome MCP**: E2E testing, performance profiling, accessibility audits
- **Lighthouse**: Performance and best practices scoring
- **Testing Library**: Component and integration testing
- **Vitest**: Unit test runner
- **Axe**: Accessibility violation detection
- **Browser Stack** (optional): Cross-browser testing

---

## Workflow (CoD^Σ)

```
Implementation_Complete → Automated_Tests ∥ Manual_Tests
  ↓
{Unit, Integration, E2E} → Test_Results[PASS/FAIL]
  ↓
Accessibility_Audit ∥ Performance_Audit ∥ Security_Audit
  ↓
Browser_Compatibility → Compatibility_Matrix
  ↓
Findings_Report → Remediation ⇄ Retest
  ↓
QA_Sign_Off → Phase_8_Docs
```

---

## Detailed Steps

### Step 1: Automated Testing Suite

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

**Run E2E Tests**:
```bash
npm run test:e2e

# Target: All user journeys complete successfully
```

**Automated Test Checklist**:
- [ ] All unit tests passing (100% AC coverage)
- [ ] All integration tests passing (API, DB, Auth)
- [ ] All E2E tests passing (critical user journeys)
- [ ] Test coverage report generated
- [ ] No flaky tests (tests pass consistently)

### Step 2: Accessibility Audit

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

**Form Accessibility**:
- [ ] Error messages associated with inputs (aria-describedby)
- [ ] Required fields indicated (aria-required or visual)
- [ ] Validation errors announced to screen readers
- [ ] Autocomplete attributes present (email, password)

**Accessibility Audit Report**:
```markdown
## Accessibility Audit Results

**Standard**: WCAG 2.1 Level AA

**Automated Scan** (axe-core):
- Total issues: 3
- Critical: 0
- Serious: 1 (Missing alt text on hero image)
- Moderate: 2 (Form labels not explicitly associated)

**Manual Testing**:
- Keyboard navigation: ✅ PASS
- Screen reader (NVDA): ✅ PASS
- Color contrast: ⚠️ PARTIAL (1 button fails contrast)
- Focus indicators: ✅ PASS

**Remediation Required**:
1. SERIOUS: Add alt="Dashboard hero illustration" to hero-image.png
2. MODERATE: Wrap label around input in LoginForm:45
3. MODERATE: Add aria-label to search input in Header:89
4. MODERATE: Increase button contrast from 3.2:1 to 4.5:1

**Status**: ⚠️ BLOCKED (1 serious issue requires fix)
```

### Step 3: Performance Audit

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

**Performance Audit Report**:
```markdown
## Performance Audit Results

**Lighthouse Score**: 92/100 ✅

**Core Web Vitals**:
- LCP: 1.8s ✅ (target: <2.5s)
- FID: 45ms ✅ (target: <100ms)
- CLS: 0.05 ✅ (target: <0.1)

**Bundle Analysis**:
- Initial JS: 145 KB ✅
- Initial CSS: 12 KB ✅
- Total page weight: 890 KB ⚠️ (hero image 650 KB)

**Recommendations**:
1. Compress hero image (650KB → <200KB) using Next.js Image
2. Enable response caching for API routes (Cache-Control headers)
3. Preload critical fonts (already using next/font - optimal)

**Status**: ✅ PASS (score ≥90, all CVW good)
```

### Step 4: Security Audit

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

**Security Audit Report**:
```markdown
## Security Audit Results

**npm audit**: 0 vulnerabilities ✅

**Authentication**: ✅ PASS
- Passwords hashed via bcrypt (12 rounds)
- Session tokens HttpOnly + Secure + SameSite=Strict
- Protected routes validated via middleware

**Data Validation**: ✅ PASS
- Server-side validation via Zod schemas
- Supabase RLS policies enforce authorization
- No dangerouslySetInnerHTML usage

**Environment**: ✅ PASS
- .env.local not committed
- API keys in environment variables only
- No hardcoded credentials

**API Security**: ⚠️ PARTIAL
- Rate limiting: ❌ NOT IMPLEMENTED
- CORS: ✅ Configured correctly
- Error messages: ✅ No sensitive info leaked

**Remediation Required**:
1. HIGH: Implement rate limiting on /api/auth/* routes (use Upstash Redis)

**Status**: ⚠️ BLOCKED (1 high severity issue)
```

### Step 5: Browser Compatibility Testing

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

**Cloud Testing** (optional via BrowserStack):
- [ ] Edge (Windows)
- [ ] Safari (macOS + iOS)
- [ ] Mobile Chrome (Android)

**Feature Detection** (ensure graceful degradation):
```javascript
// Check for modern features
if ('IntersectionObserver' in window) {
  // Use lazy loading
} else {
  // Load all images immediately
}
```

**Browser Compatibility Matrix**:
```markdown
## Browser Compatibility Results

| Browser           | Version | Status | Issues |
|-------------------|---------|--------|--------|
| Chrome (Desktop)  | 120     | ✅ PASS | None   |
| Chrome (Mobile)   | 120     | ✅ PASS | None   |
| Firefox (Desktop) | 121     | ✅ PASS | None   |
| Safari (Desktop)  | 17      | ⚠️ PARTIAL | Button hover state not working |
| Safari (iOS)      | 17      | ✅ PASS | None   |
| Edge (Desktop)    | 120     | ✅ PASS | None   |

**Issues Found**:
1. MEDIUM: Safari desktop button hover (webkit-appearance issue)
   - Fix: Add explicit :hover styles with -webkit-appearance: none

**Status**: ⚠️ PARTIAL (1 medium issue requires fix)
```

### Step 6: Mobile Responsiveness Testing

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

**Responsive Audit Report**:
```markdown
## Mobile Responsiveness Results

**Devices Tested**: iPhone SE, iPhone 14 Pro, iPad Mini

**Breakpoint Coverage**:
- sm (640px): ✅ PASS
- md (768px): ✅ PASS
- lg (1024px): ✅ PASS
- xl (1280px): ✅ PASS

**Mobile Issues**:
- None found ✅

**Landscape Orientation**: ✅ PASS (tested on iPhone 14 Pro)

**Status**: ✅ PASS
```

### Step 7: Manual Exploratory Testing

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

**Exploratory Testing Log**:
```markdown
## Exploratory Testing Results

**Tester**: [Name]
**Date**: YYYY-MM-DD
**Duration**: 45 minutes

**Journeys Tested**: New user signup, Returning user login, Profile editing

**Findings**:
1. MEDIUM: Error message unclear when email already exists
   - Current: "An error occurred"
   - Better: "This email is already registered. Try logging in."
2. LOW: Loading state missing on profile save button
   - Add spinner to button during save operation
3. LOW: Empty state for dashboard stats needs better messaging
   - Current: No stats displayed
   - Better: "No activity yet. Get started by [action]."

**Positive Observations**:
- Login flow very fast (<1s)
- Error handling generally good
- Mobile experience smooth

**Status**: ⚠️ PARTIAL (1 medium, 2 low issues)
```

### Step 8: Remediation & Retesting

**Bug Tracking**:
```markdown
## Bug Tracker

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

### Step 9: QA Sign-Off

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

## Sub-Agents

**qa-validator agent** (optional):
- Runs automated QA suite (tests, lighthouse, a11y audits)
- Generates comprehensive QA report
- Identifies remediation priorities

**Invocation**:
```bash
# Run QA validator agent in parallel
Task(qa-validator, "Run complete QA suite and generate report")
```

---

## Quality Checks

### Pre-Sign-Off Checklist
- [ ] All quality gates passed (functional, accessible, performant, secure, compatible)
- [ ] QA report generated with findings
- [ ] All blocking issues resolved
- [ ] Regression testing complete
- [ ] Performance baseline documented

### Compliance Checklist
- [ ] WCAG 2.1 AA compliant (accessibility)
- [ ] GDPR compliant (if handling EU data)
- [ ] COPPA compliant (if targeting children under 13)
- [ ] SOC 2 considerations (if B2B SaaS)

---

## Outputs

### 1. QA Report
**Location**: `/docs/qa-report.md`
**Content**: Comprehensive findings across all quality dimensions
**Format**: Issues with severity, status, remediation steps

### 2. Performance Baseline
**Location**: `/docs/performance-baseline.md`
**Content**: Lighthouse scores, Core Web Vitals, bundle analysis
**Usage**: Compare against future deployments (no regression)

### 3. Accessibility Audit
**Location**: `/docs/accessibility-audit.md`
**Content**: WCAG compliance results, manual checks, remediation
**Status**: PASS (100 score) or BLOCKED with issues

### 4. Browser Compatibility Matrix
**Location**: `/docs/browser-compatibility.md`
**Content**: Tested browsers with versions and status
**Format**: Table with PASS/FAIL/PARTIAL per browser

### 5. Bug Tracker
**Location**: `/docs/bug-tracker.md` (or issue tracker)
**Content**: All bugs with severity, status, assignments
**Updated**: Throughout remediation process

---

## Next Phase Handover

**Prerequisites for Phase 8 (Documentation)**:
- ✅ QA report complete
- ✅ All blocking bugs resolved (CRITICAL, HIGH)
- ✅ Performance baseline documented
- ✅ Accessibility audit PASS
- ✅ Production readiness sign-off

**Handover Context**:
- QA report with all findings
- Known issues (MEDIUM, LOW) for documentation
- Performance targets for monitoring
- Browser support matrix for user guidance

**Continue with**: `phase-8-docs.md`

---

## Common Issues & Solutions

### Issue: Lighthouse score drops after fixes
**Cause**: New code added without optimization
**Solution**: Re-run bundle analyzer, optimize images, check for render-blocking resources

### Issue: Accessibility score failing on contrast
**Cause**: Design system colors don't meet 4.5:1 ratio
**Solution**: Adjust CSS variables in globals.css, verify with contrast checker

### Issue: Tests passing locally but failing in CI
**Cause**: Environment differences, timing issues, missing dependencies
**Solution**: Use fixed test data, add explicit waits, ensure CI has all dependencies

### Issue: Mobile testing reveals layout issues
**Cause**: Fixed widths, missing responsive classes
**Solution**: Use responsive Tailwind classes (sm:, md:, lg:), test at breakpoints

---

## Success Criteria

- ✅ All automated tests passing (100% AC coverage)
- ✅ Accessibility: WCAG 2.1 AA (score 100)
- ✅ Performance: Lighthouse ≥90 all categories
- ✅ Security: 0 critical/high vulnerabilities
- ✅ Browser compatibility: All target browsers working
- ✅ Mobile responsive: All breakpoints tested
- ✅ All blocking bugs resolved
- ✅ QA report generated
- ✅ Production readiness sign-off complete

---

## Evidence Requirements (Constitution Article II)

**All QA findings MUST document**:
- **Test results**: Actual output from test runs (pass/fail)
- **Lighthouse scores**: Screenshot or JSON output with scores
- **Accessibility violations**: Specific elements with file:line references
- **Browser screenshots**: Visual proof of compatibility issues
- **Performance metrics**: Core Web Vitals with measurement timestamps

**Example Good Evidence**:
"Accessibility violation (SERIOUS): Hero image missing alt text at app/page.tsx:67. Axe-core scan found img element with no alt attribute. Fixed by adding alt='Dashboard analytics illustration' at app/page.tsx:67. Retest confirms violation resolved (scan result: 0 serious issues)."

---

## QA Report Template

```markdown
# QA Report - [Project Name]

**Date**: YYYY-MM-DD
**Version**: v1.0.0
**QA Engineer**: [Name]

---

## Executive Summary

**Overall Status**: ✅ PASS / ⚠️ PARTIAL / ❌ FAIL

**Quality Gates**:
- Functional: ✅ PASS
- Accessible: ✅ PASS (WCAG 2.1 AA)
- Performant: ✅ PASS (Lighthouse 92/100)
- Secure: ⚠️ PARTIAL (1 high issue pending)
- Compatible: ✅ PASS (all target browsers)

**Blocking Issues**: 1 HIGH severity (rate limiting)
**Non-Blocking Issues**: 3 MEDIUM, 2 LOW

**Recommendation**: Resolve 1 HIGH severity issue before production deployment.

---

## Detailed Results

### 1. Functional Testing
[Insert test results]

### 2. Accessibility Audit
[Insert accessibility results]

### 3. Performance Audit
[Insert Lighthouse scores]

### 4. Security Audit
[Insert security findings]

### 5. Browser Compatibility
[Insert compatibility matrix]

### 6. Mobile Responsiveness
[Insert mobile test results]

---

## Issues Found

[Insert bug tracker]

---

## Recommendations

1. Fix HIGH severity issue (rate limiting) before deploying
2. Track MEDIUM issues as technical debt for next sprint
3. Monitor Core Web Vitals in production via Vercel Analytics
4. Set up error tracking (Sentry) to catch production issues

---

## Sign-Off

- QA Engineer: [Name], Date
- Tech Lead: [Name], Date
- Product Owner: [Name], Date
```
