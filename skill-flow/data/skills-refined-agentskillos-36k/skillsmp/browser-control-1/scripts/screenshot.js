#!/usr/bin/env bun

/**
 * Take screenshot of a webpage
 *
 * Usage: bun screenshot.js <url> [output.png] [--full]
 *
 * Options:
 *   --full    Capture full page (not just viewport)
 *
 * Examples:
 *   bun screenshot.js https://www.marriott.com
 *   bun screenshot.js https://www.marriott.com hotel.png --full
 */

import puppeteer from 'puppeteer-core';
import path from 'path';
import sharp from 'sharp';
import { unlink } from 'fs/promises';

const CDP_ENDPOINT = 'http://127.0.0.1:9222';

async function screenshot(url, outputPath, options = {}) {
  let browser;

  try {
    browser = await puppeteer.connect({
      browserURL: CDP_ENDPOINT,
      defaultViewport: null
    });

    const pages = await browser.pages();
    const page = pages.length > 0 ? pages[0] : await browser.newPage();

    // Navigate to URL - don't manipulate viewport, use browser's current size
    await page.goto(url, {
      waitUntil: 'networkidle2',
      timeout: 30000
    });

    // Default output path
    if (!outputPath) {
      const urlObj = new URL(url);
      outputPath = `screenshot-${urlObj.hostname}-${Date.now()}.png`;
    }

    // Wait for initial content to load
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Take screenshot - fullPage flag captures entire page height
    // Note: Sites with aggressive lazy-loading (AirBnB) may show placeholder images
    // outside the initial viewport. For best results, use browser's current viewport.
    await page.screenshot({
      path: outputPath,
      fullPage: options.fullPage || false
    });

    // Check actual screenshot dimensions and resize if needed
    const MAX_DIMENSION = 7500; // Safety margin under 8000px API limit
    const metadata = await sharp(outputPath).metadata();

    let originalDimensions = {
      width: metadata.width,
      height: metadata.height
    };

    let width = originalDimensions.width;
    let height = originalDimensions.height;
    let scaled = false;

    // Resize if exceeds API limits
    if (width > MAX_DIMENSION || height > MAX_DIMENSION) {
      const scale = Math.min(
        MAX_DIMENSION / width,
        MAX_DIMENSION / height
      );
      width = Math.floor(width * scale);
      height = Math.floor(height * scale);

      const tempPath = outputPath + '.resized';

      await sharp(outputPath)
        .resize(width, height, {
          fit: 'inside',
          withoutEnlargement: true
        })
        .toFile(tempPath);

      // Replace original with resized
      await Bun.write(outputPath, await Bun.file(tempPath).arrayBuffer());

      // Delete temp file
      try {
        await unlink(tempPath);
      } catch (e) {
        // Ignore cleanup errors
      }

      scaled = true;
    }

    const title = await page.title();

    return {
      success: true,
      url,
      title,
      screenshot: path.resolve(outputPath),
      dimensions: { width, height },
      originalDimensions,
      scaled,
      safeToRead: true,
      fullPage: options.fullPage || false,
      timestamp: new Date().toISOString()
    };

  } catch (error) {
    return {
      success: false,
      url,
      error: error.message,
      hint: error.message.includes('connect') || error.message.includes('ECONNREFUSED')
        ? 'Is browser running? Start with: ./scripts/launch-chrome.sh'
        : null,
      timestamp: new Date().toISOString()
    };
  } finally {
    if (browser) {
      browser.disconnect();
    }
  }
}

async function main() {
  const args = process.argv.slice(2);
  const url = args[0];

  if (!url) {
    console.error(JSON.stringify({
      error: 'Missing URL',
      usage: 'bun screenshot.js <url> [output.png] [--full]'
    }));
    process.exit(1);
  }

  // Parse args
  let outputPath = null;
  const options = {};

  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--full') {
      options.fullPage = true;
    } else if (!args[i].startsWith('--')) {
      outputPath = args[i];
    }
  }

  const result = await screenshot(url, outputPath, options);
  console.log(JSON.stringify(result, null, 2));

  if (!result.success) {
    process.exit(1);
  }
}

main();
