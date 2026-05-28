# MCP Server Configuration for Radulator QA

This skill requires two MCP servers to function:

1. **Playwright MCP** - For browser automation and testing
2. **GitHub MCP** - For repository management and PR operations

## Recommended Setup: Docker Desktop MCP Toolkit (Claude Code CLI)

**This is the recommended approach** for Claude Code CLI users, as it provides:
- ✅ Team collaboration via version-controlled `.mcp.json`
- ✅ CI/CD ready configuration
- ✅ Centralized secret management
- ✅ One-click MCP server setup

### Step 1: Install Docker Desktop

Download and install Docker Desktop from https://www.docker.com/products/docker-desktop

Verify installation:
```bash
docker --version
docker ps
```

### Step 2: Enable Docker MCP Toolkit

1. Open Docker Desktop
2. Go to Settings → Features in development (Beta)
3. Enable "MCP Toolkit"
4. Restart Docker Desktop

### Step 3: Add MCP Servers via Docker Desktop

1. Open Docker Desktop → MCP Toolkit → Catalog
2. Search for and add "Playwright" server
3. Search for and add "GitHub Official" server
4. For GitHub: Follow the OAuth flow to authenticate with your GitHub account

### Step 4: Configure GitHub Token (Optional)

If you prefer using a Personal Access Token instead of OAuth:

1. Create a GitHub Personal Access Token at https://github.com/settings/tokens
   - Scopes: `repo`, `read:org`, `workflow`
2. Add token to your shell configuration:

```bash
# Add to ~/.zshrc or ~/.bashrc
export GITHUB_TOKEN="your_token_here"
```

3. Restart your terminal or run: `source ~/.zshrc`

### Step 5: Create Project MCP Configuration

In your Radulator project root, create `.mcp.json`:

```json
{
  "mcpServers": {
    "MCP_DOCKER": {
      "command": "docker",
      "args": ["mcp", "gateway", "run"],
      "type": "stdio"
    }
  }
}
```

**Important**: Add `.mcp.json` to git for team collaboration!

### Step 6: Connect Claude Code CLI

```bash
cd /path/to/Radulator
docker mcp client connect claude-code
```

Restart Claude Code CLI if it's currently running.

### Step 7: Verify Connection

```bash
# List available tools
docker mcp tools ls

# You should see ~67 tools:
# - 21 Playwright tools (browser_*)
# - 40+ GitHub tools (create_pull_request, etc.)
# - MCP meta-tools (mcp-add, etc.)
```

---

## Alternative Setup: Claude Desktop (GUI)

If you prefer using Claude Desktop GUI instead of Claude Code CLI:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    },
    "github": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN_HERE>"
      }
    }
  }
}
```

### Prerequisites

1. **Node.js & NPM** - Required for Playwright MCP
   ```bash
   # Verify installation
   node --version
   npm --version
   ```

2. **Docker** - Required for GitHub MCP
   ```bash
   # Verify installation
   docker --version
   
   # Pull GitHub MCP image
   docker pull ghcr.io/github/github-mcp-server
   ```

3. **GitHub Personal Access Token**
   - Go to GitHub Settings → Developer Settings → Personal Access Tokens
   - Create a **Classic Token** with these scopes:
     - `repo` (full access to repositories)
     - `read:org` (read organization data)
     - `workflow` (update GitHub Action workflows)
   - Copy the token and replace `<YOUR_TOKEN_HERE>` in the config

## Verification

### For Claude Code CLI (Docker MCP Gateway):

```bash
# Check connection status
docker mcp client ls

# List available tools
docker mcp tools ls

# Test a simple browser tool
docker mcp tools call browser_navigate --args '{"url":"https://google.com"}'

# Test a GitHub tool
docker mcp tools call get_me
```

### For Claude Desktop (GUI):

1. Restart Claude Desktop
2. Start a new conversation
3. Check for MCP server indicators in the UI
4. Test Playwright: Ask Claude to "open a browser to google.com"
5. Test GitHub: Ask Claude to "list my GitHub repositories"

## Troubleshooting

### Docker MCP Gateway Issues

**Problem**: "docker: 'mcp' is not a docker command"
**Solution**:
- Ensure Docker Desktop is installed (not just Docker Engine)
- Enable MCP Toolkit in Docker Desktop Settings → Beta Features
- Restart Docker Desktop

**Problem**: "MCP servers not showing tools"
**Solution**:
```bash
# Check server status
docker mcp server list

# Reconnect client
docker mcp client disconnect claude-code
docker mcp client connect claude-code

# Restart Claude Code CLI
```

**Problem**: "GitHub OAuth failed"
**Solution**:
- Open Docker Desktop → MCP Toolkit → My servers
- Click on "github-official" → Re-authenticate
- Or use Personal Access Token approach (see Step 4)

**Problem**: "Playwright browser not found"
**Solution**:
- Docker Desktop MCP Toolkit auto-installs browsers
- If issues persist, check Docker Desktop logs

### Legacy Setup Issues (Claude Desktop / Manual MCP)

**Problem**: "npx command not found"
**Solution**: Install Node.js from https://nodejs.org

**Problem**: Playwright browser not found
**Solution**:
```bash
npx playwright install
```

**Problem**: "Docker daemon not running"
**Solution**: Start Docker Desktop

**Problem**: "Authentication failed"
**Solution**:
- Verify token has correct permissions
- Check token hasn't expired
- Ensure no extra spaces in token string

**Problem**: "Cannot pull image"
**Solution**:
```bash
docker pull ghcr.io/github/github-mcp-server
```

## Security Notes

- **Never commit your GitHub token** to any repository
- Store tokens in environment variables or secure vaults
- Use tokens with minimal required permissions
- Rotate tokens regularly (every 90 days recommended)
- Consider using organization tokens for team projects

## Legacy Setup (Manual MCP Servers - Not Recommended)

**Note**: This approach is NOT recommended for Claude Code CLI users. Use Docker Desktop MCP Toolkit instead for better team collaboration and CI/CD support.

If you must use manual MCP server configuration (for older setups or special requirements):

**For project-level configuration** (`.mcp.json` in project root):

```json
{
  "mcpServers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@playwright/mcp-server"]
    },
    "github": {
      "type": "stdio",
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

Then set environment variable in `~/.zshrc` or `~/.bashrc`:
```bash
export GITHUB_TOKEN="your_token_here"
```

**Limitations of manual setup**:
- ❌ No centralized secret management
- ❌ Harder to share with team
- ❌ Not CI/CD ready
- ❌ Each developer must configure independently
- ❌ No automatic browser installation for Playwright

## Related Resources

- Playwright MCP: https://github.com/microsoft/playwright
- GitHub MCP: https://github.com/github/github-mcp-server
- MCP Protocol: https://modelcontextprotocol.io
