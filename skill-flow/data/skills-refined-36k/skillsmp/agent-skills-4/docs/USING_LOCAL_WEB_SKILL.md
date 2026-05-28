# Using the Local-Web Skill with AI Agents

This guide explains how to enable AI coding agents (Codex CLI, Claude Code, Cursor, etc.) to view and interact with local/LAN web pages they normally cannot access.

## The Problem

Cloud-based AI agents make HTTP requests through cloud servers. This means they **cannot access**:
- `localhost:3000` - Your local dev server
- `192.168.x.x` - Devices on your LAN
- `10.0.0.x` - Private network addresses
- `mydevice.local` - mDNS hostnames

When you ask an AI agent to fetch `http://localhost:3000/`, it fails because the cloud server can't reach your machine.

## The Solution: Local-Web Skill

The `local-web` skill (in the `networks` module) provides CLI commands that run **locally** and can access any URL your machine can reach.

## Installation

### Step 1: Install the Networks Module

```bash
cd ~/scripts
pip install -e modules/networks/
```

### Step 2: Install Browser Dependencies (for screenshots/interaction)

```bash
pip install playwright
playwright install firefox
```

### Step 3: Verify Installation

```bash
networks --help
networks web-fetch --help
```

## Using with Codex CLI

### Option 1: Tell Codex About the Skill

When starting a session, inform Codex about the available commands:

```
I have a local-web skill installed that lets you access local/LAN URLs.
Use these commands:

- `networks web-fetch <url> --json` - Fetch HTML from local URL
- `networks web-list <url> --element-type button` - List buttons on page
- `networks web-screenshot <url> -o <path>` - Screenshot a page
- `networks web-interact <url> --action click --selector "<text>"` - Click elements
- `networks web-crawl <url> --max-pages 10` - Crawl and screenshot

My local server is at http://localhost:3000/
Please use these tools to view and interact with it.
```

### Option 2: Add SKILL.md to Your Project

Copy the skill definition to your project so Codex auto-discovers it:

```bash
# In your project directory
mkdir -p .codex/skills
cp ~/scripts/modules/networks/SKILL.md .codex/skills/local-web.md
```

Or create a symlink:
```bash
ln -s ~/scripts/modules/networks/SKILL.md .codex/skills/local-web.md
```

### Option 3: Install as Global Skill (Codex)

```bash
# Add to Codex global skills directory
mkdir -p ~/.codex/skills
cp ~/scripts/modules/networks/SKILL.md ~/.codex/skills/local-web.md
```

## Step-by-Step: Agent Viewing a Local Web Page

### 1. Agent Lists Available Elements

```bash
$ networks web-list http://localhost:3000/ --element-type button
Found 47 button elements on http://localhost:3000/:
  1. [button] Dashboard → .nav-btn
  2. [button] Settings → .nav-btn
  3. [button] Submit → #submit-btn
  ...
```

### 2. Agent Takes a Screenshot

```bash
$ networks web-screenshot http://localhost:3000/ -o /tmp/page.png
✓ Screenshot saved: /tmp/page.png (1280x720)
```

### 3. Agent Clicks a Button

```bash
$ networks web-interact http://localhost:3000/ --action click --selector "Settings"
✓ click on Settings
  Elements found: 1
  Before: /tmp/interact_abc123_before.png
  After: /tmp/interact_abc123_after.png
```

### 4. Agent Gets HTML Content

```bash
$ networks web-fetch http://localhost:3000/api/status --json
{
  "url": "http://localhost:3000/api/status",
  "success": true,
  "status_code": 200,
  "content_type": "application/json",
  "content": "{\"status\": \"ok\", \"version\": \"1.2.3\"}",
  ...
}
```

### 5. Agent Crawls the Site

```bash
$ networks web-crawl http://localhost:3000/ --max-pages 5 -o ./crawl_output/
✓ Crawled 5 pages from http://localhost:3000/
  - Home: http://localhost:3000/
  - Dashboard: http://localhost:3000/dashboard
  - Settings: http://localhost:3000/settings
  ...
```

## Example Session with Claude Code

```
User: I have a web app running at http://localhost:3000/. Can you check what's on the homepage?

Claude: I'll use the local-web skill to access your local server.

$ networks web-fetch http://localhost:3000/ --content-only | head -50
<!DOCTYPE html>
<html>
<head><title>My App</title></head>
<body>
  <h1>Welcome to My App</h1>
  <nav>
    <button>Dashboard</button>
    <button>Settings</button>
  </nav>
  ...

The homepage shows "My App" with navigation buttons for Dashboard and Settings.

User: Can you click on Settings and show me what's there?

Claude: I'll click the Settings button and take a screenshot.

$ networks web-interact http://localhost:3000/ --action click --selector "Settings"
✓ click on Settings
  Elements found: 1
  After: /tmp/interact_settings_after.png

$ networks web-list http://localhost:3000/settings --element-type input
Found 5 input elements:
  1. [input] → #username
  2. [input] → #email
  3. [input] → #theme-select
  ...

The Settings page has input fields for username, email, and theme selection.
```

## Available Commands

| Command | Description |
|---------|-------------|
| `networks web-fetch <url>` | Fetch HTML content |
| `networks web-check <url>` | Check if URL is accessible |
| `networks web-screenshot <url>` | Take a screenshot |
| `networks web-list <url>` | List interactive elements |
| `networks web-interact <url>` | Click, type, hover, scroll |
| `networks web-crawl <url>` | Crawl site with screenshots |

### Common Options

- `--json` / `-j` - Output as JSON (LLM-optimized)
- `--browser firefox|chromium|webkit` - Choose browser (default: firefox)
- `--timeout SECONDS` - Set timeout

## Troubleshooting

### "playwright not installed"

```bash
pip install playwright
playwright install firefox
```

### "Browser launch failed" (libasound.so.2 error on Linux)

Use Firefox instead of Chromium:
```bash
playwright install firefox
networks web-screenshot http://localhost:3000/ --browser firefox
```

Or install missing dependencies:
```bash
sudo apt-get install libasound2
```

### "connection refused"

The server isn't running:
```bash
networks web-check http://localhost:3000/
# ✗ localhost:3000 connection refused
```

Start your server first!

## How It Works

1. **AI agent** runs in the cloud, cannot access local URLs
2. **Agent calls** `networks web-fetch http://localhost:3000/`
3. **Command runs locally** on your machine via shell
4. **Local machine** fetches the URL successfully
5. **Output returned** to the agent through shell stdout

The agent never directly accesses the URL - it uses your local machine as a proxy through CLI commands.

## See Also

- [SKILL.md](../scripts/modules/networks/SKILL.md) - Full skill documentation
- [README.md](../scripts/modules/networks/README.md) - Networks module documentation
- [Agent Skills Spec](https://agentskills.io) - Agent Skills specification
