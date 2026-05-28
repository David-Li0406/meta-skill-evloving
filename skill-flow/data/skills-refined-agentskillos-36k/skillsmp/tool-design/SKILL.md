---
name: Tool Design
description: This skill should be used when the user asks to "design MCP tool", "create tool schema", "tool best practices", "input validation", "output schema", "error handling for tools", or discusses designing individual MCP tools with proper schemas and responses.
version: 0.1.0
---

# Tool Design

## Purpose

Design individual MCP tools with clear input/output schemas, proper error handling, and token-efficient responses following best practices.

## When to Use

- Designing new MCP tools
- Refining existing tool schemas
- Implementing error handling
- Optimizing tool responses
- Validating tool design

## Input Schema Design

### Clear, Minimal Parameters

```json
{
  "name": "search",
  "input": {
    "pattern": {
      "type": "string",
      "required": true,
      "description": "Search pattern (regex supported)"
    },
    "filter": {
      "type": "string",
      "required": false,
      "description": "File filter (*.ts, src/**)"
    },
    "max": {
      "type": "integer",
      "required": false,
      "default": 50,
      "description": "Maximum results"
    }
  }
}
```

**Key principles:**
- Required vs optional clearly marked
- Defaults documented
- Types explicit
- Descriptions concise

### Accept Extra Parameters

```typescript
// Pseudocode - Always permissive
function search(params) {
  const {pattern, filter, max, ...extra} = params

  const warnings = []
  if (Object.keys(extra).length > 0) {
    warnings.push(`Unknown params ignored: ${Object.keys(extra).join(', ')}`)
  }

  return {results: search(pattern, filter, max), warnings}
}
```

## Output Schema Design

### Standard Structure

```json
{
  "data": {},           // Primary response data
  "metadata": {},       // Automation flags (has_more, total, etc.)
  "errors": [],         // Error list (empty if none)
  "warnings": [],       // Warning list (unknown params, etc.)
  "next_steps": ""      // Guidance for user
}
```

### Token-Efficient Responses

**Don't repeat inputs:**
```json
// Bad
{
  "query": "authenticate",  // User just sent this
  "filter": "*.ts",         // User just sent this
  "results": [...]
}

// Good
{
  "results": [...],
  "total": 127
}
```

### Progressive Detail

```json
{
  "results": [
    {"id": "a1", "name": "...", "confidence": 0.95, "full_details": {...}},  // High confidence
    {"id": "b2", "name": "...", "confidence": 0.70, "summary": "..."},       // Medium
    {"id": "c3", "name": "...", "confidence": 0.40}                           // Low - just ID
  ]
}
```

## Error Handling

> **See also:** [Client Guidance](../client-guidance/SKILL.md) for comprehensive error-as-progressive-enhancement patterns including similar tool suggestions, parameter corrections, and schema hints.

### Error Response Structure

```json
{
  "error": {
    "code": "INVALID_PATTERN",
    "message": "Regex pattern is malformed",
    "details": {
      "pattern": "([unclosed",
      "position": 2,
      "expected": "]"
    },
    "suggestion": "Check regex syntax. Example: \"function.*User\"",
    "schema_hint": {
      "pattern": {"type": "string", "required": true}
    }
  }
}
```

### Standard Error Codes

```
INVALID_INPUT       - Bad input parameters
NOT_FOUND           - Resource not found
PERMISSION_DENIED   - Access denied
TIMEOUT             - Operation timed out
INTERNAL_ERROR      - Server error
RATE_LIMITED        - Too many requests
UNKNOWN_TOOL        - Tool name not found (suggest similar)
MISSING_REQUIRED    - Required parameter missing (include schema)
```

### Graceful Degradation

```json
{
  "results": [...],  // Partial results
  "warnings": ["Timeout after 5s, showing partial results"],
  "complete": false,
  "partial": true
}
```

### Client Guidance in Errors

Errors should guide clients toward success:

```json
{
  "error": {
    "code": "UNKNOWN_TOOL",
    "message": "Tool 'serach' not found",
    "suggestions": {
      "did_you_mean": "search",
      "similar_tools": ["search", "search_code"]
    }
  }
}
```

```json
{
  "error": {
    "code": "MISSING_REQUIRED",
    "message": "Required parameter 'pattern' is missing",
    "schema_hint": {
      "required": ["pattern"],
      "optional": ["filter", "max"],
      "example": {"pattern": "User", "filter": "*.ts"}
    }
  }
}
```

## Tool Types and Patterns

### Query Tools (Fast, <100 tokens)

```json
{
  "name": "search",
  "purpose": "Fast discovery",
  "output": {
    "results": [{"id": "...", "preview": "..."}],
    "has_more": true,
    "total": 127
  },
  "avg_tokens": 80
}
```

### Lookup Tools (Medium, ~200 tokens)

```json
{
  "name": "get_definition",
  "purpose": "Detailed information",
  "input": {"id": "from_search"},
  "output": {
    "id": "...",
    "full_details": {...}
  },
  "avg_tokens": 200
}
```

### Analysis Tools (Slow, ~500 tokens)

```json
{
  "name": "trace_callers",
  "purpose": "Deep analysis",
  "input": {"symbol_id": "..."},
  "output": {
    "call_graph": {...},
    "analysis": {...}
  },
  "avg_tokens": 500,
  "warning": "Expensive operation"
}
```

## Validation Patterns

### Input Validation

```typescript
// Pseudocode
function validateInput(params) {
  if (!params.pattern) {
    return error("INVALID_INPUT", "pattern is required")
  }

  if (params.max && (params.max < 1 || params.max > 1000)) {
    return error("INVALID_INPUT", "max must be 1-1000")
  }

  // Validate but don't reject extra params
  const known = ['pattern', 'filter', 'max']
  const extra = Object.keys(params).filter(k => !known.includes(k))

  return {valid: true, warnings: extra.length > 0 ? [`Unknown: ${extra}`] : []}
}
```

## Quick Reference

**Tool design checklist:**

- [ ] Clear input schema with required/optional marked
- [ ] Output schema documented
- [ ] Error codes and messages defined
- [ ] Accept extra parameters with warnings
- [ ] Progressive detail by relevance
- [ ] Token budget appropriate for tool type
- [ ] Automation flags included
- [ ] Next steps provided to user

**Client guidance checklist:**

- [ ] Unknown tool errors suggest similar tools
- [ ] Unknown params suggest correct names
- [ ] Missing required errors include schema hints
- [ ] Type errors show expected vs received
- [ ] Errors include actionable next_steps
- [ ] High-confidence typos can be auto-corrected

**Token budgets by tool type:**

- Query: 50-100 tokens
- Lookup: 150-250 tokens
- Analysis: 400-600 tokens
- Management: 50-150 tokens
