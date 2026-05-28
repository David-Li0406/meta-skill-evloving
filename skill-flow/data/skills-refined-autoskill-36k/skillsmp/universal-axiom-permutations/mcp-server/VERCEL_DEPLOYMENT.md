# Deploying Universal Axiom MCP Server to Vercel

This guide explains how to deploy the Universal Axiom MCP server as a serverless HTTP API on Vercel.

## Prerequisites

1. A [Vercel account](https://vercel.com/signup)
2. [Vercel CLI](https://vercel.com/docs/cli) installed: `npm i -g vercel`
3. Node.js 18+ installed

## Security

This deployment uses the latest versions of all dependencies with **zero known vulnerabilities**:
- `@vercel/node@^5.5.27` (latest runtime)
- `vercel@^50.4.11` (latest CLI)
- Dependency overrides to ensure secure transitive dependencies

All security vulnerabilities have been resolved through npm package overrides.

## Quick Deploy

### Option 1: Deploy via CLI (Recommended)

```bash
cd mcp-server

# Install dependencies
npm install

# Login to Vercel (if not already)
vercel login

# Deploy to preview
npm run deploy

# Deploy to production
npm run deploy:prod
```

### Option 2: Deploy via GitHub

1. Push your repository to GitHub
2. Go to [vercel.com/new](https://vercel.com/new)
3. Import your repository
4. Set the **Root Directory** to `mcp-server`
5. Click Deploy

## Configuration

The deployment uses these files:
- `vercel.json` - Vercel configuration (functions, routes, headers)
- `tsconfig.vercel.json` - TypeScript config for serverless build
- `api/mcp.ts` - The serverless function endpoint

## API Endpoints

Once deployed, your MCP server will be available at:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/mcp` | GET | Health check - returns server info |
| `/api/mcp` | POST | MCP JSON-RPC endpoint |
| `/mcp` | POST | Alias for `/api/mcp` |
| `/health` | GET | Alias for health check |

## Usage Examples

### Health Check

```bash
curl https://your-deployment.vercel.app/api/mcp
```

Response:
```json
{
  "name": "universal-axiom-server",
  "version": "0.2.0",
  "status": "healthy"
}
```

### Initialize MCP Session

```bash
curl -X POST https://your-deployment.vercel.app/api/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "initialize"}'
```

### List Available Tools

```bash
curl -X POST https://your-deployment.vercel.app/api/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}'
```

### Call a Tool

```bash
curl -X POST https://your-deployment.vercel.app/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "compute_intelligence",
      "arguments": {
        "impulses": 1.5,
        "elements": 2.0,
        "pressure": 1.0,
        "subjectivity": 0.2,
        "purpose": 1.0,
        "time": 1.0,
        "n": 3
      }
    }
  }'
```

## Available Tools

The MCP server exposes these tools:

| Tool | Description |
|------|-------------|
| `compute_intelligence` | Calculate intelligence using the Universal Axiom formula |
| `evolve_system` | Evolve a system forward in time |
| `apply_pressure` | Apply pressure changes to the system |
| `adjust_subjectivity` | Adjust subjectivity level |
| `simulate_evolution` | Simulate evolution over multiple steps |
| `simulate_contradiction_resolution` | Simulate contradiction resolution |
| `get_coherence_metric` | Calculate system coherence |
| `analyze_permutation` | Diagnose system layer issues |
| `compare_permutations` | Compare two system configurations |
| `optimize_system` | Get optimization suggestions |
| `predict_trajectory` | Predict future system states |
| `detect_collapse_risk` | Analyze collapse risk indicators |

## Connecting to MCP Clients

### Claude Desktop (with HTTP transport)

Add to your Claude Desktop config (`~/.claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "universal-axiom": {
      "transport": "http",
      "url": "https://your-deployment.vercel.app/api/mcp"
    }
  }
}
```

### Custom Client Example (JavaScript)

```javascript
async function callMCPTool(url, toolName, args) {
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: Date.now(),
      method: 'tools/call',
      params: { name: toolName, arguments: args }
    })
  });
  return response.json();
}

// Usage
const result = await callMCPTool(
  'https://your-deployment.vercel.app/api/mcp',
  'compute_intelligence',
  { impulses: 1.5, n: 5 }
);
console.log(result);
```

## Environment Variables

No environment variables are required for basic deployment.

Optional variables you can set in Vercel dashboard:
- `NODE_ENV` - Set to `production` (default)

## Local Development

```bash
cd mcp-server
npm install

# Run local Vercel dev server
npm run dev:vercel
```

The server will be available at `http://localhost:3000/api/mcp`

## Troubleshooting

### Function Timeout
Vercel serverless functions have a 10-second timeout on the free tier. Complex simulations with many steps may timeout. Consider reducing `steps` parameter or upgrading to Pro tier (60s timeout).

### CORS Issues
CORS headers are configured in `vercel.json`. If you still encounter issues, check that your client sends the correct `Content-Type: application/json` header.

### Cold Starts
First request after inactivity may be slower due to cold start. Subsequent requests will be fast.

## Cost Considerations

Vercel free tier includes:
- 100GB bandwidth/month
- 100,000 function invocations/month

The Universal Axiom MCP server is lightweight and should easily fit within free tier limits for personal use.

## Links

- [Universal Axiom Repository](https://github.com/TheUniversalAxiom/pointy-stick)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [Vercel Documentation](https://vercel.com/docs)
