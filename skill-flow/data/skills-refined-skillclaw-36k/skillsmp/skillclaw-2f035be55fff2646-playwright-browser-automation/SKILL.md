---
name: playwright-browser-automation
description: Use this skill when you want to automate browser interactions, validate web functionality, or perform any browser-based testing with Playwright.
---

# Playwright Browser Automation

This skill provides comprehensive browser automation capabilities using Playwright. It can auto-detect development servers, manage server lifecycles, and write clean test scripts to a temporary directory.

## CRITICAL WORKFLOW

1. **Auto-detect dev servers** - For localhost testing, always run server detection first:
   ```bash
   cd $SKILL_DIR && node -e "require('./lib/helpers').detectDevServers().then(servers => console.log(JSON.stringify(servers)))"
   ```
   - If **1 server found**: Use it automatically and inform the user.
   - If **multiple servers found**: Ask the user which one to test.
   - If **no servers found**: Ask for a URL or offer to help start a dev server.

2. **Write scripts to /tmp** - Always write test files to `/tmp/playwright-test-*.js` to avoid cluttering the skill directory.

3. **Use visible browser by default** - Always launch the browser in non-headless mode (`headless: false`) unless the user specifically requests headless mode.

4. **Parameterize URLs** - Make URLs configurable via an environment variable or a constant at the top of the script.

5. **Wait for dynamic content** - Use `waitForLoadState('networkidle')` before inspecting dynamic web applications to ensure all content is loaded.

## How It Works

1. You describe what you want to test or automate.
2. The skill auto-detects running dev servers (or asks for a URL if testing an external site).
3. It writes custom Playwright code in `/tmp/playwright-test-*.js`.
4. Execute the script via:
   ```bash
   cd $SKILL_DIR && node run.js /tmp/playwright-test-*.js
   ```
5. Results are displayed in real-time, with the browser window visible for debugging.

## Key Rules

- Always execute via `run.js` — never run scripts directly with `node /tmp/script.js`.
- Always detect servers first for localhost testing.
- Use `headless: false` by default to avoid detection issues with automated browsing.

## Helpers

Optional utilities in `lib/helpers.js` can assist with common tasks, such as detecting running servers or safely interacting with page elements.