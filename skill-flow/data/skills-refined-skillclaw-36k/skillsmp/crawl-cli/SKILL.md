---
name: crawl-cli
description: "Use when implementing web scraping, data extraction, or automated browser interactions. Covers Puppeteer, Playwright, rate limiting, and ethical scraping."
---

# Web Crawling & Data Extraction

## Overview

Web crawling and scraping patterns for data extraction using modern browser automation tools. Focus on ethical scraping, rate limiting, error handling, and scalable extraction pipelines.

## When to Use

- Building data extraction pipelines
- Automating browser interactions
- Scraping websites for content or data
- Monitoring web page changes
- Generating screenshots or PDFs

## Quick Reference

| Tool | Best For | Speed | JS Support |
|------|----------|-------|------------|
| **Playwright** | E2E testing + scraping | Fast | Full |
| **Puppeteer** | Chrome-specific automation | Fast | Full |
| **Cheerio** | Static HTML parsing | Fastest | None |
| **Crawlee** | Large-scale crawling | Optimized | Both |

---

## Playwright Setup (Recommended)

### Installation

```bash
npm install playwright
npx playwright install chromium
```

### Basic Scraper

```typescript
// lib/scraper.ts
import { chromium, Browser, Page } from 'playwright';

export class Scraper {
  private browser: Browser | null = null;

  async init(): Promise<void> {
    this.browser = await chromium.launch({
      headless: true,
    });
  }

  async scrape(url: string): Promise<string> {
    if (!this.browser) throw new Error('Browser not initialized');

    const context = await this.browser.newContext({
      userAgent: 'Mozilla/5.0 (compatible; MyBot/1.0; +https://example.com/bot)',
    });
    const page = await context.newPage();

    try {
      await page.goto(url, { waitUntil: 'networkidle' });
      const content = await page.content();
      return content;
    } finally {
      await context.close();
    }
  }

  async close(): Promise<void> {
    if (this.browser) {
      await this.browser.close();
    }
  }
}
```

### Data Extraction Pattern

```typescript
// lib/extractor.ts
import { Page } from 'playwright';

interface ProductData {
  title: string;
  price: string;
  description: string;
  images: string[];
}

export async function extractProduct(page: Page): Promise<ProductData> {
  return await page.evaluate(() => {
    return {
      title: document.querySelector('h1.product-title')?.textContent?.trim() || '',
      price: document.querySelector('.price')?.textContent?.trim() || '',
      description: document.querySelector('.description')?.textContent?.trim() || '',
      images: Array.from(document.querySelectorAll('.product-image img'))
        .map(img => (img as HTMLImageElement).src),
    };
  });
}
```

---

## Rate Limiting

### Essential Rate Limiter

```typescript
// lib/rate-limiter.ts
export class RateLimiter {
  private queue: Array<() => Promise<void>> = [];
  private processing = false;
  private lastRequest = 0;
  private readonly minDelay: number;

  constructor(requestsPerSecond: number = 1) {
    this.minDelay = 1000 / requestsPerSecond;
  }

  async schedule<T>(fn: () => Promise<T>): Promise<T> {
    return new Promise((resolve, reject) => {
      this.queue.push(async () => {
        try {
          const result = await fn();
          resolve(result);
        } catch (error) {
          reject(error);
        }
      });
      this.processQueue();
    });
  }

  private async processQueue(): Promise<void> {
    if (this.processing || this.queue.length === 0) return;

    this.processing = true;

    while (this.queue.length > 0) {
      const now = Date.now();
      const timeSinceLastRequest = now - this.lastRequest;

      if (timeSinceLastRequest < this.minDelay) {
        await this.sleep(this.minDelay - timeSinceLastRequest);
      }

      const task = this.queue.shift();
      if (task) {
        this.lastRequest = Date.now();
        await task();
      }
    }

    this.processing = false;
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Usage
const limiter = new RateLimiter(2); // 2 requests per second
await limiter.schedule(() => scraper.scrape(url));
```

### Adaptive Rate Limiting

```typescript
// lib/adaptive-rate-limiter.ts
export class AdaptiveRateLimiter {
  private delay: number;
  private readonly minDelay: number;
  private readonly maxDelay: number;
  private consecutiveErrors = 0;

  constructor(options: {
    initialDelay?: number;
    minDelay?: number;
    maxDelay?: number;
  } = {}) {
    this.delay = options.initialDelay || 1000;
    this.minDelay = options.minDelay || 500;
    this.maxDelay = options.maxDelay || 30000;
  }

  async wait(): Promise<void> {
    await new Promise(resolve => setTimeout(resolve, this.delay));
  }

  onSuccess(): void {
    this.consecutiveErrors = 0;
    // Gradually decrease delay on success
    this.delay = Math.max(this.minDelay, this.delay * 0.9);
  }

  onError(statusCode?: number): void {
    this.consecutiveErrors++;

    if (statusCode === 429) {
      // Rate limited - significant backoff
      this.delay = Math.min(this.maxDelay, this.delay * 3);
    } else {
      // Other error - moderate backoff
      this.delay = Math.min(this.maxDelay, this.delay * 1.5);
    }
  }

  shouldAbort(): boolean {
    return this.consecutiveErrors > 10;
  }
}
```

---

## Error Handling

### Retry Strategy

```typescript
// lib/retry.ts
interface RetryOptions {
  maxRetries: number;
  baseDelay: number;
  maxDelay: number;
  retryOn?: number[];
}

export async function withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions
): Promise<T> {
  const { maxRetries, baseDelay, maxDelay, retryOn = [429, 500, 502, 503, 504] } = options;

  let lastError: Error | null = null;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      // Check if we should retry
      const statusCode = (error as any).statusCode;
      if (statusCode && !retryOn.includes(statusCode)) {
        throw error;
      }

      if (attempt < maxRetries) {
        // Exponential backoff with jitter
        const delay = Math.min(
          maxDelay,
          baseDelay * Math.pow(2, attempt) + Math.random() * 1000
        );
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError;
}

// Usage
const result = await withRetry(
  () => scraper.scrape(url),
  { maxRetries: 3, baseDelay: 1000, maxDelay: 30000 }
);
```

### Error Classification

```typescript
// lib/errors.ts
export class ScraperError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly recoverable: boolean,
    public readonly url?: string
  ) {
    super(message);
    this.name = 'ScraperError';
  }
}

export const ErrorCodes = {
  BLOCKED: 'BLOCKED',
  RATE_LIMITED: 'RATE_LIMITED',
  NOT_FOUND: 'NOT_FOUND',
  TIMEOUT: 'TIMEOUT',
  PARSE_ERROR: 'PARSE_ERROR',
  NETWORK_ERROR: 'NETWORK_ERROR',
} as const;

export function classifyError(error: Error, statusCode?: number): ScraperError {
  if (statusCode === 403) {
    return new ScraperError('Access blocked', ErrorCodes.BLOCKED, false);
  }
  if (statusCode === 429) {
    return new ScraperError('Rate limited', ErrorCodes.RATE_LIMITED, true);
  }
  if (statusCode === 404) {
    return new ScraperError('Page not found', ErrorCodes.NOT_FOUND, false);
  }
  if (error.message.includes('timeout')) {
    return new ScraperError('Request timeout', ErrorCodes.TIMEOUT, true);
  }
  return new ScraperError(error.message, ErrorCodes.NETWORK_ERROR, true);
}
```

---

## Complete Crawler Implementation

```typescript
// lib/crawler.ts
import { chromium, Browser, BrowserContext, Page } from 'playwright';

interface CrawlerOptions {
  maxConcurrency: number;
  requestsPerSecond: number;
  maxDepth: number;
  respectRobotsTxt: boolean;
}

interface CrawlResult {
  url: string;
  status: 'success' | 'error';
  data?: any;
  error?: string;
  timestamp: Date;
}

export class Crawler {
  private browser: Browser | null = null;
  private visited = new Set<string>();
  private queue: Array<{ url: string; depth: number }> = [];
  private results: CrawlResult[] = [];
  private readonly options: CrawlerOptions;
  private rateLimiter: RateLimiter;

  constructor(options: Partial<CrawlerOptions> = {}) {
    this.options = {
      maxConcurrency: 3,
      requestsPerSecond: 1,
      maxDepth: 3,
      respectRobotsTxt: true,
      ...options,
    };
    this.rateLimiter = new RateLimiter(this.options.requestsPerSecond);
  }

  async crawl(startUrl: string, extractor: (page: Page) => Promise<any>): Promise<CrawlResult[]> {
    this.browser = await chromium.launch({ headless: true });
    this.queue.push({ url: startUrl, depth: 0 });

    try {
      while (this.queue.length > 0) {
        const batch = this.queue.splice(0, this.options.maxConcurrency);
        await Promise.all(
          batch.map(item => this.processUrl(item.url, item.depth, extractor))
        );
      }
    } finally {
      await this.browser?.close();
    }

    return this.results;
  }

  private async processUrl(
    url: string,
    depth: number,
    extractor: (page: Page) => Promise<any>
  ): Promise<void> {
    if (this.visited.has(url)) return;
    this.visited.add(url);

    await this.rateLimiter.schedule(async () => {
      const context = await this.browser!.newContext();
      const page = await context.newPage();

      try {
        const response = await page.goto(url, {
          waitUntil: 'networkidle',
          timeout: 30000
        });

        if (!response || !response.ok()) {
          this.results.push({
            url,
            status: 'error',
            error: `HTTP ${response?.status()}`,
            timestamp: new Date(),
          });
          return;
        }

        const data = await extractor(page);
        this.results.push({
          url,
          status: 'success',
          data,
          timestamp: new Date(),
        });

        // Discover new links if not at max depth
        if (depth < this.options.maxDepth) {
          const links = await this.extractLinks(page);
          links.forEach(link => {
            if (!this.visited.has(link)) {
              this.queue.push({ url: link, depth: depth + 1 });
            }
          });
        }
      } catch (error) {
        this.results.push({
          url,
          status: 'error',
          error: (error as Error).message,
          timestamp: new Date(),
        });
      } finally {
        await context.close();
      }
    });
  }

  private async extractLinks(page: Page): Promise<string[]> {
    return page.evaluate(() => {
      const baseUrl = window.location.origin;
      return Array.from(document.querySelectorAll('a[href]'))
        .map(a => (a as HTMLAnchorElement).href)
        .filter(href => href.startsWith(baseUrl));
    });
  }
}
```

---

## Ethical Scraping

### robots.txt Parser

```typescript
// lib/robots.ts
interface RobotsRule {
  userAgent: string;
  allow: string[];
  disallow: string[];
  crawlDelay?: number;
}

export async function parseRobotsTxt(baseUrl: string): Promise<RobotsRule[]> {
  try {
    const response = await fetch(`${baseUrl}/robots.txt`);
    if (!response.ok) return [];

    const text = await response.text();
    const rules: RobotsRule[] = [];
    let currentRule: RobotsRule | null = null;

    for (const line of text.split('\n')) {
      const trimmed = line.trim();
      if (trimmed.startsWith('#') || !trimmed) continue;

      const [key, ...valueParts] = trimmed.split(':');
      const value = valueParts.join(':').trim();

      switch (key.toLowerCase()) {
        case 'user-agent':
          if (currentRule) rules.push(currentRule);
          currentRule = { userAgent: value, allow: [], disallow: [] };
          break;
        case 'allow':
          currentRule?.allow.push(value);
          break;
        case 'disallow':
          currentRule?.disallow.push(value);
          break;
        case 'crawl-delay':
          if (currentRule) currentRule.crawlDelay = parseInt(value, 10);
          break;
      }
    }

    if (currentRule) rules.push(currentRule);
    return rules;
  } catch {
    return [];
  }
}

export function isAllowed(url: string, rules: RobotsRule[], userAgent: string): boolean {
  const path = new URL(url).pathname;
  const applicableRules = rules.filter(
    r => r.userAgent === '*' || r.userAgent.toLowerCase() === userAgent.toLowerCase()
  );

  for (const rule of applicableRules) {
    for (const disallow of rule.disallow) {
      if (path.startsWith(disallow)) {
        // Check if explicitly allowed
        for (const allow of rule.allow) {
          if (path.startsWith(allow)) return true;
        }
        return false;
      }
    }
  }

  return true;
}
```

### Best Practices Checklist

```markdown
## Ethical Scraping Checklist

- [ ] Check robots.txt before scraping
- [ ] Implement rate limiting (1-2 requests/second max)
- [ ] Use descriptive User-Agent with contact info
- [ ] Handle rate limits gracefully (429 responses)
- [ ] Cache responses to avoid redundant requests
- [ ] Respect nofollow and noindex directives
- [ ] Scrape during off-peak hours when possible
- [ ] Don't scrape personal data without consent
- [ ] Review website Terms of Service
- [ ] Implement request timeouts
```

---

## Common Patterns

### Screenshot Capture

```typescript
async function captureScreenshot(
  url: string,
  options: { fullPage?: boolean; format?: 'png' | 'jpeg' } = {}
): Promise<Buffer> {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.setViewportSize({ width: 1280, height: 720 });
  await page.goto(url, { waitUntil: 'networkidle' });

  const screenshot = await page.screenshot({
    fullPage: options.fullPage ?? false,
    type: options.format ?? 'png',
  });

  await browser.close();
  return screenshot;
}
```

### PDF Generation

```typescript
async function generatePDF(url: string): Promise<Buffer> {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto(url, { waitUntil: 'networkidle' });

  const pdf = await page.pdf({
    format: 'A4',
    printBackground: true,
    margin: { top: '1cm', bottom: '1cm', left: '1cm', right: '1cm' },
  });

  await browser.close();
  return pdf;
}
```

### Handling Dynamic Content

```typescript
async function waitForContent(page: Page, selector: string): Promise<void> {
  // Wait for specific element
  await page.waitForSelector(selector, { timeout: 10000 });

  // Or wait for network to be idle
  await page.waitForLoadState('networkidle');

  // Or wait for specific request
  await page.waitForResponse(
    response => response.url().includes('/api/data')
  );
}
```

---

## Red Flags - STOP

**Never:**
- Scrape without rate limiting
- Ignore robots.txt
- Scrape login-protected content without authorization
- Store scraped personal data without consent
- Overwhelm servers with concurrent requests
- Bypass anti-bot measures for malicious purposes

**Always:**
- Check Terms of Service
- Implement exponential backoff
- Use descriptive User-Agent
- Cache results to reduce requests
- Handle errors gracefully
- Document your scraping activity

---

## Integration

**Related skills:** api-design, database-patterns, testing-patterns
**Tools:** Playwright, Puppeteer, Cheerio, Crawlee
