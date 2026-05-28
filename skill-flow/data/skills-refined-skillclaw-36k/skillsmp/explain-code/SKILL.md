---
name: explain-code
description: 'Explain code operation, logic, and design clearly and systematically. Use when the user asks to explain code, understand how something works, what a function does, or requests logic analysis.'
compatibility: Requires code reading tools
allowed-tools:
    - Glob
    - Grep
    - Read
    - mcp__context7
    - mcp__fetch
    - mcp__jetbrains
    - mcp__markitdown
    - mcp__serena
---

# Code Explanation Skill

Explain code operation clearly and systematically.

## Explanation Process

1. Scope: locate file/function/class/block, map dependencies and calls;
   use `mcp__serena__find_symbol`, `mcp__serena__find_referencing_symbols`, `mcp__jetbrains__get_symbol_info` as needed.
2. Structure:
    - Overview(2-3 sentences): what/why/role.
    - Flow: main logic, core algorithm, key branches.
    - I/O: params, returns, side effects.
    - Edge/limits: exceptions, boundaries, known limits.
    - Usage: basic call, common patterns, integration points.

## Explanation Level Adjustment

### For Beginners

- Basic concepts, terminology definitions, detailed steps, analogies/examples

### For Intermediate Developers (Default)

- Core logic 중심, 패턴/컨벤션 언급, 적정 추상화

### For Advanced Developers

- Design rationale, performance, alternatives, trade-offs

## Output Format

```markdown
## Overview

[Purpose and role of the code]

## How It Works

### Main Flow

1. [First step]
2. [Second step]
   ...

### Core Logic

(key code excerpt with comments)

[Logic explanation]

## Input/Output

| Parameter | Type | Description |
|-----------|------|-------------|
| param1    | Type | Description |

**Return**: `Type` - Description

## Caveats

- [Edge cases or limitations]

## Usage Example

(example code)
```

## Language-Specific Explanations

### JavaScript/TypeScript

- Closures and scope
- Async patterns (Promise, async/await)
- Prototype chain

### Python

- Decorators and context managers
- Generator patterns
- Magic methods

### Java/Kotlin

- Object-oriented design patterns
- Generics and type variance
- Stream API

### Go

- Goroutines and channels
- Interface implementation
- Error handling patterns

## Edge Cases

- **Complex code**: Break into smaller chunks
- **Library code**: Reference official documentation
- **Legacy code**: Provide historical context if available
- **Multi-language**: Explain language-specific idioms

## Tips

- MCP tools are optional; omit if unavailable or add others as needed
