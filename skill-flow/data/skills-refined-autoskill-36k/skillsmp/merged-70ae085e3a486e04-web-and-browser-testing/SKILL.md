---
name: web-and-browser-testing
description: Use this skill when you need to interact with and test local web applications using Playwright, supporting UI testing, screenshot management, server management, and browser log capturing.
---

# Web and Browser Testing

This skill provides a comprehensive toolkit for testing local web applications using Playwright. It supports UI testing, screenshot management, server management, and capturing browser logs.

## Testing Workflow

To test a local web application, write native Python Playwright scripts.

### Available Helper Scripts
- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)

**Always run the script with `--help`** to see usage instructions before attempting to run it directly. These scripts are designed to be called as black-box scripts rather than being included in your context window.

## Decision Tree: Choose Your Method

```
User Task → Is it a static HTML?
    ├─ Yes → Read the HTML file directly to identify selectors
    │         ├─ Success → Write Playwright scripts using these selectors
    │         └─ Failure/Incomplete → Handle as a dynamic application (see below)
    │
    └─ No (Dynamic Web Application) → Is the server running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write concise Playwright scripts
        │
        └─ Yes → Scout first, then operate:
            1. Navigate and wait for network idle
            2. Take screenshots or inspect the DOM
            3. Identify selectors from the rendered state
            4. Perform actions using the discovered selectors
```

## Example: Using with_server.py

To start the server, first run `--help`, then use the helper:

**Single Server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Multiple Servers (e.g., backend + frontend):**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

When writing automation scripts, include only Playwright logic (the server is managed by the helper):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Always start chromium in headless mode
    page = browser.new_page()
    page.goto('http://localhost:5173')  # Server is running and ready
    page.wait_for_load_state('networkidle')  # Key: wait for JS execution
    # ... your automation logic
    browser.close()
```

## Screenshot Management

### Quick Screenshot Command
```bash
python commands/screenshot.py <url> [output.png] [--login]
```

### Console Check Command
```bash
python commands/console-check.py <url> [--login] [--wait N]
```

### Discover Page Elements Command
```bash
python commands/discover.py <url> [--login]
```

### Run Test Command
```bash
python commands/run-test.py <script.py> [--server "cmd" --port N]
```

## Best Practices

- **Use bundled scripts as black boxes** - When handling tasks, consider if there are existing scripts in `scripts/` that can reliably handle common and complex workflows without polluting your context window. Use `--help` to see usage, then call directly.
- Use `sync_playwright()` for synchronous scripts.
- Always close the browser after completion.
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs.
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`.

## Common Pitfalls

❌ Do not check the DOM before waiting for `networkidle` in dynamic applications.  
✅ Always wait for `page.wait_for_load_state('networkidle')` before checking.

## Directory Structure

**Project Structure:**
```
project/
├── .env.test                              # Test credentials (do not commit)
├── .env.test.example                      # Template (can commit)
└── browser-tests/
    ├── 2026-01-09-001-crm-autofill/
    │   ├── test_crm_autofill.py           # Test script
    │   ├── result.html                     # Test report
    │   └── screenshots/                    # Screenshots
    │       ├── 01_login.png
    │       └── 02_result.png
    └── 2026-01-09-002-phone-extraction/
        ├── test_phone_extraction.py
        ├── result.html
        └── screenshots/
```

**Skill Directory:**
```
~/.claude/skills/browser-testing/
├── SKILL.md
├── commands/
│   ├── screenshot.py
│   ├── discover.py
│   └── run-test.py
├── scripts/
│   └── with_server.py
└── examples/
    └── ...
```

## Conclusion

This skill provides a robust framework for testing web applications, ensuring that you can effectively manage server lifecycles, capture browser logs, and automate UI interactions with Playwright.