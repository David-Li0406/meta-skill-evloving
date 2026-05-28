---
name: firefox-browser
description: Use this skill to control the user's Firefox browser with their logins and cookies intact, allowing for browsing, interacting with authenticated pages, filling forms, clicking buttons, taking screenshots, and retrieving page content.
---

# Firefox Browser Agent Bridge

Control the user's actual Firefox browser session via WebSocket. This uses their real browser with existing logins and cookies - **not** a headless browser.

## Quick Start

```bash
# 0. If Firefox isn't running, start it first
nohup firefox &>/dev/null &

# 1. Check connection
browser ping

# 2. See what tabs are open
browser listTabs '{}'

# 3. Start a new session (recommended)
browser newSession '{"url": "https://example.com"}'

# 4. Read the page with interactable elements marked
browser getContent '{"format": "annotated"}'
```

## Client Usage

```bash
browser <action> '<json_params>'
```

## Actions Reference

### Session & Tab Management

| Action       | Description                               | Key Params                  |
|--------------|-------------------------------------------|-----------------------------|
| `listTabs`   | List all open tabs across windows         | -                           |
| `newSession` | Create new tab to work in                 | `url` (optional)           |
| `setActiveTab` | Switch which tab agent works on         | `tabId`, `focus`           |
| `getActiveTab` | Get current tab info                    | -                           |

### Navigation & Page Info

| Action         | Description                               | Key Params                  |
|----------------|-------------------------------------------|-----------------------------|
| `navigate`     | Go to URL in current tab                  | `url`, `wait`, `newTab`    |
| `getContent`   | Get page content                          | `format`: `annotated`, `text`, `html` |
| `getInteractables` | List clickable elements and inputs   | `selector` (optional scope) |
| `screenshot`   | Capture visible area as PNG               | `filename` (optional)       |

### Interaction

| Action         | Description                               | Key Params                  |
|----------------|-------------------------------------------|-----------------------------|
| `click`        | Click element                             | `selector`, `text`, or `x`/`y` coords |
| `type`         | Type into focused/selected input         | `selector`, `text`, `submit`, `clear` |
| `fillForm`     | Fill form fields (inputs, textareas, selects) | `fields[]` array with selector/value |
| `waitFor`      | Wait for element/text                     | `selector`, `text`, `timeout` |

#### fillForm - The Right Way to Fill Forms

**IMPORTANT:** There is no `fill` command. Use `fillForm` with a `fields` array:

```bash
# Fill a single field
browser fillForm '{"fields": [{"selector": "#email", "value": "test@example.com"}]}'

# Fill multiple fields at once (text inputs, textareas, AND select dropdowns)
browser fillForm '{"fields": [
  {"selector": "#email", "value": "test@example.com"},
  {"selector": "#password", "value": "securepassword"}
]}'
```