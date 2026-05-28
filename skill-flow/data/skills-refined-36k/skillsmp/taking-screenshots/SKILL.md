---
name: Taking Screenshots
description: Use Playwright MCP for browser screenshots. Desktop screenshots not supported.
---

# Taking Screenshots

## Browser Screenshots

Use the Playwright MCP `browser_take_screenshot` tool to capture browser content:

```
browser_take_screenshot
  - filename: optional, defaults to page-{timestamp}.png
  - fullPage: true to capture full scrollable page
  - type: "png" or "jpeg"
```

**Workflow:**
1. `browser_navigate` to the page you want to capture
2. `browser_take_screenshot` to save the image
3. The screenshot is saved and can be referenced

## Desktop Screenshots

Desktop screenshots (outside the browser) are **not supported** in this profile. The platform-specific CLI tools (screencapture on macOS, gnome-screenshot on Linux) are not cross-platform compatible.

If you need desktop screenshots, ask the user to take one manually and provide the file path.
