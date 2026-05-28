# Module 2: MCP Integration (Optional)

## Learning Objectives

By the end of this module, learners will:
- Understand what MCP servers provide
- Configure at least one MCP server (if beneficial for their workflow)
- Know where to find additional MCP servers

> **Note**: MCP is powerful but optional. Many teams get significant value from Claude Code without any MCP integration. Skip this module if you want to focus on the core workflow first.

## What is MCP?

**MCP (Model Context Protocol)** lets Claude access external tools and data in real-time:
- Query GitHub issues and PRs
- Explore database schemas
- Read Slack messages
- And more...

### When to Use MCP

| Situation | MCP Helpful? |
|-----------|--------------|
| You frequently reference GitHub issues | Yes - GitHub MCP |
| You need database schema context | Yes - Postgres MCP |
| You build frontend from Figma designs | Yes - Figma MCP |
| You work with a single codebase | Maybe not |
| You're just getting started | Skip for now |

## Quick Start: GitHub MCP

The most universally useful MCP. Here's how to set it up:

### Step 1: Create a GitHub Token

```
GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
Create with scope: repo
```

### Step 2: Set Environment Variable

```bash
# Add to your shell profile (~/.zshrc or ~/.bashrc)
export GITHUB_TOKEN="ghp_your_token_here"
source ~/.zshrc
```

### Step 3: Create MCP Config

Create `~/.claude/mcp_servers.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Step 4: Restart Claude Code

The MCP will be available in your next session.

### Test It

```
"List open issues in this repository"
"Summarize my recent PRs"
```

## Figma MCP (Frontend Developers)

If you work with Figma designs, this MCP lets Claude reference your design files directly.

### Step 1: Get Figma Access Token

```
Figma → Settings → Account → Personal Access Tokens → Create new token
```

### Step 2: Set Environment Variable

```bash
export FIGMA_ACCESS_TOKEN="your_token_here"
source ~/.zshrc
```

### Step 3: Add to MCP Config

Update `~/.claude/mcp_servers.json`:

```json
{
  "mcpServers": {
    "github": { ... },
    "figma": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-figma"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "${FIGMA_ACCESS_TOKEN}"
      }
    }
  }
}
```

### Test It

```
"Get the design specs for this Figma frame: [paste Figma URL]"
"Generate a React component matching this design: [Figma URL]"
```

### Use in Spec-Driven Development

With Figma MCP, your spec can reference designs directly:

```markdown
## Feature: Profile Card Component

### Design
Figma: https://figma.com/file/xxx/Profile-Card

### Requirements
- Match the design exactly
- Use our existing Button and Avatar components
- Responsive: stack vertically on mobile
```

Claude will pull colors, spacing, typography directly from Figma.

## Other MCP Servers

| Server | Use Case | Setup |
|--------|----------|-------|
| Postgres | Database schema/queries | Requires `DATABASE_URL` |
| Filesystem | Enhanced file ops | Path configuration |
| Memory | Persistent storage | Minimal config |
| **Figma** | Design specs for frontend | Requires `FIGMA_ACCESS_TOKEN` |

Find more at: [MCP Server Registry](https://github.com/modelcontextprotocol/servers)

## Security Notes

- Use minimum required token scopes
- Never hardcode tokens in config files
- Start with read-only access
- Review MCP access periodically

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "Server not found" | Run `npx -y @modelcontextprotocol/server-github --help` to test |
| "Auth failed" | Check `echo $GITHUB_TOKEN` is set |
| No response | Restart Claude Code after config changes |

## Checkpoint

Module 2 is complete when:
- [ ] You've decided whether MCP is valuable for your workflow
- [ ] If yes: at least one MCP configured and tested
- [ ] If no: that's fine! Move to Module 3

## Next

Ready for the core workflow? **Module 3: Test-Driven Agentic** teaches the most important pattern.

Type "next" or run `/onboard-tda` to continue.
