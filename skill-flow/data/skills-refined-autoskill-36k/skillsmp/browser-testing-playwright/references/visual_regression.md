# Visual Regression Testing

Visual regression testing catches unintended UI changes by comparing screenshots of your application over time. Playwright has built-in support for visual testing with the `toHaveScreenshot()` assertion.

## How it Works

1.  **First Run**: The first time you run a test with `toHaveScreenshot()`, Playwright generates a "golden" or "snapshot" image of the element or page. This image is stored in a new directory next to your test file (e.g., `my-test.spec.ts-snapshots`).
2.  **Subsequent Runs**: On future test runs, Playwright takes a new screenshot and compares it to the saved snapshot. If the new screenshot is different, the test fails.
3.  **Updating Snapshots**: If a visual change is intentional, you can update the snapshots by running your tests with the `--update-snapshots` flag.

```bash
npx playwright test --update-snapshots
```

## Example: Testing a Component's Appearance

You can take a screenshot of the entire page or a specific element. It's often best to target specific, stable components to reduce test flakiness.

```typescript
// tests/component-visual.spec.ts
import { test, expect } from '@playwright/test';

test('should render the hero component correctly', async ({ page }) => {
  await page.goto('/');

  const heroComponent = page.locator('.hero-section');

  // Ensure the component is visible before taking a screenshot
  await expect(heroComponent).toBeVisible();

  // Take a screenshot and compare it to the snapshot
  await expect(heroComponent).toHaveScreenshot('hero-component.png');
});

test('should render the full landing page correctly', async ({ page }) => {
    await page.goto('/');

    // Take a screenshot of the entire page
    await expect(page).toHaveScreenshot('landing-page.png');
});
```

## Best Practices

-   **Target Specific Elements**: Screenshotting small, self-contained components is more reliable than screenshotting an entire page, which might contain dynamic content (like animations or dates).
-   **Control for Dynamic Data**: If a component displays dynamic data, mock it or use static data during visual tests to prevent false positives.
-   **Set a Threshold**: You can allow for minor differences in screenshots by setting a `maxDiffPixels` or `maxDiffPixelRatio` threshold. This can be useful for dealing with anti-aliasing differences across machines.

    ```typescript
    await expect(heroComponent).toHaveScreenshot('hero-component.png', {
      maxDiffPixels: 100, // Allow up to 100 pixels to be different
    });
    ```
-   **Name Your Snapshots**: Use descriptive names for your snapshots (e.g., `hero-component-hover.png`). The filename you provide is used to store the snapshot.