---
name: prometheus-testing
description: "Enforce Prometheus Testing Doctrine during development. Provides: (1) Test level guidance (MT/IT/SOC), (2) Playwright patterns for 1890x940 viewport, (3) SOC report generation, (4) Trigger threshold management. Triggers: test, testing, MT, IT, SOC, Playwright, E2E, unit test, test doctrine, run tests, test coverage."
---

# Prometheus Testing Skill

## CRITICAL: Testing Doctrine Reference

This skill enforces the **Prometheus Testing Doctrine**.
Full doctrine: `docs/Prometheus_Testing_Doctrine.txt`
Framework reference: `docs/TESTING.md`

> **"Testing is not optional. Testing scales with system maturity."**

## Test Levels

### Level 1: Minor Tests (MT)

**Purpose:** Immediate sanity checks during development

**Who:** Claude Code (CC)

**When:** Continuously during implementation

**Scope:** Component-level or local logic

**Command:**
```bash
cd prometheus-ui && npm run test:mt
```

**Examples:**
- Component renders without runtime errors
- Buttons trigger expected handlers
- State updates propagate correctly
- No console warnings or errors
- Basic interaction sanity checks

**Pass Criteria:** Works as expected in isolation

**CC Obligation:** Run MT after ANY code change before proceeding

---

### Level 2: Implementation Tests (IT)

**Purpose:** Verify complete feature/subsystem works as designed

**Who:** Claude Code (CC)

**When:** At completion of each Task Order or Phase

**Scope:** Page-level or subsystem-level

**Command:**
```bash
cd prometheus-ui && npm run test:it
```

**Examples:**
- CRUD operations on SCALAR hierarchy
- Profile switching without state leakage
- Cross-context stability (FORMAT ↔ DESIGN ↔ BUILD)
- IndexedDB persistence across reloads
- Bidirectional sync verification

**Pass Criteria:** Feature behaves correctly under normal operator use

**Trigger Thresholds:**
| Metric | Threshold | Action |
|--------|-----------|--------|
| File changes | 10 | IT recommended |
| Commits | 5 | IT recommended |

---

### Level 3: System Operator Check (SOC)

**Purpose:** Deliberate, exhaustive verification of system readiness

**Who:** Claude Code (CC), **ONLY when directed by Founder**

**When:**
- Prior to major merges
- Prior to demos
- Prior to releases
- When explicitly ordered by Founder

**Scope:** Entire system. No exemptions.

**Command:**
```bash
cd prometheus-ui && npm run test:soc        # Standard SOC
cd prometheus-ui && npm run test:soc:full   # Full exhaustive SOC
```

**SOC is NOT:**
- Routine
- Optional when invoked
- Polite

---

## Viewport Configuration

**CRITICAL:** All Playwright tests use the Implementation Viewport Baseline.

```javascript
// playwright.config.js
use: {
  viewport: { width: 1890, height: 940 }
}
```

Before ANY screenshot or test:
```javascript
await page.setViewportSize({ width: 1890, height: 940 });
const vp = page.viewportSize();
console.log(`Viewport: ${vp.width} × ${vp.height}`);
```

## Quick Commands

| Level | Command | Context |
|-------|---------|---------|
| MT | `npm run test:mt` | After any code change |
| MT (watch) | `npm run test` | During active development |
| MT (coverage) | `npm run test:coverage` | Before commits |
| IT | `npm run test:it` | After task/phase completion |
| E2E | `npm run test:e2e` | Feature verification |
| E2E (visible) | `npm run test:e2e:headed` | Debugging |
| SOC | `npm run test:soc` | By Founder order |
| SOC Full | `npm run test:soc:full` | Before releases |
| All | `npm run test:all` | Complete verification |

## Test Patterns

### Component Sanity (MT)

```javascript
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import MyComponent from './MyComponent';

describe('MyComponent', () => {
  it('renders without error', () => {
    render(<MyComponent />);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('handles click events', async () => {
    const onClick = vi.fn();
    render(<MyComponent onClick={onClick} />);
    await userEvent.click(screen.getByRole('button'));
    expect(onClick).toHaveBeenCalledOnce();
  });
});
```

### E2E Page Test (IT)

```javascript
import { test, expect } from '@playwright/test';

test.describe('Design Page', () => {
  test.beforeEach(async ({ page }) => {
    // Enforce viewport baseline
    await page.setViewportSize({ width: 1890, height: 940 });
    await page.goto('http://localhost:5173');
    // Navigate to Design page
    await page.click('[data-testid="login-button"]');
    await page.click('[data-testid="nav-design"]');
  });

  test('SCALAR hierarchy displays correctly', async ({ page }) => {
    await expect(page.locator('[data-testid="scalar-tree"]')).toBeVisible();
  });

  test('can add topic to lesson', async ({ page }) => {
    await page.click('[data-testid="add-topic-btn"]');
    await page.fill('[data-testid="topic-name-input"]', 'New Topic');
    await page.click('[data-testid="save-topic-btn"]');
    await expect(page.locator('text=New Topic')).toBeVisible();
  });
});
```

### Visual Validation (SOC)

```javascript
test('visual baseline - navigation hub', async ({ page }) => {
  await page.setViewportSize({ width: 1890, height: 940 });
  await page.goto('http://localhost:5173');
  await page.click('[data-testid="login-button"]');

  // Visual assertions
  const navWheel = page.locator('[data-testid="nav-wheel"]');
  await expect(navWheel).toBeVisible();

  // Check positioning
  const box = await navWheel.boundingBox();
  expect(box.x).toBeCloseTo(945 - box.width / 2, -1); // Centred
});
```

### Stress Test (SOC)

```javascript
test('rapid clicking does not break state', async ({ page }) => {
  await page.goto('http://localhost:5173');
  await page.click('[data-testid="login-button"]');

  // Rapid clicks
  for (let i = 0; i < 10; i++) {
    await page.click('[data-testid="nav-design"]');
    await page.click('[data-testid="nav-build"]');
  }

  // Verify stability
  await expect(page).toHaveURL(/design|build/);
  const consoleErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  expect(consoleErrors).toHaveLength(0);
});
```

## SOC Report Format

Each SOC generates a report in `prometheus-ui/test-results/`:

```
SOC REPORT
================================
Date: [timestamp]
Type: [SOC | SOC_FULL]
Duration: [X] seconds

SCOPE:
- UI & Interaction: [count] tests
- State & Logic: [count] tests
- Data Integrity: [count] tests
- Visual Validation: [count] tests
- Behaviour Under Misuse: [count] tests

RESULTS:
- Passed: [count]
- Failed: [count]
- Skipped: [count]

FAILURES:
[List of failed tests with details]

FIXES APPLIED:
[List of fixes made during SOC]

KNOWN ISSUES:
[Remaining issues for future work]

================================
END OF REPORT
```

## CC Testing Obligations

### During Development
1. Run MT after EVERY code change
2. Verify no console errors/warnings
3. Check component isolation

### After Task/Phase
1. Run IT for affected subsystems
2. Verify cross-page stability
3. Check data persistence
4. Document test results

### When Founder Orders SOC
1. Run full SOC suite
2. Generate SOC report
3. Fix all failures before proceeding
4. Document known issues
5. Report to Founder

## Trigger Management

Check threshold status:
```bash
node prometheus-ui/scripts/test-triggers.js --status
```

Reset counters after IT:
```bash
node prometheus-ui/scripts/test-triggers.js --reset
```

## Directory Structure

```
prometheus-ui/
├── src/test/
│   ├── setup.js                    # Test setup/mocks
│   └── *.test.js                   # Unit tests
├── e2e/
│   ├── soc-full.spec.js            # Full SOC E2E
│   └── visual-validation.spec.js   # Visual tests
├── scripts/
│   ├── run-soc.js                  # SOC runner
│   └── test-triggers.js            # Trigger system
├── test-results/                    # Generated reports
├── vitest.config.js                # Vitest config
└── playwright.config.js            # Playwright config
```

## Compliance Statement

Per the Testing Doctrine:

> "All contributors must understand this doctrine, reference it when implementing features, and acknowledge it in repository documentation. Failure to adhere to this doctrine is a defect."

This skill exists to make the doctrine **BINDING** and **ENFORCEABLE**.

## See Also

- `docs/Prometheus_Testing_Doctrine.txt` - Full doctrine
- `docs/TESTING.md` - Framework reference
- `PLAYWRIGHT_CONFIG.md` - Viewport standards
- `/prometheus-ui` - UI coordinate system
