---
name: web-browser
description: Use this skill to interact with web pages by performing actions such as clicking buttons, filling out forms, and navigating links through remote control of Chrome or Chromium browsers using the Chrome DevTools Protocol (CDP).
---

# Web Browser Skill

Minimal CDP tools for collaborative site exploration.

## Start Chrome

```bash
./scripts/start.js              # Fresh profile
./scripts/start.js --profile    # Copy your profile (cookies, logins)
```

Start Chrome on `:9222` with remote debugging.

## Navigate

```bash
./scripts/nav.js https://example.com
./scripts/nav.js https://example.com --new
```

Navigate current tab or open a new tab.

## Evaluate JavaScript

```bash
./scripts/eval.js 'document.title'
./scripts/eval.js 'document.querySelectorAll("a").length'
./scripts/eval.js 'JSON.stringify(Array.from(document.querySelectorAll("a")).map(a => ({ text: a.textContent.trim(), href: a.href })).filter(link => !link.href.startsWith("https://")))'
```

Execute JavaScript in the active tab (async context). Be careful with string escaping; best to use single quotes.

## Screenshot

```bash
./scripts/screenshot.js
```

Screenshot the current viewport, returning a temporary file path.

## Pick Elements

```bash
./scripts/pick.js "Click the submit button"
```

Interactive element picker. Click to select, Cmd/Ctrl+Click for multi-select, Enter to finish.

## Dismiss Cookie Dialogs

```bash
./scripts/dismiss-cookies.js          # Accept cookies
./scripts/dismiss-cookies.js --reject # Reject cookies (where possible)
```

Automatically dismisses EU cookie consent dialogs. Supports various common consent frameworks. Run after navigating to a page (with a short delay for dialogs to load):

```bash
./scripts/nav.js https://example.com && sleep 2 && ./scripts/dismiss-cookies.js
```

## Background Logging (Console + Errors + Network)

Automatically started by `start.js` and writes JSONL logs to:

```
~/.cache/agent-web/logs/YYYY-MM-DD/<targetId>.jsonl
```

Manually start:

```bash
./scripts/watch.js
```

Tail the latest log:

```bash
./scripts/logs-tail.js           # dump current log and exit
./scripts/logs-tail.js --follow  # keep following
```

Summarize network responses:

```bash
./scripts/net-summary.js
```

## Best Practices

1. **Always stop browser**: Use `node scripts/stop.js` when done to release resources.
2. **Check port**: Use `node scripts/get-port.js` to see the current port.
3. **Error handling**: If errors occur, restart the browser and retry.
4. **Wait strategies**: Use `wait-for.js` for dynamic content.
5. **Network monitoring**: Use `network.js start/stop` to analyze requests.
6. **Debugging**: Use `debug.js` and `inspect.js` for troubleshooting.

## Process Management

```bash
# View process
ps aux | grep "scraping-web-browser"

# Stop browser
node scripts/stop.js

# Force stop
pkill -f "scraping-web-browser"
```