---
name: visual-regression-testing
description: Use this skill for screenshot-based regression testing of UI components with Playwright, ensuring visual consistency by comparing rendered pixels against baseline images.
---

# Visual Regression Testing Skill

This skill orchestrates **screenshot-based regression testing** for UI components using Playwright. It captures rendered pixels and compares them to baseline PNGs to detect unintended visual changes.

## When to Use This

- Testing React components (buttons, controls, panels, etc.)
- Verifying UI styling changes and theme/dark mode appearance
- Ensuring component layout integrity and alignment

## Architecture

```
stories/
  components/                    → Shared React components for stories
    StripViewer.tsx
    ProgressionStrip.tsx
  ui-components/                 → UI component stories (if present)
    Button.visual.spec.ts
    Panel.visual.spec.ts
```

## Commands

```bash
# Run visual regression tests
npm run test:visual:headless        # CI/agents
npm run test:visual:headed          # Debugging with browser UI

# Update baselines after intentional changes
npm run test:visual:update:headless
npm run test:visual:update:headed

# Clear test artifacts
npm run reset:visual                # Clear results/reports only
npm run reset:visual:all            # Clear results + colocated baselines

# Verify stories compile (fast check)
npm run stories:build
```

## Test Structure

```typescript
// Example: stories/ui-components/Button.visual.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Button Component', () => {
  test('primary button', async ({ page }) => {
    await page.goto('http://localhost:3001/?page=ui-button');

    const button = page.getByTestId('button-primary');
    await expect(button).toHaveScreenshot('button-primary.png');
  });

  test('disabled button', async ({ page }) => {
    await page.goto('http://localhost:3001/?page=ui-button');

    const button = page.getByTestId('button-disabled');
    await expect(button).toHaveScreenshot('button-disabled.png');
  });
});
```

## Best Practices

1. **Target specific elements** - Use `data-testid` to capture just the component.
2. **Test states** - Include tests for different states like hover, focus, and disabled.

## Important Notes

- Always use the development server (localhost) for testing, as using `file://` URLs may trigger CORS errors.
- For canvas-based visualizations, consider using specialized skills like `canvas-filmstrip-testing`.