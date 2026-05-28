#!/usr/bin/env node

/*
 * Capture a screenshot of the current page.
 *
 * This script connects to the last active tab of a running Chrome session and saves a screenshot.  You can choose
 * between capturing the entire page or just the visible viewport, specify the output file and choose the image format.
 */

import fs from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import puppeteer from 'puppeteer-core';

function printUsage() {
  console.log('Usage: screenshot.js [options]');
  console.log('\nOptions:');
  console.log('  --file <path>     Output file path (default: temp directory with timestamp)');
  console.log('  --fullpage        Capture the entire page instead of just the viewport');
  console.log('  --format <fmt>    Image format: png|jpeg (default png)');
  console.log('\nExamples:');
  console.log('  screenshot.js');
  console.log('  screenshot.js --file ~/Desktop/page.png --fullpage');
}

const argv = process.argv.slice(2);
let filePath = null;
let fullPage = false;
let format = 'png';

for (let i = 0; i < argv.length; i++) {
  const arg = argv[i];
  switch (arg) {
    case '--file':
      if (!argv[i + 1]) {
        console.error('✗ --file requires a path');
        printUsage();
        process.exit(1);
      }
      filePath = argv[i + 1];
      i++;
      break;
    case '--fullpage':
      fullPage = true;
      break;
    case '--format':
      if (!argv[i + 1]) {
        console.error('✗ --format requires a value');
        printUsage();
        process.exit(1);
      }
      format = argv[i + 1].toLowerCase();
      if (format !== 'png' && format !== 'jpeg' && format !== 'jpg') {
        console.error('✗ --format must be png or jpeg');
        process.exit(1);
      }
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

const port = process.env.BROWSER_PORT ? parseInt(process.env.BROWSER_PORT, 10) : 9222;

try {
  const browser = await puppeteer.connect({
    browserURL: `http://localhost:${port}`,
    defaultViewport: null,
  });
  const pages = await browser.pages();
  const page = pages.at(-1);
  if (!page) {
    console.error('✗ No active tab found');
    process.exit(1);
  }
  // Determine file path
  if (!filePath) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const ext = format === 'jpg' ? 'jpeg' : format;
    filePath = join(tmpdir(), `screenshot-${timestamp}.${ext}`);
  } else {
    // Ensure parent directory exists
    try {
      const dir = require('node:path').dirname(filePath);
      fs.mkdirSync(dir, { recursive: true });
    } catch {
      // ignore
    }
  }
  await page.screenshot({ path: filePath, fullPage, type: format === 'jpg' ? 'jpeg' : format });
  console.log(filePath);
  await browser.disconnect();
} catch (err) {
  console.error('✗ Error taking screenshot:', err.message || err);
  process.exit(1);
}