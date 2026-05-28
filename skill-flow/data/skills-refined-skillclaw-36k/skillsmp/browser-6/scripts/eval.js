#!/usr/bin/env node

/*
 * Evaluate JavaScript within the context of the active page.
 *
 * This script connects to an existing Chrome session and executes arbitrary JavaScript in the last active tab.
 * You can provide the code inline or read it from a file via the --file option.  Results are printed to stdout in
 * a human‑readable form.  Arrays and objects are iterated and their keys and values printed on separate lines.
 */

import fs from 'node:fs';
import puppeteer from 'puppeteer-core';

function printUsage() {
  console.log('Usage: eval.js [--file <path>] <code>');
  console.log('\nOptions:');
  console.log('  --file <path>   Read JavaScript from a file instead of the command line');
  console.log('\nExamples:');
  console.log("  eval.js 'document.title'");
  console.log("  eval.js \"(() => { const links = document.querySelectorAll('a'); return links.length; })()\"");
  console.log('  eval.js --file scripts/sample.js');
}

const argv = process.argv.slice(2);
let code = '';
let fromFile = false;

for (let i = 0; i < argv.length; i++) {
  const arg = argv[i];
  if (arg === '--file') {
    if (!argv[i + 1]) {
      console.error('✗ --file requires a path');
      printUsage();
      process.exit(1);
    }
    const filePath = argv[i + 1];
    try {
      code = fs.readFileSync(filePath, 'utf8');
    } catch (err) {
      console.error(`✗ Failed to read file: ${err.message || err}`);
      process.exit(1);
    }
    fromFile = true;
    i++;
  } else if (arg === '--help' || arg === '-h') {
    printUsage();
    process.exit(0);
  } else if (!fromFile) {
    // Collect inline code arguments
    code += (code ? ' ' : '') + arg;
  } else {
    // If code already loaded from file, treat additional args as error
    console.error('✗ Unknown argument: ' + arg);
    printUsage();
    process.exit(1);
  }
}

if (!code) {
  printUsage();
  process.exit(1);
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
  const result = await page.evaluate((c) => {
    const AsyncFunction = (async () => {}).constructor;
    return new AsyncFunction(`return (${c})`)();
  }, code);
  // Pretty print the result
  if (Array.isArray(result)) {
    for (let i = 0; i < result.length; i++) {
      if (i > 0) console.log('');
      if (result[i] && typeof result[i] === 'object') {
        for (const [key, value] of Object.entries(result[i])) {
          console.log(`${key}: ${value}`);
        }
      } else {
        console.log(result[i]);
      }
    }
  } else if (result && typeof result === 'object') {
    for (const [key, value] of Object.entries(result)) {
      console.log(`${key}: ${value}`);
    }
  } else {
    console.log(result);
  }
  await browser.disconnect();
} catch (err) {
  console.error('✗ Error evaluating script:', err.message || err);
  process.exit(1);
}