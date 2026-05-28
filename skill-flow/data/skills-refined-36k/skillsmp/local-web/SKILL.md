---
name: local-web
description: Access local/LAN URLs that cloud AI agents cannot reach. Fetch HTML content, take screenshots, interact with page elements, crawl sites, and list UI elements for private network addresses (192.168.x.x, localhost, etc). Use when user asks about local servers, development servers, internal tools, or any URL on private/LAN networks that returns "connection refused" from agent fetch tools.
metadata:
  short-description: Fetch and interact with local/LAN URLs
  author: mcarls
  version: "0.3.0"
compatibility: Python 3.8+, Linux/macOS/Windows, optional playwright for browser automation
---

# Local Web Access

## Overview

Cloud-based AI agents (Claude, Codex, etc.) cannot access private network URLs because their requests go through cloud servers. This skill runs locally on the user's machine and can access any URL their machine can reach.

- Fetch HTML content from local/LAN URLs
- Take screenshots using headless browser (Firefox/Chromium/WebKit)
- List interactive elements (buttons, links, inputs, forms)
- Click buttons, type text, and observe effects
- Crawl sites automatically with screenshots
- LLM-optimized JSON output or human-readable output

## When to Use This Skill

Use this skill when:
- User asks about content on `localhost`, `127.0.0.1`, or `192.168.x.x` URLs
- User asks about their local development server
- User mentions internal tools or dashboards
- Agent's built-in web fetch returns "connection refused" for local URLs
- User needs screenshots of local web apps
- User wants to interact with a local web UI (click buttons, fill forms)
- User wants to discover what elements are on a page

## Quick Start

```bash
# Install the networks module
pip install -e /path/to/networks

# For browser features (screenshots, interact, crawl, list)
pip install playwright && playwright install firefox

# Fetch HTML from local URL (JSON output for agents)
networks web-fetch http://localhost:3000/ --json

# List all buttons on a page
networks web-list http://localhost:3000/ --element-type button

# Take screenshot
networks web-screenshot http://localhost:3000/ -o screenshot.png

# Click a button and see before/after screenshots
networks web-interact http://localhost:3000/ --action click --selector "Stats"

# Crawl a site with screenshots
networks web-crawl http://localhost:3000/ --max-pages 10 -o ./crawl_output/
```

## Commands

### web-fetch - Fetch HTML Content

Fetches HTML content from any URL accessible from the local machine.

```bash
networks web-fetch <url> [options]
```

Options:
- `-t, --timeout SECONDS` - Request timeout (default: 10)
- `-j, --json` - Output as JSON (LLM-optimized)
- `-c, --content-only` - Output only HTML content (no metadata)
- `-H, --headers` - Include response headers in output
- `-k, --insecure` - Skip SSL verification (for self-signed certs)

Examples:
```bash
# Fetch local React dev server
networks web-fetch http://localhost:3000/ --json

# Fetch with headers for debugging
networks web-fetch http://192.168.1.50:8080/api/status --headers --json

# Fetch self-signed HTTPS
networks web-fetch https://localhost:8443/ --insecure --json
```

JSON Output:
```json
{
  "url": "http://localhost:3000/",
  "success": true,
  "status_code": 200,
  "content_type": "text/html; charset=utf-8",
  "content": "<!DOCTYPE html>...",
  "content_length": 1234,
  "headers": null,
  "error": null
}
```

### web-check - Check Connectivity

Quick connectivity check before attempting a full fetch.

```bash
networks web-check <url> [options]
```

Options:
- `-t, --timeout SECONDS` - Connection timeout (default: 5)
- `-j, --json` - Output as JSON

Examples:
```bash
# Check if dev server is running
networks web-check http://localhost:3000/

# Check LAN device
networks web-check http://192.168.1.100:80/ --json
```

### web-screenshot - Capture Screenshots

Take a visual screenshot of a webpage using headless browser.

**Prerequisite:** Install playwright
```bash
pip install playwright
playwright install firefox  # or chromium
```

```bash
networks web-screenshot <url> [options]
```

Options:
- `-o, --output PATH` - Output file path (default: temp file)
- `-w, --width INT` - Viewport width (default: 1280)
- `-H, --height INT` - Viewport height (default: 720)
- `-v, --viewport-only` - Only capture viewport (not full page)
- `-t, --timeout SECONDS` - Page load timeout (default: 30)
- `-b, --base64` - Include base64 image in output for LLM viewing
- `-B, --browser` - Browser to use: firefox, chromium, webkit (default: firefox)
- `-j, --json` - Output as JSON

Examples:
```bash
# Screenshot local dashboard
networks web-screenshot http://localhost:3000/ -o dashboard.png

# Get base64 for inline LLM viewing
networks web-screenshot http://localhost:8080/ --base64 --json

# Use chromium instead of firefox
networks web-screenshot http://localhost:3000/ -o shot.png --browser chromium
```

### web-list - List Interactive Elements

Discover buttons, links, inputs, and forms on a page.

```bash
networks web-list <url> [options]
```

Options:
- `-e, --element-type` - Type to find: button, link, input, form, all (default: all)
- `-t, --timeout SECONDS` - Page load timeout (default: 30)
- `-B, --browser` - Browser to use (default: firefox)
- `-j, --json` - Output as JSON

Examples:
```bash
# List all buttons
networks web-list http://localhost:3000/ --element-type button

# List all interactive elements as JSON
networks web-list http://localhost:3000/ --json

# Find all forms
networks web-list http://localhost:3000/ -e form
```

### web-interact - Interact with Page Elements

Click buttons, type text, hover, scroll, and observe effects with before/after screenshots.

```bash
networks web-interact <url> [options]
```

Options:
- `-a, --action` - Action: click, type, hover, scroll, wait (default: click)
- `-s, --selector` - CSS selector or text to find element
- `-T, --text` - Text to type (for type action) or text content to find
- `-w, --wait SECONDS` - Wait after action for effects (default: 1)
- `-t, --timeout SECONDS` - Page load timeout (default: 30)
- `-B, --browser` - Browser to use (default: firefox)
- `-j, --json` - Output as JSON

Examples:
```bash
# Click a button by text
networks web-interact http://localhost:3000/ --action click --selector "Submit"

# Type into an input field
networks web-interact http://localhost:3000/ --action type --selector "#search" --text "query"

# Hover over an element
networks web-interact http://localhost:3000/ --action hover --selector ".menu-item"

# Scroll the page
networks web-interact http://localhost:3000/ --action scroll
```

### web-crawl - Crawl a Site

Automatically discover pages and capture screenshots.

```bash
networks web-crawl <url> [options]
```

Options:
- `-n, --max-pages INT` - Maximum pages to crawl (default: 20)
- `-o, --output-dir PATH` - Directory to save screenshots
- `--no-screenshots` - Skip screenshots (faster)
- `-t, --timeout SECONDS` - Timeout per page (default: 30)
- `-B, --browser` - Browser to use (default: firefox)
- `-j, --json` - Output as JSON

Examples:
```bash
# Crawl and screenshot up to 10 pages
networks web-crawl http://localhost:3000/ --max-pages 10 -o ./crawl_output/

# Quick crawl without screenshots
networks web-crawl http://localhost:3000/ --no-screenshots --json
```

## Python API

The module can also be used programmatically:

```python
from networks import fetch_url, screenshot_url, check_local_access, is_local_url

# Check if URL is local/private
if is_local_url("http://192.168.1.1/"):
    print("This is a local URL")

# Fetch content
result = fetch_url("http://localhost:3000/", timeout=10)
if result.success:
    print(result.content)
else:
    print(f"Error: {result.error}")

# Check connectivity
accessible, message = check_local_access("http://localhost:8080/")
print(message)

# Screenshot (requires playwright)
result = screenshot_url("http://localhost:3000/", output_path="shot.png")
print(f"Saved to: {result.output_path}")
```

## Troubleshooting

### "connection refused"
- The service isn't running on that port
- Run: `networks web-check <url>` to verify

### "timeout"
- Service is slow or not responding
- Try: `networks web-fetch <url> -t 30` for longer timeout

### "playwright not installed" (for screenshots)
- Run: `pip install playwright && playwright install chromium`

### SSL certificate errors
- For self-signed certs: `networks web-fetch <url> --insecure`
