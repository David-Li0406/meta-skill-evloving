#!/usr/bin/env bun
/**
 * Playwright Runner - Browser automation for design-implementation skill
 *
 * Usage:
 *   bun playwright-runner.ts screenshot --url http://localhost:5173 --output screenshot.png
 *   bun playwright-runner.ts capture --url http://localhost:5173 --output capture.json
 *   bun playwright-runner.ts full --url http://localhost:5173 --output-dir ./history/feature-1
 *
 * Commands:
 *   screenshot  - Take a screenshot
 *   capture     - Capture console logs, network errors, and screenshot
 *   full        - Full verification (screenshot + console + network + interactions)
 */

import { chromium, Browser, Page, ConsoleMessage, Request, Response } from 'playwright';
import { parseArgs } from 'util';

// Types
interface CaptureResult {
  screenshot: string;
  console: ConsoleEntry[];
  network: NetworkEntry[];
  errors: string[];
  timestamp: string;
}

interface ConsoleEntry {
  type: string;
  text: string;
  location?: string;
}

interface NetworkEntry {
  url: string;
  method: string;
  status: number;
  failed: boolean;
  error?: string;
}

interface Config {
  headless: boolean;
  viewport: { width: number; height: number };
  timeout: number;
}

// Load config
function loadConfig(): Config {
  try {
    const configPath = new URL('../config.json', import.meta.url).pathname;
    const config = JSON.parse(Bun.file(configPath).text());
    return {
      headless: config.browser?.headless ?? false,
      viewport: config.browser?.viewport ?? { width: 1280, height: 720 },
      timeout: config.browser?.timeout ?? 30000,
    };
  } catch {
    return {
      headless: false,
      viewport: { width: 1280, height: 720 },
      timeout: 30000,
    };
  }
}

// Screenshot command
async function takeScreenshot(url: string, output: string, config: Config): Promise<void> {
  const browser = await chromium.launch({ headless: config.headless });
  const page = await browser.newPage({ viewport: config.viewport });

  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: config.timeout });
    await page.screenshot({ path: output, fullPage: true });
    console.log(JSON.stringify({ success: true, screenshot: output }));
  } finally {
    await browser.close();
  }
}

// Full capture command
async function captureAll(url: string, outputDir: string, config: Config): Promise<CaptureResult> {
  const browser = await chromium.launch({ headless: config.headless });
  const page = await browser.newPage({ viewport: config.viewport });

  const consoleEntries: ConsoleEntry[] = [];
  const networkEntries: NetworkEntry[] = [];
  const errors: string[] = [];

  // Capture console
  page.on('console', (msg: ConsoleMessage) => {
    const entry: ConsoleEntry = {
      type: msg.type(),
      text: msg.text(),
      location: msg.location()?.url,
    };
    consoleEntries.push(entry);

    if (msg.type() === 'error') {
      errors.push(`Console error: ${msg.text()}`);
    }
  });

  // Capture page errors
  page.on('pageerror', (error: Error) => {
    errors.push(`Page error: ${error.message}`);
  });

  // Capture network
  page.on('requestfailed', (request: Request) => {
    const entry: NetworkEntry = {
      url: request.url(),
      method: request.method(),
      status: 0,
      failed: true,
      error: request.failure()?.errorText,
    };
    networkEntries.push(entry);
    errors.push(`Network failed: ${request.method()} ${request.url()} - ${request.failure()?.errorText}`);
  });

  page.on('response', (response: Response) => {
    if (response.status() >= 400) {
      const entry: NetworkEntry = {
        url: response.url(),
        method: response.request().method(),
        status: response.status(),
        failed: true,
      };
      networkEntries.push(entry);
      errors.push(`Network error: ${response.status()} ${response.request().method()} ${response.url()}`);
    }
  });

  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: config.timeout });

    // Wait a bit for any async errors
    await page.waitForTimeout(1000);

    // Take screenshot
    const screenshotPath = `${outputDir}/screenshot.png`;
    await Bun.write(outputDir, ''); // Ensure dir exists
    await page.screenshot({ path: screenshotPath, fullPage: true });

    const result: CaptureResult = {
      screenshot: screenshotPath,
      console: consoleEntries,
      network: networkEntries,
      errors,
      timestamp: new Date().toISOString(),
    };

    // Write capture data
    await Bun.write(`${outputDir}/capture.json`, JSON.stringify(result, null, 2));

    return result;
  } finally {
    await browser.close();
  }
}

// Interactive browser session (for debugging)
async function launchInteractive(url: string, config: Config): Promise<void> {
  const browser = await chromium.launch({
    headless: false,  // Always visible for interactive
    slowMo: 100,
  });
  const page = await browser.newPage({ viewport: config.viewport });

  console.log(JSON.stringify({
    message: 'Browser launched. Press Ctrl+C to close.',
    url
  }));

  await page.goto(url, { waitUntil: 'networkidle', timeout: config.timeout });

  // Keep browser open until interrupted
  await new Promise(() => {});
}

// Main
async function main() {
  const { values, positionals } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      url: { type: 'string', short: 'u' },
      output: { type: 'string', short: 'o' },
      'output-dir': { type: 'string', short: 'd' },
      headless: { type: 'boolean' },
    },
    allowPositionals: true,
  });

  const command = positionals[0];
  const config = loadConfig();

  // Override headless from CLI flag
  if (values.headless !== undefined) {
    config.headless = values.headless;
  }

  if (!values.url) {
    console.error('Error: --url is required');
    process.exit(1);
  }

  try {
    switch (command) {
      case 'screenshot':
        if (!values.output) {
          console.error('Error: --output is required for screenshot');
          process.exit(1);
        }
        await takeScreenshot(values.url, values.output, config);
        break;

      case 'capture':
      case 'full':
        const outputDir = values['output-dir'] || './capture';
        const result = await captureAll(values.url, outputDir, config);
        console.log(JSON.stringify(result, null, 2));
        break;

      case 'interactive':
      case 'debug':
        await launchInteractive(values.url, config);
        break;

      default:
        console.error(`Unknown command: ${command}`);
        console.error('Available commands: screenshot, capture, full, interactive');
        process.exit(1);
    }
  } catch (error) {
    console.error(JSON.stringify({
      error: true,
      message: error instanceof Error ? error.message : String(error)
    }));
    process.exit(1);
  }
}

main();
