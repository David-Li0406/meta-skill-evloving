# Browser Automation - Sharp Edges

## Using waitForTimeout Instead of Proper Waits

### **Id**
manual-timeout-flakiness
### **Severity**
critical
### **Situation**
Waiting for elements or page state
### **Symptom**
  Tests pass locally, fail in CI. Pass 9 times, fail on the 10th.
  "Element not found" errors that seem random. Tests take 30+ seconds
  when they should take 3.
  
### **Why**
  waitForTimeout is a fixed delay. If the page loads in 500ms, you wait
  2000ms anyway. If the page takes 2100ms (CI is slower), you fail.
  There's no correct value - it's always either too short or too long.
  
### **Solution**
  # REMOVE all waitForTimeout calls
  
  # WRONG:
  await page.goto('/dashboard');
  await page.waitForTimeout(2000);  # Arbitrary!
  await page.click('.submit');
  
  # CORRECT - Auto-wait handles it:
  await page.goto('/dashboard');
  await page.getByRole('button', { name: 'Submit' }).click();
  
  # If you need to wait for specific condition:
  await expect(page.getByText('Dashboard')).toBeVisible();
  await page.waitForURL('**/dashboard');
  await page.waitForResponse(resp => resp.url().includes('/api/data'));
  
  # For animations, wait for element to be stable:
  await page.getByRole('button').click();  # Auto-waits for stable
  
  # NEVER use setTimeout or waitForTimeout in production code
  
### **Detection Pattern**
  - waitForTimeout
  - setTimeout
  - sleep

## CSS Selectors Tied to Styling Classes

### **Id**
fragile-css-selectors
### **Severity**
high
### **Situation**
Selecting elements for interaction
### **Symptom**
  Tests break after CSS refactoring. Selectors like .btn-primary stop
  working. Frontend redesign breaks all tests without changing behavior.
  
### **Why**
  CSS class names are implementation details for styling, not semantic
  meaning. When designers change from .btn-primary to .button--primary,
  your tests break even though behavior is identical.
  
### **Solution**
  # Use user-facing locators instead:
  
  # WRONG - Tied to CSS:
  await page.locator('.btn-primary.submit-form').click();
  await page.locator('#sidebar > div.menu > ul > li:nth-child(3)').click();
  
  # CORRECT - User-facing:
  await page.getByRole('button', { name: 'Submit' }).click();
  await page.getByRole('menuitem', { name: 'Settings' }).click();
  
  # If you must use CSS, use data-testid:
  <button data-testid="submit-order">Submit</button>
  
  await page.getByTestId('submit-order').click();
  
  # Locator priority:
  # 1. getByRole - matches accessibility
  # 2. getByText - matches visible content
  # 3. getByLabel - matches form labels
  # 4. getByTestId - explicit test contract
  # 5. CSS/XPath - last resort only
  
### **Detection Pattern**
  - locator.*\.
  - querySelector
  - \$\(

## navigator.webdriver Exposes Automation

### **Id**
navigator-webdriver-detection
### **Severity**
high
### **Situation**
Scraping sites with bot detection
### **Symptom**
  Immediate 403 errors. CAPTCHA challenges. Empty pages. "Access Denied"
  messages. Works for 1 request, then gets blocked.
  
### **Why**
  By default, headless browsers set navigator.webdriver = true. This is
  the first thing bot detection checks. It's a bright red flag that
  says "I'm automated."
  
### **Solution**
  # Use stealth plugins:
  
  ## Puppeteer Stealth (best option):
  import puppeteer from 'puppeteer-extra';
  import StealthPlugin from 'puppeteer-extra-plugin-stealth';
  
  puppeteer.use(StealthPlugin());
  
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--disable-blink-features=AutomationControlled'],
  });
  
  ## Playwright Stealth:
  import { chromium } from 'playwright-extra';
  import stealth from 'puppeteer-extra-plugin-stealth';
  
  chromium.use(stealth());
  
  ## Manual (partial):
  await page.evaluateOnNewDocument(() => {
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined,
    });
  });
  
  # Note: This is cat-and-mouse. Detection evolves.
  # For serious scraping, consider managed solutions like Browserbase.
  
### **Detection Pattern**
  - puppeteer.launch
  - chromium.launch
  - headless

## Tests Share State and Affect Each Other

### **Id**
test-pollution
### **Severity**
high
### **Situation**
Running multiple tests in sequence
### **Symptom**
  Tests pass individually but fail when run together. Order matters -
  test B fails if test A runs first. Random failures that "fix themselves"
  on rerun.
  
### **Why**
  Shared browser context means shared cookies, localStorage, and session
  state. Test A logs in, test B expects logged-out state. Test A adds
  item to cart, test B's cart count is wrong.
  
### **Solution**
  # Each test must be fully isolated:
  
  ## Playwright Test (automatic isolation):
  test('first test', async ({ page }) => {
    // Fresh context, fresh page
  });
  
  test('second test', async ({ page }) => {
    // Completely isolated from first test
  });
  
  ## Manual isolation:
  const context = await browser.newContext();  // Fresh context
  const page = await context.newPage();
  // ... test code ...
  await context.close();  // Clean up
  
  ## Shared authentication (the right way):
  // 1. Save auth state to file
  await context.storageState({ path: './auth.json' });
  
  // 2. Reuse in other tests
  const context = await browser.newContext({
    storageState: './auth.json'
  });
  
  # Never modify global state in tests
  # Never rely on previous test's actions
  
### **Detection Pattern**
  - browser.newPage
  - beforeAll.*login
  - global

## No Trace Capture for CI Failures

### **Id**
missing-traces-in-ci
### **Severity**
medium
### **Situation**
Debugging test failures in CI
### **Symptom**
  "Test failed in CI" with no useful information. Can't reproduce
  locally. Screenshot shows page but not what went wrong. Guessing
  at root cause.
  
### **Why**
  CI runs headless on different hardware. Timing is different. Network
  is different. Without traces, you can't see what actually happened -
  the sequence of actions, network requests, console logs.
  
### **Solution**
  # Enable traces for failures:
  
  ## playwright.config.ts:
  export default defineConfig({
    use: {
      trace: 'retain-on-failure',    # Keep trace on failure
      screenshot: 'only-on-failure', # Screenshot on failure
      video: 'retain-on-failure',    # Video on failure
    },
    outputDir: './test-results',
  });
  
  ## View trace locally:
  npx playwright show-trace test-results/path/to/trace.zip
  
  ## In CI, upload test-results as artifact:
  # GitHub Actions:
  - uses: actions/upload-artifact@v3
    if: failure()
    with:
      name: playwright-traces
      path: test-results/
  
  # Trace shows:
  # - Timeline of actions
  # - Screenshots at each step
  # - Network requests and responses
  # - Console logs
  # - DOM snapshots
  
### **Detection Pattern**
  - playwright.config
  - defineConfig

## Tests Pass Headed but Fail Headless

### **Id**
headless-vs-headed-differences
### **Severity**
medium
### **Situation**
Running tests in headless mode for CI
### **Symptom**
  Works perfectly when you watch it. Fails mysteriously in CI.
  "Element not visible" in headless but visible in headed mode.
  
### **Why**
  Headless browsers have no display, which affects some CSS (visibility
  calculations), viewport sizing, and font rendering. Some animations
  behave differently. Popup windows may not work.
  
### **Solution**
  # Set consistent viewport:
  const browser = await chromium.launch({
    headless: true,
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
  });
  
  # Or in config:
  export default defineConfig({
    use: {
      viewport: { width: 1280, height: 720 },
    },
  });
  
  # Debug headless failures:
  # 1. Run with headed mode locally
  npx playwright test --headed
  
  # 2. Slow down to watch
  npx playwright test --headed --slowmo 100
  
  # 3. Use trace viewer for CI failures
  npx playwright show-trace trace.zip
  
  # 4. For stubborn issues, screenshot at failure point:
  await page.screenshot({ path: 'debug.png', fullPage: true });
  
### **Detection Pattern**
  - headless.*true
  - launch

## Getting Blocked by Rate Limiting

### **Id**
rate-limiting-blocks
### **Severity**
high
### **Situation**
Scraping multiple pages quickly
### **Symptom**
  Works for first 50 pages, then 429 errors. Suddenly all requests fail.
  IP gets blocked. CAPTCHA starts appearing after successful requests.
  
### **Why**
  Sites monitor request patterns. 100 requests per second from one IP
  is obviously automated. Rate limits protect servers and catch scrapers.
  
### **Solution**
  # Add delays between requests:
  
  const randomDelay = () =>
    new Promise(r => setTimeout(r, 1000 + Math.random() * 2000));
  
  for (const url of urls) {
    await randomDelay();  // 1-3 second delay
    await page.goto(url);
    // ... scrape ...
  }
  
  # Use rotating proxies:
  const proxies = ['http://proxy1:8080', 'http://proxy2:8080'];
  let proxyIndex = 0;
  
  const getNextProxy = () => proxies[proxyIndex++ % proxies.length];
  
  const context = await browser.newContext({
    proxy: { server: getNextProxy() },
  });
  
  # Limit concurrent requests:
  import pLimit from 'p-limit';
  const limit = pLimit(3);  // Max 3 concurrent
  
  await Promise.all(
    urls.map(url => limit(() => scrapePage(url)))
  );
  
  # Rotate user agents:
  const userAgents = [
    'Mozilla/5.0 (Windows...',
    'Mozilla/5.0 (Macintosh...',
  ];
  
  await page.setExtraHTTPHeaders({
    'User-Agent': userAgents[Math.floor(Math.random() * userAgents.length)]
  });
  
### **Detection Pattern**
  - for.*goto
  - Promise.all.*goto
  - scrape

## New Windows/Popups Not Handled

### **Id**
popup-handling-failure
### **Severity**
medium
### **Situation**
Clicking links that open new windows
### **Symptom**
  Click button, nothing happens. Test hangs. "Window not found" errors.
  Actions succeed but verification fails because you're on wrong page.
  
### **Why**
  target="_blank" links open new windows. Your page reference still
  points to the original page. The new window exists but you're not
  listening for it.
  
### **Solution**
  # Wait for popup BEFORE triggering it:
  
  ## New window/tab:
  const pagePromise = context.waitForEvent('page');
  await page.getByRole('link', { name: 'Open in new tab' }).click();
  const newPage = await pagePromise;
  await newPage.waitForLoadState();
  
  // Now interact with new page
  await expect(newPage.getByRole('heading')).toBeVisible();
  
  // Close when done
  await newPage.close();
  
  ## Popup windows:
  const popupPromise = page.waitForEvent('popup');
  await page.getByRole('button', { name: 'Open popup' }).click();
  const popup = await popupPromise;
  await popup.waitForLoadState();
  
  ## Multiple windows:
  const pages = context.pages();  // Get all open pages
  
### **Detection Pattern**
  - target=.*_blank
  - window.open
  - popup

## Can't Interact with Elements in iframes

### **Id**
iframe-not-accessible
### **Severity**
medium
### **Situation**
Page contains embedded iframes
### **Symptom**
  Element clearly visible but "not found". Selector works in DevTools
  but not in Playwright. Parent page selectors work, iframe content
  doesn't.
  
### **Why**
  iframes are separate documents. page.locator only searches the main
  frame. You need to explicitly get the iframe's frame to interact
  with its contents.
  
### **Solution**
  # Get frame by name or selector:
  
  ## By frame name:
  const frame = page.frame('payment-iframe');
  await frame.getByRole('textbox', { name: 'Card number' }).fill('4242...');
  
  ## By selector:
  const frame = page.frameLocator('iframe#payment');
  await frame.getByRole('textbox', { name: 'Card number' }).fill('4242...');
  
  ## Nested iframes:
  const outer = page.frameLocator('iframe#outer');
  const inner = outer.frameLocator('iframe#inner');
  await inner.getByRole('button').click();
  
  ## Wait for iframe to load:
  await page.waitForSelector('iframe#payment');
  const frame = page.frameLocator('iframe#payment');
  await frame.getByText('Secure Payment').waitFor();
  
### **Detection Pattern**
  - iframe
  - frame
  - embed