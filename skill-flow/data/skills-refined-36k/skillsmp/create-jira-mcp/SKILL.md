---
name: create-jira-mcp
description: Sets up Jira MCP server integration for Claude Code. Use when setting up Jira, connecting to Atlassian, configuring MCP for ticket management, or adding Jira capabilities.
allowed-tools: Bash, Read, Write, AskUserQuestion, Glob
---

# Create Jira MCP Integration

## Purpose

Guide users through setting up a Jira MCP server to enable Claude Code to interact with Jira for ticket management.

## Instructions

### 1. Check Prerequisites

Verify Node.js is installed (v18+ required):
```bash
node --version
```

### 2. Check Existing Environment Variables

Before asking for credentials, check if environment variables are already set. **Mark the output as sensitive** to avoid exposing credentials in logs:

```bash
# Check if variables exist (values will be hidden)
printenv JIRA_HOST JIRA_EMAIL JIRA_API_TOKEN 2>/dev/null | wc -l
```

Or check each individually:
```bash
[ -n "$JIRA_HOST" ] && echo "JIRA_HOST is set" || echo "JIRA_HOST is not set"
[ -n "$JIRA_EMAIL" ] && echo "JIRA_EMAIL is set" || echo "JIRA_EMAIL is not set"
[ -n "$JIRA_API_TOKEN" ] && echo "JIRA_API_TOKEN is set" || echo "JIRA_API_TOKEN is not set"
```

**Important**: Never echo the actual values of these variables. Only check if they exist.

If all three variables are set, skip to Step 4 (Create Local MCP Server Installation).

### 3. Gather Jira Credentials (if not already set)

Only ask for credentials that are missing:
- **Jira Host**: Their Atlassian domain (e.g., `your-domain.atlassian.net`)
- **Jira Email**: Their Atlassian account email
- **Jira API Token**: Generated from https://id.atlassian.net/manage-profile/security/api-tokens

Inform them they need to create an API token if they don't have one:
1. Go to https://id.atlassian.net/manage-profile/security/api-tokens
2. Click "Create API token"
3. Name it (e.g., "Claude Code")
4. Copy the token immediately (it won't be shown again)

### 4. Set Environment Variables (if not already set)

Guide the user to set any missing environment variables. Provide commands for their shell:

```bash
export JIRA_HOST="https://your-domain.atlassian.net"
export JIRA_EMAIL="your-email@example.com"
export JIRA_API_TOKEN="your-api-token"
```

For permanent setup, add to shell profile (`~/.zshrc` or `~/.bashrc`):
```bash
echo 'export JIRA_HOST="https://your-domain.atlassian.net"' >> ~/.zshrc
echo 'export JIRA_EMAIL="your-email@example.com"' >> ~/.zshrc
echo 'export JIRA_API_TOKEN="your-api-token"' >> ~/.zshrc
source ~/.zshrc
```

### 5. Create Local MCP Server Installation

Create the MCP servers directory and install dependencies:

```bash
mkdir -p .mcp-servers/jira && cd .mcp-servers/jira
npm init -y && npm install mcp-atlassian jsdom
cd ../..
```

Add `.mcp-servers/` to `.gitignore` if not already present.

### 6. Register the MCP Server

Add the Jira MCP server to Claude Code:

```bash
claude mcp add-json jira '{
    "type": "stdio",
    "command": "node",
    "args": [".mcp-servers/jira/node_modules/mcp-atlassian/dist/index.js"],
    "env": {
      "ATLASSIAN_BASE_URL": "${JIRA_HOST}",
      "ATLASSIAN_EMAIL": "${JIRA_EMAIL}",
      "ATLASSIAN_API_TOKEN": "${JIRA_API_TOKEN}"
    }
}' -s project
```

### 7. Display Restart Notice

**IMPORTANT**: After completing all setup steps, you MUST display this notice to the user:

```
================================================
  RESTART REQUIRED
================================================
  The Jira MCP server has been configured.

  Please restart Claude Code for the MCP
  server to be registered and available.

  After restarting:
  1. Run /mcp to verify the server is connected
  2. Test with: "List all Jira projects"
================================================
```

This notice is critical because MCP servers are only loaded when Claude Code starts.

## Output Format

Provide step-by-step guidance with commands the user can copy and run. After each step, confirm success before proceeding.

**Always end with the restart notice** - this is mandatory to ensure users know to restart Claude Code.

## Troubleshooting

**Authentication failed:**
- Verify JIRA_HOST is just the domain (e.g., `your-domain.atlassian.net`), not the full URL
- Check JIRA_EMAIL matches the Atlassian account email
- Regenerate the API token if unsure

**Node.js issues:**
- Ensure Node.js v18+ is installed
- Run `node --version` to verify

**MCP not connecting:**
- Restart Claude Code after adding the server
- Check `/mcp` shows the jira server as connected
- Verify environment variables are set with `echo $JIRA_HOST`

## Best Practices

- Never commit API tokens to version control
- Use environment variables for all credentials
- Always mark credential checks as sensitive output to avoid exposing values in logs
- Create a dedicated Jira service account for team use
- Test with read-only operations first (list projects, search issues)

## Example

**User**: "Set up Jira MCP for my project"

**Response**:
1. Verify Node.js v18+ is installed
2. Check if JIRA_HOST, JIRA_EMAIL, JIRA_API_TOKEN already exist (mark output sensitive)
3. Only ask for missing credentials
4. Guide through environment variable setup for any missing vars
5. Run installation commands
6. Register the MCP server
7. Display the RESTART REQUIRED notice prominently
