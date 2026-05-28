import { test, expect } from '@playwright/test';
async function collectConsoleErrors(page) {
  const errors: string[] = [];
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
  });
  return errors;
}

async function loadDemo(page) {
  await page.goto('/demo/');
  const story = page.locator('#story');
  await expect(story).toBeVisible();
  await page.waitForFunction(() => {
    const el = document.querySelector('#story');
    return !!el && el.textContent && el.textContent.trim().length > 0;
  }, undefined, { timeout: 5000 });
  const choices = page.locator('.choice-btn');
  await expect.poll(async () => choices.count(), { timeout: 5000 }).toBeGreaterThan(0);
  return { story, choices };
}

// Click (baseline smoke)
test('demo loads and presents initial UI (click)', async ({ page }) => {
  const errors = await collectConsoleErrors(page);
  const { story, choices } = await loadDemo(page);
  const firstChoice = choices.first();
  const beforeText = await story.textContent();
  await firstChoice.click();
  await expect(story).not.toHaveText(beforeText || '');
  expect(errors, 'Console errors should be empty').toEqual([]);
});

// Keyboard advance
test('choice can be selected via keyboard', async ({ page }) => {
  const errors = await collectConsoleErrors(page);
  const { story, choices } = await loadDemo(page);
  const firstChoice = choices.first();
  await firstChoice.focus();
  const beforeText = await story.textContent();
  await page.keyboard.press('Enter');
  await expect(story).not.toHaveText(beforeText || '');
  expect(errors, 'Console errors should be empty').toEqual([]);
});

// Touch/tap advance (touch project only)
test('choice can be selected via tap (touch)', async ({ page, browserName }) => {
  test.skip(!!page.context()._options?.hasTouch === false, 'Tap only for touch-enabled context');
  const errors = await collectConsoleErrors(page);
  const { story, choices } = await loadDemo(page);
  const firstChoice = choices.first();
  const beforeText = await story.textContent();
  await firstChoice.tap();
  await expect(story).not.toHaveText(beforeText || '');
  expect(errors, 'Console errors should be empty').toEqual([]);
});

// Controller/gamepad surrogate via Space key
test('choice can be selected via controller (Space key surrogate)', async ({ page }) => {
  const errors = await collectConsoleErrors(page);
  const { story, choices } = await loadDemo(page);
  const firstChoice = choices.first();
  await firstChoice.focus();
  const beforeText = await story.textContent();
  await page.keyboard.press('Space');
  await expect(story).not.toHaveText(beforeText || '');
  expect(errors, 'Console errors should be empty').toEqual([]);
});
