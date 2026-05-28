# Dynamic Manifests

> **Definition**: A runtime capability discovery system that allows clients to query available tools, resources, and features dynamically without requiring restarts or static configuration.

**Navigation**: [← Progressive Disclosure](./progressive-disclosure.md) | [↑ Best Practices](../SKILL.md) | [Deferred Loading →](./deferred-loading.md)

---

## Table of Contents

- [What Is It?](#what-is-it) ← Start here
- [Quick Start](#quick-start) ← Get it working in 5 minutes
- [Why Dynamic?](#why-dynamic)
- [Configuration](#configuration) ← For practitioners
- [Server Implementation](#server-implementation)
- [Client Implementation](#client-implementation)
- [Capability Systems](#capability-systems) ← For architects
- [MCP-Specific Setup](#mcp-specific-setup)
- [Troubleshooting](#troubleshooting)

---

## What Is It?

Traditional systems load capabilities at startup. Dynamic manifests query them at runtime.

### Visual Comparison

```
STATIC MANIFEST (Old Way)
─────────────────────────────────────
Startup:
  Load manifest.json → Parse all tools → Cache forever
  Tools: [A, B, C, D, E]

Hour 1: User needs Tool A
  ✓ Use cached Tool A

Hour 2: Server adds Tool F
  ✗ Client doesn't know about Tool F
  ✗ Requires restart to see Tool F

Hour 3: Server removes Tool D
  ✗ Client still tries to use Tool D
  ✗ Error: Tool not found


DYNAMIC MANIFEST (New Way)
─────────────────────────────────────
Startup:
  Connect to server → Register for updates
  Initial query: Tools = [A, B, C, D, E]

Hour 1: User needs Tool A
  Query server → Tools available: [A, B, C, D, E]
  ✓ Use Tool A

Hour 2: Server adds Tool F
  Server notifies → Client updates
  Query server → Tools available: [A, B, C, D, E, F]
  ✓ Tool F immediately available

Hour 3: Server removes Tool D
  Server notifies → Client updates
  Query server → Tools available: [A, B, C, E, F]
  ✓ Client never tries to use Tool D
```

### Key Difference

| Aspect | Static | Dynamic |
|--------|--------|---------|
| **When capabilities are discovered** | Startup only | Runtime, continuously |
| **Adding new features** | Requires restart | Available immediately |
| **Removing features** | Clients break until restart | Graceful degradation |
| **Conditional availability** | Not possible | Context-aware |
| **Memory usage** | All features loaded | On-demand loading |

---

## Quick Start

Get dynamic manifests working in 5 minutes.

### Step 1: Server Configuration

Create manifest file at standard location:

**.well-known/mcp/manifest.json**
```json
{
  "id": "my-mcp-server",
  "name": "My MCP Server",
  "version": "1.0.0",
  "last_updated": "2025-10-20T10:00:00Z",
  "capabilities": {
    "tools": true,
    "resources": true,
    "prompts": true,
    "dynamic_discovery": true
  },
  "tools": [
    {
      "name": "get_weather",
      "description": "Get current weather for a location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "City name"
          }
        },
        "required": ["location"]
      }
    }
  ]
}
```

### Step 2: Client Configuration

**For Claude Desktop** (claude_desktop_config.json):
```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["path/to/server.js"],
      "dynamicDiscovery": true,
      "discoveryInterval": 5000
    }
  }
}
```

**For Spring AI**:
```java
@Bean
public McpClient mcpClient() {
    return McpClient.builder()
        .dynamicToolDiscovery(true)
        .discoveryIntervalMs(5000)
        .build();
}
```

### Step 3: Test

Add new tool to manifest (without restart):
```json
{
  "tools": [
    {
      "name": "get_weather",
      ...
    },
    {
      "name": "get_forecast",
      "description": "Get 5-day forecast",
      "parameters": { ... }
    }
  ]
}
```

Client should see new tool within 5 seconds!

---

## Why Dynamic?

### Problem 1: Static Configuration is Brittle

```
Dev adds new feature → Commit server code
  ↓
Deploy server → New feature available
  ↓
❌ But: Clients don't know about it
  ↓
Users restart apps → Feature finally available
```

This creates delays and poor UX.

### Problem 2: Context Awareness

Static manifests can't adapt:

```
User A (beginner):      Static manifest shows all 50 tools ❌
User B (expert):        Static manifest shows all 50 tools ❌
User C (admin):         Static manifest shows all 50 tools ❌

Everyone sees everything, regardless of skill/permissions.
```

Dynamic manifests adapt:

```
User A (beginner):      Query → 5 basic tools ✓
User B (expert):        Query → 25 tools (basic + advanced) ✓
User C (admin):         Query → 50 tools (all features) ✓

Each user sees appropriate capabilities.
```

### Problem 3: Performance

Static manifests load everything:

```
Startup: Load 50 tools → Initialize all dependencies
Memory: 500MB
Time: 10 seconds
```

Dynamic manifests load on-demand:

```
Startup: Connect to server
Memory: 50MB
Time: 1 second

Later: User requests Tool X → Load Tool X dependencies
```

---

## Configuration

### Server-Side: Expose Discovery Endpoints

Your MCP server must implement:

```
GET /.well-known/mcp/manifest.json    → Full manifest
GET /tools/list                        → Available tools
GET /resources/list                    → Available resources
GET /prompts/list                      → Available prompts
```

**Example Express.js Server**:
```javascript
const express = require('express');
const app = express();

// Manifest endpoint
app.get('/.well-known/mcp/manifest.json', (req, res) => {
  res.json({
    id: 'my-server',
    version: '1.0.0',
    last_updated: new Date().toISOString(),
    capabilities: {
      tools: true,
      dynamic_discovery: true
    },
    tools: getAvailableTools(req.user) // Context-aware!
  });
});

// Tools list endpoint
app.get('/tools/list', (req, res) => {
  const tools = getAvailableTools(req.user);
  res.json({ tools });
});

function getAvailableTools(user) {
  const tools = [
    { name: 'basic_tool', description: '...' }
  ];

  if (user.isAdmin) {
    tools.push({ name: 'admin_tool', description: '...' });
  }

  return tools;
}

app.listen(3000);
```

### Client-Side: Enable Dynamic Discovery

**Key Configuration Options**:

| Option | Description | Default | Recommended |
|--------|-------------|---------|-------------|
| `dynamicDiscovery` | Enable runtime queries | `false` | `true` |
| `discoveryInterval` | How often to check (ms) | `10000` | `5000` |
| `cacheManifest` | Cache between queries | `true` | `true` |
| `cacheTimeout` | Cache duration (ms) | `300000` | `60000` |

**Example: Python Client**:
```python
from mcp import MCPClient

client = MCPClient(
    server_url="http://localhost:3000",
    dynamic_discovery=True,
    discovery_interval=5000,  # Check every 5 seconds
)

# Don't cache tools - always query fresh
async def execute_tool(tool_name, params):
    # This queries server each time
    tools = await client.get_available_tools()
    tool = tools.get(tool_name)

    if not tool:
        raise Exception(f"Tool {tool_name} not available")

    return await tool.execute(params)
```

### Optimization: Smart Caching

Don't query on every request - use smart caching:

```python
import hashlib
import json
from datetime import datetime, timedelta

class SmartManifestCache:
    def __init__(self, client, ttl_seconds=60):
        self.client = client
        self.ttl = timedelta(seconds=ttl_seconds)
        self.cached_manifest = None
        self.cached_hash = None
        self.last_fetch = None

    async def get_tools(self):
        now = datetime.now()

        # Check if cache is still valid
        if (self.cached_manifest and self.last_fetch and
            now - self.last_fetch < self.ttl):
            return self.cached_manifest

        # Fetch new manifest
        manifest = await self.client.fetch_manifest()
        manifest_hash = hashlib.md5(
            json.dumps(manifest, sort_keys=True).encode()
        ).hexdigest()

        # Only update if manifest changed
        if manifest_hash != self.cached_hash:
            print("Manifest changed! New tools available.")
            self.cached_manifest = manifest
            self.cached_hash = manifest_hash

        self.last_fetch = now
        return self.cached_manifest
```

---

## Server Implementation

### Pattern 1: Basic Dynamic Server

Minimal implementation with runtime queries:

```python
from fastapi import FastAPI
from typing import List, Dict

app = FastAPI()

# Dynamic tool registry
tool_registry = {}

def register_tool(name: str, config: Dict):
    """Register a tool at runtime"""
    tool_registry[name] = config

def unregister_tool(name: str):
    """Remove a tool at runtime"""
    if name in tool_registry:
        del tool_registry[name]

@app.get("/.well-known/mcp/manifest.json")
async def get_manifest():
    return {
        "id": "dynamic-server",
        "version": "1.0.0",
        "last_updated": datetime.now().isoformat(),
        "capabilities": {
            "tools": True,
            "dynamic_discovery": True
        },
        "tools": list(tool_registry.values())
    }

@app.get("/tools/list")
async def list_tools():
    return {"tools": list(tool_registry.values())}

# Add/remove tools dynamically
@app.post("/admin/register_tool")
async def admin_register_tool(tool_config: Dict):
    register_tool(tool_config["name"], tool_config)
    return {"status": "registered"}

# Initial tools
register_tool("get_weather", {
    "name": "get_weather",
    "description": "Get weather for a location",
    "parameters": {...}
})
```

### Pattern 2: Context-Aware Capabilities

Adapt capabilities based on user/context:

```python
from fastapi import FastAPI, Request
from typing import Optional

@app.get("/tools/list")
async def list_tools(request: Request):
    user = get_user_from_request(request)
    context = detect_context(request)

    tools = []

    # Basic tools for everyone
    tools.extend(get_basic_tools())

    # Skill-based tools
    if user.skill_level >= "intermediate":
        tools.extend(get_advanced_tools())

    # Permission-based tools
    if user.has_permission("admin"):
        tools.extend(get_admin_tools())

    # Context-based tools
    if context.project_type == "data_science":
        tools.extend(get_data_tools())

    if context.language == "python":
        tools.extend(get_python_tools())

    return {"tools": tools}

def detect_context(request: Request) -> Context:
    """Detect context from request headers/params"""
    return Context(
        project_type=request.headers.get("X-Project-Type"),
        language=request.headers.get("X-Language"),
        working_dir=request.headers.get("X-Working-Dir")
    )
```

### Pattern 3: Change Notifications

Notify clients when capabilities change:

```python
from fastapi import FastAPI, WebSocket
from typing import Set
import asyncio

app = FastAPI()
active_connections: Set[WebSocket] = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        active_connections.remove(websocket)

async def notify_tools_changed():
    """Notify all connected clients that tools changed"""
    message = {
        "event": "tools_changed",
        "timestamp": datetime.now().isoformat()
    }

    disconnected = set()
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except:
            disconnected.add(connection)

    # Clean up disconnected clients
    active_connections.difference_update(disconnected)

# When tools change
@app.post("/admin/register_tool")
async def admin_register_tool(tool_config: Dict):
    register_tool(tool_config["name"], tool_config)
    await notify_tools_changed()  # ← Notify clients!
    return {"status": "registered"}
```

---

## Client Implementation

### Pattern 1: Polling

Periodically check for changes:

```python
import asyncio
from typing import Optional

class PollingMCPClient:
    def __init__(self, server_url: str, poll_interval: int = 5):
        self.server_url = server_url
        self.poll_interval = poll_interval
        self.cached_tools = None
        self._polling_task = None

    async def start(self):
        """Start polling for manifest changes"""
        self._polling_task = asyncio.create_task(self._poll_loop())

    async def stop(self):
        """Stop polling"""
        if self._polling_task:
            self._polling_task.cancel()

    async def _poll_loop(self):
        """Poll server for changes"""
        while True:
            try:
                tools = await self._fetch_tools()
                if tools != self.cached_tools:
                    print("Tools changed!")
                    self.cached_tools = tools
                    await self._on_tools_changed(tools)
            except Exception as e:
                print(f"Error polling: {e}")

            await asyncio.sleep(self.poll_interval)

    async def _fetch_tools(self):
        """Fetch tools from server"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.server_url}/tools/list") as resp:
                data = await resp.json()
                return data["tools"]

    async def _on_tools_changed(self, tools):
        """Handle tool changes"""
        # Update UI, clear caches, etc.
        pass
```

### Pattern 2: WebSocket Subscriptions

Real-time updates via WebSocket:

```python
import asyncio
import websockets
import json

class WebSocketMCPClient:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.ws = None
        self.cached_tools = None

    async def connect(self):
        """Connect to server WebSocket"""
        ws_url = self.server_url.replace("http", "ws") + "/ws"
        self.ws = await websockets.connect(ws_url)

        # Start listening for events
        asyncio.create_task(self._listen())

        # Fetch initial tools
        await self.refresh_tools()

    async def _listen(self):
        """Listen for server events"""
        async for message in self.ws:
            event = json.loads(message)

            if event["event"] == "tools_changed":
                print("Server notified: tools changed")
                await self.refresh_tools()

    async def refresh_tools(self):
        """Fetch latest tools from server"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.server_url}/tools/list") as resp:
                data = await resp.json()
                self.cached_tools = data["tools"]
                print(f"Refreshed {len(self.cached_tools)} tools")
```

### Pattern 3: Lazy Query

Don't cache - always query fresh:

```python
class LazyMCPClient:
    """Client that always queries server for latest capabilities"""

    def __init__(self, server_url: str):
        self.server_url = server_url

    async def get_tool(self, tool_name: str):
        """Get a specific tool (always fresh from server)"""
        tools = await self._fetch_tools()
        return next((t for t in tools if t["name"] == tool_name), None)

    async def execute_tool(self, tool_name: str, params: dict):
        """Execute a tool (checks availability first)"""
        tool = await self.get_tool(tool_name)

        if not tool:
            raise Exception(f"Tool {tool_name} not available")

        # Execute tool...
        return await self._execute(tool, params)

    async def _fetch_tools(self):
        """Always fetch fresh from server"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.server_url}/tools/list") as resp:
                data = await resp.json()
                return data["tools"]
```

---

## Capability Systems

### Tiered Capabilities

Implement progressive disclosure through capability tiers:

```python
class CapabilityTier(Enum):
    BASIC = 1       # Everyone gets these
    INTERMEDIATE = 2 # Requires skill level
    ADVANCED = 3     # Requires permission
    EXPERT = 4       # Requires admin

class CapabilityManager:
    def __init__(self):
        self.capabilities = {
            CapabilityTier.BASIC: [
                "search", "file_read", "file_write"
            ],
            CapabilityTier.INTERMEDIATE: [
                "bulk_operations", "advanced_search"
            ],
            CapabilityTier.ADVANCED: [
                "system_config", "deployment"
            ],
            CapabilityTier.EXPERT: [
                "debug_mode", "raw_sql"
            ]
        }

    def get_capabilities_for_user(self, user):
        """Return capabilities based on user tier"""
        capabilities = []

        # Basic: everyone
        capabilities.extend(self.capabilities[CapabilityTier.BASIC])

        # Intermediate: skill-based
        if user.skill_level >= "intermediate":
            capabilities.extend(self.capabilities[CapabilityTier.INTERMEDIATE])

        # Advanced: permission-based
        if user.has_permission("advanced"):
            capabilities.extend(self.capabilities[CapabilityTier.ADVANCED])

        # Expert: admin only
        if user.is_admin:
            capabilities.extend(self.capabilities[CapabilityTier.EXPERT])

        return capabilities
```

### Conditional Capabilities

Enable features based on runtime conditions:

```python
class ConditionalCapabilities:
    def get_capabilities(self, context):
        caps = self.get_base_capabilities()

        # Environment-based
        if context.environment == "production":
            caps.remove("debug_tools")
        else:
            caps.append("mock_data_generator")

        # Project-based
        if context.has_file("package.json"):
            caps.extend(["npm_tools", "node_debugger"])

        if context.has_file("requirements.txt"):
            caps.extend(["pip_tools", "python_debugger"])

        # Time-based
        if context.is_business_hours():
            caps.append("live_support_chat")

        # Resource-based
        if context.disk_space > 10_000_000_000:  # 10GB
            caps.append("video_processing")

        return caps
```

### Gradual Feature Rollout

Use dynamic manifests for A/B testing and gradual rollouts:

```python
class FeatureRollout:
    def __init__(self):
        self.features = {
            "new_search_algorithm": {
                "rollout_percentage": 10,  # 10% of users
                "enabled_for": set()
            },
            "beta_ui": {
                "rollout_percentage": 5,
                "enabled_for": set()
            }
        }

    def should_enable_feature(self, feature_name, user_id):
        """Determine if feature should be enabled for user"""
        feature = self.features.get(feature_name)
        if not feature:
            return False

        # Already enabled?
        if user_id in feature["enabled_for"]:
            return True

        # Roll dice
        import random
        if random.random() * 100 < feature["rollout_percentage"]:
            feature["enabled_for"].add(user_id)
            return True

        return False

    def get_capabilities_for_user(self, user_id):
        caps = ["basic_tool_1", "basic_tool_2"]

        if self.should_enable_feature("new_search_algorithm", user_id):
            caps.append("new_search_tool")

        if self.should_enable_feature("beta_ui", user_id):
            caps.append("beta_ui_tools")

        return caps
```

---

## MCP-Specific Setup

### Standard MCP Manifest Location

```
project_root/
├── .well-known/
│   └── mcp/
│       └── manifest.json  ← Must be here
```

### MCP Manifest Schema

```json
{
  "$schema": "https://spec.modelcontextprotocol.io/manifest/v1",
  "id": "unique-server-id",
  "name": "Human Readable Name",
  "version": "1.0.0",
  "description": "What this server does",
  "last_updated": "2025-10-20T10:00:00Z",

  "capabilities": {
    "tools": true,
    "resources": true,
    "prompts": true,
    "sampling": false,
    "dynamic_discovery": true
  },

  "tools": [
    {
      "name": "tool_name",
      "description": "What the tool does",
      "inputSchema": {
        "type": "object",
        "properties": {
          "param1": {
            "type": "string",
            "description": "Parameter description"
          }
        },
        "required": ["param1"]
      }
    }
  ],

  "resources": [
    {
      "uri": "resource://path/to/resource",
      "name": "Resource Name",
      "description": "What the resource provides",
      "mimeType": "application/json"
    }
  ]
}
```

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "my-dynamic-server": {
      "command": "node",
      "args": ["path/to/server.js"],

      // Enable dynamic discovery
      "dynamicDiscovery": true,

      // How often to check for changes (ms)
      "discoveryInterval": 5000,

      // Optional: Environment variables
      "env": {
        "API_KEY": "your-key-here"
      }
    }
  }
}
```

### Known Limitations

⚠️ **Claude Code Issue #4110**: Dynamic resources may not be discovered properly in Claude Code. Workarounds:
- Use static resources
- Use tools instead of resources
- Poll for changes manually

---

## Troubleshooting

### Problem: Changes Not Appearing

**Symptoms**: Server updated, client doesn't see changes

**Check**:
1. Is `dynamicDiscovery` enabled in client config?
   ```json
   { "dynamicDiscovery": true }
   ```

2. Is manifest endpoint returning updated timestamp?
   ```bash
   curl http://localhost:3000/.well-known/mcp/manifest.json
   # Check "last_updated" field
   ```

3. Is cache timeout too long?
   ```json
   { "cacheTimeout": 60000 }  // Try lower value
   ```

4. Check client logs:
   ```bash
   tail -f ~/.config/claude/logs/mcp.log
   ```

### Problem: Too Many Requests

**Symptoms**: Server overwhelmed with manifest queries

**Solutions**:
1. Increase discovery interval:
   ```json
   { "discoveryInterval": 30000 }  // 30 seconds
   ```

2. Implement rate limiting:
   ```python
   from slowapi import Limiter

   limiter = Limiter(key_func=get_remote_address)

   @app.get("/tools/list")
   @limiter.limit("10/minute")
   async def list_tools():
       ...
   ```

3. Use ETags for conditional requests:
   ```python
   @app.get("/tools/list")
   async def list_tools(request: Request):
       tools = get_tools()
       tools_hash = hashlib.md5(json.dumps(tools).encode()).hexdigest()

       if request.headers.get("If-None-Match") == tools_hash:
           return Response(status_code=304)  # Not Modified

       return Response(
           content=json.dumps(tools),
           headers={"ETag": tools_hash}
       )
   ```

### Problem: Stale Cache

**Symptoms**: Client sees old capabilities after server update

**Solutions**:
1. Add cache-busting timestamp:
   ```json
   {
     "last_updated": "2025-10-20T10:30:00Z",
     "cache_key": "v1-20251020-103000"
   }
   ```

2. Implement version-based invalidation:
   ```python
   @app.get("/tools/list")
   async def list_tools(client_version: Optional[str] = None):
       current_version = "v1.2.3"

       if client_version != current_version:
           # Force full refresh
           return {
               "version": current_version,
               "invalidate_cache": True,
               "tools": get_tools()
           }

       return {"tools": get_tools()}
   ```

---

## Related Concepts

### Dynamic Manifests ↔ [Progressive Disclosure](./progressive-disclosure.md)

- Progressive disclosure: **Design pattern** for revealing information gradually
- Dynamic manifests: **Technical implementation** for discovering capabilities

Example flow:
1. User opens app (Progressive disclosure: show basic UI)
2. Client queries server (Dynamic manifest: get available tools)
3. Server returns capabilities based on user tier (Progressive disclosure: only relevant features)
4. UI updates to show available features (Progressive disclosure: tiered feature set)

### Dynamic Manifests → [Deferred Loading](./deferred-loading.md)

Dynamic manifests tell you **what's available**.
Deferred loading determines **when to load it**.

```
Dynamic Manifest Query:
  Server: "Tool X is available"

Deferred Loading Decision:
  Client: "Don't load Tool X yet, wait until user calls it"

User Invokes Tool X:
  Client: "Now load Tool X's dependencies"
```

See: [Deferred Loading: Lazy Initialization](./deferred-loading.md#lazy-initialization)

---

**Navigation**: [← Progressive Disclosure](./progressive-disclosure.md) | [↑ Best Practices](../SKILL.md) | [Deferred Loading →](./deferred-loading.md)

**Last Updated**: 2025-10-20
