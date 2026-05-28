---
name: fix-paypal-mcp
description: Diagnose and fix PayPal MCP server initialization issues by installing a custom runner script.
---

# Fix PayPal MCP Server

This skill fixes common initialization errors with the PayPal MCP server, such as `npx` failures, "tools argument missing", or ESM/CommonJS conflicts.

## When to Use
Use this skill when:
- The PayPal MCP server fails to start with "EOF" or "initialization failed".
- You see errors about missing `--tools` arguments.
- You encounter `require is not defined` errors.
- The default `npx @paypal/agent-toolkit` command does not work.

## How it Works
The default `@paypal/agent-toolkit` package does not have a bin entry/executable. This skill provides a custom runner script (`run-paypal-mcp.cjs`) that manually initializes the toolkit and connects it to the MCP SDK.

## Setup Instructions

### 1. Copy the Runner Script
Copy the resource file `resources/run-paypal-mcp.cjs` to your project root (e.g., `scripts/run-paypal-mcp.cjs` or just `./run-paypal-mcp.cjs`).

### 2. Configure Environment
Ensure your `.env.local` or MCP environment config has:
- `PAYPAL_ACCESS_TOKEN`: A valid access token.
- `PAYPAL_ENVIRONMENT`: `PRODUCTION` or `SANDBOX`.

### 3. Update MCP Configuration
Edit your `mcp_config.json` (or `.cursor/mcp.json`) to use the new script with `node` instead of `npx`.

```json
"paypal-mcp-server": {
  "command": "node",
  "args": [
    "/absolute/path/to/your/run-paypal-mcp.cjs"
  ],
  "env": {
    "PAYPAL_ACCESS_TOKEN": "...",
    "PAYPAL_ENVIRONMENT": "PRODUCTION"
  }
}
```

### 4. Restart
Restart Antigravity or the MCP server functionality.

## Dependencies
The script requires:
- `@paypal/agent-toolkit`
- `@modelcontextprotocol/sdk`

If you see `zod` errors, check for `v3` export issues in the `zod` package and patch if necessary (add `"./v3": "./lib/index.js"` to `node_modules/zod/package.json`).
