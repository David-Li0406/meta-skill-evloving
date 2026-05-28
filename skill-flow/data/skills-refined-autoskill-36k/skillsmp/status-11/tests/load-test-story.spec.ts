import { test, expect } from '@playwright/test';

async function collectConsoleErrors(page) {
  const errors: string[] = [];
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
  });
  return errors;
}

test('demo loads test-story.ink via ?story and presents UI', async ({ page }) => {
  const errors = await collectConsoleErrors(page);

  // Load the demo and request the test story explicitly
  await page.goto('/demo/?story=/stories/test-story.ink');

  // Ensure the demo actually fetched the specific story file
  await page.waitForResponse(resp => resp.url().endsWith('/stories/test-story.ink') && resp.status() === 200, { timeout: 5000 });

  const story = page.locator('#story');
  await expect(story).toBeVisible();

  // Wait until the story area has text content
  await page.waitForFunction(() => {
    const el = document.querySelector('#story');
    return !!el && el.textContent && el.textContent.trim().length > 0;
  }, undefined, { timeout: 5000 });

  const choices = page.locator('.choice-btn');
  await expect.poll(async () => choices.count(), { timeout: 5000 }).toBeGreaterThan(0);

  // Verify rendered content is from the test story (not the default demo)
  const rendered = await story.textContent();
  await expect(rendered).toContain('They are keeping me waiting.');

  // No console errors
  expect(errors, 'Console errors should be empty').toEqual([]);
});
