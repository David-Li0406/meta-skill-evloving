---
name: browser-automation
description: Use this skill to automate browser tasks such as web scraping, navigation, and interaction with web pages using Puppeteer.
---

# Browser Automation with Puppeteer

This skill provides expert guidance for automating browser tasks using Puppeteer, including web scraping, navigation, and interaction with web pages.

## Core Expertise
- Puppeteer API and browser automation patterns
- Page navigation and interaction
- Element selection and manipulation
- Screenshot and PDF generation
- Network request interception
- Headless and headful browser modes
- Performance optimization and memory management
- Integration with testing frameworks (Jest, Mocha)

## Key Features
- Cross-platform Chrome detection and customizable launch options.
- Support for executing JavaScript in the context of web pages.
- Interactive element picker for selecting DOM elements visually.
- Robust error handling and waiting strategies for dynamic content.

## Project Setup

1. Ensure [Node.js](https://nodejs.org/) version 18 or higher is installed.
2. Install Puppeteer in your project directory:

   ```bash
   npm init -y
   npm install puppeteer
   ```

3. Make sure Google Chrome is installed on your machine. If not in a standard location, specify its path via the `CHROME_PATH` environment variable.

## Basic Structure

```javascript
const puppeteer = require('puppeteer');

async function main() {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();
    await page.goto('<url>', { waitUntil: 'networkidle2' });
    // Your automation code here
  } finally {
    await browser.close();
  }
}

main().catch(console.error);
```

## Page Navigation

```javascript
await page.goto('<url>', { waitUntil: 'networkidle2' });
await page.goBack();
await page.goForward();
await page.reload({ waitUntil: 'networkidle2' });
```

## Element Selection

### Query Selectors

```javascript
const element = await page.$('<selector>');
const elements = await page.$$('selector');
const text = await page.$eval('<selector>', el => el.textContent);
```

### Page Interactions

```javascript
await page.click('<selector>');
await page.type('<selector>', '<text>', { delay: 50 });
```

## Screenshots and PDFs

### Screenshots

```javascript
await page.screenshot({ path: '<path>', fullPage: true });
```

### PDF Generation

```javascript
await page.pdf({ path: '<path>', format: 'A4', printBackground: true });
```

## Network Interception

```javascript
await page.setRequestInterception(true);
page.on('request', request => {
  if (['image', 'stylesheet'].includes(request.resourceType())) {
    request.abort();
  } else {
    request.continue();
  }
});
```

## Error Handling

```javascript
async function scrapeWithRetry(url, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const browser = await puppeteer.launch();
      const page = await browser.newPage();
      await page.goto(url, { waitUntil: 'networkidle2' });
      const data = await page.$eval('.content', el => el.textContent);
      await browser.close();
      return data;
    } catch (error) {
      console.error(`Attempt ${i + 1} failed:`, error.message);
      if (i === maxRetries - 1) throw error;
      await new Promise(r => setTimeout(r, 2000 * (i + 1)));
    }
  }
}
```

## Best Practices

1. Always close browser instances in finally blocks.
2. Use `waitForSelector` before interacting with elements.
3. Implement proper error handling and retries.
4. Monitor memory usage in long-running scripts.

## Key Dependencies

- puppeteer
- puppeteer-core (for custom Chrome installations)
- puppeteer-cluster (for parallel scraping)
- puppeteer-extra (for plugins)