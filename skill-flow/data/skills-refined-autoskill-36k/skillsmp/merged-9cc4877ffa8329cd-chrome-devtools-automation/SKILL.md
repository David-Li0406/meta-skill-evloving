---
name: chrome-devtools-automation
description: Use this skill for browser automation, debugging, and performance analysis with Puppeteer CLI scripts. Ideal for tasks like web scraping, taking screenshots, monitoring network traffic, and form automation.
---

# Chrome DevTools Automation Skill

Browser automation via Puppeteer scripts with persistent sessions. All scripts output JSON for easy parsing.

## Skill Location

Skills can exist in **project-scope** or **user-scope**. Priority: project-scope > user-scope.

```bash
# Detect skill location
SKILL_DIR=""
if [ -d ".claude/skills/chrome-devtools/scripts" ]; then
  SKILL_DIR=".claude/skills/chrome-devtools/scripts"
elif [ -d "$HOME/.claude/skills/chrome-devtools/scripts" ]; then
  SKILL_DIR="$HOME/.claude/skills/chrome-devtools/scripts"
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
- Run multiple scripts/sessions in parallel to simulate real user interactions.
- Run multiple scripts/sessions in parallel to simulate different device types (mobile, tablet, desktop).

## ARIA Snapshot (Element Discovery)

When page structure is unknown, use `aria-snapshot.js` to get a YAML-formatted accessibility tree with semantic roles, accessible names, states, and stable element references.

### Get ARIA Snapshot

```bash
# Generate ARIA snapshot and output to stdout
node aria-snapshot.js --url https://example.com

# Save to file in snapshots directory
node aria-snapshot.js --url https://example.com --output ./.claude/chrome-devtools/snapshots/page.yaml
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
- main:
  - list:
    - listitem:
      - link "Show HN: My new project" [ref=e8]
      - text: "128 points by user 3 hours ago"
- contentinfo:
  - textbox [ref=e10]
    /placeholder: "Search"
```

### Interacting by Reference

Use `select-ref.js` to interact with elements by their ref:

```bash
# Click element with ref e5
node select-ref.js --ref e5 --action click

# Fill input with ref e10
node select-ref.js --ref e10 --action fill --value "search query"

# Get text content
node select-ref.js --ref e8 --action text

# Screenshot specific element
node select-ref.js --ref e1 --action screenshot --output ./logo.png
```

## Session Persistence

Browser state persists across script executions via WebSocket endpoint file (`.browser-session.json`).

**Default behavior**: Scripts disconnect but keep browser running for session reuse.

```bash
# First script: launches browser, navigates, disconnects (browser stays running)
node navigate.js --url https://example.com/login

# Subsequent scripts: connect to existing browser, reuse page state
node fill.js --selector "#email" --value "user@example.com"
node fill.js --selector "#password" --value "secret"
node click.js --selector "button[type=submit]"

# Close browser when done
node navigate.js --url about:blank --close true
```

## Available Scripts

All in `.claude/skills/chrome-devtools/scripts/`:

| Script | Purpose |
|--------|---------|
| `navigate.js` | Navigate to URLs |
| `screenshot.js` | Capture screenshots (auto-compress >5MB via Sharp) |
| `click.js` | Click elements |
| `fill.js` | Fill form fields |
| `evaluate.js` | Execute JS in page context |
| `snapshot.js` | Extract interactive elements (JSON format) |
| `aria-snapshot.js` | Get ARIA accessibility tree (YAML format with refs) |
| `select-ref.js` | Interact with elements by ref from ARIA snapshot |
| `console.js` | Monitor console messages/errors |
| `network.js` | Track HTTP requests/responses |
| `performance.js` | Measure Core Web Vitals |

## Common Workflows

### Web Scraping
```bash
node evaluate.js --url https://example.com --script "
  Array.from(document.querySelectorAll('.item')).map(el => ({
    title: el.querySelector('h2')?.textContent,
    link: el.querySelector('a')?.href
  }))
" | jq '.result'
```

### Performance Testing
```bash
node performance.js --url https://example.com | jq '.vitals'
```

### Form Automation
```bash
node fill.js --url https://example.com --selector "#search" --value "query" --close false
node click.js --selector "button[type=submit]"
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| `Cannot find package 'puppeteer'` | Run `npm install` in scripts directory |
| `libnss3.so` missing (Linux) | Run `./install-deps.sh` |
| Element not found | Use `snapshot.js` to find correct selector |
| Script hangs | Use `--timeout 60000` or `--wait-until load` |
| Screenshot >5MB | Auto-compressed; use `--max-size 3` for lower |
| Session stale | Delete `.browser-session.json` and retry |

## Reference Documentation

- `./references/cdp-domains.md` - Chrome DevTools Protocol domains
- `./references/puppeteer-reference.md` - Puppeteer API patterns
- `./references/performance-guide.md` - Core Web Vitals optimization
- `./scripts/README.md` - Detailed script options