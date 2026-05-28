import { test, expect } from '@playwright/test';

// Lightweight demo loader similar to existing helpers
async function loadDemo(page) {
  await page.goto('/demo/');
  await page.waitForSelector('#story');
  await page.waitForFunction(() => {
    const el = document.querySelector('#story');
    return !!el && el.textContent && el.textContent.trim().length > 0;
  }, undefined, { timeout: 5000 });
}

test('director writes telemetry buffer to sessionStorage when approving mock proposals', async ({ page }) => {
  await loadDemo(page);

  // Ensure Director is present
  const hasDirector = await page.evaluate(() => typeof (window as any).Director !== 'undefined');
  expect(hasDirector).toBe(true);

  // Clear any existing buffer
  await page.evaluate(() => sessionStorage.removeItem('ge-hch.director.telemetry'));

  // Prepare a mock proposal and force addAIChoice several times
  const approvals = await page.evaluate(async () => {
    // ensure fallback return paths allow approval
    (window as any).__proposalValidReturnPaths = ['campfire', 'pines'];
    const inkrunner = (window as any).__inkrunner;
    inkrunner.clearMockProposals();

    const count = 3;
    for (let i = 0; i < count; i++) {
      const mock = {
        choice_text: `AI test ${i}`,
        content: { text: 'Short safe AI content', return_path: 'campfire' },
        metadata: { confidence_score: 0.95 }
      };
      // add as mock and request director evaluation
      inkrunner.enqueueMockProposal(mock);
      // force director on and use mock proposal path
      // await the result so Director runs
      // @ts-ignore
      await inkrunner.addAIChoice({ forceDirectorEnabled: true, forceMockProposal: true });
    }

    // Read buffer
    const raw = sessionStorage.getItem('ge-hch.director.telemetry') || '[]';
    const arr = JSON.parse(raw);
    return arr;
  });

  // Expect telemetry buffer to contain entries
  expect(Array.isArray(approvals)).toBe(true);
  expect(approvals.length).toBeGreaterThanOrEqual(1);

  // Validate structure of the last entry
  const last = approvals[approvals.length - 1];
  expect(last).toHaveProperty('proposal_id');
  expect(last).toHaveProperty('timestamp');
  expect(last).toHaveProperty('decision');
  expect(last).toHaveProperty('riskScore');
  expect(last).toHaveProperty('latencyMs');
  expect(last).toHaveProperty('writerMs');
  expect(last).toHaveProperty('directorMs');
  expect(last).toHaveProperty('totalMs');
  expect(last).toHaveProperty('metrics');
  expect(typeof last.writerMs).toBe('number');
  expect(typeof last.directorMs).toBe('number');
  expect(typeof last.totalMs).toBe('number');

  // Timestamp should be parseable
  const parsed = Date.parse(last.timestamp);
  expect(Number.isNaN(parsed)).toBe(false);
});
