# SDK Usage

Programmatic access to Claude Code via TypeScript and Python SDKs.

## Overview

| SDK | Package | Best For |
|-----|---------|----------|
| TypeScript | `@anthropic-ai/claude-code` | Node.js/Bun applications |
| Python | `claude-code-sdk` | Python automation, data pipelines |

Both SDKs provide:
- Streaming responses
- Session management
- Custom tool configuration
- Hook integration
- Error handling

## TypeScript SDK

### Installation

```bash
npm install @anthropic-ai/claude-code
# or
bun add @anthropic-ai/claude-code
```

### Prerequisites

- Node.js 18+ or Bun
- Claude Code CLI installed: `npm install -g @anthropic-ai/claude-code`
- `ANTHROPIC_API_KEY` environment variable set

### Basic Usage

```typescript
import { query } from '@anthropic-ai/claude-code';

async function main() {
  const response = await query({
    prompt: "What is this project?",
    cwd: process.cwd(),
  });

  for await (const message of response) {
    if (message.type === 'text') {
      console.log(message.content);
    }
  }
}

main();
```

### Query Options

```typescript
interface QueryOptions {
  prompt: string;                    // The prompt to send
  cwd?: string;                      // Working directory
  systemPrompt?: string;             // Custom system prompt
  appendSystemPrompt?: string;       // Append to default prompt
  allowedTools?: string[];           // Tools to auto-approve
  disallowedTools?: string[];        // Tools to disable
  maxTurns?: number;                 // Limit agentic turns
  outputFormat?: 'text' | 'json' | 'stream-json';
  sessionId?: string;                // Resume specific session
  continue?: boolean;                // Continue last session
  model?: string;                    // Model to use
  permissionMode?: string;           // Permission mode
}
```

### Streaming Responses

```typescript
import { query } from '@anthropic-ai/claude-code';

async function streamResponse() {
  const response = await query({
    prompt: "Explain this codebase",
    outputFormat: 'stream-json',
  });

  for await (const event of response) {
    switch (event.type) {
      case 'content_block_delta':
        process.stdout.write(event.delta.text);
        break;
      case 'message_stop':
        console.log('\n--- Done ---');
        break;
      case 'tool_use':
        console.log(`Tool: ${event.name}`);
        break;
    }
  }
}
```

### Session Management

```typescript
import { query } from '@anthropic-ai/claude-code';

async function multiTurnConversation() {
  // First turn
  let sessionId: string | undefined;

  const first = await query({
    prompt: "Analyze the authentication system",
    outputFormat: 'json',
  });

  for await (const message of first) {
    if (message.session_id) {
      sessionId = message.session_id;
    }
  }

  // Continue conversation
  const second = await query({
    prompt: "What security improvements would you suggest?",
    sessionId: sessionId,
  });

  for await (const message of second) {
    console.log(message);
  }
}
```

### Tool Configuration

```typescript
import { query } from '@anthropic-ai/claude-code';

async function restrictedTools() {
  const response = await query({
    prompt: "Fix the failing tests",
    allowedTools: ['Read', 'Edit', 'Bash(npm test:*)'],
    disallowedTools: ['Write'],  // Can't create new files
    maxTurns: 5,
  });

  for await (const message of response) {
    console.log(message);
  }
}
```

### Error Handling

```typescript
import { query, CLINotFoundError, CLIConnectionError } from '@anthropic-ai/claude-code';

async function safeQuery() {
  try {
    const response = await query({ prompt: "Hello" });
    for await (const message of response) {
      console.log(message);
    }
  } catch (error) {
    if (error instanceof CLINotFoundError) {
      console.error("Claude Code CLI not installed");
      console.error("Run: npm install -g @anthropic-ai/claude-code");
    } else if (error instanceof CLIConnectionError) {
      console.error("Failed to connect to Claude Code");
    } else {
      throw error;
    }
  }
}
```

## Python SDK

### Installation

```bash
pip install claude-code-sdk
```

### Prerequisites

- Python 3.10+
- Node.js installed
- Claude Code CLI: `npm install -g @anthropic-ai/claude-code`
- `ANTHROPIC_API_KEY` environment variable set

### Basic Usage

```python
import asyncio
from claude_code_sdk import query

async def main():
    async for message in query(prompt="What is this project?"):
        print(message)

asyncio.run(main())
```

### Query Options

```python
from claude_code_sdk import query, ClaudeCodeOptions

options = ClaudeCodeOptions(
    prompt="Fix the failing tests",
    cwd="/path/to/project",
    system_prompt="You are a test engineer",
    max_turns=5,
    allowed_tools=["Read", "Edit", "Bash"],
    permission_mode="auto-accept",
)

async for message in query(**options):
    print(message)
```

### Message Types

```python
from claude_code_sdk import query, AssistantMessage, ToolUseBlock, TextBlock

async def process_messages():
    async for message in query(prompt="Analyze code"):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Text: {block.text}")
                elif isinstance(block, ToolUseBlock):
                    print(f"Tool: {block.name}, Input: {block.input}")
```

### Session Management

```python
from claude_code_sdk import query

async def multi_turn():
    session_id = None

    # First turn
    async for message in query(prompt="Analyze auth system", output_format="json"):
        if hasattr(message, 'session_id'):
            session_id = message.session_id
        print(message)

    # Continue conversation
    async for message in query(
        prompt="What improvements do you suggest?",
        session_id=session_id
    ):
        print(message)
```

### Custom Tools (In-Process MCP)

```python
from claude_code_sdk import ClaudeSDKClient, tool

@tool("greet", "Greet a user by name", {"name": str})
async def greet_user(args):
    return {
        "content": [{
            "type": "text",
            "text": f"Hello, {args['name']}!"
        }]
    }

async def with_custom_tools():
    client = ClaudeSDKClient(tools=[greet_user])

    async for message in client.query("Greet the user named Alice"):
        print(message)
```

### Hooks

```python
from claude_code_sdk import ClaudeCodeOptions

def pre_tool_hook(tool_name: str, tool_input: dict) -> bool:
    """Return False to block tool execution."""
    if tool_name == "Bash" and "rm -rf" in tool_input.get("command", ""):
        print("Blocked dangerous command!")
        return False
    return True

options = ClaudeCodeOptions(
    prompt="Clean up the project",
    hooks={
        "pre_tool": pre_tool_hook
    }
)
```

### Error Handling

```python
from claude_code_sdk import (
    query,
    CLINotFoundError,
    CLIConnectionError,
    ProcessError,
    CLIJSONDecodeError
)

async def safe_query():
    try:
        async for message in query(prompt="Hello"):
            print(message)
    except CLINotFoundError:
        print("Claude Code CLI not installed")
        print("Run: npm install -g @anthropic-ai/claude-code")
    except CLIConnectionError as e:
        print(f"Connection failed: {e}")
    except ProcessError as e:
        print(f"Process error: {e}")
    except CLIJSONDecodeError as e:
        print(f"Failed to parse response: {e}")
```

## SDK vs CLI Comparison

| Feature | CLI (`claude -p`) | SDK |
|---------|-------------------|-----|
| Setup | Just CLI | CLI + package |
| Streaming | `--output-format stream-json` | Native async iterators |
| Custom tools | Limited | Full MCP support |
| Hooks | Via config | In-process functions |
| Error handling | Exit codes | Typed exceptions |
| Session management | `--resume` flag | Session objects |
| Type safety | None | Full TypeScript/Python types |

## When to Use Each

### Use CLI (`claude -p`) when:
- Simple one-shot tasks
- Shell scripts
- CI/CD pipelines
- Quick automation

### Use SDK when:
- Building applications
- Need streaming responses
- Custom tool integration
- Complex session management
- Type safety required
- Error handling important

## Common Patterns

### TypeScript: Batch Processing

```typescript
import { query } from '@anthropic-ai/claude-code';

async function batchProcess(files: string[]) {
  const results = [];

  for (const file of files) {
    const response = await query({
      prompt: `Add JSDoc comments to ${file}`,
      allowedTools: ['Read', 'Edit'],
      maxTurns: 3,
    });

    let result = '';
    for await (const message of response) {
      if (message.type === 'text') {
        result += message.content;
      }
    }
    results.push({ file, result });
  }

  return results;
}
```

### Python: CI/CD Integration

```python
import asyncio
import json
from claude_code_sdk import query

async def code_review(diff: str) -> dict:
    result = {
        "passed": True,
        "issues": [],
        "suggestions": []
    }

    async for message in query(
        prompt=f"Review this diff for issues:\n\n{diff}",
        output_format="json",
        allowed_tools=["Read"],
        max_turns=1
    ):
        if hasattr(message, 'structured_output'):
            return message.structured_output

    return result

# Usage in CI
if __name__ == "__main__":
    diff = open("pr.diff").read()
    result = asyncio.run(code_review(diff))

    if not result["passed"]:
        print("Review failed!")
        for issue in result["issues"]:
            print(f"- {issue}")
        exit(1)
```
