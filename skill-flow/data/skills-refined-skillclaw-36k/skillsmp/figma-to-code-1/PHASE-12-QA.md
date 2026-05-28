# Phase 12: Automated QA

## Step 1: Screenshot Capture

Create Playwright script for screenshots:

```typescript
// qa/screenshot-capture.ts
import { test } from '@playwright/test';

const pages = [
  { url: '/', name: 'home' },
  // Add all pages from your build
];

const viewports = [
  { width: 1440, height: 900, name: 'desktop' },
  { width: 768, height: 1024, name: 'tablet' },
  { width: 375, height: 812, name: 'mobile' },
];

test('capture all pages', async ({ page }) => {
  for (const p of pages) {
    for (const vp of viewports) {
      await page.setViewportSize({ width: vp.width, height: vp.height });
      await page.goto(p.url);
      await page.screenshot({
        path: `qa/screenshots/${p.name}-${vp.name}.png`,
        fullPage: true,
      });
    }
  }
});
```

Run:
```bash
npx playwright test qa/screenshot-capture.ts
```

## Step 2: Structural Verification

Compare against `/docs/component-inventory.md`:
- [ ] Section count matches Figma
- [ ] Section order matches Figma
- [ ] All components present

## Step 3: Layout Verification

For each screenshot:
- [ ] Layout matches Figma
- [ ] Spacing is correct
- [ ] Typography matches
- [ ] Colors match design tokens

## Step 4: Content Verification

- [ ] ALL text matches CMS entries
- [ ] NO hardcoded content visible
- [ ] Images load from CDN

## Step 5: Responsive Check

- [ ] Mobile layout works
- [ ] Tablet layout works
- [ ] No horizontal scroll issues
- [ ] Navigation collapses properly

## Step 6: Design Token QA

Compare implementation against `/docs/design-tokens.md`. Search codebase for hardcoded values (e.g., `#hex`, `[Npx]`) that should use tokens. Generate a QA report (`/docs/QA-REPORT.md`) documenting token coverage percentage, issues found, and recommendations.

## Fix Discrepancies

1. Document issues found
2. Fix each issue (replace hardcoded values with tokens)
3. Re-run screenshot capture
4. Verify fixes

## Git Commit

```bash
git commit -m "fix: QA complete - visual fixes applied"
```

## Checkpoint

```bash
osascript -e 'display notification "Phase 12: QA complete" with title "Claude Code" sound name "Ping"'
```

**Next:** Proceed to [PHASE-13-PRODUCTION.md](PHASE-13-PRODUCTION.md)
