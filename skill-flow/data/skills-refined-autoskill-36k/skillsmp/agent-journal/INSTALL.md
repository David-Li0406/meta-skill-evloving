# Agent Journal Skill Installation

Install the agent-journal skill for AI agents to search past sessions, manage knowledge, and index content.

## Prerequisites

```bash
# Install the agent-journal CLI tool
dotnet tool install -g AgentJournal
```

---

## Copilot CLI Installation

### Option 1: Copy to global skills directory

```bash
# Windows
mkdir %USERPROFILE%\.copilot\skills\agent-journal
copy .github\skills\agent-journal\SKILL.md %USERPROFILE%\.copilot\skills\agent-journal\

# macOS/Linux
mkdir -p ~/.copilot/skills/agent-journal
cp .github/skills/agent-journal/SKILL.md ~/.copilot/skills/agent-journal/
```

### Option 2: Symlink (recommended for development)

```bash
# Windows (run as admin)
mklink /D %USERPROFILE%\.copilot\skills\agent-journal .github\skills\agent-journal

# macOS/Linux
ln -s $(pwd)/.github/skills/agent-journal ~/.copilot/skills/agent-journal
```

---

## Claude Code Installation

### Option 1: Copy commands to global directory

```bash
# Windows
mkdir %USERPROFILE%\.claude\commands
copy .claude\commands\*.md %USERPROFILE%\.claude\commands\

# macOS/Linux
mkdir -p ~/.claude/commands
cp .claude/commands/*.md ~/.claude/commands/
```

### Option 2: Project-level (automatic)

The `.claude/commands/` directory in this repo is automatically available when working in this project.

### Available Claude Commands

After installation, use these slash commands:

| Command | Description |
|---------|-------------|
| `/journal` | Full skill reference |
| `/journal-search <query>` | Search past sessions |
| `/journal-remember <fact>` | Store knowledge |
| `/journal-recall <query>` | Search knowledge bank |
| `/journal-index <path>` | Index content from directory |

---

## MCP Server Configuration

For deeper AI agent integration, configure the MCP server:

### Claude Desktop

Edit `~/.config/claude/claude_desktop_config.json` (macOS/Linux) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "agent-journal": {
      "command": "agent-journal",
      "args": ["mcp"]
    }
  }
}
```

### Claude CLI

```bash
claude mcp add --transport stdio agent-journal -- agent-journal mcp
```

---

## Verify Installation

```bash
# Test CLI
agent-journal --version

# Test search
agent-journal search "test" --max 1

# Test MCP server
agent-journal mcp --list-tools
```
