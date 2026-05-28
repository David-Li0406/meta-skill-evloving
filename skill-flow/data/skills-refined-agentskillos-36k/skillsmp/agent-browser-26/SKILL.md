---
name: agent-browser
description: Browser automation for AI agents using `npx agent-browser` CLI. Use for testing websites, verifying UI changes, checking console errors, taking screenshots, and automating user flows. Triggers on "browser test", "UI verification", "web automation", "screenshot", "form test".
user-invocable: false
context: fork
agent: Explore
allowed-tools:
  - Bash
  - Read
---

# Agent Browser Skill

Browser automation CLI optimized for AI agents. All commands use `npx agent-browser`.

## Core Workflow

**Always follow: snapshot → identify refs → act → snapshot again**

```bash
npx agent-browser open http://localhost:4321    # Navigate
npx agent-browser snapshot -i                    # Get interactive elements with refs
npx agent-browser click @e2                      # Act using ref from snapshot
npx agent-browser snapshot -i                    # Get updated state
```

**Important:** Always use `snapshot -i` (interactive elements only) by default. This dramatically reduces output by filtering to buttons, links, inputs, and actionable elements.

## Quick Reference

### Navigation
| Command | Description |
|---------|-------------|
| `open <url>` | Navigate to URL |
| `back` | Go back |
| `reload` | Reload page |
| `close` | Close browser |

### Page Analysis
| Command | Description |
|---------|-------------|
| `snapshot -i` | Interactive elements only (preferred) |
| `snapshot` | Full accessibility tree |
| `snapshot -i -c` | Interactive + compact (minimal) |
| `errors` | Check for JS errors |
| `console` | View console logs |

### Interaction
| Command | Description |
|---------|-------------|
| `click @e1` | Click element |
| `fill @e2 "text"` | Clear and type |
| `type @e2 "text"` | Type without clearing |
| `press Enter` | Press key |
| `hover @e3` | Hover element |
| `scroll down 500` | Scroll page |

### Capture
| Command | Description |
|---------|-------------|
| `screenshot` | Screenshot viewport |
| `screenshot --full` | Full page |
| `screenshot /path/file.png` | Save to path |
| `pdf /path/file.pdf` | Save as PDF |

### Get Information
| Command | Description |
|---------|-------------|
| `get text @e1` | Get element text |
| `get url` | Get current URL |
| `get title` | Get page title |
| `get value @e2` | Get input value |

## Common Workflows

### Test Local Dev Server
```bash
npx agent-browser open http://localhost:4321
npx agent-browser snapshot -i
npx agent-browser errors
npx agent-browser screenshot .claude/tmp/screenshots/homepage.png
```

### Test Form Submission
```bash
npx agent-browser snapshot -i
npx agent-browser fill @e3 "test@example.com"
npx agent-browser fill @e4 "message"
npx agent-browser click @e5
npx agent-browser snapshot -i
```

### Test Navigation Flow
```bash
npx agent-browser snapshot -i
npx agent-browser click @e5
npx agent-browser snapshot -i
```

## Snapshot Output Format

```
- document:
  - button "Toggle theme" [ref=e1]
  - main:
    - heading "Title" [ref=e2] [level=1]
    - link "About" [ref=e3]:
      - /url: /about
    - textbox "Email" [ref=e4]
```

- `[ref=eN]` - Element reference for targeting
- `/url:` - Link href
- `[level=N]` - Heading level

## Snapshot Options

| Flag | Purpose |
|------|---------|
| `-i` | Interactive elements only (recommended) |
| `-c` | Compact output |
| `-d 3` | Limit tree depth |
| `-s "#main"` | Scope to CSS selector |

## Alternative Selectors

When refs aren't available:
```bash
npx agent-browser click "#submit"           # CSS selector
npx agent-browser click "text=Sign In"      # Text content
```

## Sessions (Multiple Browsers)

```bash
npx agent-browser --session test1 open site-a.com
npx agent-browser --session test2 open site-b.com
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Browser not installed | `npx agent-browser install` |
| Element not found | Run `snapshot` again - refs change on update |
| Page still loading | `npx agent-browser wait 2000` or `wait --load networkidle` |

## Notes

- Save screenshots to `.claude/tmp/screenshots/`
- Refs (`@e1`, `@e2`) are stable identifiers from snapshots
- Prefer refs over CSS selectors when possible
