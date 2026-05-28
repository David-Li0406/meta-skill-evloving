---
name: screenshot-regression-testing
description: Use this skill for screenshot-based regression testing of UI components and visual elements with Playwright, ensuring visual consistency across changes.
---

# Screenshot Regression Testing Skill

This skill orchestrates **screenshot-based regression testing** for UI components, particularly React components, using Playwright. It captures rendered pixels and compares them to baseline PNGs to detect unintended visual changes.

## When to Use This

- Testing React components (buttons, controls, panels, etc.)
- Verifying UI styling changes and theme/dark mode appearance
- Ensuring component layout and alignment are correct
- Auto-apply when editing files in `stories/` or `*.visual.spec.ts`

## Architecture

```
stories/
  components/                    → Shared React components for stories
    StripViewer.tsx
    ProgressionStrip.tsx
  ui-components/                 → UI component stories (if present)
    Button.visual.spec.ts
    Panel.visual.spec.ts
  01-bathymetry/
    01-bathymetry.mdx              → MDX story page
    01-bathymetry.visual.spec.ts   → Playwright visual test
    strip-bathymetry-basic.png     → Baseline screenshot (colocated)
  02-energy-field/
  ...
  visual-test-helpers.ts           → Test helper utilities
  App.tsx                          → Story viewer app
```

## Commands

```bash
# Verify stories compile (fast check)
npm run stories:build

# Run visual tests
npm run test:visual:headless        # CI/agents
npm run test:visual:headed          # Debugging with browser UI

# Update baselines after intentional changes
npm run test:visual:update:headless
npm run test:visual:update:headed

# Clear test artifacts
npm run reset:visual                # Clear results/reports only
npm run reset:visual:all            # Clear results + colocated baselines

# Start stories dev server for interactive debugging
npm run stories                   # Starts on http://localhost:3001
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
2. **Test states** - Include hover, focus, disabled, and active states.
3. **Consistent viewport** - Set fixed dimensions to avoid flaky tests.
4. **Wait for render** - Ensure the component is fully rendered before taking a screenshot.

```typescript
// Wait for component to be ready
await page.waitForSelector('[data-testid="my-component"]');
await page.waitForLoadState('networkidle');

// Screenshot just the component
const element = page.getByTestId('my-component');
await expect(element).toHaveScreenshot('my-component.png');
```

## Debugging with Chrome DevTools MCP

When a visual test fails, use the following commands to debug:

```typescript
// Start dev server
npm run stories

// Open in browser
mcp__chrome-devtools__new_page({ url: "http://localhost:3001/?page=ui-button" })

// Take snapshot to find element UIDs
mcp__chrome-devtools__take_snapshot()

// Screenshot specific element
mcp__chrome-devtools__take_screenshot({ uid: "<element-uid>" })

// After fixing, reload and re-check
mcp__chrome-devtools__navigate_page({ type: "reload" })
```

## Common Issues

- **Import Extensions After TS Migration**: Ensure imports do not include file extensions.
- **Missing Exports**: Verify that all necessary components are exported correctly.

## Related Skills

- **canvas-filmstrip-testing** - For matrix-to-canvas rendered progressions.
- **matrix-data-model-progression-testing** - Data verification before visual updates.