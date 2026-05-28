---
name: webapp-browser-testing
description: Use this skill when you need to interact with and test local web applications using Playwright, including UI testing, screenshot capture, and server management.
---

# Web Application Browser Testing

This skill provides a comprehensive toolkit for testing local web applications using Playwright. It supports UI testing, screenshot capture, server management, and browser log retrieval.

## Setup

1. **Install Playwright**: Ensure you have Playwright installed in your Python environment.
   ```bash
   pip install playwright
   playwright install
   ```

2. **Server Management**: Use the provided scripts to manage your server lifecycle.
   - To start a server, run:
     ```bash
     python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
     ```

## Testing Workflow

### Decision Tree for Testing

```
User Task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using these selectors
    │         └─ Failure/Incomplete → Handle as dynamic application (see below)
    │
    └─ No (Dynamic Web Application) → Is the server running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write a streamlined Playwright script
        │
        └─ Yes → Scout first, then act:
            1. Navigate and wait for network idle
            2. Take a screenshot or inspect the DOM
            3. Identify selectors from the rendered state
            4. Perform actions using the discovered selectors
```

### Example: Using with_server.py

To start the server and run your automation script:
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

### Playwright Script Example

Here’s a basic example of a Playwright script:
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Always start in headless mode
    page = browser.new_page()
    page.goto('http://localhost:5173')  # Ensure the server is running and ready
    page.wait_for_load_state('networkidle')  # Important: wait for JS execution
    # ... your automation logic
    browser.close()
```

### Common Commands

- **Console Check**: Check for console errors.
  ```bash
  python commands/console-check.py <url> [--login] [--wait N]
  ```

- **Screenshot**: Capture a screenshot of a page.
  ```bash
  python commands/screenshot.py <url> [output.png] [--login]
  ```

- **Discover Elements**: Explore page elements.
  ```bash
  python commands/discover.py <url> [--login]
  ```

### Best Practices

- Use bundled scripts as black boxes to handle common workflows without cluttering your context.
- Always close the browser after tests.
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs.
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`.

## Cleanup Commands

To clean up test directories:
```bash
# Clean all test subprojects
rm -rf browser-tests/20*/

# Clean specific date
rm -rf browser-tests/2026-01-09-*/ 
```

## References

- **Examples**: Check the `examples/` directory for common patterns and tutorials.
- **Documentation**: Refer to Playwright's official documentation for advanced usage and features.