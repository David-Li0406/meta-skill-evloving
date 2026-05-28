#!/usr/bin/env node

/*
 * Navigate to a URL using an existing Chrome session controlled by Puppeteer.
 *
 * This script connects to the browser started via start.js on the configured port (default 9222),
 * chooses the last active page or opens a new one if requested, and navigates to the specified URL.
 * It supports waiting for different load events so that scraping or automation can begin at the right time.
 */

import puppeteer from 'puppeteer-core';

function printUsage() {
  console.log('Usage: nav.js <url> [options]');
  console.log('\nOptions:');
  console.log('  --new            Open the URL in a new tab instead of the current tab');
  console.log('  --wait <event>   Wait condition: load|domcontentloaded|networkidle0|networkidle2 (default domcontentloaded)');
  console.log('\nExamples:');
  console.log('  nav.js https://example.com       # Navigate current tab');
  console.log('  nav.js https://example.com --new # Open in new tab');
}

const argv = process.argv.slice(2);
if (argv.length < 1) {
  printUsage();
  process.exit(1);
}

let url = argv[0];
let newTab = false;
let waitUntil = 'domcontentloaded';

for (let i = 1; i < argv.length; i++) {
  const arg = argv[i];
  switch (arg) {
    case '--new':
      newTab = true;
      break;
    case '--wait':
      if (!argv[i + 1]) {
        console.error('✗ --wait requires a value');
        printUsage();
        process.exit(1);
      }
      waitUntil = argv[i + 1];
      i++;
      break;
    case '--help':
    case '-h':
      printUsage();
      process.exit(0);
    default:
      console.error(`✗ Unknown argument: ${arg}`);
      printUsage();
      process.exit(1);
  }
}

// If URL is missing a scheme, prefix with http:// for convenience
if (!/^[a-zA-Z][a-zA-Z0-9+.-]*:\/\//.test(url)) {
  url = `http://${url}`;
}

const port = process.env.BROWSER_PORT ? parseInt(process.env.BROWSER_PORT, 10) : 9222;

try {
  const browser = await puppeteer.connect({
    browserURL: `http://localhost:${port}`,
    defaultViewport: null,
  });
  let page;
  if (newTab) {
    page = await browser.newPage();
  } else {
    const pages = await browser.pages();
    page = pages.at(-1);
  }
  if (!page) {
    console.error('✗ No active tab found');
    process.exit(1);
  }
  await page.goto(url, { waitUntil });
  console.log(`${newTab ? '✓ Opened' : '✓ Navigated to'}: ${url}`);
  await browser.disconnect();
} catch (err) {
  console.error('✗ Error navigating:', err.message || err);
  process.exit(1);
}