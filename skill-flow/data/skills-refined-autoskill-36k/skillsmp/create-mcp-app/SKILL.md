---
name: create-mcp-app
description: Build interactive UIs that run inside MCP-enabled hosts like Claude Desktop. Use when the user wants to create an MCP App, build an MCP UI, or create interactive content for Claude Desktop.
---

# Create MCP App

Build interactive UIs that run inside MCP-enabled hosts like Claude Desktop. An MCP App combines an MCP tool with an HTML resource to display rich, interactive content.

## Core Concept: Tool + Resource

Every MCP App requires two parts linked together:

1. **Tool** - Called by the LLM/host, returns data
2. **Resource** - Serves the bundled HTML UI that displays the data
3. **Link** - The tool's `_meta.ui.resourceUri` references the resource

```
Host calls tool → Server returns result → Host renders resource UI → UI receives result
```

## Quick Start Decision Tree

### Framework Selection

| Framework | SDK Support | Best For |
|-----------|-------------|----------|
| React | `useApp` hook provided | Teams familiar with React |
| Vanilla JS | Manual lifecycle | Simple apps, no build complexity |
| Vue/Svelte/Preact/Solid | Manual lifecycle | Framework preference |

### Project Context

**Adding to existing MCP server:**
- Import `registerAppTool`, `registerAppResource` from SDK
- Add tool registration with `_meta.ui.resourceUri`
- Add resource registration serving bundled HTML

**Creating new MCP server:**
- Set up server with transport (stdio or HTTP)
- Register tools and resources
- Configure build system with `vite-plugin-singlefile`

## Getting Reference Code

Clone the SDK repository for working examples and API documentation:

```bash
git clone --branch "v$(npm view @modelcontextprotocol/ext-apps version)" --depth 1 https://github.com/modelcontextprotocol/ext-apps.git /tmp/mcp-ext-apps
```

### Framework Templates

Learn and adapt from `/tmp/mcp-ext-apps/examples/basic-server-{framework}/`:

| Template | Key Files |
|----------|-----------|
| `basic-server-vanillajs/` | `server.ts`, `src/mcp-app.ts`, `mcp-app.html` |
| `basic-server-react/` | `server.ts`, `src/mcp-app.tsx` (uses `useApp` hook) |
| `basic-server-vue/` | `server.ts`, `src/App.vue` |
| `basic-server-svelte/` | `server.ts`, `src/App.svelte` |
| `basic-server-preact/` | `server.ts`, `src/mcp-app.tsx` |
| `basic-server-solid/` | `server.ts`, `src/mcp-app.tsx` |

Each template includes:
- Complete `server.ts` with `registerAppTool` and `registerAppResource`
- Client-side app with all lifecycle handlers
- `vite.config.ts` with `vite-plugin-singlefile`
- `package.json` with all required dependencies
- `.gitignore` excluding `node_modules/` and `dist/`

### API Reference (Source Files)

Read JSDoc documentation directly from source:

| File | Contents |
|------|----------|
| `src/app.ts` | `App` class, handlers (`ontoolinput`, `ontoolresult`, `onhostcontextchanged`, `onteardown`), lifecycle |
| `src/server/index.ts` | `registerAppTool`, `registerAppResource`, tool visibility options |
| `src/spec.types.ts` | All type definitions: `McpUiHostContext`, CSS variable keys, display modes |
| `src/styles.ts` | `applyDocumentTheme`, `applyHostStyleVariables`, `applyHostFonts` |
| `src/react/useApp.tsx` | `useApp` hook for React apps |
| `src/react/useHostStyles.ts` | `useHostStyles`, `useHostStyleVariables`, `useHostFonts` hooks |

### Advanced Examples

| Example | Pattern Demonstrated |
|---------|---------------------|
| `examples/wiki-explorer-server/` | `callServerTool` for interactive data fetching |
| `examples/system-monitor-server/` | Polling pattern with interval management |
| `examples/video-resource-server/` | Binary/blob resources |
| `examples/sheet-music-server/` | `ontoolinput` - processing tool args before execution completes |
| `examples/threejs-server/` | `ontoolinputpartial` - streaming/progressive rendering |
| `examples/map-server/` | `updateModelContext` - keeping model informed of UI state |
| `examples/transcript-server/` | `updateModelContext` + `sendMessage` - background context updates + user-initiated messages |
| `examples/basic-host/` | Reference host implementation using `AppBridge` |

## Critical Implementation Notes

### Adding Dependencies

Use `npm install` to add dependencies rather than manually writing version numbers:

```bash
npm install @modelcontextprotocol/ext-apps @modelcontextprotocol/sdk zod
```

This lets npm resolve the latest compatible versions. Never specify version numbers from memory.

### TypeScript Server Execution

Use `tsx` as a devDependency for running TypeScript server files:

```bash
npm install -D tsx
```

```json
"scripts": {
  "serve": "tsx server.ts"
}
```

Note: The SDK examples use `bun` but generated projects should use `tsx` for broader compatibility.

### Handler Registration Order

Register ALL handlers BEFORE calling `app.connect()`:

```typescript
const app = new App({ name: "My App", version: "1.0.0" });

// Register handlers first
app.ontoolinput = (params) => { /* handle input */ };
app.ontoolresult = (result) => { /* handle result */ };
app.onhostcontextchanged = (ctx) => { /* handle context */ };
app.onteardown = async () => { return {}; };

// Then connect
await app.connect();
```

### Tool Visibility

Control who can access tools via `_meta.ui.visibility`:

```typescript
// Default: visible to both model and app
_meta: { ui: { resourceUri, visibility: ["model", "app"] } }

// UI-only (hidden from model) - for refresh buttons, form submissions
_meta: { ui: { resourceUri, visibility: ["app"] } }

// Model-only (app cannot call)
_meta: { ui: { resourceUri, visibility: ["model"] } }
```

### Host Styling Integration

**Vanilla JS** - Use helper functions:
```typescript
import { applyDocumentTheme, applyHostStyleVariables, applyHostFonts } from "@modelcontextprotocol/ext-apps";

app.onhostcontextchanged = (ctx) => {
  if (ctx.theme) applyDocumentTheme(ctx.theme);
  if (ctx.styles?.variables) applyHostStyleVariables(ctx.styles.variables);
  if (ctx.styles?.css?.fonts) applyHostFonts(ctx.styles.css.fonts);
};
```

**React** - Use hooks:
```typescript
import { useApp, useHostStyles } from "@modelcontextprotocol/ext-apps/react";

const { app } = useApp({ appInfo, capabilities, onAppCreated });
useHostStyles(app); // Handles theme, styles, fonts automatically
```

### Safe Area Handling

Always respect `safeAreaInsets`:

```typescript
app.onhostcontextchanged = (ctx) => {
  if (ctx.safeAreaInsets) {
    const { top, right, bottom, left } = ctx.safeAreaInsets;
    document.body.style.padding = `${top}px ${right}px ${bottom}px ${left}px`;
  }
};
```

## Common Mistakes to Avoid

1. **Handlers after connect()** - Register ALL handlers BEFORE calling `app.connect()`
2. **Missing single-file bundling** - Must use `vite-plugin-singlefile`
3. **Forgetting resource registration** - Both tool AND resource must be registered
4. **Missing resourceUri link** - Tool must have `_meta.ui.resourceUri`
5. **Ignoring safe area insets** - Always handle `ctx.safeAreaInsets`
6. **No text fallback** - Always provide `content` array for non-UI hosts
7. **Hardcoded styles** - Use host CSS variables for theme integration

## Testing

### Using basic-host

Test MCP Apps locally with the basic-host example:

```bash
# Terminal 1: Build and run your server
npm run build && npm run serve

# Terminal 2: Run basic-host (from cloned repo)
cd /tmp/mcp-ext-apps/examples/basic-host
npm install
SERVERS='["http://localhost:3001/mcp"]' npm run start
# Open http://localhost:8080
```

Configure `SERVERS` with a JSON array of your server URLs (default: `http://localhost:3001/mcp`).

### Debug with sendLog

Send debug logs to the host application (rather than just the iframe's dev console):

```typescript
await app.sendLog({ level: "info", data: "Debug message" });
await app.sendLog({ level: "error", data: { error: err.message } });
```
