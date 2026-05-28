# Hooks System Reference

Complete reference for Claude Agent SDK hooks system - intercept and control agent behavior.

## Overview

Hooks provide interception points throughout the agent execution lifecycle. Use hooks for:

- **Approval workflows** - Require human approval for specific actions
- **Audit logging** - Track all agent activities
- **Security controls** - Restrict or modify agent behavior
- **Rate limiting** - Control execution speed
- **Custom validation** - Add business logic checks

## Hook Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                      Agent Execution                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  on_session_start()                                          │
│       ↓                                                      │
│  ┌─────────────────────────────────────────┐                 │
│  │ For each query:                         │                 │
│  │                                         │                 │
│  │   on_query_start()                      │                 │
│  │       ↓                                 │                 │
│  │   ┌───────────────────────────┐         │                 │
│  │   │ For each tool call:       │         │                 │
│  │   │                           │         │                 │
│  │   │   on_tool_call()          │ ──→ ALLOW/REJECT/MODIFY   │
│  │   │       ↓                   │         │                 │
│  │   │   [Tool Execution]        │         │                 │
│  │   │       ↓                   │         │                 │
│  │   │   on_tool_result()        │         │                 │
│  │   │                           │         │                 │
│  │   └───────────────────────────┘         │                 │
│  │       ↓                                 │                 │
│  │   on_query_end()                        │                 │
│  │                                         │                 │
│  └─────────────────────────────────────────┘                 │
│       ↓                                                      │
│  on_session_end()                                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Base Hook Class

### Python

```python
from claude_sdk import Hook, HookResult
from claude_sdk.types import ToolCallContext, ToolResultContext, QueryContext

class BaseHook(Hook):
    """Base class for all hooks."""

    async def on_session_start(self, session_id: str) -> None:
        """Called when a new session starts."""
        pass

    async def on_session_end(self, session_id: str) -> None:
        """Called when session ends."""
        pass

    async def on_query_start(self, context: QueryContext) -> HookResult:
        """Called before processing a query."""
        return HookResult.ALLOW

    async def on_query_end(self, context: QueryContext, result: str) -> None:
        """Called after query completes."""
        pass

    async def on_tool_call(self, context: ToolCallContext) -> HookResult:
        """Called before tool execution. Return ALLOW, REJECT, or MODIFY."""
        return HookResult.ALLOW

    async def on_tool_result(self, context: ToolResultContext) -> None:
        """Called after tool execution completes."""
        pass

    async def on_error(self, error: Exception) -> None:
        """Called when an error occurs."""
        pass
```

### TypeScript

```typescript
import { Hook, HookResult, ToolCallContext, ToolResultContext, QueryContext } from '@anthropic/claude-sdk';

class BaseHook implements Hook {
  async onSessionStart(sessionId: string): Promise<void> {}

  async onSessionEnd(sessionId: string): Promise<void> {}

  async onQueryStart(context: QueryContext): Promise<HookResult> {
    return HookResult.ALLOW;
  }

  async onQueryEnd(context: QueryContext, result: string): Promise<void> {}

  async onToolCall(context: ToolCallContext): Promise<HookResult> {
    return HookResult.ALLOW;
  }

  async onToolResult(context: ToolResultContext): Promise<void> {}

  async onError(error: Error): Promise<void> {}
}
```

## HookResult Values

| Result | Description |
|--------|-------------|
| `HookResult.ALLOW` | Allow the action to proceed |
| `HookResult.REJECT` | Block the action |
| `HookResult.MODIFY` | Modify the action (with modified context) |

```python
# Allow
return HookResult.ALLOW

# Reject with reason
return HookResult.reject("Operation not permitted in production")

# Modify arguments
return HookResult.modify(modified_args={"path": "/safe/path"})
```

---

## Common Hook Patterns

### 1. Approval Hook

Require human approval for specific actions.

```python
from claude_sdk import Hook, HookResult
import asyncio

class ApprovalHook(Hook):
    """Require approval for write operations."""

    WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "Bash"}

    def __init__(self, approval_handler=None):
        self.approval_handler = approval_handler or self._default_approval

    async def on_tool_call(self, context: ToolCallContext) -> HookResult:
        if context.tool_name not in self.WRITE_TOOLS:
            return HookResult.ALLOW

        approved = await self.approval_handler(
            tool=context.tool_name,
            args=context.args,
            session_id=context.session_id
        )

        if approved:
            return HookResult.ALLOW
        return HookResult.reject(f"User rejected {context.tool_name}")

    async def _default_approval(self, tool: str, args: dict, session_id: str) -> bool:
        """Default CLI approval prompt."""
        print(f"\n{'='*50}")
        print(f"APPROVAL REQUIRED: {tool}")
        print(f"Arguments: {args}")
        print(f"{'='*50}")

        response = input("Approve? (y/n): ").strip().lower()
        return response == 'y'
```

### 2. Audit Hook

Log all agent activities.

```python
import json
from datetime import datetime
from claude_sdk import Hook

class AuditHook(Hook):
    """Log all agent activities for audit trail."""

    def __init__(self, log_file: str = "agent_audit.log"):
        self.log_file = log_file

    async def on_session_start(self, session_id: str):
        self._log("SESSION_START", {"session_id": session_id})

    async def on_session_end(self, session_id: str):
        self._log("SESSION_END", {"session_id": session_id})

    async def on_query_start(self, context: QueryContext):
        self._log("QUERY_START", {
            "session_id": context.session_id,
            "prompt": context.prompt[:200]  # Truncate for log
        })
        return HookResult.ALLOW

    async def on_tool_call(self, context: ToolCallContext):
        self._log("TOOL_CALL", {
            "session_id": context.session_id,
            "tool": context.tool_name,
            "args": self._sanitize_args(context.args)
        })
        return HookResult.ALLOW

    async def on_tool_result(self, context: ToolResultContext):
        self._log("TOOL_RESULT", {
            "session_id": context.session_id,
            "tool": context.tool_name,
            "success": context.success,
            "result_length": len(str(context.result))
        })

    def _log(self, event: str, data: dict):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            **data
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def _sanitize_args(self, args: dict) -> dict:
        """Remove sensitive information from args."""
        sanitized = args.copy()
        for key in ["password", "token", "api_key", "secret"]:
            if key in sanitized:
                sanitized[key] = "***REDACTED***"
        return sanitized
```

### 3. Rate Limit Hook

Control execution speed.

```python
import time
from collections import defaultdict
from claude_sdk import Hook, HookResult

class RateLimitHook(Hook):
    """Limit tool execution rate."""

    def __init__(
        self,
        max_calls_per_minute: int = 60,
        max_concurrent: int = 5
    ):
        self.max_calls_per_minute = max_calls_per_minute
        self.max_concurrent = max_concurrent
        self.call_times = []
        self.active_calls = 0

    async def on_tool_call(self, context: ToolCallContext) -> HookResult:
        now = time.time()

        # Clean old entries
        self.call_times = [t for t in self.call_times if now - t < 60]

        # Check rate limit
        if len(self.call_times) >= self.max_calls_per_minute:
            wait_time = 60 - (now - self.call_times[0])
            return HookResult.reject(
                f"Rate limit exceeded. Try again in {wait_time:.1f}s"
            )

        # Check concurrent limit
        if self.active_calls >= self.max_concurrent:
            return HookResult.reject(
                f"Too many concurrent calls ({self.max_concurrent} max)"
            )

        self.call_times.append(now)
        self.active_calls += 1
        return HookResult.ALLOW

    async def on_tool_result(self, context: ToolResultContext):
        self.active_calls -= 1
```

### 4. Sandbox Hook

Restrict file system access.

```python
import os
from claude_sdk import Hook, HookResult

class SandboxHook(Hook):
    """Restrict file system access to specific directories."""

    def __init__(self, allowed_paths: list, denied_patterns: list = None):
        self.allowed_paths = [os.path.abspath(p) for p in allowed_paths]
        self.denied_patterns = denied_patterns or [
            ".env", ".git", "node_modules", "__pycache__",
            ".ssh", ".aws", "credentials"
        ]

    async def on_tool_call(self, context: ToolCallContext) -> HookResult:
        if context.tool_name not in {"Read", "Write", "Edit", "Glob", "Grep"}:
            return HookResult.ALLOW

        path = context.args.get("path", "")
        abs_path = os.path.abspath(path)

        # Check allowed paths
        if not any(abs_path.startswith(allowed) for allowed in self.allowed_paths):
            return HookResult.reject(
                f"Access denied: {path} is outside allowed directories"
            )

        # Check denied patterns
        for pattern in self.denied_patterns:
            if pattern in abs_path:
                return HookResult.reject(
                    f"Access denied: {pattern} files are restricted"
                )

        return HookResult.ALLOW
```

### 5. Modification Hook

Modify tool arguments.

```python
from claude_sdk import Hook, HookResult

class PathNormalizationHook(Hook):
    """Normalize all file paths to project directory."""

    def __init__(self, project_root: str):
        self.project_root = project_root

    async def on_tool_call(self, context: ToolCallContext) -> HookResult:
        if context.tool_name not in {"Read", "Write", "Edit"}:
            return HookResult.ALLOW

        path = context.args.get("path", "")

        # Convert relative to absolute
        if not os.path.isabs(path):
            modified_args = context.args.copy()
            modified_args["path"] = os.path.join(self.project_root, path)
            return HookResult.modify(modified_args=modified_args)

        return HookResult.ALLOW
```

---

## Hook Composition

### Multiple Hooks

Hooks execute in order; first rejection stops the chain.

```python
client = ClaudeSDKClient(
    hooks=[
        AuditHook("audit.log"),        # Always logs (doesn't reject)
        RateLimitHook(max_calls=60),   # May reject
        SandboxHook(["/project"]),     # May reject
        ApprovalHook(),                # May reject
    ]
)
```

### Hook Priority

```python
from claude_sdk import Hook

class HighPriorityHook(Hook):
    priority = 100  # Higher = executes first

class LowPriorityHook(Hook):
    priority = 1    # Lower = executes later
```

---

## Async Hook Patterns

### External Approval Service

```python
import aiohttp
from claude_sdk import Hook, HookResult

class ExternalApprovalHook(Hook):
    """Request approval from external service."""

    def __init__(self, approval_url: str, api_key: str):
        self.approval_url = approval_url
        self.api_key = api_key

    async def on_tool_call(self, context: ToolCallContext) -> HookResult:
        if context.tool_name not in {"Write", "Edit", "Bash"}:
            return HookResult.ALLOW

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                self.approval_url,
                json={
                    "tool": context.tool_name,
                    "args": context.args,
                    "session_id": context.session_id
                },
                headers={"Authorization": f"Bearer {self.api_key}"}
            )

            result = await response.json()
            if result.get("approved"):
                return HookResult.ALLOW
            return HookResult.reject(result.get("reason", "Not approved"))
```

### WebSocket Approval

```python
import websockets
from claude_sdk import Hook, HookResult

class WebSocketApprovalHook(Hook):
    """Real-time approval via WebSocket."""

    def __init__(self, ws_url: str):
        self.ws_url = ws_url
        self._ws = None

    async def on_session_start(self, session_id: str):
        self._ws = await websockets.connect(self.ws_url)

    async def on_session_end(self, session_id: str):
        if self._ws:
            await self._ws.close()

    async def on_tool_call(self, context: ToolCallContext) -> HookResult:
        await self._ws.send(json.dumps({
            "type": "approval_request",
            "tool": context.tool_name,
            "args": context.args
        }))

        response = json.loads(await self._ws.recv())
        if response.get("approved"):
            return HookResult.ALLOW
        return HookResult.reject(response.get("reason"))
```

---

## Testing Hooks

```python
import pytest
from claude_sdk import ClaudeSDKClient
from claude_sdk.testing import MockToolCall

@pytest.fixture
def approval_hook():
    return ApprovalHook(approval_handler=lambda *args: True)

@pytest.fixture
def client(approval_hook):
    return ClaudeSDKClient(hooks=[approval_hook])

async def test_approval_hook_allows_read():
    hook = ApprovalHook()
    context = MockToolCall(tool_name="Read", args={"path": "file.txt"})

    result = await hook.on_tool_call(context)
    assert result == HookResult.ALLOW

async def test_approval_hook_requires_approval_for_write():
    approved = False
    hook = ApprovalHook(approval_handler=lambda *args: approved)
    context = MockToolCall(tool_name="Write", args={"path": "file.txt"})

    result = await hook.on_tool_call(context)
    assert result.is_rejected

async def test_sandbox_hook_blocks_outside_paths():
    hook = SandboxHook(allowed_paths=["/project"])
    context = MockToolCall(tool_name="Read", args={"path": "/etc/passwd"})

    result = await hook.on_tool_call(context)
    assert result.is_rejected
```

---

## Best Practices

### 1. Keep Hooks Lightweight

```python
# Good - fast check
async def on_tool_call(self, context):
    if context.tool_name in self.blocked_tools:
        return HookResult.REJECT
    return HookResult.ALLOW

# Avoid - heavy operation in hook
async def on_tool_call(self, context):
    # Don't do database queries or API calls for every tool call
    result = await slow_database_check(context)
    return result
```

### 2. Handle Errors Gracefully

```python
async def on_tool_call(self, context):
    try:
        return await self._check_approval(context)
    except Exception as e:
        logger.error(f"Hook error: {e}")
        # Fail safe - block on error
        return HookResult.reject("Internal approval error")
```

### 3. Use Hooks for Cross-Cutting Concerns

```python
# Good - audit is cross-cutting
class AuditHook(Hook): ...

# Avoid - business logic in hooks
class ValidateOrderHook(Hook):  # Should be in tool logic
    ...
```
