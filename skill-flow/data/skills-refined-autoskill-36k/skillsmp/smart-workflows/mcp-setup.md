# MCP Server Setup Guide

## Overview

MCP-B uses the Model Context Protocol (MCP) to provide specialized tools and context to GitHub Copilot agents. This guide explains the setup and best practices.

## Architecture

```
.vscode/
├── mcp.json          # Workspace MCP server configuration (version controlled)
└── README.md         # MCP server documentation

.github/
└── agents/           # Custom Copilot agent definitions
    ├── data-collector.agent.md
    ├── data-prep.agent.md
    ├── model-trainer.agent.md
    ├── results-analyst.agent.md
    ├── visualization.agent.md
    └── publisher.agent.md
```

## Configuration Location

Following best practices for 2025:

- ✅ **Workspace config**: `.vscode/mcp.json` (version controlled, team-wide)
- ✅ **Agent definitions**: `.github/agents/*.agent.md` (version controlled)
- ❌ **Not used**: `.github/copilot/mcp.json` (deprecated location)

### Why .vscode/mcp.json?

1. **Team consistency**: All developers use the same MCP servers
2. **IDE integration**: Native support in VS Code and other IDEs
3. **Best practice**: Recommended by GitHub and Microsoft for 2024-2025
4. **Automatic loading**: IDEs detect and use this location automatically

## Available MCP Servers

### 1. Serena - Semantic Code Analysis

**Purpose**: Deep code understanding with symbol-level analysis

**Capabilities**:
- Find symbol definitions and references
- Understand code structure semantically
- Refactoring assistance
- Cross-project navigation

**Usage in prompts**:
```
@data-collector Use #serena to find all API client patterns in the codebase
```

**Installation**: Automatic via `uvx` (requires Python uvx tool)

### 2. Context7 - Live Documentation

**Purpose**: Up-to-date API documentation and best practices

**Capabilities**:
- Latest API documentation
- Version-specific guides
- Best practice patterns
- Framework documentation

**Usage in prompts**:
```
@model-trainer Use #context7 to look up PyTorch training best practices
```

**Requirements**:
- Environment variable: `CONTEXT7_API_KEY`
- Get your key at: [Context7 Website]

### 3. GitHub - Repository Operations

**Purpose**: Direct GitHub API access

**Capabilities**:
- Create/update issues and PRs
- Search code across repositories
- Repository operations
- Workflow management

**Requirements**:
- Environment variable: `GITHUB_TOKEN`
- Token needs appropriate repository permissions

### 4. Filesystem - Safe File Operations

**Purpose**: File operations within workspace boundaries

**Capabilities**:
- Read files safely
- Write files with validation
- Search within project
- Respects .gitignore

**Security**: Restricted to `${workspaceFolder}` only

## Environment Variables

### Required Setup

Create a `.env` file (not version controlled) or set environment variables:

```bash
# Context7 API Key (required for documentation lookups)
export CONTEXT7_API_KEY="your-context7-api-key"

# GitHub Token (required for GitHub operations)
export GITHUB_TOKEN="your-github-personal-access-token"
```

### VS Code Integration

Add to your `.vscode/settings.json` (user or workspace):

```json
{
  "terminal.integrated.env.linux": {
    "CONTEXT7_API_KEY": "${env:CONTEXT7_API_KEY}",
    "GITHUB_TOKEN": "${env:GITHUB_TOKEN}"
  },
  "terminal.integrated.env.osx": {
    "CONTEXT7_API_KEY": "${env:CONTEXT7_API_KEY}",
    "GITHUB_TOKEN": "${env:GITHUB_TOKEN}"
  },
  "terminal.integrated.env.windows": {
    "CONTEXT7_API_KEY": "${env:CONTEXT7_API_KEY}",
    "GITHUB_TOKEN": "${env:GITHUB_TOKEN}"
  }
}
```

## Agent Usage

Each agent in `.github/agents/` can use all configured MCP servers:

### Example: Data Collector Agent

```
@data-collector Help me fetch data from the GitHub API.

The agent will:
1. Use #context7 to look up GitHub API documentation
2. Use #serena to analyze existing API client code
3. Use #github for actual API operations
4. Use filesystem to save the collected data
```

### Example: Model Trainer Agent

```
@model-trainer Set up a PyTorch training loop with early stopping.

The agent will:
1. Use #context7 to get PyTorch best practices
2. Use #serena to find existing training patterns
3. Use filesystem to create the training script
```

## Best Practices

### ✅ DO

1. **Version control the MCP config**: Team consistency
2. **Use environment variables for secrets**: Security
3. **Document required MCP servers**: Clear expectations
4. **Test MCP servers locally**: Verify before committing
5. **Reference MCP servers in prompts**: `#serena`, `#context7`
6. **Keep MCP config minimal**: Only include needed servers

### ❌ DON'T

1. **Commit secrets to version control**: Use environment variables
2. **Use global config only**: Team members will have different setups
3. **Enable all tools for all agents**: Least-privilege principle
4. **Skip documentation**: Document what each server does
5. **Use untrusted MCP servers**: Security risk
6. **Ignore MCP server updates**: Keep dependencies current

## Troubleshooting

### MCP Servers Not Loading

1. **Check VS Code logs**: View → Output → GitHub Copilot
2. **Verify environment variables**: `echo $CONTEXT7_API_KEY`
3. **Restart IDE**: Sometimes required after config changes
4. **Check tool installation**: `npx --version`, `uvx --version`

### Agent Not Using MCP Server

1. **Explicit reference**: Use `#serena` or `#context7` in prompt
2. **Check agent configuration**: Verify agent file exists
3. **IDE support**: Ensure IDE supports GitHub Copilot agents
4. **Update Copilot**: Use latest version

### Permission Errors

1. **GitHub token**: Ensure token has correct scopes
2. **Filesystem access**: Check workspace folder permissions
3. **Context7 key**: Verify API key is valid

## Migration from Old Setup

If you have `.github/copilot/mcp.json`:

1. **Move to new location**: Copy to `.vscode/mcp.json`
2. **Update .gitignore**: Allow `.vscode/mcp.json`
3. **Test**: Verify MCP servers still work
4. **Remove old file**: Delete `.github/copilot/mcp.json`
5. **Document**: Update team documentation

## References

- [GitHub Copilot MCP Documentation](https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp)
- [VS Code MCP Guide](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Serena MCP Server](https://github.com/oraios/serena)
- [Context7](https://www.npmjs.com/package/@upstash/context7-mcp)

## Security Considerations

### MCP Server Trust

- MCP servers execute code with your permissions
- Only use servers from trusted sources
- Review server code when possible
- Use organization-approved servers only

### Secret Management

- Never commit API keys or tokens
- Use environment variables or secure vaults
- Rotate keys regularly
- Limit token permissions to minimum required

### Access Control

- Filesystem server restricted to workspace
- GitHub server uses token permissions
- Context7 server uses API key quotas
- Serena runs locally (no external calls)

## Team Onboarding

### New Developer Setup

1. Clone repository
2. Install prerequisites: `node`, `npm`, `npx`, Python with `uv`
3. Set environment variables (see `.env.example`)
4. Open workspace in VS Code
5. Install GitHub Copilot extension
6. Verify MCP servers: Check Output → GitHub Copilot

### CI/CD Integration

For GitHub Actions or CI environments:

```yaml
- name: Setup MCP Environment
  env:
    CONTEXT7_API_KEY: ${{ secrets.CONTEXT7_API_KEY }}
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    # Your CI commands here
```

## Updating MCP Configuration

When adding new MCP servers:

1. **Update `.vscode/mcp.json`**: Add server configuration
2. **Update `.vscode/README.md`**: Document the server
3. **Update this guide**: Add usage examples
4. **Test**: Verify server works locally
5. **Document environment variables**: If any required
6. **Commit**: Version control the changes
7. **Notify team**: Communication about new capabilities

## Support

For issues:
1. Check GitHub Copilot logs in VS Code
2. Verify environment variable configuration
3. Consult MCP server documentation
4. File issue in repository

---

**Last Updated**: January 2025  
**Version**: 1.0  
**Status**: Production
