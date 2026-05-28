# Rory — Your CMO in the Terminal

Hey, I'm Rory. I'm an AI-powered Chief Marketing Officer assistant for Claude Code and Claude Desktop. Delegate your marketing strategy, research, and content creation to a remote-first expert agent that already knows your brand.

## Quick Start

### 1. Install

```bash
curl -fsSL https://raw.githubusercontent.com/robynnai/robynn-claude-cmo/main/install.sh | bash
```

The installer will:
- Set up the plugin in `~/.claude/skills/rory`
- Create a virtual environment and install dependencies
- Prompt for your API key (optional, can skip and configure later)
- Configure both Claude Code and Claude Desktop automatically

### 2. Get Your API Key

1. Go to https://robynn.ai/settings/api-keys
2. Sign up if you don't have an account (**20 free tasks/month**)
3. Generate and copy your API key

### 3. Configure Rory

**Option A: Interactive wizard**
```bash
rory init
```
Opens browser → guides you through signup → saves your key

**Option B: Direct setup with API key**
```bash
rory init <your_api_key>
```

**Option C: Manual configuration**
```bash
rory config <your_api_key>
```

### 4. Verify

```bash
rory status
```

You should see:
```
Status: 🟢 Connected (Pro Tier)
Organization: your-org-id
Company:      Your Company
Brand Voice:  ✅ Configured
Features:     5 loaded
```

### 5. Configure Your Brand Hub

For best results, visit https://robynn.ai/dashboard and configure:
- **Brand Book** → Company name, tagline, elevator pitch
- **Strategy & Messaging** → Target audience, pain points
- **Knowledge Base** → Product features, differentiators
- **Aesthetics** → Colors, logo, design style

## How It Works

Rory uses a **remote-first thin-client architecture**:

1. **You run `rory init`** to connect your Robynn account
2. **You ask Rory** to create content, do research, or manage ads
3. **Rory sends your request** to the Robynn CMO v2 agent
4. **The agent fetches YOUR brand context** automatically
5. **Results come back already on-brand**

**No local brand files.** Your brand context lives in the cloud and is always up-to-date.

## Features

### Content Creation
- LinkedIn posts, tweets, blog outlines
- Cold emails, one-pagers, marketing briefs
- All content uses YOUR voice from Brand Hub

### Research
- Company deep-dives (website, tech stack, funding, team)
- Competitive intelligence and comparisons
- People finding (contacts, decision-makers)
- Market research and topic analysis

### Ads Management
- Google Ads performance and campaigns
- LinkedIn Ads targeting and analytics
- All campaigns created in DRAFT mode (never auto-activated)

## Usage Examples

Just ask Claude naturally:

```
"Write a LinkedIn post about our new AI feature"
"Research Stripe and summarize their marketing strategy"
"Find VP of Marketing contacts at Series A fintech startups"
"Create a marketing brief for our product launch"
"Analyze our competitors in the CRM space"
```

Or use CLI commands directly:

```bash
rory research Stripe
rory competitors HubSpot
rory write linkedin post about our new feature
rory brief --for "product launch campaign"
```

## Pricing

| Tier | Limit | Price |
|------|-------|-------|
| Anonymous | 5 tasks/day | $0 |
| Free | 20 tasks/month | $0 |
| Pro | 500 tasks/day | See robynn.ai/pricing |

## Commands

Run `rory help` to see all commands.

### Account & Setup

| Command | Description |
|---------|-------------|
| `rory init` | Interactive setup wizard (opens browser) |
| `rory init <api_key>` | Direct setup with API key |
| `rory config <api_key>` | Save API key manually |
| `rory logout` | Remove saved API key |
| `rory uninstall` | Remove the Rory plugin completely |

### Status & Info

| Command | Description |
|---------|-------------|
| `rory status` | Check connection and Brand Hub status |
| `rory status --debug` | Show raw API response for debugging |
| `rory usage` | View remaining tasks and tier info |
| `rory sync` | Verify Brand Hub connection |
| `rory voice` | Preview brand voice settings |
| `rory help` | Show help with all commands and examples |

### Content & Research

| Command | Description |
|---------|-------------|
| `rory research <company>` | Deep-dive company research |
| `rory competitors <company>` | Competitive intelligence |
| `rory write <type> [topic]` | Create content (linkedin, tweet, email, blog) |
| `rory brief --for <topic>` | Generate a marketing brief |
| `rory "<any request>"` | Free-form natural language query |

### Options

| Option | Description |
|--------|-------------|
| `--json` | Output results in JSON format |

## Uninstall

```bash
rory uninstall
```

This will prompt for confirmation before removing the plugin directory.

## Alternative Installation

### Manual Clone

```bash
git clone https://github.com/robynnai/robynn-claude-cmo.git ~/.claude/skills/rory
cd ~/.claude/skills/rory
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Then configure your API key:
```bash
echo "ROBYNN_API_KEY=your-api-key-here" >> .env
```

## Claude Desktop (MCP) Setup

The install script automatically configures Claude Desktop. Just run the installer and restart Claude Desktop.

### Manual Configuration

If you need to configure manually, edit your Claude Desktop config:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux:** `~/.config/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "Robynn AI - Rory": {
      "command": "/Users/YOUR_USERNAME/.claude/skills/rory/.venv/bin/python",
      "args": ["/Users/YOUR_USERNAME/.claude/skills/rory/mcp_server.py"],
      "env": {
        "ROBYNN_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Then restart Claude Desktop.

### Available MCP Tools

| Tool | Description |
|------|-------------|
| `rory_query` | Send any marketing request to Rory |
| `rory_research_company` | Research a specific company |
| `rory_research_competitors` | Analyze competitors |
| `rory_write_content` | Create marketing content (type + topic) |
| `rory_status` | Check API connection and Brand Hub status |
| `rory_usage` | Check remaining task quota |

### Example Prompts for Claude Desktop

```
"Use Rory to write a LinkedIn post about our new feature"
"Ask Rory to research Stripe's marketing strategy"
"Check my Rory usage"
"Have Rory analyze our competitors"
```

## Dependencies

Core dependencies (installed automatically):
- `httpx` - HTTP client for API calls
- `rich` - Terminal styling for help display
- `pydantic` - Data validation
- `python-dotenv` - Environment configuration
- `fastmcp` - MCP server framework

Optional (for local research tools):
- `google-ads` - Google Ads API integration

## Development

### Running Tests

```bash
cd ~/.claude/skills/rory
.venv/bin/pytest tests/
```

### Project Structure

```
robynn-claude-cmo/
├── rory.py              # Main CLI entry point
├── mcp_server.py        # MCP server for Claude Desktop
├── install.sh           # Installation script
├── bin/rory             # Shell wrapper script
├── tools/               # Core tool implementations
│   ├── robynn.py        # Robynn API client
│   ├── remote_cmo.py    # Remote CMO execution
│   ├── onboarding.py    # Setup wizard
│   ├── help_display.py  # CLI help display
│   └── ...              # Research & ads tools
├── agents/              # Agent skill definitions
├── skills/              # Skill configurations
└── tests/               # Test suite
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- Documentation: https://robynn.ai/docs/rory
- Issues: https://github.com/robynnai/robynn-claude-cmo/issues
- Email: support@robynn.ai
