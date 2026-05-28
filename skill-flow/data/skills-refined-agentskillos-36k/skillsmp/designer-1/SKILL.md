---
name: designer
description: Start Penpot MCP servers and work with designs. Enables AI-assisted design workflows with Penpot.
---

# Designer Skill

Work with Penpot designs using the Penpot MCP server. Enables design-to-code and code-to-design workflows.

## Trigger

When user invokes `/designer` or asks to work with Penpot designs.

## Prerequisites

### One-time Setup

Before first use, the Penpot MCP server must be installed and configured:

**1. Clone and build the Penpot MCP server:**

```bash
mkdir -p ~/.local/share
git clone https://github.com/penpot/penpot-mcp.git ~/.local/share/penpot-mcp
cd ~/.local/share/penpot-mcp
npm install
npm run build:all
```

**2. Add Penpot MCP to OpenCode config:**

Create or update `opencode.json` in the project root:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "penpot": {
      "type": "remote",
      "url": "http://localhost:4401/mcp",
      "enabled": true
    }
  }
}
```

Or use the CLI:

```bash
opencode mcp add
# Select: Current project or Global
# Type: remote
# URL: http://localhost:4401/mcp
```

Verify with:

```bash
opencode mcp list
```

You should see `penpot` listed as connected (when servers are running).

## Process

### Step 1: Start Penpot MCP Servers

Check if the servers are already running:

```bash
pgrep -f "penpot-mcp" && curl -s http://localhost:4401/mcp > /dev/null 2>&1
```

If not running, start them:

```bash
cd ~/.local/share/penpot-mcp && npm run start:all &>/tmp/penpot-mcp.log &
```

Wait for servers to be ready (ports 4400-4403):
- **4400**: Plugin server (serves the Penpot plugin UI)
- **4401**: MCP HTTP/SSE endpoint
- **4402**: WebSocket server (plugin connection)
- **4403**: REPL server

Verify with:

```bash
sleep 3 && ss -tlnp | grep -E "440[0-3]"
```

### Step 2: Guide User to Connect Plugin

Inform the user:

> **Penpot MCP servers are running!**
>
> To connect Penpot:
> 1. Open [design.penpot.app](https://design.penpot.app) in your browser
> 2. Open a **design file**
> 3. Click the **Plugins menu** (puzzle piece icon, bottom-left)
> 4. Click **"Install plugin from URL"**
> 5. Enter: `http://localhost:4400/manifest.json`
> 6. Open the installed plugin
> 7. Click **"Connect to MCP server"**
>
> **Browser Warning**: If you get "The plugin doesn't exist or the URL is not correct":
> - **Brave**: Click the lion icon → turn **Shields OFF** for this site → refresh
> - **Chrome/Edge**: Look for a popup asking to allow local network access, or click the lock icon → Site settings → allow insecure content
> - **Firefox**: Usually works without issues (recommended)
>
> Let me know when you're connected!

### Step 3: Wait for Connection

The user must confirm the plugin is connected before MCP tools will work.

Check server logs if needed:

```bash
tail -20 /tmp/penpot-mcp.log
```

Look for WebSocket connection messages indicating the plugin connected.

### Step 4: Use Penpot MCP Tools

Once connected, the following MCP tools are available:

| Tool | Description |
|------|-------------|
| `penpot_execute_code` | Execute JavaScript code using the Penpot Plugin API |
| `penpot_high_level_overview` | Get an overview of the Penpot API and how to use it |
| `penpot_penpot_api_info` | Get documentation for specific Penpot API types |
| `penpot_export_shape` | Export a shape as PNG/SVG image |
| `penpot_import_image` | Import an image into the design |

### Step 5: Execute Design Tasks

Common design operations:

**Get Design Overview**

```javascript
// Get pages
const pages = penpotUtils.getPages();

// Get structure of current page (depth 3)
const structure = penpotUtils.shapeStructure(penpot.root, 3);

return { pages, structure };
```

**Find Elements**

```javascript
// Find shapes by name
const button = penpotUtils.findShape(s => s.name === "BaseButton");

// Find all text elements
const texts = penpotUtils.findShapes(s => s.type === "text", penpot.root);

// Get selected elements
const selected = penpot.selection;
```

**Modify Designs**

```javascript
// Change fill color
const shape = penpotUtils.findShape(s => s.name === "MyShape");
shape.fills = [{ fillColor: "#EC4899", fillOpacity: 1 }];
```

**Work with Components**

```javascript
// List library components
const components = penpot.library.local.components.map(c => ({
  id: c.id, 
  name: c.name
}));

// Get main instance of a component
const component = penpot.library.local.components.find(c => c.name === "Button");
const mainShape = component.mainInstance();
```

**Export Assets**

```
Use penpot_export_shape to export specific shapes as PNG/SVG
```

## Stopping the Servers

When done, stop the servers:

```bash
pkill -f "penpot-mcp"
```

## Troubleshooting

### "The plugin doesn't exist or the URL is not correct"

This is a browser security issue blocking localhost connections:
- **Brave**: Click lion icon → turn **Shields OFF** for design.penpot.app → refresh
- **Chrome/Edge**: Allow local network access when prompted, or go to lock icon → Site settings → Insecure content → Allow
- **Firefox**: Recommended - works without extra configuration

### Plugin won't connect to MCP server

- Check browser console (F12) for WebSocket errors
- Ensure servers are running: `ss -tlnp | grep 440`
- Keep the plugin UI open - closing it disconnects WebSocket

### Servers not responding

- Check logs: `tail -50 /tmp/penpot-mcp.log`
- Restart: `pkill -f penpot-mcp && cd ~/.local/share/penpot-mcp && npm run start:all`

### MCP tools not available in OpenCode

1. Ensure servers are running first
2. Check config: `opencode mcp list` should show penpot as connected
3. If not listed, add it: create `opencode.json` with penpot config (see Prerequisites)
4. Restart OpenCode after adding config

### "No results found" when searching for penpot tools

The MCP config was not loaded. Ensure:
1. `opencode.json` exists in project root (not `.opencode/config.json`)
2. Uses correct format with `"mcp"` key (not `"mcpServers"`)
3. Penpot servers are running before starting OpenCode

## Architecture

```
+----------------+     +------------------+     +------------------+
|                |     |                  |     |                  |
|   OpenCode     |<--->|   MCP Server     |<--->|  Penpot Plugin   |
|                |     |   (port 4401)    |     |  (WebSocket)     |
|                |     |                  |     |                  |
+----------------+     +------------------+     +------------------+
                              ^                         |
                              |                         v
                              |                 +------------------+
                              |                 |                  |
                              |                 |     Penpot       |
                              |                 |   (browser)      |
                              |                 |                  |
                              +-----------------+------------------+
```

## Resources

- [Penpot MCP GitHub](https://github.com/penpot/penpot-mcp)
- [Penpot Plugin API](https://help.penpot.app/plugins/)
- [Penpot Help](https://help.penpot.app/)
