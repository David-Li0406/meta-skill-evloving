---
name: mre-playwright
description: Automatically create a Minimum Reproducible Example (MRE) using Playwright to reproduce a browser-based bug from a GitHub issue.
---

Create a Minimum Reproducible Example (MRE) using Playwright to reproduce a browser-based bug from a GitHub issue.

## Usage

```
/mre-playwright <issue_url_or_number>
```

## Instructions

### 1. Fetch and Understand the Issue

```bash
gh issue view title,body,comments <number >--json
```

Extract:

- Bug description
- Code snippets from the issue
- Steps to reproduce
- Expected vs actual behavior

### 2. Create MRE Directory

```
claude/<issue_name>/
├── reproduce_<number>.py
└── screenshot_*.png (generated when run)
```

### 3. MRE Script Structure

```python
"""
Playwright reproducer for GitHub issue #<NUMBER>:
<ISSUE_TITLE>

<ISSUE_URL>

Run with: python reproduce_<NUMBER>.py

The bug: <ONE_LINE_DESCRIPTION>
"""

import time
from pathlib import Path

import holoviews as hv
import panel as pn
from playwright.sync_api import sync_playwright

hv.extension("bokeh")
pn.extension()

SCREENSHOT_DIR = Path(__file__).parent


def create_app():
    """Create minimal app that demonstrates the bug.

    Use EXACT code from issue when possible, or simplify while
    preserving the bug trigger conditions.
    """
    # ... app setup
    return app


def serve_app(app, port=5006):
    """Start the app server."""
    return pn.serve(app, port=port, show=False, threaded=True)


def main():
    print("=" * 60)
    print("Reproducer for GitHub issue #<NUMBER>")
    print("<SHORT_DESCRIPTION>")
    print("=" * 60)

    app = create_app()
    port = 5006
    server = serve_app(app, port)
    time.sleep(2)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, slow_mo=100)
            page = browser.new_page()
            page.goto(f"http://localhost:{port}")

            # Wait for app to render
            page.wait_for_selector(".bk-events", timeout=10000)
            time.sleep(1)

            # === STEP 1: Initial State ===
            print("\n--- Step 1: Initial state ---")
            page.screenshot(path=str(SCREENSHOT_DIR / "step1_initial.png"))
            # Capture/print relevant state

            # === STEP 2: Trigger the Bug ===
            print("\n--- Step 2: <ACTION_DESCRIPTION> ---")
            # Interact with the page:
            # page.locator('button:text("Click")').click()
            # page.mouse.click(x, y)
            # page.keyboard.press("Enter")
            time.sleep(0.5)
            page.screenshot(path=str(SCREENSHOT_DIR / "step2_action.png"))

            # === STEP 3: Verify Bug ===
            print("\n--- Step 3: Check for bug ---")
            page.screenshot(path=str(SCREENSHOT_DIR / "step3_result.png"))

            # Bug detection - adapt to your specific bug
            bug_detected = check_for_bug(page)

            print("\n" + "=" * 60)
            if bug_detected:
                print("BUG CONFIRMED!")
                print("  - <DESCRIBE_WHAT_IS_WRONG>")
            else:
                print("Bug not detected (may be fixed)")
            print("=" * 60)

            print(f"\nScreenshots saved in: {SCREENSHOT_DIR}")
            time.sleep(2)
            browser.close()
    finally:
        server.stop()

    print("\nDone.")


def check_for_bug(page):
    """Programmatically verify the bug exists.

    Return True if bug is present, False if not.
    """
    # Example: Check via JavaScript
    # result = page.evaluate("() => { return someCheck(); }")
    # return result["buggy_condition"]

    # Example: Check DOM state
    # element = page.locator(".problematic-element")
    # return element.is_visible() when it shouldn't be

    return False


if __name__ == "__main__":
    main()
```

### 4. Common Interaction Patterns

**Click buttons/elements:**

```python
page.locator('button:text("Submit")').click()
page.locator('[data-testid="my-button"]').click()
page.locator('input[type="checkbox"]').check()
```

**Mouse interactions:**

```python
bbox = page.locator(".canvas").bounding_box()
page.mouse.click(bbox["x"] + 100, bbox["y"] + 100)
page.mouse.dblclick(x, y)
page.mouse.move(x, y)
page.mouse.down()
page.mouse.up()
```

**Keyboard:**

```python
page.keyboard.press("Enter")
page.keyboard.type("text")
page.locator("input").fill("value")
```

**Wait for state:**

```python
page.wait_for_selector(".element")
page.wait_for_timeout(500)
page.locator(".element").wait_for(state="visible")
```

### 5. Bug Detection Patterns

**JavaScript inspection for Bokeh renderers:**

```python
GET_RENDERERS_JS = """() => {
    const doc = window.Bokeh?.documents?.[0];
    if (!doc) return {error: 'No Bokeh document'};

    const renderers = [];
    for (const model of doc._all_models.values()) {
        if (model.type === 'GlyphRenderer') {
            let dataLen = 0;
            if (model.data_source?.data) {
                const keys = Object.keys(model.data_source.data);
                if (keys.length > 0) {
                    dataLen = model.data_source.data[keys[0]].length;
                }
            }
            renderers.push({
                name: model.name || 'unnamed',
                visible: model.visible,
                glyph_type: model.glyph?.type || 'unknown',
                data_length: dataLen
            });
        }
    }
    return {renderers: renderers};
}"""

result = page.evaluate(JS_GET_RENDERERS)
# Check renderer visibility states
patches_hidden = any(r["glyph_type"] == "Patches" and not r["visible"] for r in result["renderers"])
```

**DOM-based checks:**

```python
element = page.locator(".should-be-hidden")
bug_detected = element.is_visible()  # Bug if visible when shouldn't be
```

**Screenshot comparison (visual bugs):**

```python
# Take screenshot and note for manual verification
page.screenshot(path="bug_state.png")
print("Check bug_state.png - element X should not appear")
```

### 6. Principles for Good MREs

1. **Minimal** - Remove all code not needed to trigger the bug
2. **Complete** - Single file, runs with `python reproduce.py`
3. **Exact** - Use issue's code when possible, preserving the trigger
4. **Visual** - Screenshots at each step
5. **Programmatic** - Code that confirms bug exists (not just visual)
6. **Documented** - Clear comments explaining each step

### 7. After Creating

1. Run the script to verify it reproduces the bug
2. Check screenshots show the problem clearly
3. Confirm bug detection logic works
4. Show user the output and screenshots for verification
