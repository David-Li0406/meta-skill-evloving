---
name: dev-browser
description: Browser automation with persistent page state. Use when users ask to navigate websites, fill forms, take screenshots, extract web data, test web apps, or automate browser workflows. Trigger phrases include "go to [url]", "click on", "fill out the form", "take a screenshot", "scrape", "automate", "test the website", "log into", or any browser interaction request.
---

# Dev Browser Skill

Browser automation that maintains page state across script executions. Write small, focused scripts to accomplish tasks incrementally.

## Choosing Your Approach

- **Local/source-available sites**: Read the source code first to write selectors directly
- **Unknown page layouts**: Use `getAISnapshot()` to discover elements and `selectSnapshotRef()` to interact with them
- **Visual feedback**: Take screenshots to see what the user sees

## Setup

**IMPORTANT: Always use Standalone Mode for browser automation.**

### Standalone Mode (Default)

Launches a Chromium browser with a **persistent profile**. Login sessions, cookies, and local storage persist across browser restarts.

**Start the server:**

```bash
~/.config/opencode/skill/dev-browser/server.sh &
```

Wait for the `Ready` message before running scripts. Add `--headless` flag if user requests headless mode.

**Key points:**
- Profile stored at `~/.config/opencode/skill/dev-browser/profiles/browser-data`
- Once logged in, future sessions remain authenticated
- Use this mode for local dev testing with auth (localhost:3000, etc.)

## Writing Scripts

> **Run all scripts from the dev-browser directory.**

Execute scripts inline using heredocs:

```bash
cd ~/.config/opencode/skill/dev-browser && npx tsx <<'EOF'
import { connect, waitForPageLoad } from "@/client.js";

const client = await connect();
const page = await client.page("example");
await page.setViewportSize({ width: 1280, height: 800 });

await page.goto("https://example.com");
await waitForPageLoad(page);

console.log({ title: await page.title(), url: page.url() });
await client.disconnect();
EOF
```

### Key Principles

1. **Small scripts**: Each script does ONE thing (navigate, click, fill, check)
2. **Evaluate state**: Log/return state at the end to decide next steps
3. **Descriptive page names**: Use `"checkout"`, `"login"`, not `"main"`
4. **Disconnect to exit**: `await client.disconnect()` - pages persist on server
5. **Plain JS in evaluate**: `page.evaluate()` runs in browser - no TypeScript syntax

## Workflow Loop

1. **Write a script** to perform one action
2. **Run it** and observe the output
3. **Evaluate** - did it work? What's the current state?
4. **Decide** - is the task complete or do we need another script?
5. **Repeat** until task is done

## Client API

```typescript
const client = await connect();
const page = await client.page("name"); // Get or create named page
const pages = await client.list(); // List all page names
await client.close("name"); // Close a page
await client.disconnect(); // Disconnect (pages persist)

// ARIA Snapshot methods
const snapshot = await client.getAISnapshot("name"); // Get accessibility tree
const element = await client.selectSnapshotRef("name", "e5"); // Get element by ref

// Token-efficient content extraction
const outline = await client.getOutline("name"); // Tree of all elements
const interactive = await client.getInteractiveOutline("name"); // Only interactive elements
const text = await client.getVisibleText("name"); // Visible text only
```

## Token-Efficient Content Extraction

| Method | Use case | Token efficiency |
|--------|----------|------------------|
| `getInteractiveOutline()` | Discover clickable elements | Most efficient |
| `getOutline()` | Understand page structure | Very efficient |
| `getVisibleText()` | Extract readable content | Very efficient |
| `getAISnapshot()` | Need ref-based clicking | Full ARIA tree |
| `screenshot()` | Visual debugging | Uses vision tokens |

## Screenshots

```typescript
await page.screenshot({ path: "tmp/screenshot.png" });
await page.screenshot({ path: "tmp/full.png", fullPage: true });
```

## ARIA Snapshot (Element Discovery)

Use `getAISnapshot()` to discover page elements. Returns YAML-formatted accessibility tree with `[ref=eN]` references for interaction:

```typescript
const snapshot = await client.getAISnapshot("hackernews");
console.log(snapshot); // Find the ref you need

const element = await client.selectSnapshotRef("hackernews", "e2");
await element.click();
```

## Error Recovery

Page state persists after failures. Debug with:

```bash
cd ~/.config/opencode/skill/dev-browser && npx tsx <<'EOF'
import { connect } from "@/client.js";

const client = await connect();
const page = await client.page("hackernews");

await page.screenshot({ path: "tmp/debug.png" });
console.log({
  url: page.url(),
  title: await page.title(),
  bodyText: await page.textContent("body").then((t) => t?.slice(0, 200)),
});

await client.disconnect();
EOF
```
