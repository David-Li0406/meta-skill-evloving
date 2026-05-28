/**
 * Universal Playwright Executor for Claude Code
 *
 * Executes Playwright automation code from:
 * - File path: node run.js script.js
 * - Inline code: node run.js 'await page.goto("...")'
 * - Stdin: cat script.js | node run.js
 *
 * Ensures proper module resolution by running from skill directory.
 */

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { execSync } = require("child_process");

// Change to skill directory for proper module resolution
process.chdir(__dirname);

/**
 * Check if Playwright is installed
 */
function checkPlaywrightInstalled() {
  try {
    require.resolve("playwright");
    return true;
  } catch (e) {
    return false;
  }
}

/**
 * Check if a command exists (cross-platform)
 */
function commandExists(cmd) {
  try {
    const checkCmd =
      process.platform === "win32" ? `where ${cmd}` : `which ${cmd}`;
    execSync(checkCmd, { stdio: "ignore" });
    return true;
  } catch (e) {
    return false;
  }
}

/**
 * Get package manager (prefer bun over npm)
 */
function getPackageManager() {
  if (commandExists("bun")) {
    return { install: "bun install", exec: "bunx" };
  }
  return { install: "npm install", exec: "npx" };
}

/**
 * Install Playwright library (not browser)
 */
function installPlaywrightLib() {
  const pm = getPackageManager();
  console.log(
    `Playwright not found. Installing with ${pm.install.split(" ")[0]}...`
  );
  try {
    execSync(pm.install, { stdio: "inherit", cwd: __dirname });
    console.log("Playwright library installed successfully");
    console.log('Note: Using system Chrome by default (channel: "chrome")');
    return true;
  } catch (e) {
    console.error("Failed to install Playwright:", e.message);
    console.error("Please run manually: cd", __dirname, "&& npm install");
    return false;
  }
}

/**
 * Get code to execute from various sources
 */
function getCodeToExecute() {
  const args = process.argv.slice(2);

  // Case 1: File path provided
  if (args.length > 0 && fs.existsSync(args[0])) {
    const filePath = path.resolve(args[0]);
    console.log(`Executing file: ${filePath}`);
    return fs.readFileSync(filePath, "utf8");
  }

  // Case 2: Inline code provided as argument
  if (args.length > 0) {
    console.log("Executing inline code");
    return args.join(" ");
  }

  // Case 3: Code from stdin
  if (!process.stdin.isTTY) {
    console.log("Reading from stdin");
    return fs.readFileSync(0, "utf8");
  }

  // No input
  console.error("No code to execute");
  console.error("Usage:");
  console.error("  node run.js script.js          # Execute file");
  console.error('  node run.js "code here"        # Execute inline');
  console.error("  cat script.js | node run.js    # Execute from stdin");
  process.exit(1);
}

/**
 * Clean up old temporary execution files from previous runs
 */
function cleanupOldTempFiles() {
  try {
    const files = fs.readdirSync(__dirname);
    const tempFiles = files.filter(
      (f) => f.startsWith(".temp-execution-") && f.endsWith(".js")
    );

    if (tempFiles.length > 0) {
      tempFiles.forEach((file) => {
        const filePath = path.join(__dirname, file);
        try {
          fs.unlinkSync(filePath);
        } catch (e) {
          // Ignore errors - file might be in use or already deleted
        }
      });
    }
  } catch (e) {
    // Ignore directory read errors
  }
}

/**
 * Wrap code in async IIFE if not already wrapped
 */
function wrapCodeIfNeeded(code) {
  // Check if code already has require() and async structure
  const hasRequire = code.includes("require(");
  const hasAsyncIIFE =
    code.includes("(async () => {") || code.includes("(async()=>{");

  // If it's already a complete script, return as-is
  if (hasRequire && hasAsyncIIFE) {
    return code;
  }

  // If it's just Playwright commands, wrap in full template
  if (!hasRequire) {
    return `
const { chromium, firefox, webkit, devices } = require('playwright');
const helpers = require('./lib/helpers');

// Use system Chrome by default
const DEFAULT_LAUNCH_OPTIONS = { channel: 'chrome' };

(async () => {
  try {
    ${code}
  } catch (error) {
    // Check if error is due to missing browser
    if (error.message && error.message.includes('Executable doesn\\'t exist')) {
      console.error('\\nError: System Chrome/Chromium not found.');
      console.error('Options:');
      console.error('  1. Install Chrome/Chromium on your system');
      console.error('  2. Run: cd ${__dirname} && npx playwright install chromium');
      console.error('     (or: bunx playwright install chromium)');
    } else {
      console.error('Automation error:', error.message);
      if (error.stack) {
        console.error(error.stack);
      }
    }
    process.exit(1);
  }
})();
`;
  }

  // If has require but no async wrapper
  if (!hasAsyncIIFE) {
    return `
(async () => {
  try {
    ${code}
  } catch (error) {
    console.error('Automation error:', error.message);
    if (error.stack) {
      console.error(error.stack);
    }
    process.exit(1);
  }
})();
`;
  }

  return code;
}

/**
 * Main execution
 */
async function main() {
  console.log("Playwright Skill - Universal Executor\n");

  // Clean up old temp files from previous runs
  cleanupOldTempFiles();

  // Check Playwright installation
  if (!checkPlaywrightInstalled()) {
    const installed = installPlaywrightLib();
    if (!installed) {
      process.exit(1);
    }
  }

  // Get code to execute
  const rawCode = getCodeToExecute();
  const code = wrapCodeIfNeeded(rawCode);

  // Create temporary file with secure random name
  const randomId = crypto.randomBytes(16).toString("hex");
  const tempFile = path.join(__dirname, `.temp-execution-${randomId}.js`);

  try {
    // Write code to temp file
    fs.writeFileSync(tempFile, code, "utf8");

    // Execute the code
    console.log("Starting automation...\n");
    require(tempFile);

    // Clean up require cache to prevent memory leak
    delete require.cache[require.resolve(tempFile)];
  } catch (error) {
    console.error("Execution failed:", error.message);
    if (error.stack) {
      console.error("\nStack trace:");
      console.error(error.stack);
    }
    // Clean up require cache even on error
    try {
      delete require.cache[require.resolve(tempFile)];
    } catch (e) {}
    process.exit(1);
  }
}

// Run main function
main().catch((error) => {
  console.error("Fatal error:", error.message);
  process.exit(1);
});
