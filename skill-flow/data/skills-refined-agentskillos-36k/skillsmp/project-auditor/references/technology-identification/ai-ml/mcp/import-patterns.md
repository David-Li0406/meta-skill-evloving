# MCP Import Patterns

Import statement patterns for detecting Model Context Protocol usage.

## Confidence

**Detection Confidence**: 95%

## JavaScript/TypeScript Patterns

### ES Module Imports

```regex
import.*from ['"]@modelcontextprotocol/sdk['"]
import.*from ['"]@modelcontextprotocol/server['"]
import.*from ['"]@modelcontextprotocol/client['"]
import { Server } from ['"]@modelcontextprotocol/sdk/server['"]
import { Client } from ['"]@modelcontextprotocol/sdk/client['"]
import { StdioServerTransport } from ['"]@modelcontextprotocol/sdk/server/stdio['"]
import { SSEServerTransport } from ['"]@modelcontextprotocol/sdk/server/sse['"]
```

### CommonJS Requires

```regex
require\(['"]@modelcontextprotocol/sdk['"]\)
require\(['"]@modelcontextprotocol/server['"]\)
```

### TypeScript Type Imports

```regex
import type.*from ['"]@modelcontextprotocol/sdk['"]
```

## Python Patterns

### Standard Imports

```regex
^from mcp import
^from mcp\.server import
^from mcp\.client import
^from mcp\.server\.stdio import
^from mcp\.server\.models import
^import mcp$
^import mcp\.
from modelcontextprotocol import
```

## Example Detections

### JavaScript Server

```javascript
import { Server } from "@modelcontextprotocol/sdk/server";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio";
```

### Python Server

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
```

### Python Client

```python
from mcp import Client
from mcp.client import list_tools, call_tool
```
