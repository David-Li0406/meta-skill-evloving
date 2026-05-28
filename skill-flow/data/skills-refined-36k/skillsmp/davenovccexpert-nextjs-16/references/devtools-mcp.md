<overview>
Next.js 16 DevTools MCP (Model Context Protocol) enables AI-assisted debugging with contextual insight into your application.
</overview>

<basics>
**What is DevTools MCP?**

MCP is a protocol that allows AI coding assistants (Claude, Cursor, etc.) to access your Next.js application's internals in real-time during development.

**Enabled by default** in Next.js 16+ at:
```
http://localhost:3000/_next/mcp
```

No configuration needed - just run `npm run dev`.
</basics>

<setup>
**For AI assistants to use MCP, configure the MCP server:**

```json
// .cursor/mcp.json or equivalent
{
  "mcpServers": {
    "next-devtools": {
      "command": "npx",
      "args": ["-y", "next-devtools-mcp@latest"]
    }
  }
}
```

**Claude Code users:** MCP is typically auto-detected. If not:
```json
// claude_desktop_config.json
{
  "mcpServers": {
    "next-devtools": {
      "command": "npx",
      "args": ["-y", "next-devtools-mcp@latest"]
    }
  }
}
```
</setup>

<available_tools>
**Runtime tools (require dev server running):**

<tool name="get_errors">
**Purpose:** Get all errors from the application

**Returns:**
- Build errors
- Runtime errors
- TypeScript errors

**Example output:**
```json
{
  "buildErrors": [],
  "runtimeErrors": [
    {
      "message": "Cannot read properties of undefined",
      "stack": "...",
      "source": "app/dashboard/page.tsx:25"
    }
  ],
  "typeErrors": [
    {
      "message": "Type 'string' is not assignable to type 'number'",
      "file": "lib/utils.ts",
      "line": 15
    }
  ]
}
```
</tool>

<tool name="get_logs">
**Purpose:** Get development log file path

**Returns:** Path to log file containing:
- Browser console output
- Server-side logs
- API route logs
</tool>

<tool name="get_routes">
**Purpose:** Get all routes in the application (added in 16.1)

**Returns:**
```json
{
  "routes": [
    { "path": "/", "type": "page" },
    { "path": "/dashboard", "type": "page" },
    { "path": "/api/users", "type": "api" }
  ]
}
```
</tool>

<tool name="get_page_metadata">
**Purpose:** Get metadata about routes, pages, and components

**Returns:**
- Route structure
- Component tree
- Data dependencies
</tool>

<tool name="get_project_metadata">
**Purpose:** Get project configuration and structure

**Returns:**
- Next.js version
- Dependencies
- Config options
- Dev server URL
</tool>

<tool name="get_server_action_by_id">
**Purpose:** Look up Server Action by ID

**Use case:** Debugging Server Action execution issues
</tool>

**Static tools (work without dev server):**

<tool name="nextjs_docs">
**Purpose:** Query official Next.js documentation

**Use case:** Getting authoritative answers about Next.js features
</tool>

<tool name="upgrade_nextjs_16">
**Purpose:** Help with upgrading to Next.js 16

**Provides:** Migration steps, breaking changes, codemods
</tool>

<tool name="enable_cache_components">
**Purpose:** Help configure cache components

**Provides:** Configuration snippets, usage examples
</tool>
</available_tools>

<debugging_workflow>
**1. Start with errors:**
```
Ask AI: "What errors does my Next.js app have?"
AI uses: get_errors tool
```

**2. Get context:**
```
Ask AI: "Show me all routes in my app"
AI uses: get_routes tool
```

**3. Investigate specific issues:**
```
Ask AI: "Why is my dashboard page throwing a hydration error?"
AI uses: get_errors, get_page_metadata
```

**4. Check Server Actions:**
```
Ask AI: "Debug the Server Action that's failing"
AI uses: get_server_action_by_id
```
</debugging_workflow>

<common_debug_scenarios>
<scenario name="hydration-error">
**Problem:** "Hydration failed because the initial UI does not match"

**AI debugging flow:**
1. `get_errors` - See full error details
2. `get_page_metadata` - Identify component causing mismatch
3. Analyze Server vs Client rendering differences

**Common causes AI will identify:**
- Using `window`/`document` in Server Component
- Different Date/time between server and client
- Browser extensions modifying DOM
</scenario>

<scenario name="build-error">
**Problem:** Build fails with cryptic error

**AI debugging flow:**
1. `get_errors` - Get complete error with stack trace
2. `get_project_metadata` - Check config and dependencies
3. Provide fix based on error pattern
</scenario>

<scenario name="server-action-fail">
**Problem:** Server Action not working

**AI debugging flow:**
1. `get_server_action_by_id` - Find the action
2. `get_errors` - Check for runtime errors
3. `get_logs` - See server-side logs
</scenario>

<scenario name="routing-issue">
**Problem:** Route not found or wrong route

**AI debugging flow:**
1. `get_routes` - Map all routes
2. `get_page_metadata` - Check route configuration
3. Identify missing files or incorrect structure
</scenario>
</common_debug_scenarios>

<troubleshooting>
**MCP not working?**

1. **Check dev server is running:**
```bash
npm run dev
# Should show: Ready - started server on localhost:3000
```

2. **Verify MCP endpoint:**
```bash
curl http://localhost:3000/_next/mcp
# Should return MCP server info
```

3. **Clear npx cache:**
```bash
npx clear-npx-cache
# Then restart MCP client
```

4. **Check Next.js version:**
```bash
npx next --version
# Should be 16.0.0 or higher
```

5. **Restart MCP client** (Cursor, Claude Code, etc.)

**Error: "Module not found"**
- Clear npx cache
- Restart MCP client
- Ensure `next-devtools-mcp@latest` is accessible
</troubleshooting>

<best_practices>
**For effective AI-assisted debugging:**

1. **Keep dev server running** - Most tools need it

2. **Describe symptoms clearly:**
   - "Page loads but button doesn't work"
   - "Error appears after form submit"
   - "Build passes but runtime error"

3. **Provide context:**
   - "This worked before I added the Server Action"
   - "Only happens on this specific page"

4. **Let AI use tools** - Don't manually copy-paste errors; let AI fetch them via MCP

5. **Iterate with AI:**
   - AI suggests fix
   - You apply fix
   - AI re-checks via MCP
   - Repeat until resolved
</best_practices>
