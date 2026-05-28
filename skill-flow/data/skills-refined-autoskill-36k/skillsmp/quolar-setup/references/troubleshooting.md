# Quolar Setup Troubleshooting

Solutions for common issues encountered during Quolar setup and configuration.

---

## MCP Server Issues

### Linear MCP Not Connected

**Error:**
```
Error: MCP server 'linear' not connected
```

**Solution:**

Add Linear MCP to your config with LINEAR_API_KEY:

```json
// In ~/.claude/settings.json or claude_desktop_config.json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@linear/mcp-server"],
      "env": { "LINEAR_API_KEY": "lin_api_xxx" }
    }
  }
}
```

**Get your API key:**
1. Go to Linear Settings
2. Navigate to API section
3. Click "Personal API keys"
4. Create new key or copy existing

---

### Quoth MCP Not Connected

**Error:**
```
Error: MCP server 'quoth' not connected
```

**Solution:**

Add Quoth MCP via command line:

```bash
claude mcp add --transport http quoth https://quoth.ai-innovation.site/api/mcp
```

This opens a browser for OAuth authentication. Complete the login flow.

**Verify connection:**
```
/mcp
```
Should show `quoth` in the list of connected servers.

---

### Exolar MCP Not Connected (Optional)

**Error:**
```
Warning: MCP server 'exolar' not connected
```

**Solution:**

Exolar is optional but provides test analytics. Add via command line:

```bash
claude mcp add exolar-qa --transport http https://exolar.ai-innovation.site/api/mcp/mcp -s user
```

**Note:** If you don't need test analytics, this warning can be ignored.

---

### Linear Authentication Failed

**Error:**
```
Error: 401 Unauthorized
Error: Authentication failed
```

**Causes:**
- API key is invalid
- API key has expired
- API key lacks required permissions

**Solution:**

1. Verify LINEAR_API_KEY is valid:
   ```bash
   curl -H "Authorization: $LINEAR_API_KEY" https://api.linear.app/graphql
   ```

2. Get a new key:
   - Linear Settings → API → Personal API keys
   - Create new key with required scopes

3. Update the key in your MCP config

4. Restart Claude Code:
   ```bash
   claude --restart
   ```

---

## Configuration Issues

### Config File Syntax Error

**Error:**
```
Error: Failed to parse quolar.config.ts
SyntaxError: Unexpected token
```

**Solution:**

Ensure the config follows this exact structure:

```typescript
import { defineConfig } from '@quolar/core'

export default defineConfig({
  testFramework: {
    provider: 'playwright',
    config: './playwright.config.ts',
    testDir: './automation/playwright/tests'
  },
  tickets: {
    provider: 'linear',
    workspace: 'your-workspace'
  },
  documentation: {
    provider: 'quoth'
  },
  analytics: {
    provider: 'exolar'
  },
  workflow: {
    maxHealingAttempts: 3
  }
})
```

**Common syntax errors:**
- Missing commas between properties
- Missing closing brackets
- Using single quotes where double needed in JSON
- Trailing commas in JSON (not allowed)

---

### Config File Not Found

**Error:**
```
Error: quolar.config.ts not found
```

**Solution:**

Create the config file in project root:

```bash
touch quolar.config.ts
```

Then add configuration content. Use the `/quolar-setup` command to generate automatically.

---

### Invalid Workspace Name

**Error:**
```
Error: Linear workspace 'xyz' not found
```

**Solution:**

1. Find your workspace name in Linear URL:
   - Go to Linear
   - Look at URL: `https://linear.app/{workspace}/...`
   - The workspace name is in the URL

2. Update quolar.config.ts:
   ```typescript
   tickets: {
     provider: 'linear',
     workspace: 'correct-workspace-name'
   }
   ```

---

## Playwright Issues

### Playwright Not Installed

**Error:**
```
Error: playwright command not found
Error: Cannot find module '@playwright/test'
```

**Solution:**

Install Playwright and browser binaries:

```bash
npm install -D @playwright/test
npx playwright install
```

Or with yarn:

```bash
yarn add -D @playwright/test
npx playwright install
```

---

### Playwright Config Not Found

**Error:**
```
Error: playwright.config.ts not found
```

**Solution:**

1. Check if config exists:
   ```bash
   ls playwright.config.ts
   ```

2. If missing, create a basic config:
   ```typescript
   // playwright.config.ts
   import { defineConfig } from '@playwright/test'

   export default defineConfig({
     testDir: './automation/playwright/tests',
     use: {
       baseURL: 'http://localhost:5173'
     }
   })
   ```

3. Or initialize Playwright:
   ```bash
   npm init playwright@latest
   ```

---

### Browser Binaries Missing

**Error:**
```
Error: Executable doesn't exist at /path/to/chromium
browserType.launch: Browser was not installed
```

**Solution:**

Install browser binaries:

```bash
npx playwright install
```

For specific browsers:

```bash
npx playwright install chromium
npx playwright install firefox
npx playwright install webkit
```

---

## Directory Issues

### Test Directory Doesn't Exist

**Error:**
```
Error: Test directory not found: ./automation/playwright/tests
```

**Solution:**

Create the directory structure:

```bash
mkdir -p automation/playwright/tests
mkdir -p automation/playwright/page-objects
mkdir -p automation/playwright/utils
```

The `/quolar-setup` command creates these automatically.

---

### Permission Denied

**Error:**
```
Error: EACCES: permission denied
```

**Solution:**

1. Check directory permissions:
   ```bash
   ls -la automation/
   ```

2. Fix permissions:
   ```bash
   chmod 755 automation/playwright/tests
   ```

3. Or run with sudo (not recommended):
   ```bash
   sudo mkdir -p automation/playwright/tests
   ```

---

## Network Issues

### Connection Timeout

**Error:**
```
Error: connect ETIMEDOUT
Error: Network request failed
```

**Causes:**
- Firewall blocking MCP connections
- VPN interference
- Slow network

**Solution:**

1. Check network connectivity:
   ```bash
   curl https://quoth.ai-innovation.site/api/mcp
   ```

2. Try without VPN if connected

3. Check firewall settings for Node.js/npx

4. Increase timeout in Claude settings (if available)

---

### SSL Certificate Error

**Error:**
```
Error: self signed certificate in certificate chain
Error: unable to verify the first certificate
```

**Solution:**

1. Update Node.js to latest version

2. Set NODE_TLS_REJECT_UNAUTHORIZED (temporary, not recommended for production):
   ```bash
   export NODE_TLS_REJECT_UNAUTHORIZED=0
   ```

3. Update CA certificates on your system

---

## Re-running Setup

To completely reset and re-run setup:

```bash
# Remove existing config
rm quolar.config.ts

# Clear MCP cache (if issues persist)
claude mcp remove linear
claude mcp remove quoth

# Re-run setup
/quolar-setup
```

---

## Getting Help

If issues persist:

1. Check the detailed documentation at `skills/test-ticket/SKILL.md`
2. Review the configuration reference at `skills/test-ticket/reference.md`
3. Verify MCP server status with `/mcp`
4. Check Claude Code logs for detailed error messages
