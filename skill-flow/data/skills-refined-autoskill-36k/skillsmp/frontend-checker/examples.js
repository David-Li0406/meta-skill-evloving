/**
 * Frontend Health Checker Examples
 *
 * Collection of Puppeteer scripts for checking frontend health
 */

// ============================================
// Example 1: Basic Health Check (No Auth)
// ============================================

const basicHealthCheck = `
const puppeteer = require('puppeteer');

const PAGES = [
  { path: '/', name: 'Home' },
  { path: '/login', name: 'Login' },
  { path: '/register', name: 'Register' },
  { path: '/blog', name: 'Blog' }
];

async function checkPage(page, path, name) {
  const errors = [];
  const warnings = [];

  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
    if (msg.type() === 'warning') warnings.push(msg.text());
  });

  try {
    await page.goto(\`http://localhost:3000\${path}\`, { waitUntil: 'networkidle2' });
    return { page: name, status: 'OK', errors, warnings };
  } catch (err) {
    return { page: name, status: 'FAILED', error: err.message };
  }
}

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();

  const results = [];
  for (const { path, name } of PAGES) {
    results.push(await checkPage(page, path, name));
  }

  console.table(results);
  await browser.close();
})();
`;

// ============================================
// Example 2: Health Check with Auth
// ============================================

const authHealthCheck = `
const puppeteer = require('puppeteer');

async function login(page, email, password) {
  await page.goto('http://localhost:3000/login');
  await page.waitForSelector('input[name="email"]');

  await page.type('input[name="email"]', email);
  await page.type('input[name="password"]', password);
  await page.click('button[type="submit"]');

  await page.waitForNavigation({ waitUntil: 'networkidle2' });
  return page;
}

const PROTECTED_PAGES = [
  '/dashboard',
  '/dashboard/stats',
  '/dashboard/posts',
  '/dashboard/settings'
];

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();

  // Login first
  await login(page, 'admin@example.com', 'password');

  // Check protected pages
  for (const path of PROTECTED_PAGES) {
    const errors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') errors.push(msg.text());
    });

    await page.goto(\`http://localhost:3000\${path}\`);
    console.log(\`\${path}: \${errors.length} errors\`);
  }

  await browser.close();
})();
`;

// ============================================
// Example 3: Network Failure Detection
// ============================================

const networkFailureCheck = `
const puppeteer = require('puppeteer');

async function checkNetworkFailures(url) {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();

  const failedRequests = [];

  page.on('response', response => {
    if (response.status() >= 400) {
      failedRequests.push({
        url: response.url(),
        status: response.status(),
        method: response.request().method()
      });
    }
  });

  await page.goto(url, { waitUntil: 'networkidle2' });

  if (failedRequests.length > 0) {
    console.log('Network failures found:');
    console.table(failedRequests);
  } else {
    console.log('No network failures detected.');
  }

  await browser.close();
  return failedRequests;
}

// Usage
checkNetworkFailures('http://localhost:3000/dashboard');
`;

// ============================================
// Example 4: Broken Link Checker
// ============================================

const brokenLinkCheck = `
const puppeteer = require('puppeteer');

async function findBrokenLinks(url) {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();

  await page.goto(url, { waitUntil: 'networkidle2' });

  const links = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('a'))
      .map(a => ({
        href: a.href,
        text: a.textContent.trim().substring(0, 50)
      }))
      .filter(link => link.href && !link.href.startsWith('javascript:'));
  });

  const brokenLinks = [];

  for (const link of links) {
    try {
      const response = await page.goto(link.href, { waitUntil: 'domloaded' });
      if (response && response.status() >= 400) {
        brokenLinks.push({ ...link, status: response.status() });
      }
    } catch (err) {
      brokenLinks.push({ ...link, status: 'FAILED', error: err.message });
    }
  }

  console.log(\`Checked \${links.length} links, found \${brokenLinks.length} broken\`);
  if (brokenLinks.length > 0) {
    console.table(brokenLinks);
  }

  await browser.close();
  return brokenLinks;
}

findBrokenLinks('http://localhost:3000');
`;

// ============================================
// Example 5: Screenshot on Error
// ============================================

const screenshotOnError = `
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function checkWithScreenshots(url) {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();

  const errors = [];

  page.on('console', msg => {
    if (msg.type() === 'error') {
      errors.push(msg.text());
    }
  });

  await page.goto(url, { waitUntil: 'networkidle2' });

  if (errors.length > 0) {
    const timestamp = Date.now();
    const filename = \`error-\${timestamp}.png\`;
    await page.screenshot({ path: filename, fullPage: true });
    console.log(\`Errors found. Screenshot saved: \${filename}\`);
    console.log('Errors:', errors);
  } else {
    console.log('No errors detected.');
  }

  await browser.close();
}

checkWithScreenshots('http://localhost:3000/dashboard');
`;

// ============================================
// Example 6: Full Health Check Report
// ============================================

const fullHealthReport = `
const puppeteer = require('puppeteer');
const fs = require('fs');

const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';
const AUTH = {
  email: process.env.TEST_EMAIL || 'admin@example.com',
  password: process.env.TEST_PASSWORD || 'password'
};

const PAGES = {
  public: [
    { path: '/', name: 'Home' },
    { path: '/login', name: 'Login' },
    { path: '/register', name: 'Register' },
    { path: '/blog', name: 'Blog' }
  ],
  protected: [
    { path: '/dashboard', name: 'Dashboard' },
    { path: '/dashboard/stats', name: 'Statistics' },
    { path: '/dashboard/posts', name: 'Posts Manager' },
    { path: '/dashboard/users-manager', name: 'Users Manager' },
    { path: '/dashboard/settings', name: 'Settings' }
  ]
};

async function login(page) {
  await page.goto(\`\${BASE_URL}/login\`);
  await page.waitForSelector('input[name="email"]');

  await page.type('input[name="email"]', AUTH.email);
  await page.type('input[name="password"]', AUTH.password);
  await page.click('button[type="submit"]');

  await page.waitForNavigation({ waitUntil: 'networkidle2' });
}

async function checkPage(page, path, name) {
  const errors = [];
  const warnings = [];
  const networkErrors = [];

  page.on('console', msg => {
    const text = msg.text();
    if (msg.type() === 'error') errors.push(text);
    if (msg.type() === 'warning') warnings.push(text);
  });

  page.on('response', response => {
    if (response.status() >= 400) {
      networkErrors.push({
        url: response.url(),
        status: response.status()
      });
    }
  });

  const startTime = Date.now();

  try {
    await page.goto(\`\${BASE_URL}\${path}\`, { waitUntil: 'networkidle2', timeout: 30000 });
    const loadTime = Date.now() - startTime;

    return {
      page: name,
      path,
      status: 'OK',
      loadTime,
      errors,
      warnings,
      networkErrors
    };
  } catch (err) {
    return {
      page: name,
      path,
      status: 'FAILED',
      error: err.message,
      loadTime: Date.now() - startTime
    };
  }
}

async function generateReport() {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  const results = { public: [], protected: [], summary: {} };

  // Check public pages
  for (const { path, name } of PAGES.public) {
    results.public.push(await checkPage(page, path, name));
  }

  // Login and check protected pages
  await login(page);
  for (const { path, name } of PAGES.protected) {
    results.protected.push(await checkPage(page, path, name));
  }

  await browser.close();

  // Generate summary
  const allResults = [...results.public, ...results.protected];
  results.summary = {
    total: allResults.length,
    passed: allResults.filter(r => r.status === 'OK').length,
    failed: allResults.filter(r => r.status === 'FAILED').length,
    withErrors: allResults.filter(r => r.errors?.length > 0).length,
    withNetworkErrors: allResults.filter(r => r.networkErrors?.length > 0).length,
    avgLoadTime: Math.round(allResults.reduce((sum, r) => sum + (r.loadTime || 0), 0) / allResults.length)
  };

  // Save report
  const reportPath = 'health-report.json';
  fs.writeFileSync(reportPath, JSON.stringify(results, null, 2));

  console.log('\\n=== FRONTEND HEALTH CHECK REPORT ===\\n');
  console.log(\`Total: \${results.summary.total}\`);
  console.log(\`Passed: \${results.summary.passed}\`);
  console.log(\`Failed: \${results.summary.failed}\`);
  console.log(\`With Errors: \${results.summary.withErrors}\`);
  console.log(\`With Network Errors: \${results.summary.withNetworkErrors}\`);
  console.log(\`Avg Load Time: \${results.summary.avgLoadTime}ms\`);
  console.log(\`\\nReport saved: \${reportPath}\`);

  return results;
}

generateReport();
`;

// Export for module usage
module.exports = {
  basicHealthCheck,
  authHealthCheck,
  networkFailureCheck,
  brokenLinkCheck,
  screenshotOnError,
  fullHealthReport
};

console.log(`
╔════════════════════════════════════════════════════════════╗
║         Frontend Health Checker - Examples                  ║
╠════════════════════════════════════════════════════════════╣
║
║  1. Basic Health Check      → No auth required
║  2. Auth Health Check       → With login flow
║  3. Network Failure Check   → Detect 4xx/5xx responses
║  4. Broken Link Check       → Find broken links
║  5. Screenshot on Error     → Capture errors visually
║  6. Full Health Report      → Complete JSON report
║
╚════════════════════════════════════════════════════════════╝

Usage:
  1. Copy the example code to a new .js file
  2. Configure BASE_URL if needed
  3. Run: node <filename>.js
`);
