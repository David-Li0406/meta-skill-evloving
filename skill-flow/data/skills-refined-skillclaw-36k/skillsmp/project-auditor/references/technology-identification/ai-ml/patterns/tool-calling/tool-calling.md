# AI Tool Calling Patterns

**Category**: ai-ml/patterns
**Description**: Detection patterns for AI tool calling / function calling implementations

## Overview

Tool calling (also known as function calling) is a key AI capability that allows LLMs to interact with external systems. This pattern detects various implementations across AI providers.

## OpenAI Function Calling

### Python Patterns
File extensions: .py

**Pattern**: `functions=\[|function_call=`
- Legacy function calling syntax
- Example: `response = openai.ChatCompletion.create(..., functions=[...])`

**Pattern**: `tools=\[.*{"type":\s*"function"`
- New tools API syntax
- Example: `tools=[{"type": "function", "function": {"name": "search"}}]`

**Pattern**: `tool_choice=|function_call=`
- Tool selection configuration
- Example: `tool_choice="auto"` or `tool_choice={"type": "function", "function": {"name": "search"}}`

**Pattern**: `tool_calls|function_call.*arguments`
- Response parsing
- Example: `message.tool_calls[0].function.arguments`

### JavaScript/TypeScript Patterns
File extensions: .js, .ts

**Pattern**: `functions:\s*\[|functionCall:`
- Function calling configuration
- Example: `{ functions: [...], function_call: "auto" }`

**Pattern**: `tools:\s*\[.*type:\s*['"]function['"]`
- Tools API configuration
- Example: `tools: [{ type: "function", function: {...} }]`

## Anthropic Tool Use

### Python Patterns

**Pattern**: `tools=\[.*{"name":`
- Claude tool definitions
- Example: `tools=[{"name": "search", "description": "...", "input_schema": {...}}]`

**Pattern**: `tool_use|ToolUseBlock`
- Tool use response handling
- Example: `if block.type == "tool_use":`

**Pattern**: `tool_result|ToolResultBlock`
- Tool result submission
- Example: `{"type": "tool_result", "tool_use_id": "...", "content": "..."}`

## Google Gemini Function Calling

### Python Patterns

**Pattern**: `genai\.protos\.FunctionDeclaration`
- Gemini function declarations
- Example: `FunctionDeclaration(name="search", description="...", parameters={...})`

**Pattern**: `function_calling_config|tool_config`
- Function calling configuration
- Example: `tool_config={"function_calling_config": {"mode": "AUTO"}}`

## Generic Tool Patterns

### Schema Definition Patterns

**Pattern**: `"type":\s*"function"|type:\s*['"]function['"]`
- Function type in tool definition
- Indicates tool/function calling setup

**Pattern**: `input_schema|parameters.*properties`
- JSON Schema for tool inputs
- Example: `"input_schema": {"type": "object", "properties": {...}}`

**Pattern**: `"required":\s*\[|required:\s*\[`
- Required parameters specification
- Example: `"required": ["query"]`

### Tool Execution Patterns

**Pattern**: `tool_calls?\[|function_call\.name`
- Tool call extraction from response
- Example: `tool_call = response.choices[0].message.tool_calls[0]`

**Pattern**: `json\.loads\(.*arguments\)|JSON\.parse\(.*arguments\)`
- Argument parsing
- Example: `args = json.loads(tool_call.function.arguments)`

## Usage Classification

### Implementation Maturity

1. **Basic**: Single tool, manual parsing
2. **Intermediate**: Multiple tools, structured handling
3. **Advanced**: Dynamic tool registration, error handling
4. **Production**: Validation, logging, retry logic

### Security Indicators

**High Risk**:
- `eval\(|exec\(` with tool arguments
- No input validation on tool inputs
- Direct database queries from tool inputs

**Good Practices**:
- Schema validation before execution
- Rate limiting on tool calls
- Audit logging of tool invocations

## Detection Confidence

- **OpenAI Function Calling**: 95% (HIGH)
- **Anthropic Tool Use**: 95% (HIGH)
- **Gemini Function Calling**: 90% (HIGH)
- **Generic Tool Patterns**: 80% (MEDIUM)
