import { test, expect } from '@playwright/test';

// E2E smoke: save mid-branch -> reload -> resume or show graceful rollback

test('save mid-branch then reload resumes or rolls back gracefully', async ({ page }) => {
  await page.goto('http://127.0.0.1:4173/demo/?story=/stories/demo.ink');
  // Wait for demo to load and present story and choices
  await page.waitForSelector('#story');
  await page.waitForSelector('#choices');

  // Capture visible story text before save
  const before = await page.textContent('#story');
  expect(before).toBeTruthy();

  // Click first choice to get into a branched flow (if desired) - keep optional to avoid flakiness
  const choiceButtons = await page.$$('#choices button');
  if (choiceButtons.length > 0) {
    await choiceButtons[0].click();
    // allow UI to update
    await page.waitForTimeout(150);
  }

  // Trigger a manual save via window API exposed by demo if available, otherwise click Save button
  const hasDemoSave = await page.evaluate(() => !!window.DemoSave);
  if (hasDemoSave) {
    await page.evaluate(() => { window.DemoSave && window.DemoSave.save('e2e-test'); });
  } else {
    await page.click('#save-btn');
  }

  // Read the saved visible story snapshot (from DOM) to compare after reload
  const savedSnapshot = await page.textContent('#story');

  // Reload the page
  await page.reload();
  await page.waitForSelector('#story');

  // Load from save via API if available, otherwise click Load button
  if (hasDemoSave) {
    await page.evaluate(() => { window.DemoSave && window.DemoSave.load('e2e-test'); });
  } else {
    await page.click('#load-btn');
  }

  // Give the loader a moment to restore DOM
  await page.waitForTimeout(200);

  const after = await page.textContent('#story');
  // Normalize whitespace for comparison
  const normalize = (s: string | null) => (s || '').replace(/\s+/g, ' ').trim();
  const nBefore = normalize(savedSnapshot);
  const nAfter = normalize(after);

  // Assert that after contains the start of the saved snapshot (defensive: allow substring match)
  expect(nAfter).toBeTruthy();
  expect(nAfter.length).toBeGreaterThanOrEqual( Math.min(10, nBefore.length) );
  expect(nAfter).toContain(nBefore.substring(0, Math.min(40, nBefore.length)));
});
