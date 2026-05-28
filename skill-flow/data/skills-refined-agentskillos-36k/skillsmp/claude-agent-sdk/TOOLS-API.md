# Built-in Tools Reference

Complete reference for Claude Agent SDK built-in tools.

## Overview

Claude Agent SDK provides built-in tools that agents can use autonomously. These tools are sandboxed and controllable via hooks.

## File System Tools

### Read

Read file contents.

```python
# Python
from claude_sdk.tools import Read

content = await Read("path/to/file.py")
content = await Read("path/to/file.py", encoding="utf-8")

# With line range
content = await Read("file.py", start_line=10, end_line=50)
```

```typescript
// TypeScript
import { Read } from '@anthropic/claude-sdk/tools';

const content = await Read("path/to/file.ts");
const content = await Read("path/to/file.ts", { encoding: "utf-8" });

// With line range
const content = await Read("file.ts", { startLine: 10, endLine: 50 });
```

**Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | string | File path (absolute or relative) |
| `encoding` | string | Text encoding (default: utf-8) |
| `start_line` | int | Start reading from this line |
| `end_line` | int | Stop reading at this line |

---

### Write

Write content to a file.

```python
# Python
from claude_sdk.tools import Write

await Write("output.txt", "Hello, World!")
await Write("data.json", json.dumps(data), encoding="utf-8")

# Create with directories
await Write("path/to/new/file.txt", content, create_dirs=True)
```

```typescript
// TypeScript
import { Write } from '@anthropic/claude-sdk/tools';

await Write("output.txt", "Hello, World!");
await Write("data.json", JSON.stringify(data), { encoding: "utf-8" });

// Create with directories
await Write("path/to/new/file.txt", content, { createDirs: true });
```

**Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | string | File path |
| `content` | string | Content to write |
| `encoding` | string | Text encoding (default: utf-8) |
| `create_dirs` | bool | Create parent directories |
| `overwrite` | bool | Overwrite if exists (default: true) |

---

### Edit

Edit existing file content.

```python
# Python
from claude_sdk.tools import Edit

# Replace text
await Edit("file.py", old_text="def old_name", new_text="def new_name")

# Replace all occurrences
await Edit("file.py", old_text="foo", new_text="bar", replace_all=True)
```

```typescript
// TypeScript
import { Edit } from '@anthropic/claude-sdk/tools';

// Replace text
await Edit("file.ts", { oldText: "const oldName", newText: "const newName" });

// Replace all occurrences
await Edit("file.ts", { oldText: "foo", newText: "bar", replaceAll: true });
```

**Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | string | File path |
| `old_text` | string | Text to find |
| `new_text` | string | Replacement text |
| `replace_all` | bool | Replace all occurrences |

---

### MultiEdit

Apply multiple edits to files atomically.

```python
# Python
from claude_sdk.tools import MultiEdit

edits = [
    {"path": "file1.py", "old_text": "old1", "new_text": "new1"},
    {"path": "file2.py", "old_text": "old2", "new_text": "new2"},
]
await MultiEdit(edits)
```

```typescript
// TypeScript
import { MultiEdit } from '@anthropic/claude-sdk/tools';

const edits = [
  { path: "file1.ts", oldText: "old1", newText: "new1" },
  { path: "file2.ts", oldText: "old2", newText: "new2" },
];
await MultiEdit(edits);
```

---

## Search Tools

### Glob

Find files by pattern.

```python
# Python
from claude_sdk.tools import Glob

files = await Glob("**/*.py")
files = await Glob("src/**/*.tsx", exclude=["node_modules/**"])
```

```typescript
// TypeScript
import { Glob } from '@anthropic/claude-sdk/tools';

const files = await Glob("**/*.ts");
const files = await Glob("src/**/*.tsx", { exclude: ["node_modules/**"] });
```

**Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `pattern` | string | Glob pattern |
| `path` | string | Base directory |
| `exclude` | string[] | Patterns to exclude |
| `include_hidden` | bool | Include hidden files |

---

### Grep

Search file contents.

```python
# Python
from claude_sdk.tools import Grep

# Simple search
matches = await Grep("TODO", path="src/")

# Regex search
matches = await Grep(r"def \w+\(", path="**/*.py", regex=True)

# With context lines
matches = await Grep("error", path="logs/", before=2, after=2)
```

```typescript
// TypeScript
import { Grep } from '@anthropic/claude-sdk/tools';

// Simple search
const matches = await Grep("TODO", { path: "src/" });

// Regex search
const matches = await Grep("function \\w+\\(", { path: "**/*.ts", regex: true });

// With context lines
const matches = await Grep("error", { path: "logs/", before: 2, after: 2 });
```

**Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `pattern` | string | Search pattern |
| `path` | string | File/directory path |
| `regex` | bool | Use regex matching |
| `case_sensitive` | bool | Case sensitive (default: true) |
| `before` | int | Context lines before match |
| `after` | int | Context lines after match |
| `max_matches` | int | Limit results |

---

## Command Execution

### Bash

Execute shell commands.

```python
# Python
from claude_sdk.tools import Bash

# Simple command
result = await Bash("ls -la")

# With working directory
result = await Bash("npm test", cwd="/path/to/project")

# With timeout
result = await Bash("long-running-command", timeout=60)
```

```typescript
// TypeScript
import { Bash } from '@anthropic/claude-sdk/tools';

// Simple command
const result = await Bash("ls -la");

// With working directory
const result = await Bash("npm test", { cwd: "/path/to/project" });

// With timeout
const result = await Bash("long-running-command", { timeout: 60 });
```

**Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `command` | string | Command to execute |
| `cwd` | string | Working directory |
| `timeout` | int | Timeout in seconds |
| `env` | dict | Environment variables |

**Returns**:
```python
class BashResult:
    stdout: str       # Standard output
    stderr: str       # Standard error
    exit_code: int    # Exit code
    timed_out: bool   # Whether command timed out
```

**Security Controls**:

```python
# Restrict allowed commands
result = await query(
    prompt="Run tests",
    tools=["Bash"],
    allowed_commands=["pytest", "python", "pip"],
    denied_commands=["rm", "sudo", "curl | bash"]
)
```

---

## Web Tools

### WebSearch

Search the web.

```python
# Python
from claude_sdk.tools import WebSearch

results = await WebSearch("Python async best practices")
results = await WebSearch("site:github.com pytorch examples")
```

```typescript
// TypeScript
import { WebSearch } from '@anthropic/claude-sdk/tools';

const results = await WebSearch("Python async best practices");
const results = await WebSearch("site:github.com pytorch examples");
```

**Returns**:
```python
class SearchResults:
    results: List[SearchResult]

class SearchResult:
    title: str
    url: str
    snippet: str
```

---

### WebFetch

Fetch content from a URL.

```python
# Python
from claude_sdk.tools import WebFetch

content = await WebFetch("https://example.com/api/data")
content = await WebFetch(
    "https://api.example.com/data",
    headers={"Authorization": "Bearer token"}
)
```

```typescript
// TypeScript
import { WebFetch } from '@anthropic/claude-sdk/tools';

const content = await WebFetch("https://example.com/api/data");
const content = await WebFetch(
  "https://api.example.com/data",
  { headers: { Authorization: "Bearer token" } }
);
```

**Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | string | URL to fetch |
| `headers` | dict | Request headers |
| `timeout` | int | Timeout in seconds |
| `method` | string | HTTP method (default: GET) |

---

## Agent Delegation

### Task

Delegate subtasks to specialized subagents.

```python
# Python
from claude_sdk.tools import Task

# Simple delegation
result = await Task(
    prompt="Analyze this file for security issues",
    tools=["Read", "Grep"]
)

# With specialized agent
result = await Task(
    prompt="Write comprehensive tests",
    agent_type="test-writer",
    tools=["Read", "Write", "Bash"],
    system_prompt="You are an expert test writer."
)
```

```typescript
// TypeScript
import { Task } from '@anthropic/claude-sdk/tools';

// Simple delegation
const result = await Task({
  prompt: "Analyze this file for security issues",
  tools: ["Read", "Grep"]
});

// With specialized agent
const result = await Task({
  prompt: "Write comprehensive tests",
  agentType: "test-writer",
  tools: ["Read", "Write", "Bash"],
  systemPrompt: "You are an expert test writer."
});
```

**Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | string | Task description |
| `tools` | string[] | Tools for subagent |
| `agent_type` | string | Specialized agent type |
| `system_prompt` | string | Custom instructions |
| `max_tokens` | int | Token limit |
| `timeout` | int | Timeout in seconds |

---

## Tool Configuration

### Enabling/Disabling Tools

```python
# Enable specific tools
result = await query(
    prompt="Read and analyze files",
    tools=["Read", "Grep", "Glob"]  # Only these tools available
)

# Enable all tools
result = await query(
    prompt="Full access task",
    tools="all"
)

# Disable specific tools
result = await query(
    prompt="Read-only access",
    tools=["Read", "Grep", "Glob"],
    disabled_tools=["Write", "Edit", "Bash"]
)
```

### Tool Permissions via Hooks

```python
from claude_sdk import Hook, HookResult

class ToolPermissionHook(Hook):
    """Control tool access based on context."""

    # Read-only tools (always allowed)
    READ_ONLY = {"Read", "Grep", "Glob", "WebSearch"}

    # Write tools (require approval)
    WRITE_TOOLS = {"Write", "Edit", "MultiEdit"}

    # Dangerous tools (always require approval)
    DANGEROUS = {"Bash", "Task"}

    async def on_tool_call(self, tool_name: str, args: dict) -> HookResult:
        if tool_name in self.READ_ONLY:
            return HookResult.ALLOW

        if tool_name in self.WRITE_TOOLS:
            return await self._request_write_approval(tool_name, args)

        if tool_name in self.DANGEROUS:
            return await self._request_dangerous_approval(tool_name, args)

        return HookResult.REJECT  # Unknown tool

    async def _request_write_approval(self, tool, args):
        # Implementation
        return HookResult.ALLOW

    async def _request_dangerous_approval(self, tool, args):
        # Stricter approval process
        return HookResult.ALLOW
```

---

## Tool Output Limits

Default limits to prevent excessive output:

| Tool | Default Limit |
|------|---------------|
| Read | 100,000 characters |
| Grep | 1,000 matches |
| Glob | 10,000 files |
| Bash | 100,000 characters stdout |
| WebFetch | 1,000,000 characters |

Override limits:

```python
result = await Read("large_file.txt", max_chars=500000)
results = await Grep("pattern", max_matches=5000)
```

---

## Error Handling

```python
from claude_sdk.tools import ToolError, PermissionDeniedError, NotFoundError

try:
    content = await Read("nonexistent.py")
except NotFoundError as e:
    print(f"File not found: {e.path}")
except PermissionDeniedError as e:
    print(f"Permission denied: {e.path}")
except ToolError as e:
    print(f"Tool error: {e}")
```

---

## Best Practices

### 1. Use Minimal Tools

```python
# Good - only necessary tools
result = await query(
    prompt="Count lines in Python files",
    tools=["Glob", "Read"]  # Minimal set
)

# Avoid - too many tools
result = await query(
    prompt="Count lines in Python files",
    tools="all"  # Unnecessary access
)
```

### 2. Validate Tool Results

```python
from claude_sdk.tools import Bash

result = await Bash("python script.py")
if result.exit_code != 0:
    raise Exception(f"Script failed: {result.stderr}")
```

### 3. Handle Large Outputs

```python
# Use pagination for large files
content = await Read("large.log", start_line=0, end_line=100)

# Use search instead of reading all
matches = await Grep("ERROR", path="large.log", max_matches=50)
```
