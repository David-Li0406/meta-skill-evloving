# Browser Automation

## Patterns


---
  #### **Name**
Test Isolation Pattern
  #### **Description**
Each test runs in complete isolation with fresh state
  #### **When**
Testing, any automation that needs reproducibility
  #### **Example**
    # TEST ISOLATION:
    
    """
    Each test gets its own:
    - Browser context (cookies, storage)
    - Fresh page
    - Clean state
    """
    
    ## Playwright Test Example
    """
    import { test, expect } from '@playwright/test';
    
    // Each test runs in isolated browser context
    test('user can add item to cart', async ({ page }) => {
      // Fresh context - no cookies, no storage from other tests
      await page.goto('/products');
      await page.getByRole('button', { name: 'Add to Cart' }).click();
      await expect(page.getByTestId('cart-count')).toHaveText('1');
    });
    
    test('user can remove item from cart', async ({ page }) => {
      // Completely isolated - cart is empty
      await page.goto('/cart');
      await expect(page.getByText('Your cart is empty')).toBeVisible();
    });
    """
    
    ## Shared Authentication Pattern
    """
    // Save auth state once, reuse across tests
    // setup.ts
    import { test as setup } from '@playwright/test';
    
    setup('authenticate', async ({ page }) => {
      await page.goto('/login');
      await page.getByLabel('Email').fill('user@example.com');
      await page.getByLabel('Password').fill('password');
      await page.getByRole('button', { name: 'Sign in' }).click();
    
      // Wait for auth to complete
      await page.waitForURL('/dashboard');
    
      // Save authentication state
      await page.context().storageState({
        path: './playwright/.auth/user.json'
      });
    });
    
    // playwright.config.ts
    export default defineConfig({
      projects: [
        { name: 'setup', testMatch: /.*\.setup\.ts/ },
        {
          name: 'tests',
          dependencies: ['setup'],
          use: {
            storageState: './playwright/.auth/user.json',
          },
        },
      ],
    });
    """
    

---
  #### **Name**
User-Facing Locator Pattern
  #### **Description**
Select elements the way users see them
  #### **When**
Always - the default approach for selectors
  #### **Example**
    # USER-FACING LOCATORS:
    
    """
    Priority order:
    1. getByRole  - Best: matches accessibility tree
    2. getByText  - Good: matches visible content
    3. getByLabel - Good: matches form labels
    4. getByTestId - Fallback: explicit test contracts
    5. CSS/XPath - Last resort: fragile, avoid
    """
    
    ## Good Examples (User-Facing)
    """
    // By role - THE BEST CHOICE
    await page.getByRole('button', { name: 'Submit' }).click();
    await page.getByRole('link', { name: 'Sign up' }).click();
    await page.getByRole('heading', { name: 'Dashboard' }).isVisible();
    await page.getByRole('textbox', { name: 'Search' }).fill('query');
    
    // By text content
    await page.getByText('Welcome back').isVisible();
    await page.getByText(/Order #\d+/).click();  // Regex supported
    
    // By label (forms)
    await page.getByLabel('Email address').fill('user@example.com');
    await page.getByLabel('Password').fill('secret');
    
    // By placeholder
    await page.getByPlaceholder('Search...').fill('query');
    
    // By test ID (when no user-facing option works)
    await page.getByTestId('submit-button').click();
    """
    
    ## Bad Examples (Fragile)
    """
    // DON'T - CSS selectors tied to structure
    await page.locator('.btn-primary.submit-form').click();
    await page.locator('#header > div > button:nth-child(2)').click();
    
    // DON'T - XPath tied to structure
    await page.locator('//div[@class="form"]/button[1]').click();
    
    // DON'T - Auto-generated selectors
    await page.locator('[data-v-12345]').click();
    """
    
    ## Filtering and Chaining
    """
    // Filter by containing text
    await page.getByRole('listitem')
      .filter({ hasText: 'Product A' })
      .getByRole('button', { name: 'Add to cart' })
      .click();
    
    // Filter by NOT containing
    await page.getByRole('listitem')
      .filter({ hasNotText: 'Sold out' })
      .first()
      .click();
    
    // Chain locators
    const row = page.getByRole('row', { name: 'John Doe' });
    await row.getByRole('button', { name: 'Edit' }).click();
    """
    

---
  #### **Name**
Auto-Wait Pattern
  #### **Description**
Let Playwright wait automatically, never add manual waits
  #### **When**
Always with Playwright
  #### **Example**
    # AUTO-WAIT PATTERN:
    
    """
    Playwright waits automatically for:
    - Element to be attached to DOM
    - Element to be visible
    - Element to be stable (not animating)
    - Element to receive events
    - Element to be enabled
    
    NEVER add manual waits!
    """
    
    ## Wrong - Manual Waits
    """
    // DON'T DO THIS
    await page.goto('/dashboard');
    await page.waitForTimeout(2000);  // NO! Arbitrary wait
    await page.click('.submit-button');
    
    // DON'T DO THIS
    await page.waitForSelector('.loading-spinner', { state: 'hidden' });
    await page.waitForTimeout(500);  // "Just to be safe" - NO!
    """
    
    ## Correct - Let Auto-Wait Work
    """
    // Auto-waits for button to be clickable
    await page.getByRole('button', { name: 'Submit' }).click();
    
    // Auto-waits for text to appear
    await expect(page.getByText('Success!')).toBeVisible();
    
    // Auto-waits for navigation to complete
    await page.goto('/dashboard');
    // Page is ready - no manual wait needed
    """
    
    ## When You DO Need to Wait
    """
    // Wait for specific network request
    const responsePromise = page.waitForResponse(
      response => response.url().includes('/api/data')
    );
    await page.getByRole('button', { name: 'Load' }).click();
    const response = await responsePromise;
    
    // Wait for URL change
    await Promise.all([
      page.waitForURL('**/dashboard'),
      page.getByRole('button', { name: 'Login' }).click(),
    ]);
    
    // Wait for download
    const downloadPromise = page.waitForEvent('download');
    await page.getByText('Export CSV').click();
    const download = await downloadPromise;
    """
    

---
  #### **Name**
Stealth Browser Pattern
  #### **Description**
Avoid bot detection for scraping
  #### **When**
Scraping sites with anti-bot protection
  #### **Example**
    # STEALTH BROWSER PATTERN:
    
    """
    Bot detection checks for:
    - navigator.webdriver property
    - Chrome DevTools protocol artifacts
    - Browser fingerprint inconsistencies
    - Behavioral patterns (perfect timing, no mouse movement)
    - Headless indicators
    """
    
    ## Puppeteer Stealth (Best Anti-Detection)
    """
    import puppeteer from 'puppeteer-extra';
    import StealthPlugin from 'puppeteer-extra-plugin-stealth';
    
    puppeteer.use(StealthPlugin());
    
    const browser = await puppeteer.launch({
      headless: 'new',
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-blink-features=AutomationControlled',
      ],
    });
    
    const page = await browser.newPage();
    
    // Set realistic viewport
    await page.setViewport({ width: 1920, height: 1080 });
    
    // Realistic user agent
    await page.setUserAgent(
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
      '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    );
    
    // Navigate with human-like behavior
    await page.goto('https://target-site.com', {
      waitUntil: 'networkidle0',
    });
    """
    
    ## Playwright Stealth
    """
    import { chromium } from 'playwright-extra';
    import stealth from 'puppeteer-extra-plugin-stealth';
    
    chromium.use(stealth());
    
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
      viewport: { width: 1920, height: 1080 },
      userAgent: 'Mozilla/5.0 ...',
      locale: 'en-US',
      timezoneId: 'America/New_York',
    });
    """
    
    ## Human-Like Behavior
    """
    // Random delays between actions
    const randomDelay = (min: number, max: number) =>
      new Promise(r => setTimeout(r, Math.random() * (max - min) + min));
    
    await page.goto(url);
    await randomDelay(500, 1500);
    
    // Mouse movement before click
    const button = await page.$('button.submit');
    const box = await button.boundingBox();
    await page.mouse.move(
      box.x + box.width / 2,
      box.y + box.height / 2,
      { steps: 10 }  // Move in steps like a human
    );
    await randomDelay(100, 300);
    await button.click();
    
    // Scroll naturally
    await page.evaluate(() => {
      window.scrollBy({
        top: 300 + Math.random() * 200,
        behavior: 'smooth'
      });
    });
    """
    

---
  #### **Name**
Error Recovery Pattern
  #### **Description**
Handle failures gracefully with screenshots and retries
  #### **When**
Any production automation
  #### **Example**
    # ERROR RECOVERY PATTERN:
    
    ## Automatic Screenshot on Failure
    """
    // playwright.config.ts
    export default defineConfig({
      use: {
        screenshot: 'only-on-failure',
        trace: 'retain-on-failure',
        video: 'retain-on-failure',
      },
      retries: 2,  // Retry failed tests
    });
    """
    
    ## Try-Catch with Debug Info
    """
    async function scrapeProduct(page: Page, url: string) {
      try {
        await page.goto(url, { timeout: 30000 });
    
        const title = await page.getByRole('heading', { level: 1 }).textContent();
        const price = await page.getByTestId('price').textContent();
    
        return { title, price, success: true };
    
      } catch (error) {
        // Capture debug info
        const screenshot = await page.screenshot({
          path: `errors/${Date.now()}-error.png`,
          fullPage: true
        });
    
        const html = await page.content();
        await fs.writeFile(`errors/${Date.now()}-page.html`, html);
    
        console.error({
          url,
          error: error.message,
          currentUrl: page.url(),
        });
    
        return { success: false, error: error.message };
      }
    }
    """
    
    ## Retry with Exponential Backoff
    """
    async function withRetry<T>(
      fn: () => Promise<T>,
      maxRetries = 3,
      baseDelay = 1000
    ): Promise<T> {
      let lastError: Error;
    
      for (let attempt = 0; attempt < maxRetries; attempt++) {
        try {
          return await fn();
        } catch (error) {
          lastError = error;
    
          if (attempt < maxRetries - 1) {
            const delay = baseDelay * Math.pow(2, attempt);
            const jitter = delay * 0.1 * Math.random();
            await new Promise(r => setTimeout(r, delay + jitter));
          }
        }
      }
    
      throw lastError;
    }
    
    // Usage
    const result = await withRetry(
      () => scrapeProduct(page, url),
      3,
      2000
    );
    """
    

---
  #### **Name**
Parallel Execution Pattern
  #### **Description**
Run tests/tasks in parallel for speed
  #### **When**
Multiple independent pages or tests
  #### **Example**
    # PARALLEL EXECUTION:
    
    ## Playwright Test Parallelization
    """
    // playwright.config.ts
    export default defineConfig({
      fullyParallel: true,
      workers: process.env.CI ? 4 : undefined,  // CI: 4 workers, local: CPU-based
    
      projects: [
        { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
        { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
        { name: 'webkit', use: { ...devices['Desktop Safari'] } },
      ],
    });
    """
    
    ## Browser Contexts for Parallel Scraping
    """
    const browser = await chromium.launch();
    
    const urls = ['url1', 'url2', 'url3', 'url4', 'url5'];
    
    // Create multiple contexts - each is isolated
    const results = await Promise.all(
      urls.map(async (url) => {
        const context = await browser.newContext();
        const page = await context.newPage();
    
        try {
          await page.goto(url);
          const data = await extractData(page);
          return { url, data, success: true };
        } catch (error) {
          return { url, error: error.message, success: false };
        } finally {
          await context.close();
        }
      })
    );
    
    await browser.close();
    """
    
    ## Rate-Limited Parallel Processing
    """
    import pLimit from 'p-limit';
    
    const limit = pLimit(5);  // Max 5 concurrent
    
    const results = await Promise.all(
      urls.map(url => limit(async () => {
        const context = await browser.newContext();
        const page = await context.newPage();
    
        // Random delay between requests
        await new Promise(r => setTimeout(r, Math.random() * 2000));
    
        try {
          return await scrapePage(page, url);
        } finally {
          await context.close();
        }
      }))
    );
    """
    

---
  #### **Name**
Network Interception Pattern
  #### **Description**
Mock, block, or modify network requests
  #### **When**
Testing, blocking ads/analytics, modifying responses
  #### **Example**
    # NETWORK INTERCEPTION:
    
    ## Block Unnecessary Resources
    """
    await page.route('**/*', (route) => {
      const url = route.request().url();
      const resourceType = route.request().resourceType();
    
      // Block images, fonts, analytics for faster scraping
      if (['image', 'font', 'media'].includes(resourceType)) {
        return route.abort();
      }
    
      // Block tracking/analytics
      if (url.includes('google-analytics') ||
          url.includes('facebook.com/tr')) {
        return route.abort();
      }
    
      return route.continue();
    });
    """
    
    ## Mock API Responses (Testing)
    """
    await page.route('**/api/products', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          { id: 1, name: 'Mock Product', price: 99.99 },
        ]),
      });
    });
    
    // Now page will receive mocked data
    await page.goto('/products');
    """
    
    ## Capture API Responses
    """
    const apiResponses: any[] = [];
    
    page.on('response', async (response) => {
      if (response.url().includes('/api/')) {
        const data = await response.json().catch(() => null);
        apiResponses.push({
          url: response.url(),
          status: response.status(),
          data,
        });
      }
    });
    
    await page.goto('/dashboard');
    // apiResponses now contains all API calls
    """
    

## Anti-Patterns


---
  #### **Name**
Arbitrary Timeouts
  #### **Description**
Using waitForTimeout or sleep instead of proper waits
  #### **Why**
    Hard-coded delays are either too short (flaky tests) or too long (slow tests).
    They don't adapt to actual page state. Playwright's auto-wait handles this.
    
  #### **Instead**
    Remove all waitForTimeout calls. Use waitForResponse, waitForURL, or
    assertions that auto-wait like expect(locator).toBeVisible().
    

---
  #### **Name**
CSS/XPath First
  #### **Description**
Reaching for CSS/XPath selectors before user-facing locators
  #### **Why**
    CSS and XPath are tied to DOM structure. When the page layout changes,
    selectors break. User-facing locators are more stable.
    
  #### **Instead**
    Start with getByRole, getByText, getByLabel. Use getByTestId for fallback.
    Only use CSS/XPath when absolutely necessary.
    

---
  #### **Name**
Single Browser Context for Everything
  #### **Description**
Reusing one context across unrelated tests
  #### **Why**
    Shared state causes test pollution. One test's cookies affect another.
    Failures become non-deterministic and hard to debug.
    
  #### **Instead**
    Each test gets fresh context. Share authentication via storageState file,
    not via shared browser context.
    

---
  #### **Name**
Ignoring Trace Files
  #### **Description**
Not enabling traces for debugging
  #### **Why**
    When tests fail in CI, you have no visibility into what happened.
    Screenshots alone don't show timing, network requests, or interactions.
    
  #### **Instead**
    Enable trace: 'retain-on-failure'. View with 'npx playwright show-trace'.
    Traces show timeline, screenshots, network, and console logs.
    

---
  #### **Name**
No Rate Limiting for Scraping
  #### **Description**
Hammering sites with requests as fast as possible
  #### **Why**
    You'll get blocked. You might cause issues for the target site. It's
    rude and potentially illegal depending on jurisdiction.
    
  #### **Instead**
    Add delays between requests. Rotate user agents and proxies.
    Respect robots.txt and rate limits.
    