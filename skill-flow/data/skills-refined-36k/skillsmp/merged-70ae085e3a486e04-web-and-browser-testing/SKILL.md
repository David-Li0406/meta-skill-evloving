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

**Always run the script with `--help` first** to see usage instructions. Avoid reading the source code directly as it may be extensive and clutter your context window. These scripts are designed to be called directly as black-box scripts.

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

When writing automation scripts, include only Playwright logic (the server is managed automatically by the helper):
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

### Example Usage
```bash
# Capture a public page
python commands/screenshot.py http://localhost:3000 homepage.png

# Capture a page that requires login
python commands/screenshot.py http://localhost:3000/dashboard dashboard.png --login
```

## Console Check Command
```bash
python commands/console-check.py <url> [--login] [--wait N]
```

### Example Usage
```bash
# Check homepage (requires login)
python commands/console-check.py http://localhost:3000 --login

# Check a specific page, waiting 10 seconds for stability
python commands/console-check.py http://localhost:3000/inbox --login --wait 10
```

## Discover Command
```bash
python commands/discover.py <url> [--login]
```

### Example Usage
```bash
# Discover elements on a public page
python commands/discover.py http://localhost:3000

# Discover elements on a page that requires login
python commands/discover.py http://localhost:3000/dashboard --login
```

## TestManager API

Provides an API for screenshot management and test report generation.

### Basic Usage
```python
from browser_testing import TestManager
import os

BASE_URL = os.getenv('TEST_BASE_URL', 'http://localhost:3000')

with TestManager() as tm:
    page = tm.page  # Playwright page object

    page.goto(f'{BASE_URL}/login')
    tm.capture('Login Page')  # Screenshot: screenshots/01_Login Page.png

    page.fill('input[type="email"]', 'test@example.com')
    page.fill('input[type="password"]', 'password')
    tm.capture('Filled Form')

    page.click('button[type="submit"]')
    page.wait_for_load_state('networkidle')
    tm.capture('Login Successful')

# Automatically:
# 1. Close the browser
# 2. Generate reports in test-reports/
```

### Common Practices
- **Use helper scripts as black boxes** - When handling tasks, check if there are existing scripts in `scripts/` that can reliably handle common and complex workflows without cluttering your context window. Use `--help` to see usage, then call directly.
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs.
- Always close the browser after completion.
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`.

## Common Pitfalls
- ❌ In dynamic applications, do not check the DOM before waiting for `networkidle`.
- ✅ Always wait for `page.wait_for_load_state('networkidle')` before checking.

## Directory Structure
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

**Skill Internal Structure**:
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