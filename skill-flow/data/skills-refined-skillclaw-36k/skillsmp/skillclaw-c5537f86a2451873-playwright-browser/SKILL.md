---
name: playwright-browser
description: Use this skill when automating browsers, testing pages, taking screenshots, checking UI, verifying login flows, or testing responsive behavior.
---

# Skill body

## Objective
Browser automation via Playwright. Write scripts and execute them using `run.js`.

## Execution
Write Playwright code to `/tmp`, and execute from the skill directory:

```bash
node $SKILL_DIR/run.js /tmp/playwright-task.js
```

For inline code (variables are auto-injected, see below):

```bash
node $SKILL_DIR/run.js "const b = await chromium.launch(); const p = await b.newPage(); await p.goto('http://localhost:3000'); console.log(await p.title()); await b.close();"
```

`$SKILL_DIR` is the directory where this file is loaded from.

## Headless vs Headed
Default: headless (invisible, less intrusive).

Use `{ headless: false }` when the user wants to see the browser.

## Defaults
Screenshots are saved to `/tmp`. Use `slowMo: 100` for debugging.

## Injected Variables
For inline code, the following variables are available:

- `BASE_URL` - from `PLAYWRIGHT_BASE_URL` environment variable
- `CI_ARGS` - browser arguments for CI (`['--no-sandbox', '--disable-setuid-sandbox']`)
- `EXTRA_HEADERS` - from `PW_HEADER_NAME/VALUE` or `PW_EXTRA_HEADERS`
- `chromium`, `firefox`, `webkit`, `devices` - from Playwright

Example:

```bash
node $SKILL_DIR/run.js "
const browser = await chromium.launch({ args: CI_ARGS });
const page = await browser.newPage();
await page.goto(BASE_URL || 'http://localhost:3000');
console.log(await page.title());
await browser.close();
"
```

## Auto-install
`run.js` auto-installs Playwright on first use. No manual setup is needed.

## Advanced Patterns
For network mocking, authentication persistence, multi-tab handling, downloads, video, and traces, refer to the [API_REFERENCE.md](API_REFERENCE.md).