# SuperThings

An intelligent Things 3 integration for Claude Code that learns from your corrections and gets better over time.

> **Fork of [hildersantos/things-mcp](https://github.com/hildersantos/things-mcp)** with silent AppleScript operations, learning system, and Claude Code commands.

## What's New in SuperThings

### Learning System
SuperThings learns from your corrections during inbox triage:
- **Title transforms**: Patterns like "Fix X" → "Delegate to Brianna: Fix X"
- **Project hints**: Keywords → project mappings with confidence scores
- **Exact overrides**: Specific title → transformation mappings

Suggestions show `[learned: Nx]` when based on patterns you've taught it.

### GTD Research Workflow
The `/gtd` command researches tasks in bulk and caches results:
- Processes tasks from Computer and Deep Work projects
- Visits URLs and summarizes actual content
- Rich TLDR bullet summaries
- Results cached for 7 days

### Triage Commands
After research, respond with:
| Command | Action | Example |
|---------|--------|---------|
| `C` | Complete task | `1: C` |
| `D [person]` | Delegate via email | `2: D Brianna` |
| `DD` | Deep Dive for more | `3: DD focus on pricing` |

### Silent Operations
Uses AppleScript instead of URL schemes so Things doesn't steal focus.

## Features

### MCP Server (19 tools)

| Category | Tools |
|----------|-------|
| **Read** | get_inbox, get_today, get_upcoming, get_anytime, get_someday, get_logbook, get_trash, get_projects, get_areas, get_tags, get_project, get_area, get_list, get_todo_details |
| **Create** | add_todo (with checklists), add_project (with headings) |
| **Update** | update_todo, update_project, add_items_to_project |
| **Navigate** | show |

### Claude Code Commands

| Command | Description |
|---------|-------------|
| `/thingsinbox` | Triage inbox with URL resolution, project assignment, learning |
| `/gtd` | Research tasks with caching and batch execution |

## Requirements

- macOS with Things 3 installed
- Node.js 18 or later
- Claude Code

## Installation

### 1. Clone and Build

```bash
git clone https://github.com/awilkinson/SuperThings.git
cd SuperThings
npm install
npm run build
```

### 2. Get Your Things Auth Token

1. Open Things → Settings → General
2. Enable Things URLs
3. Click Manage → Copy Token

### 3. Configure Claude Code

Add to your `~/claudesync/claude.json`:

```json
{
  "mcpServers": {
    "things-mcp": {
      "command": "node",
      "args": ["/path/to/SuperThings/dist/index.js"],
      "env": {
        "THINGS_AUTH_TOKEN": "your-token-here"
      }
    }
  }
}
```

Replace `/path/to/SuperThings` with the actual path and add your auth token.

### 4. Install Commands

Create symlinks in your Claude commands directory:

```bash
mkdir -p ~/claudesync/commands
ln -sf /path/to/SuperThings/commands/thingsinbox.md ~/claudesync/commands/thingsinbox.md
ln -sf /path/to/SuperThings/commands/gtd.md ~/claudesync/commands/gtd.md
```

### 5. Initialize Learning Data

```bash
mkdir -p /path/to/SuperThings/data
echo '{"title_transforms":[],"project_hints":{},"exact_overrides":{}}' > /path/to/SuperThings/data/patterns.json
echo '{"last_updated":null,"sessions":{}}' > /path/to/SuperThings/data/research-cache.json
```

## Usage

### Inbox Triage

```
/thingsinbox
```

Shows your inbox tasks with suggested titles and project assignments:

```
Inbox (44) | C=Computer D=Deep O=Out P=Call

┌─ 1 ─────────────────────────────────────────────────── C ✎
│  https://youtu.be/pE3KKUKXcTM...
│  ↓
│  Watch: Semiconductor Industry Works
├─ 2 ─────────────────────────────────────────────────── C ✎
│  Fix fireplace
│  ↓
│  Delegate to Brianna: Fix fireplace        [learned: 12x]
├─ 3 ─────────────────────────────────────────────────── C
│  Research competitor pricing
```

Reply with numbers to approve (e.g., `1,2,5-10` or `all`).

### GTD Research

```
/gtd
```

Researches tasks from Computer and Deep Work projects:

```
Research Complete: 32 tasks processed

┌─ 1 ─────────────────────────────────────────────────────────
│  Research competitor pricing
│
│  • Found 5 competitors: Acme ($15/mo), Beta ($25/mo)...
│  • Enterprise tiers range $100-500/seat
│  • Key differentiator: only Gamma has API at base tier
│  • Sources: G2, Capterra, pricing pages
│
├─ 2 ─────────────────────────────────────────────────────────
│  https://youtu.be/abc123
│
│  • Video: "The Future of AI" by Sam Altman (45 min)
│  • Key points: GPT-5 roadmap, multimodal focus
│  • Source: visited link, summarized content
```

Reply with triage commands:
```
1: C
2: D Brianna please handle by Friday
3: DD focus on North American competitors only
```

## Project IDs

Reference for Things projects:
- Computer: `LDhUsibk3dp2ZPioQySSiu`
- Deep Work: `WamuBi2sFwbUwpXz9NZetP`
- Call: `Er67bc9YAur6ZeKTCBLC4c`
- Home: `NsSR9HR3pd2bVi2z4QHFfM`
- Out and About: `5LwYiPJAkWGSCMHML8xaXb`
- Kids/Activities: `7n14Jusf7nCrLADfAANabW`
- Someday: `EZ5uJWRtcrvJ4U852NkNQ8`

## Development

```bash
npm run dev      # Watch mode
npm run lint     # Run linter
npm run format   # Format code
npm test         # Run tests
```

## File Structure

```
SuperThings/
├── src/                    # MCP server TypeScript source
├── dist/                   # Compiled MCP server
├── commands/               # Claude Code slash commands
│   ├── thingsinbox.md     # Inbox triage with learning
│   └── gtd.md             # GTD workflow with caching
├── data/                   # Learning data
│   ├── patterns.json      # Learned patterns
│   ├── history.jsonl      # Correction history
│   └── research-cache.json # GTD research cache
├── SKILL.md               # Skill instructions for Claude
├── CLAUDE.md              # Dev instructions
├── CHANGELOG.md           # Version history
└── LICENSE                # MIT
```

## Troubleshooting

### "Things 3 does not appear to be running"
Make sure Things 3 is installed and has been opened at least once.

### "Authentication failed"
Check that your THINGS_AUTH_TOKEN is correctly set in the MCP configuration.

### AppleScript Permissions
On first run, macOS may ask for permission to control Things. Grant this permission.

### Learning Not Working
Check that `data/patterns.json` exists and is writable.

## License

MIT - See [LICENSE](LICENSE) for details.

## Credits

- Original MCP: [hildersantos/things-mcp](https://github.com/hildersantos/things-mcp)
- Built with [Model Context Protocol SDK](https://github.com/anthropics/mcp)
- Things is a trademark of Cultured Code GmbH & Co. KG
