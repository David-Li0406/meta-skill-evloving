/**
 * Playwright Test Template for Radulator Calculators
 *
 * This template provides a comprehensive test structure for automated
 * testing of Radulator medical calculators.
 *
 * Features:
 * - Console error detection
 * - Network request monitoring
 * - Screenshot capture (before/after)
 * - Result extraction and verification
 * - Performance timing
 *
 * Usage:
 * Replace {{CALCULATOR_NAME}}, {{INPUTS}}, and {{EXPECTED}} with actual values
 */

const { test, expect } = require('@playwright/test');

test.describe('{{CALCULATOR_NAME}} Calculator Tests', () => {
  let consoleErrors = [];
  let networkRequests = [];

  test.beforeEach(async ({ page }) => {
    // Reset arrays
    consoleErrors = [];
    networkRequests = [];

    // Capture console errors
    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });

    // Monitor network requests
    page.on('request', request => {
      networkRequests.push({
        url: request.url(),
        method: request.method()
      });
    });

    // Navigate to Radulator
    await page.goto(process.env.RADULATOR_URL || 'http://localhost:5173');
    await page.waitForLoadState('networkidle');
  });

  test('{{TEST_CASE_NAME}}', async ({ page }) => {
    const startTime = Date.now();

    // Select calculator from sidebar
    await page.click('text={{CALCULATOR_NAME}}');
    await page.waitForTimeout(500); // Allow UI to render

    // Take "before" screenshot
    await page.screenshot({
      path: 'screenshots/{{CALCULATOR_ID}}-before.png',
      fullPage: true
    });

    // Fill input fields
    {{INPUT_ACTIONS}}

    // Take "after inputs" screenshot
    await page.screenshot({
      path: 'screenshots/{{CALCULATOR_ID}}-inputs.png',
      fullPage: true
    });

    // Click Calculate button
    await page.click('button:has-text("Calculate")');
    await page.waitForTimeout(1000); // Allow calculation to complete

    const calcTime = Date.now() - startTime;

    // Take "results" screenshot
    await page.screenshot({
      path: 'screenshots/{{CALCULATOR_ID}}-results.png',
      fullPage: true
    });

    // Extract results
    {{RESULT_EXTRACTION}}

    // Verify expected values
    {{ASSERTIONS}}

    // Performance check
    expect(calcTime).toBeLessThan(2000); // Should complete within 2 seconds

    // Console error check
    expect(consoleErrors).toHaveLength(0);

    // Network check - should only make local requests
    const externalRequests = networkRequests.filter(req =>
      !req.url.includes('localhost') &&
      !req.url.includes('127.0.0.1') &&
      !req.url.includes('file://')
    );
    expect(externalRequests).toHaveLength(0);

    // Log test summary
    console.log({
      calculator: '{{CALCULATOR_NAME}}',
      testCase: '{{TEST_CASE_NAME}}',
      executionTime: `${calcTime}ms`,
      consoleErrors: consoleErrors.length,
      externalRequests: externalRequests.length,
      status: 'PASSED'
    });
  });
});


// =====================================
// SPECIFIC CALCULATOR EXAMPLES
// =====================================

/**
 * Example 1: Adrenal CT Washout Calculator
 */
test.describe('Adrenal CT Washout Calculator', () => {
  let consoleErrors = [];

  test.beforeEach(async ({ page }) => {
    consoleErrors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });
    await page.goto('http://localhost:5173');
  });

  test('Typical adenoma test case', async ({ page }) => {
    // Select calculator
    await page.click('text=Adrenal Washout CT');

    // Fill inputs
    await page.fill('input[id="unenh"]', '10');
    await page.fill('input[id="portal"]', '100');
    await page.fill('input[id="delayed"]', '40');

    // Screenshot before calculation
    await page.screenshot({ path: 'screenshots/adrenal-ct-before.png' });

    // Calculate
    await page.click('button:has-text("Calculate")');
    await page.waitForTimeout(500);

    // Screenshot after calculation
    await page.screenshot({ path: 'screenshots/adrenal-ct-after.png' });

    // Extract results (adjust selectors based on actual DOM)
    const resultsText = await page.textContent('.results-section');

    // Verify absolute washout
    expect(resultsText).toContain('66.7');
    expect(resultsText).toContain('60.0');

    // No console errors
    expect(consoleErrors).toHaveLength(0);
  });
});

/**
 * Example 2: Prostate Volume Calculator
 */
test.describe('Prostate Volume Calculator', () => {
  test('Normal prostate test case', async ({ page }) => {
    await page.goto('http://localhost:5173');

    // Select calculator
    await page.click('text=Prostate Volume');

    // Fill inputs
    await page.fill('input[id="length"]', '4');
    await page.fill('input[id="height"]', '3');
    await page.fill('input[id="width"]', '3.5');
    await page.fill('input[id="psa"]', '2');

    // Calculate
    await page.click('button:has-text("Calculate")');
    await page.waitForTimeout(500);

    // Extract and verify volume
    const resultsText = await page.textContent('.results-section');
    expect(resultsText).toContain('21.84');
    expect(resultsText).toContain('0.092');
  });
});

/**
 * Example 3: ALBI Score Calculator
 */
test.describe('ALBI Score Calculator', () => {
  test('Grade 1 liver function - SI units', async ({ page }) => {
    await page.goto('http://localhost:5173');

    // Select calculator
    await page.click('text=ALBI Score');

    // Select SI units
    await page.click('input[value="SI"]');

    // Fill inputs
    await page.fill('input[id="albumin"]', '40');
    await page.fill('input[id="bilirubin"]', '15');

    // Calculate
    await page.click('button:has-text("Calculate")');
    await page.waitForTimeout(500);

    // Verify grade 1
    const resultsText = await page.textContent('.results-section');
    expect(resultsText).toContain('Grade 1');
    expect(resultsText).toContain('-2.87'); // Approximate ALBI score
  });
});

/**
 * Example 4: Child-Pugh Score Calculator
 */
test.describe('Child-Pugh Score Calculator', () => {
  test('Class A well-compensated', async ({ page }) => {
    await page.goto('http://localhost:5173');

    // Select calculator
    await page.click('text=Child-Pugh Score');

    // Fill numeric inputs
    await page.fill('input[id="bilirubin"]', '1.5');
    await page.fill('input[id="albumin"]', '3.8');
    await page.fill('input[id="inr"]', '1.2');

    // Select radio options
    await page.click('input[value="none"][name*="ascites"]');
    await page.click('input[value="none"][name*="encephalopathy"]');

    // Calculate
    await page.click('button:has-text("Calculate")');
    await page.waitForTimeout(500);

    // Verify Class A
    const resultsText = await page.textContent('.results-section');
    expect(resultsText).toContain('Class A');
    expect(resultsText).toContain('5');
  });
});

/**
 * Example 5: MELD-Na Score Calculator
 */
test.describe('MELD-Na Score Calculator', () => {
  test('Low risk patient', async ({ page }) => {
    await page.goto('http://localhost:5173');

    // Select calculator
    await page.click('text=MELD-Na Score');

    // Fill inputs
    await page.fill('input[id="creatinine"]', '0.8');
    await page.fill('input[id="bilirubin"]', '1.0');
    await page.fill('input[id="inr"]', '1.0');
    await page.fill('input[id="sodium"]', '140');

    // Dialysis checkbox should be unchecked by default

    // Calculate
    await page.click('button:has-text("Calculate")');
    await page.waitForTimeout(500);

    // Verify low risk
    const resultsText = await page.textContent('.results-section');
    expect(resultsText).toContain('6'); // MELD score (lower bounded)
    expect(resultsText).toContain('Low risk');
  });
});

/**
 * Example 6: IPSS Calculator
 */
test.describe('IPSS Calculator', () => {
  test('Mild symptoms', async ({ page }) => {
    await page.goto('http://localhost:5173');

    // Select calculator
    await page.click('text=IPSS');

    // Answer all 7 questions with low scores
    for (let i = 1; i <= 7; i++) {
      await page.click(`input[name="q${i}"][value="1"]`);
    }

    // QoL question
    await page.click('input[name="q8"][value="2"]');

    // Calculate
    await page.click('button:has-text("Calculate")');
    await page.waitForTimeout(500);

    // Verify mild severity
    const resultsText = await page.textContent('.results-section');
    expect(resultsText).toContain('Mild');
    expect(resultsText).toContain('7'); // Total score
  });
});

/**
 * Example 7: SHIM Score Calculator
 */
test.describe('SHIM Score Calculator', () => {
  test('No erectile dysfunction', async ({ page }) => {
    await page.goto('http://localhost:5173');

    // Select calculator
    await page.click('text=SHIM Score');

    // Answer all 5 questions with highest scores
    for (let i = 1; i <= 5; i++) {
      await page.click(`input[name="q${i}"][value="5"]`);
    }

    // Calculate
    await page.click('button:has-text("Calculate")');
    await page.waitForTimeout(500);

    // Verify no ED
    const resultsText = await page.textContent('.results-section');
    expect(resultsText).toContain('No erectile dysfunction');
    expect(resultsText).toContain('25'); // Perfect score
  });
});

/**
 * Example 8: RENAL Nephrometry Score
 */
test.describe('RENAL Nephrometry Score', () => {
  test('Low complexity tumor', async ({ page }) => {
    await page.goto('http://localhost:5173');

    // Select calculator
    await page.click('text=RENAL Nephrometry Score');

    // Fill inputs
    await page.fill('input[id="radius"]', '3.5');
    await page.click('input[value=">=50"]'); // Exophytic
    await page.click('input[value=">=7"]'); // Nearness
    await page.click('input[value="above/below"]'); // Polar location
    await page.selectOption('select[id="anterior"]', 'Anterior');

    // Calculate
    await page.click('button:has-text("Calculate")');
    await page.waitForTimeout(500);

    // Verify low complexity
    const resultsText = await page.textContent('.results-section');
    expect(resultsText).toContain('Low');
    expect(resultsText).toContain('4'); // Score
  });
});

/**
 * Example 9: Milan Criteria
 */
test.describe('Milan Criteria Calculator', () => {
  test('Within Milan criteria - 2 small tumors', async ({ page }) => {
    await page.goto('http://localhost:5173');

    // Select calculator
    await page.click('text=Milan Criteria');

    // Fill inputs
    await page.selectOption('select[id="tumorCount"]', '2');
    await page.fill('input[id="tumor1Size"]', '2.5');
    await page.fill('input[id="tumor2Size"]', '2.0');
    await page.click('input[value="no"][name*="macrovascular"]');
    await page.click('input[value="no"][name*="extrahepatic"]');

    // Calculate
    await page.click('button:has-text("Calculate")');
    await page.waitForTimeout(500);

    // Verify within criteria
    const resultsText = await page.textContent('.results-section');
    expect(resultsText).toContain('WITHIN');
    expect(resultsText).toContain('Milan');
  });
});

// =====================================
// HELPER FUNCTIONS
// =====================================

/**
 * Generic calculator test runner
 */
async function testCalculator(page, config) {
  const {
    calculatorName,
    testCaseName,
    inputs,
    expectedResults,
    screenshotPrefix
  } = config;

  // Select calculator
  await page.click(`text=${calculatorName}`);
  await page.waitForTimeout(500);

  // Screenshot: before
  if (screenshotPrefix) {
    await page.screenshot({
      path: `screenshots/${screenshotPrefix}-before.png`
    });
  }

  // Fill inputs
  for (const input of inputs) {
    if (input.type === 'text' || input.type === 'number') {
      await page.fill(`input[id="${input.id}"]`, String(input.value));
    } else if (input.type === 'radio') {
      await page.click(`input[value="${input.value}"]`);
    } else if (input.type === 'select') {
      await page.selectOption(`select[id="${input.id}"]`, input.value);
    } else if (input.type === 'checkbox') {
      if (input.value) {
        await page.check(`input[id="${input.id}"]`);
      }
    }
  }

  // Screenshot: inputs filled
  if (screenshotPrefix) {
    await page.screenshot({
      path: `screenshots/${screenshotPrefix}-inputs.png`
    });
  }

  // Calculate
  await page.click('button:has-text("Calculate")');
  await page.waitForTimeout(1000);

  // Screenshot: results
  if (screenshotPrefix) {
    await page.screenshot({
      path: `screenshots/${screenshotPrefix}-results.png`
    });
  }

  // Extract and verify results
  const resultsText = await page.textContent('.results-section');

  for (const expected of expectedResults) {
    expect(resultsText).toContain(String(expected));
  }

  return {
    testCase: testCaseName,
    status: 'PASSED'
  };
}

module.exports = { testCalculator };
