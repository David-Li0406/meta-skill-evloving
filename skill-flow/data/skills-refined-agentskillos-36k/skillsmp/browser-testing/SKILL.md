---
name: browser-testing
description: Browser testing with Playwright MCP for visual and functional validation
category: validation
depends-on: [validation-workflow]
---

# Browser Testing Skill

> "Automated tests verify logic – browser tests verify reality."

## When to Use This Skill

Use for **every validation** after automated checks pass.

## Quick Start

```typescript
// Using Playwright MCP
// 1. Navigate
await page.goto('http://localhost:3000');

// 2. Wait for canvas
await page.waitForSelector('canvas');

// 3. Take screenshot
await page.screenshot({ path: 'validation.png' });

// 4. Check console
const errors = [];
page.on('console', (msg) => {
  if (msg.type() === 'error') errors.push(msg.text());
});
```

## Test Categories

| Category    | What to Check              |
| ----------- | -------------------------- |
| Load        | Page loads, canvas renders |
| Console     | No errors or warnings      |
| Functional  | Features work as specified |
| Visual      | UI appears correctly       |
| Performance | 60 FPS, no stuttering      |
| Input       | Controls respond correctly |

## Progressive Guide

### Level 1: Basic Load Test

```typescript
test('page loads correctly', async ({ page }) => {
  // Navigate
  await page.goto('http://localhost:3000');

  // Wait for canvas
  const canvas = page.locator('canvas');
  await expect(canvas).toBeVisible();

  // Take screenshot
  await page.screenshot({ path: 'screenshots/load.png' });
});
```

### Level 2: Console Error Check

```typescript
test('no console errors', async ({ page }) => {
  const errors: string[] = [];

  page.on('console', (msg) => {
    if (msg.type() === 'error') {
      errors.push(msg.text());
    }
  });

  await page.goto('http://localhost:3000');
  await page.waitForTimeout(5000); // Wait for initial load

  expect(errors).toHaveLength(0);
});
```

### Level 3: Input Testing

```typescript
test('keyboard controls work', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.waitForSelector('canvas');

  // Focus canvas
  await page.click('canvas');

  // Press WASD keys
  await page.keyboard.press('KeyW');
  await page.waitForTimeout(500);
  await page.screenshot({ path: 'screenshots/after-w.png' });

  await page.keyboard.press('KeyA');
  await page.waitForTimeout(500);
  await page.screenshot({ path: 'screenshots/after-a.png' });
});
```

**For game-specific input patterns**, see [`game-testing.md`](game-testing.md) for:
- Continuous movement (key down/up patterns)
- Mouse aiming and clicking
- Combo sequences
- Special key combinations

### Level 4: Visual Comparison

```typescript
test('visual appearance matches', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.waitForSelector('canvas');
  await page.waitForTimeout(2000); // Wait for scene to stabilize

  // Compare with baseline
  await expect(page).toHaveScreenshot('baseline.png', {
    maxDiffPixelRatio: 0.01,
  });
});
```

**For advanced visual testing**, see [`visual-testing.md`](visual-testing.md) for:
- Game state detection (menu, playing, game over, win)
- Semantic visual comparison with Vision MCP
- UI element validation (HUD, health bars, minimap)
- GDD compliance validation

### Level 5: Performance Metrics

```typescript
test('performance is acceptable', async ({ page }) => {
  await page.goto('http://localhost:3000');

  // Get performance metrics
  const metrics = await page.evaluate(() => {
    const entries = performance.getEntriesByType('navigation');
    const nav = entries[0] as PerformanceNavigationTiming;
    return {
      loadTime: nav.loadEventEnd - nav.startTime,
      domContentLoaded: nav.domContentLoadedEventEnd - nav.startTime,
    };
  });

  expect(metrics.loadTime).toBeLessThan(3000);
  expect(metrics.domContentLoaded).toBeLessThan(2000);
});
```

## ⚠️ CRITICAL: Playwright MCP is REQUIRED

**There is NO manual testing fallback.**

If Playwright MCP is not available:

1. **FAIL the validation immediately**
2. Report as critical blocker: `"Playwright MCP not configured - cannot validate"`
3. **DO NOT** attempt manual browser testing

Browser testing via Playwright MCP is **NON-NEGOTIABLE**.

**This is a mandatory gating condition** - validation cannot proceed without Playwright MCP.

### Why No Manual Fallback?

- Manual testing is subjective and error-prone
- Automations ensure consistent validation across all tasks
- Screenshots via Playwright provide objective evidence
- Console monitoring catches issues humans miss
- No manual testing = higher quality bar

## Cross-Browser Testing

| Browser         | Priority         | Notes                   |
| --------------- | ---------------- | ----------------------- |
| Chrome/Chromium | Required         | Primary target          |
| Firefox         | Recommended      | WebGL differences       |
| Safari/WebKit   | If targeting iOS | Significant differences |
| Edge            | Optional         | Uses Chromium           |

## Anti-Patterns

❌ **DON'T:**

- Skip browser testing because automated tests passed
- Test only in one browser
- Ignore console warnings
- Skip performance check
- Assume "it works on my machine"

✅ **DO:**

- Test in browser for every validation
- Check console for errors
- Verify all acceptance criteria
- Take screenshots as evidence
- Test keyboard and mouse input

## Checklist

For each validation:

- [ ] Dev server running (`npm run dev`)
- [ ] Navigate to app URL
- [ ] Canvas loads and renders
- [ ] No console errors
- [ ] All acceptance criteria verified
- [ ] Input controls work
- [ ] Performance acceptable
- [ ] Screenshots captured

## Reference

- [Playwright Documentation](https://playwright.dev/docs/intro)
- [agents/qa/skills/validation-workflow.md](validation-workflow.md) — Full workflow
- [agents/qa/skills/game-testing.md](game-testing.md) — Game control patterns
- [agents/qa/skills/visual-testing.md](visual-testing.md) — Visual validation
- [agents/qa/AGENT.md](../AGENT.md) — Full QA instructions
