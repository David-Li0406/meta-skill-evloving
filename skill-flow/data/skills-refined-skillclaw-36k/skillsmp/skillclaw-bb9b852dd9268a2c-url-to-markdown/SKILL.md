---
name: url-to-markdown
description: Use this skill when you want to fetch any URL and convert it to markdown, supporting both auto-capture on page load and user-triggered capture for pages requiring login.
---

# URL to Markdown

Fetches any URL via Chrome CDP and converts HTML to clean markdown.

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/main.ts` | CLI entry point for URL fetching |

## Features

- Chrome CDP for full JavaScript rendering
- Two capture modes: auto or wait-for-user
- Clean markdown output with metadata
- Handles login-required pages via wait mode

## Usage

```bash
# Auto mode (default) - capture when page loads
npx -y bun ${SKILL_DIR}/scripts/main.ts <url>

# Wait mode - wait for user signal before capture
npx -y bun ${SKILL_DIR}/scripts/main.ts <url> --wait

# Save to specific file
npx -y bun ${SKILL_DIR}/scripts/main.ts <url> -o output.md
```

## Options

| Option | Description |
|--------|-------------|
| `<url>` | URL to fetch |
| `-o <path>` | Output file path (default: auto-generated) |
| `--wait` | Wait for user signal before capturing |
| `--timeout <ms>` | Page load timeout (default: 30000) |

## Capture Modes

### Auto Mode (default)

Page loads → waits for network idle → captures immediately.

Best for:
- Public pages
- Static content
- No login required

### Wait Mode (`--wait`)

Page opens → user can interact (login, scroll, etc.) → user signals ready → captures.

Best for:
- Login-required pages
- Dynamic content needing interaction
- Pages with lazy loading

**Agent workflow for wait mode**:
1. Run script with `--wait` flag
2. Script outputs: `Page opened. Press Enter when ready to capture...`
3. Use `AskUserQuestion` to ask user if page is ready
4. When user confirms, send newline to stdin to trigger capture

## Output Format

```markdown
---
url: https://example.com/page
title: "Page Title"
description: "Meta description if available"
author: "Author if available"
published: "2024-01-01"
captured_at: "2024-01-15T10:30:00Z"
---

# Page Title

Converted markdown content...
```

## Mode Selection Guide

When user requests URL capture, choose the appropriate mode based on the page's requirements.