#!/usr/bin/env node

/*
 * Launch a Chrome instance for use with the browser skill.
 *
 * This script attempts to find the Chrome executable on macOS, Linux and Windows.  You can override the auto‑detected
 * path by setting the `CHROME_PATH` environment variable or passing the `--chrome-path` flag.  The script will copy
 * your existing profile (cookies, logins, etc.) into a temporary user data directory when invoked with `--profile`.
 * Additional options allow you to specify the remote debugging port, run headless and set a custom user data
 * directory.  After launching Chrome it waits for Puppeteer to successfully connect before exiting.
 */

import { spawn, execSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import puppeteer from 'puppeteer-core';

function printUsage() {
  console.log('Usage: start.js [options]');
  console.log('\nOptions:');
  console.log('  --profile             Copy your default Chrome profile (cookies, logins)');
  console.log('  --user-data-dir <dir> Use a custom directory for Chrome user data');
  console.log('  --chrome-path <path>  Path to the Chrome executable');
  console.log('  --port <number>       Remote debugging port (default 9222)');
  console.log('  --headless            Run Chrome in headless mode');
  console.log('\nExamples:');
  console.log('  start.js                     # Start with fresh profile');
  console.log('  start.js --profile           # Start with your Chrome profile');
  console.log('  start.js --port 9223         # Start on a different port');
  console.log('  start.js --headless          # Start Chrome in headless mode');
}

// Parse command line arguments
const argv = process.argv.slice(2);
let useProfile = false;
let userDataDir = null;
let chromePath = process.env.CHROME_PATH || null;
let port = 9222;
let headless = false;

for (let i = 0; i < argv.length; i++) {
  const arg = argv[i];
  switch (arg) {
    case '--profile':
      useProfile = true;
      break;
    case '--user-data-dir':
      if (!argv[i + 1]) {
        console.error('✗ --user-data-dir requires a directory');
        printUsage();
        process.exit(1);
      }
      userDataDir = argv[i + 1];
      i++;
      break;
    case '--chrome-path':
      if (!argv[i + 1]) {
        console.error('✗ --chrome-path requires a path');
        printUsage();
        process.exit(1);
      }
      chromePath = argv[i + 1];
      i++;
      break;
    case '--port':
      if (!argv[i + 1] || Number.isNaN(parseInt(argv[i + 1], 10))) {
        console.error('✗ --port requires a number');
        printUsage();
        process.exit(1);
      }
      port = parseInt(argv[i + 1], 10);
      i++;
      break;
    case '--headless':
      headless = true;
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

// Attempt to detect Chrome path if none provided
function detectChrome() {
  const candidates = [];
  if (process.platform === 'darwin') {
    candidates.push('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');
    candidates.push('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome Canary');
  } else if (process.platform === 'win32') {
    const localApp = process.env.LOCALAPPDATA || path.join(os.homedir(), 'AppData', 'Local');
    candidates.push(path.join('C:\\', 'Program Files', 'Google', 'Chrome', 'Application', 'chrome.exe'));
    candidates.push(path.join('C:\\', 'Program Files (x86)', 'Google', 'Chrome', 'Application', 'chrome.exe'));
    candidates.push(path.join(localApp, 'Google', 'Chrome', 'Application', 'chrome.exe'));
  } else {
    // Assume Linux/Unix
    candidates.push('/usr/bin/google-chrome');
    candidates.push('/usr/bin/google-chrome-stable');
    candidates.push('/usr/bin/chromium-browser');
    candidates.push('/usr/bin/chromium');
  }
  for (const p of candidates) {
    try {
      if (fs.existsSync(p)) {
        return p;
      }
    } catch {
      /* ignore */
    }
  }
  return null;
}

if (!chromePath) {
  chromePath = detectChrome();
}

if (!chromePath) {
  console.error('✗ Could not find Chrome binary. Please install Google Chrome or set CHROME_PATH.');
  process.exit(1);
}

// Kill any existing Chrome processes for a clean launch
function killChromeProcesses() {
  try {
    if (process.platform === 'win32') {
      const exe = path.basename(chromePath);
      execSync(`taskkill /IM ${exe} /F`, { stdio: 'ignore' });
    } else {
      const exe = path.basename(chromePath);
      execSync(`pkill -f '${exe}'`, { stdio: 'ignore' });
    }
  } catch {
    // Ignore errors if process not found
  }
}

killChromeProcesses();
// Wait briefly to let processes terminate fully
await new Promise((r) => setTimeout(r, 1000));

// Determine the user data directory
const dataDir = userDataDir || path.join(os.homedir(), '.cache', 'browser-tools');
fs.mkdirSync(dataDir, { recursive: true });

// Copy the default profile into the data directory if requested
if (useProfile) {
  let defaultProfile = null;
  if (process.platform === 'darwin') {
    defaultProfile = path.join(os.homedir(), 'Library', 'Application Support', 'Google', 'Chrome');
  } else if (process.platform === 'win32') {
    const localApp = process.env.LOCALAPPDATA || path.join(os.homedir(), 'AppData', 'Local');
    defaultProfile = path.join(localApp, 'Google', 'Chrome', 'User Data');
  } else {
    defaultProfile = path.join(os.homedir(), '.config', 'google-chrome');
    if (!fs.existsSync(defaultProfile)) {
      defaultProfile = path.join(os.homedir(), '.config', 'chromium');
    }
  }
  try {
    if (defaultProfile && fs.existsSync(defaultProfile)) {
      // Use the built‑in fs.cpSync available in Node 16+ for recursive copy
      fs.cpSync(defaultProfile, dataDir, { recursive: true });
    }
  } catch {
    // Copying profile is best‑effort; ignore errors
  }
}

// Build Chrome launch arguments
const chromeArgs = [
  `--remote-debugging-port=${port}`,
  `--user-data-dir=${dataDir}`,
];

if (headless) {
  // Use new headless mode if available; fallback to legacy
  chromeArgs.push('--headless=new');
  chromeArgs.push('--disable-gpu');
}

// Spawn Chrome detached so this script can exit once Chrome is ready
spawn(chromePath, chromeArgs, { detached: true, stdio: 'ignore' }).unref();

// Wait for Chrome to be ready by attempting to connect
let connected = false;
for (let i = 0; i < 30; i++) {
  try {
    const browser = await puppeteer.connect({
      browserURL: `http://localhost:${port}`,
      defaultViewport: null,
    });
    await browser.disconnect();
    connected = true;
    break;
  } catch {
    await new Promise((res) => setTimeout(res, 500));
  }
}

if (!connected) {
  console.error('✗ Failed to connect to Chrome');
  process.exit(1);
}

// Success message
console.log(
  `✓ Chrome started on :${port}` +
    (useProfile ? ' with your profile' : '') +
    (headless ? ' (headless)' : ''),
);