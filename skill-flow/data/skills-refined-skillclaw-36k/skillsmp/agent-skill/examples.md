# Example Skills

Reference examples demonstrating well-structured skills.

## Simple skill: Code explanation

```yaml
---
name: explaining-code
description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
---

# Explaining Code

When explaining code:

1. **Start with an analogy**: Compare the code to something from everyday life
2. **Draw a diagram**: Use ASCII art to show flow, structure, or relationships
3. **Walk through the code**: Explain step-by-step what happens
4. **Highlight a gotcha**: What's a common misconception?

Keep explanations conversational. For complex concepts, use multiple analogies.
```

Why this works:
- Description includes trigger phrase "how does this work?"
- Clear, numbered instructions
- Specific outputs expected (analogy, diagram, walkthrough)

## Read-only skill: Safe file reader

```yaml
---
name: safe-reader
description: Read and search files without making changes. Use when reviewing code, auditing files, or when you need read-only access to prevent accidental modifications.
allowed-tools: Read, Grep, Glob
---

# Safe File Reader

This skill provides read-only file access.

## Instructions

1. Use Read to view file contents
2. Use Grep to search within files
3. Use Glob to find files by pattern

Never suggest edits. Only report what you find.
```

Why this works:
- `allowed-tools` restricts to read-only operations
- Clear constraint: "never suggest edits"
- Specific use case: auditing, reviewing

## Multi-file skill: API documentation

```yaml
---
name: api-docs
description: Generate API documentation from code. Use when documenting REST endpoints, writing API references, or when the user mentions OpenAPI, Swagger, or API docs.
---

# API Documentation Generator

Generate comprehensive API documentation from source code.

## Quick start

1. Identify API endpoints in the codebase
2. Extract route, method, parameters, and response types
3. Generate documentation in requested format (Markdown, OpenAPI)

For OpenAPI schema details, see [openapi-reference.md](openapi-reference.md).
For markdown templates, see [templates.md](templates.md).

## Output formats

### Markdown (default)

Generate a table with: Method, Path, Description, Parameters, Response

### OpenAPI 3.0

See [openapi-reference.md](openapi-reference.md) for schema structure.
```

Why this works:
- SKILL.md is concise overview
- Complex details in supporting files
- Clear entry point with "Quick start"

## Skill with custom model

```yaml
---
name: complex-analysis
description: Deep analysis requiring extended reasoning. Use for complex architectural decisions, security audits, or thorough code reviews where accuracy matters more than speed.
model: claude-opus-4-5-20251101
---

# Complex Analysis

For tasks requiring deep reasoning and thoroughness.

## When to use

- Architectural decisions with many tradeoffs
- Security vulnerability analysis
- Complex refactoring planning

## Instructions

1. Take time to understand the full context
2. Consider multiple approaches before recommending
3. Explain tradeoffs explicitly
4. Provide confidence levels for recommendations
```

Why this works:
- Uses more capable model for complex tasks
- Clear criteria for when to use
- Sets expectations about thoroughness

## Good vs bad descriptions

### Bad descriptions

- "Helps with code" - too vague, matches everything
- "Documentation skill" - no trigger keywords
- "For Python" - describes language, not capability

### Good descriptions

- "Generate Python type hints for untyped functions. Use when adding types, improving type coverage, or when mypy reports missing annotations."
- "Write unit tests using pytest. Use when creating tests, adding test coverage, or when the user mentions pytest, testing, or TDD."
- "Format SQL queries for readability. Use when cleaning up SQL, formatting database queries, or when the user pastes messy SQL."

Key patterns:
1. Start with what it does (verb + object)
2. Include "Use when..." with specific scenarios
3. Add keywords users would naturally say
