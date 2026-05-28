# Python SDK Reference

Complete API reference for Claude Agent SDK Python package.

## Installation

```bash
pip install claude-agent-sdk
```

## Core Functions

### query()

One-shot task execution with full autonomy.

```python
from claude_sdk import query

result = await query(
    prompt: str,                      # Task description
    model: str = "claude-sonnet-4-20250514",  # Model to use
    max_tokens: int = 4096,           # Max response tokens
    tools: List[str] = None,          # Built-in tools to enable
    mcp_servers: List[MCPServer] = None,  # MCP servers to connect
    allowed_commands: List[str] = None,   # Bash command whitelist
    denied_commands: List[str] = None,    # Bash command blacklist
    working_directory: str = None,    # Working directory for operations
    timeout: int = 300,               # Timeout in seconds
    hooks: List[Hook] = None,         # Behavior hooks
) -> QueryResult
```

**Returns**: `QueryResult` object

```python
class QueryResult:
    content: str          # Final response text
    tool_calls: List[ToolCall]  # Tools that were used
    tokens_used: int      # Total tokens consumed
    duration: float       # Execution time in seconds
    status: str           # "success", "error", "timeout"
```

**Example**:

```python
from claude_sdk import query

result = await query(
    prompt="Find all Python files with TODO comments",
    tools=["Glob", "Grep", "Read"],
    working_directory="/path/to/project"
)

print(f"Found: {result.content}")
print(f"Used {result.tokens_used} tokens in {result.duration}s")
```

---

## ClaudeSDKClient

Multi-turn conversation client for complex tasks.

### Constructor

```python
from claude_sdk import ClaudeSDKClient

client = ClaudeSDKClient(
    model: str = "claude-sonnet-4-20250514",
    system_prompt: str = None,        # System instructions
    max_tokens: int = 8192,           # Max tokens per turn
    tools: List[str] = None,          # Built-in tools
    mcp_servers: List[MCPServer] = None,
    hooks: List[Hook] = None,
    api_key: str = None,              # Override ANTHROPIC_API_KEY env
    base_url: str = None,             # Custom API endpoint
)
```

### create_session()

Create a new conversation session.

```python
async def create_session(
    session_id: str = None,           # Custom session ID
    context: dict = None,             # Initial context variables
    history: List[Message] = None,    # Pre-load conversation history
) -> Session
```

**Example**:

```python
client = ClaudeSDKClient(
    model="claude-sonnet-4-20250514",
    system_prompt="You are a code reviewer focusing on security.",
    tools=["Read", "Grep", "Glob"]
)

async with client.create_session() as session:
    # Each query maintains conversation context
    await session.query("Read the authentication module")
    await session.query("What security issues do you see?")
    recommendations = await session.query("Provide recommendations")
```

---

## Session

Active conversation session with context.

### query()

Send a query within the session.

```python
async def query(
    prompt: str,                      # User message
    tools: List[str] = None,          # Override session tools
    max_tokens: int = None,           # Override max tokens
    stream: bool = False,             # Enable streaming
) -> SessionResponse
```

### get_history()

Get conversation history.

```python
def get_history() -> List[Message]
```

### add_context()

Add context variables accessible to the agent.

```python
def add_context(key: str, value: Any)
```

### fork()

Create a branched session for exploration.

```python
async def fork(branch_name: str = None) -> Session
```

**Example**:

```python
async with client.create_session() as session:
    await session.query("Analyze options for refactoring")

    # Fork to explore different approaches
    branch_a = await session.fork("approach-a")
    branch_b = await session.fork("approach-b")

    result_a = await branch_a.query("Try extracting to separate class")
    result_b = await branch_b.query("Try using composition pattern")

    # Compare results
    await session.query(f"Compare: {result_a.content} vs {result_b.content}")
```

---

## Models

### Available Models

```python
# Recommended for most tasks
"claude-sonnet-4-20250514"

# For complex reasoning
"claude-opus-4-20250514"

# For fast, simple tasks
"claude-haiku-3-5-20241022"
```

### Model Selection Guidelines

| Use Case | Recommended Model |
|----------|------------------|
| Code review | claude-sonnet-4-20250514 |
| Complex debugging | claude-opus-4-20250514 |
| Simple file operations | claude-haiku-3-5-20241022 |
| Autonomous agents | claude-sonnet-4-20250514 |
| Cost-sensitive | claude-haiku-3-5-20241022 |

---

## Error Handling

```python
from claude_sdk import (
    ClaudeSDKError,      # Base exception
    ToolError,           # Tool execution failed
    RateLimitError,      # API rate limited
    AuthenticationError, # Invalid API key
    TimeoutError,        # Operation timed out
    HookRejectionError,  # Hook rejected action
)

try:
    result = await query("Execute task")
except ToolError as e:
    print(f"Tool {e.tool_name} failed: {e.message}")
    print(f"Arguments: {e.args}")
except RateLimitError as e:
    print(f"Rate limited. Retry after: {e.retry_after}s")
except TimeoutError:
    print("Operation timed out")
except ClaudeSDKError as e:
    print(f"SDK error: {e}")
```

---

## Configuration

### Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...

# Optional
CLAUDE_SDK_MODEL=claude-sonnet-4-20250514
CLAUDE_SDK_MAX_TOKENS=8192
CLAUDE_SDK_TIMEOUT=300
CLAUDE_SDK_LOG_LEVEL=INFO
```

### Configuration File

Create `.claude-sdk.yaml` in project root:

```yaml
model: claude-sonnet-4-20250514
max_tokens: 8192
timeout: 300

tools:
  enabled:
    - Read
    - Write
    - Edit
    - Bash
    - Grep
    - Glob

bash:
  allowed_commands:
    - python
    - pytest
    - pip
  denied_commands:
    - rm -rf
    - sudo

hooks:
  - approval:
      tools: [Write, Edit, Bash]
  - audit:
      log_file: ./logs/claude-sdk.log
```

---

## Async Patterns

### Concurrent Operations

```python
import asyncio
from claude_sdk import query

async def analyze_files(files: List[str]):
    tasks = [
        query(f"Analyze {file}", tools=["Read"])
        for file in files
    ]
    results = await asyncio.gather(*tasks)
    return results

# Run concurrently
results = await analyze_files(["main.py", "utils.py", "config.py"])
```

### Streaming Responses

```python
async with client.create_session() as session:
    async for chunk in session.query("Explain this code", stream=True):
        print(chunk.content, end="", flush=True)
```

---

## Integration with IPA Platform

### Adapter Pattern

```python
# backend/src/integrations/claude_sdk/client.py

from claude_sdk import ClaudeSDKClient
from src.core.config import settings
from src.core.logging import get_logger

logger = get_logger(__name__)

class ClaudeSDKAdapter:
    """Adapter for Claude Agent SDK in IPA Platform."""

    def __init__(self):
        self._client = ClaudeSDKClient(
            model=settings.CLAUDE_MODEL,
            api_key=settings.ANTHROPIC_API_KEY,
            hooks=[
                PlatformApprovalHook(),
                PlatformAuditHook(),
            ]
        )
        logger.info("Initialized ClaudeSDKAdapter")

    async def execute_autonomous_task(self, task: str) -> dict:
        """Execute task with full autonomy."""
        async with self._client.create_session() as session:
            result = await session.query(task)
            return {
                "content": result.content,
                "tool_calls": [tc.to_dict() for tc in result.tool_calls],
                "tokens_used": result.tokens_used,
            }
```

---

## Best Practices

### 1. Use Context Managers

```python
# Good - automatic cleanup
async with client.create_session() as session:
    await session.query("...")

# Avoid - manual cleanup needed
session = await client.create_session()
try:
    await session.query("...")
finally:
    await session.close()
```

### 2. Implement Proper Hooks

```python
from claude_sdk import Hook, HookResult

class ProductionHook(Hook):
    async def on_tool_call(self, tool_name, args):
        # Log all tool calls
        logger.info(f"Tool call: {tool_name}({args})")

        # Require approval for write operations
        if tool_name in ["Write", "Edit", "Bash"]:
            return await self._request_approval(tool_name, args)

        return HookResult.ALLOW
```

### 3. Handle Rate Limits

```python
from claude_sdk import query, RateLimitError
import asyncio

async def query_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await query(prompt)
        except RateLimitError as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(e.retry_after)
            else:
                raise
```
