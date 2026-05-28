# Claude Agent SDK / Anthropic Agents

**Category**: ai-ml/agents
**Description**: Anthropic's Claude Agent SDK and tool use patterns for building AI agents

## Package Detection

### NPM
- `@anthropic-ai/sdk`

### PYPI
- `anthropic`

## Agent Pattern Detection

### Python Tool Use Patterns
File extensions: .py

**Pattern**: `tools=\[|tool_choice=`
- Tool definition in API calls
- Example: `response = client.messages.create(..., tools=[...])`

**Pattern**: `"type":\s*"function"|type.*function`
- Function tool definitions
- Example: `{"type": "function", "function": {"name": "search", ...}}`

**Pattern**: `tool_use|ToolUseBlock|ToolResultBlock`
- Tool use response handling
- Example: `if block.type == "tool_use":`

**Pattern**: `input_schema|parameters.*schema`
- Tool schema definitions
- Example: `"input_schema": {"type": "object", "properties": {...}}`

### JavaScript/TypeScript Patterns
File extensions: .js, .ts

**Pattern**: `tools:\s*\[|toolChoice:`
- Tool configuration
- Example: `const response = await client.messages.create({ tools: [...] })`

**Pattern**: `type:\s*['"]tool_use['"]`
- Tool use content blocks
- Example: `if (block.type === 'tool_use') {...}`

**Pattern**: `ToolUseBlock|ToolResultBlock`
- TypeScript type annotations
- Example: `const toolUse: ToolUseBlock = block`

### Agentic Loop Patterns

**Pattern**: `while.*tool_use|for.*tool_use`
- Agentic conversation loops
- Example: `while response.stop_reason == "tool_use":`

**Pattern**: `stop_reason.*tool_use|stopReason.*tool_use`
- Tool use continuation detection
- Example: `if (response.stop_reason === "tool_use") {...}`

**Pattern**: `messages\.append|messages\.push`
- Conversation history management
- Example: `messages.append({"role": "assistant", "content": response.content})`

## Claude Computer Use Patterns

**Pattern**: `computer_use|computer-use`
- Computer use beta feature
- Example: `anthropic-beta: computer-use-2024-10-22`

**Pattern**: `type.*computer_20241022|type.*bash_20241022|type.*text_editor_20241022`
- Computer use tool types
- Example: `{"type": "computer_20241022", "name": "computer", ...}`

**Pattern**: `screenshot|mouse_move|key|type_text`
- Computer control actions
- Example: `{"action": "screenshot"}`, `{"action": "mouse_move", "coordinate": [x, y]}`

## Usage Classification

### Agent Complexity Levels
1. **Simple Tool Use**: Single tool call per turn
2. **Multi-Tool Agent**: Multiple tools in conversation
3. **Agentic Loop**: Autonomous multi-turn tool use
4. **Computer Use Agent**: Full computer control

### Tool Categories Detected
- **Search/Retrieval**: Information gathering tools
- **Code Execution**: Bash, Python execution
- **File Operations**: Read/write file tools
- **API Integration**: External service tools
- **Computer Control**: Mouse, keyboard, screenshot

## Detection Confidence

- **Tool Use Detection**: 95% (HIGH)
- **Agentic Loop Detection**: 90% (HIGH)
- **Computer Use Detection**: 98% (HIGH)
- **Tool Classification**: 80% (MEDIUM)

## Security Considerations

- Tool definitions should follow least privilege
- Computer use requires additional sandboxing
- Agentic loops need termination conditions
- Input validation critical for all tool inputs
- Monitor token usage for runaway agents
