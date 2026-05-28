---
name: chrome-devtools
description: Use this skill for browser automation, debugging, and performance analysis with Puppeteer CLI scripts, ideal for tasks like taking screenshots, monitoring network traffic, and web scraping.
---

# Chrome DevTools Agent Skill

Browser automation via Puppeteer scripts with persistent sessions. All scripts output JSON for easy parsing.

## Skill Location

Skills can exist in **project-scope** or **user-scope**. Priority: project-scope > user-scope.

```bash
# Detect skill location
SKILL_DIR=""
if [ -d ".opencode/skills/chrome-devtools/scripts" ]; then
  SKILL_DIR=".opencode/skills/chrome-devtools/scripts"
elif [ -d "$HOME/.opencode/skills/chrome-devtools/scripts" ]; then
  SKILL_DIR="$HOME/.opencode/skills/chrome-devtools/scripts"
fi
cd "$SKILL_DIR"
```

## Choosing Your Approach

| Scenario | Approach |
|----------|----------|
| **Source-available sites** | Read source code first, write selectors directly |
| **Unknown layouts** | Use `aria-snapshot.js` for semantic discovery |
| **Visual inspection** | Take screenshots to verify rendering |
| **Debug issues** | Collect console logs, analyze with session storage |
| **Accessibility audit** | Use ARIA snapshot for semantic structure analysis |

## Automation Browsing Running Mode

- Detect current OS and launch browser as headless only when running on Linux, WSL, or CI environments.
- For macOS/Windows, browser always runs in headed mode for better debugging.
- Run multiple scripts/sessions in parallel to simulate real user interactions and different device types (mobile, tablet, desktop).

## ARIA Snapshot (Element Discovery)

When page structure is unknown, use `aria-snapshot.js` to get a YAML-formatted accessibility tree with semantic roles, accessible names, states, and stable element references.

### Get ARIA Snapshot

```bash
# Generate ARIA snapshot and output to stdout
node "$SKILL_DIR/aria-snapshot.js" --url https://example.com

# Save to file in snapshots directory
node "$SKILL_DIR/aria-snapshot.js" --url https://example.com --output ./.opencode/chrome-devtools/snapshots/page.yaml
```

### Example YAML Output

```yaml
- banner:
  - link "Hacker News" [ref=e1]
    /url: https://news.ycombinator.com
  - navigation:
    - link "new" [ref=e2]
    - link "past" [ref=e3]
    - link "comments" [ref=e4]
```

## Available Scripts

All scripts are in `.opencode/skills/chrome-devtools/scripts/`

### Core Automation
- `navigate.js` - Navigate to URLs
- `screenshot.js` - Capture screenshots (full page or element)
- `click.js` - Click elements
- `fill.js` - Fill form fields
- `evaluate.js` - Execute JavaScript in page context

### Analysis & Monitoring
- `snapshot.js` - Extract interactive elements with metadata
- `console.js` - Monitor console messages/errors
- `network.js` - Track HTTP requests/responses
- `performance.js` - Measure Core Web Vitals + record traces