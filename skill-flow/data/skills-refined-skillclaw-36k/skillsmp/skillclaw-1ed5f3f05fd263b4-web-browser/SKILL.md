---
name: web-browser
description: Use this skill when you need to interact with web pages by performing actions such as clicking buttons, filling out forms, and navigating links through remote control of Chrome or Chromium browsers using the Chrome DevTools Protocol (CDP).
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

Screenshot the current viewport, returning the temporary file path.

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

Automatically dismisses EU cookie consent dialogs. Supports various consent frameworks. Run after navigating to a page (with a short delay for dialogs to load):

```bash
./scripts/nav.js https://example.com && sleep 2 && ./scripts/dismiss-cookies.js
```

## Debug Mode

Set `DEBUG=1` to enable verbose logging to stderr:

```bash
DEBUG=1 ./scripts/nav.js https://example.com
```