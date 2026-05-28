---
name: web-browser
description: Use this skill to interact with web pages by performing actions such as clicking buttons, filling out forms, and navigating links through remote control of Google Chrome or Chromium browsers using the Chrome DevTools Protocol (CDP).
---

# Web Browser Skill

Full-featured browser automation with CDP tools for collaborative site exploration.

## Start Chrome

```bash
./scripts/start.js              # Start Chrome with a fresh profile
./scripts/start.js --profile    # Start Chrome with your existing profile (cookies, logins)
```

Start Chrome on a random port (9222-9999) with remote debugging.

## Navigation

```bash
./scripts/nav.js https://example.com          # Navigate to a URL
./scripts/nav.js https://example.com --new     # Open a new tab with a URL
```

## Evaluate JavaScript

```bash
./scripts/eval.js 'document.title'                             # Get the page title
./scripts/eval.js 'document.querySelectorAll("a").length'    # Count links on the page
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

Automatically dismisses EU cookie consent dialogs. Run after navigating to a page.

## Background Logging

Automatically started by `start.js` and writes JSONL logs to:

```
~/.cache/agent-web/logs/YYYY-MM-DD/<targetId>.jsonl
```

Manually start logging:

```bash
./scripts/watch.js
```

Tail the latest log:

```bash
./scripts/logs-tail.js           # Dump current log and exit
./scripts/logs-tail.js --follow  # Keep following
```

Summarize network responses:

```bash
./scripts/net-summary.js
```

## Best Practices

1. **Always stop browser**: Use `node scripts/stop.js` when done to release resources.
2. **Check port**: Use `node scripts/get-port.js` to see the current port.
3. **Error handling**: If errors occur, restart the browser and retry.
4. **Persistence**: All data (cookies, localStorage, sessions) persists in `~/.cache/scraping-web-browser/`.
5. **Wait strategies**: Use `wait-for.js` for dynamic content.
6. **Network monitoring**: Use `network.js start/stop` to analyze requests.
7. **Debugging**: Use `debug.js` and `inspect.js` for troubleshooting.

## Configuration Directory

- **Config**: `~/.cache/scraping-web-browser/`
- **Port file**: `~/.cache/scraping-web-browser/port.txt`
- **Cookies**: `~/.cache/scraping-web-browser/Default/Cookies`
- **LocalStorage**: `~/.cache/scraping-web-browser/Default/Local Storage/`