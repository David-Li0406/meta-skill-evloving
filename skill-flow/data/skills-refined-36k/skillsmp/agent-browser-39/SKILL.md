---
name: agent-browser
description: Headless browser automation CLI optimized for AI agents. Use when automating multi-step browser workflows, web scraping, form filling, or testing SPAs. Uses accessibility tree snapshots with ref-based element selection for deterministic actions. Requires `agent-browser` CLI (npm install -g agent-browser).
---

# Agent Browser Skill

Fast browser automation using accessibility tree snapshots with refs for deterministic element selection.

## Core Workflow

```bash
# 1. Navigate and snapshot
agent-browser open https://example.com
agent-browser snapshot -i --json

# 2. Parse refs from JSON, then interact
agent-browser click @e2
agent-browser fill @e3 "text"

# 3. Re-snapshot after page changes
agent-browser snapshot -i --json
```

## Key Commands

### Navigation
```bash
agent-browser open <url>
agent-browser back | forward | reload | close
```

### Snapshot (Always use -i --json)
```bash
agent-browser snapshot -i --json          # Interactive elements, JSON output
agent-browser snapshot -i -c -d 5 --json  # + compact, depth limit
agent-browser snapshot -s "#main" -i      # Scope to selector
```

### Interactions (Ref-based)
```bash
agent-browser click @e2
agent-browser fill @e3 "text"
agent-browser type @e3 "text"
agent-browser hover @e4
agent-browser check @e5 | uncheck @e5
agent-browser select @e6 "value"
agent-browser press "Enter"
agent-browser scroll down 500
```

### Get Information
```bash
agent-browser get text @e1 --json
agent-browser get html @e2 --json
agent-browser get value @e3 --json
agent-browser get attr @e4 "href" --json
agent-browser get title --json
agent-browser get url --json
```

### Check State
```bash
agent-browser is visible @e2 --json
agent-browser is enabled @e3 --json
agent-browser is checked @e4 --json
```

### Wait
```bash
agent-browser wait @e2                    # Wait for element
agent-browser wait 1000                   # Wait ms
agent-browser wait --text "Welcome"       # Wait for text
agent-browser wait --load networkidle     # Wait for network
```

### Sessions (Isolated Browsers)
```bash
agent-browser --session admin open site.com
agent-browser --session user open site.com
agent-browser session list
```

### State Persistence
```bash
agent-browser state save auth.json        # Save cookies/storage
agent-browser state load auth.json        # Load (skip login)
```

### Screenshots
```bash
agent-browser screenshot page.png
agent-browser screenshot --full page.png  # Full page
```

## Snapshot Output Format

```json
{
  "success": true,
  "data": {
    "snapshot": "...",
    "refs": {
      "e1": {"role": "heading", "name": "Example Domain"},
      "e2": {"role": "button", "name": "Submit"},
      "e3": {"role": "textbox", "name": "Email"}
    }
  }
}
```

## Best Practices

1. **Always use `-i` flag** - Focus on interactive elements
2. **Always use `--json`** - Easier to parse
3. **Wait for stability** - `agent-browser wait --load networkidle`
4. **Save auth state** - Skip login flows with `state save/load`
5. **Use sessions** - Isolate different browser contexts

## Example: Form Automation

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i --json
# AI identifies: @e2=name, @e3=email, @e4=submit
agent-browser fill @e2 "John Doe"
agent-browser fill @e3 "john@example.com"
agent-browser click @e4
agent-browser wait --text "Success"
```

## Installation

```bash
npm install -g agent-browser
agent-browser install                     # Download Chromium
agent-browser install --with-deps         # Linux: + system deps
```

## Credits

Skill created by Yossi Elkrief ([@MaTriXy](https://github.com/MaTriXy))

agent-browser CLI by [Vercel Labs](https://github.com/vercel-labs/agent-browser)
