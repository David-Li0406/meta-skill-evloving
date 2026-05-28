---
name: Client Guidance
description: This skill should be used when the user asks about "error messages", "did you mean", "similar tools", "parameter suggestions", "schema hints", "MCP error handling", "guide the client", "helpful errors", "fuzzy matching", or discusses how MCP servers should guide clients with progressive error enhancement and corrective feedback.
version: 0.1.0
---

# Client Guidance

## Purpose

Design MCP error responses that guide clients toward success through progressive enhancement: suggesting similar tools, recommending correct parameters, providing schema subsets, and offering corrective feedback rather than just rejecting requests.

## When to Use

- Designing error handling for MCP tools
- Implementing "did you mean" suggestions
- Adding fuzzy matching for tool/parameter names
- Including schema hints in error responses
- Building robust client guidance patterns

## Core Principle: Errors as Progressive Enhancement

Traditional errors reject and stop. **Progressive enhancement errors** reject but guide:

```
Traditional:
  → "Unknown tool: serach"
  → Client is stuck

Progressive Enhancement:
  → "Unknown tool: serach"
  → "Did you mean: search, search_code, search_files?"
  → "Available tool categories: search (3), get (5), list (4)"
  → Client can self-correct
```

## Pattern 1: Similar Tool Suggestions

When a client calls an invalid tool, suggest similar ones:

### Implementation

```typescript
// Pseudocode
function handleToolCall(toolName: string, params: any) {
  const tool = tools.get(toolName)

  if (!tool) {
    const similar = findSimilarTools(toolName, tools.keys())
    const categories = groupToolsByCategory(tools.keys())

    return {
      error: {
        code: "UNKNOWN_TOOL",
        message: `Tool '${toolName}' not found`,
        suggestions: {
          similar_tools: similar.slice(0, 5),
          did_you_mean: similar[0],
          available_categories: Object.keys(categories),
          hint: similar.length > 0
            ? `Try: ${similar[0]}`
            : "Use info() to list all available tools"
        }
      }
    }
  }

  return tool.execute(params)
}

function findSimilarTools(input: string, available: string[]): string[] {
  // Levenshtein distance + prefix matching + substring matching
  return available
    .map(name => ({
      name,
      score: calculateSimilarity(input, name)
    }))
    .filter(t => t.score > 0.3)
    .sort((a, b) => b.score - a.score)
    .map(t => t.name)
}
```

### Example Response

**Request:** `serach(pattern: "User")`

```json
{
  "error": {
    "code": "UNKNOWN_TOOL",
    "message": "Tool 'serach' not found",
    "suggestions": {
      "did_you_mean": "search",
      "similar_tools": ["search", "search_code", "search_files"],
      "available_categories": ["search", "get", "list", "info"],
      "hint": "Try: search(pattern: \"User\")"
    }
  }
}
```

### Similarity Algorithm

Combine multiple signals for best matches:

```typescript
function calculateSimilarity(input: string, candidate: string): number {
  const scores = [
    levenshteinSimilarity(input, candidate) * 0.4,   // Typo tolerance
    prefixMatch(input, candidate) * 0.3,              // Starts with
    substringMatch(input, candidate) * 0.2,           // Contains
    wordOverlap(input, candidate) * 0.1               // Semantic similarity
  ]
  return scores.reduce((a, b) => a + b, 0)
}
```

**Priority order for suggestions:**
1. Exact prefix match (`sea` → `search`)
2. Low edit distance (`serach` → `search`)
3. Contains substring (`auth` → `authenticate`)
4. Word overlap (`user_search` → `search_users`)

## Pattern 2: Parameter Correction

When parameters are invalid, suggest corrections:

### Unknown Parameter Handling

```typescript
function validateParams(params: any, schema: Schema) {
  const known = Object.keys(schema.properties)
  const provided = Object.keys(params)
  const unknown = provided.filter(p => !known.includes(p))

  const warnings = []
  const suggestions = {}

  for (const param of unknown) {
    const similar = findSimilarParams(param, known)
    if (similar.length > 0) {
      suggestions[param] = {
        did_you_mean: similar[0],
        alternatives: similar.slice(0, 3)
      }
      warnings.push(`Unknown param '${param}', did you mean '${similar[0]}'?`)
    } else {
      warnings.push(`Unknown param '${param}' ignored`)
    }
  }

  return { warnings, suggestions, valid: true }
}
```

### Example Response

**Request:** `search(patern: "User", filtr: "*.ts")`

```json
{
  "results": [...],
  "warnings": [
    "Unknown param 'patern', did you mean 'pattern'?",
    "Unknown param 'filtr', did you mean 'filter'?"
  ],
  "suggestions": {
    "patern": {
      "did_you_mean": "pattern",
      "alternatives": ["pattern"]
    },
    "filtr": {
      "did_you_mean": "filter",
      "alternatives": ["filter", "file_filter"]
    }
  },
  "hint": "Corrected call: search(pattern: \"User\", filter: \"*.ts\")"
}
```

### Auto-Correction Option

For high-confidence matches, optionally auto-correct:

```typescript
function handleParams(params: any, schema: Schema) {
  const corrected = {}
  const corrections = []

  for (const [key, value] of Object.entries(params)) {
    if (schema.properties[key]) {
      corrected[key] = value
    } else {
      const match = findBestMatch(key, Object.keys(schema.properties))
      if (match && match.confidence > 0.9) {
        // Auto-correct with notification
        corrected[match.name] = value
        corrections.push({
          from: key,
          to: match.name,
          confidence: match.confidence,
          auto_corrected: true
        })
      }
    }
  }

  return { corrected, corrections }
}
```

**Response with auto-correction:**

```json
{
  "results": [...],
  "corrections": [
    {
      "from": "patern",
      "to": "pattern",
      "confidence": 0.95,
      "auto_corrected": true
    }
  ],
  "note": "Parameter 'patern' was auto-corrected to 'pattern'"
}
```

## Pattern 3: Schema Hints in Errors

Include relevant schema information in error responses:

### Missing Required Parameter

```json
{
  "error": {
    "code": "MISSING_REQUIRED",
    "message": "Required parameter 'pattern' is missing",
    "schema_hint": {
      "required": ["pattern"],
      "optional": ["filter", "max", "offset"],
      "example": {
        "pattern": "authenticate",
        "filter": "*.ts",
        "max": 50
      }
    },
    "documentation_url": "https://docs.example.com/tools/search"
  }
}
```

### Invalid Type

```json
{
  "error": {
    "code": "INVALID_TYPE",
    "message": "Parameter 'max' must be integer, got string",
    "details": {
      "parameter": "max",
      "expected_type": "integer",
      "received_type": "string",
      "received_value": "fifty"
    },
    "schema_hint": {
      "max": {
        "type": "integer",
        "minimum": 1,
        "maximum": 1000,
        "default": 50,
        "description": "Maximum number of results to return"
      }
    },
    "hint": "Use a number: max: 50"
  }
}
```

### Out of Range

```json
{
  "error": {
    "code": "OUT_OF_RANGE",
    "message": "Parameter 'max' value 5000 exceeds maximum 1000",
    "details": {
      "parameter": "max",
      "value": 5000,
      "minimum": 1,
      "maximum": 1000
    },
    "hint": "Use max: 1000 for maximum results, or paginate with offset"
  }
}
```

## Pattern 4: Progressive Schema Disclosure

Provide schema at different detail levels based on context:

### Level 1: Minimal (in error messages)

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "schema_hint": {
      "required": ["pattern"],
      "optional": ["filter", "max"]
    }
  }
}
```

### Level 2: With Types (on request)

```json
{
  "schema": {
    "pattern": {"type": "string", "required": true},
    "filter": {"type": "string", "required": false},
    "max": {"type": "integer", "required": false, "default": 50}
  }
}
```

### Level 3: Full (via info tool or --schema flag)

```json
{
  "schema": {
    "pattern": {
      "type": "string",
      "required": true,
      "description": "Search pattern (regex supported)",
      "examples": ["authenticate", "User.*", "^function"]
    },
    "filter": {
      "type": "string",
      "required": false,
      "description": "File filter glob pattern",
      "examples": ["*.ts", "src/**/*.js"]
    },
    "max": {
      "type": "integer",
      "required": false,
      "default": 50,
      "minimum": 1,
      "maximum": 1000,
      "description": "Maximum results to return"
    }
  }
}
```

### Implementation

```typescript
function getSchemaHint(schema: Schema, level: 'minimal' | 'typed' | 'full') {
  switch (level) {
    case 'minimal':
      return {
        required: schema.required,
        optional: Object.keys(schema.properties).filter(k => !schema.required.includes(k))
      }
    case 'typed':
      return Object.fromEntries(
        Object.entries(schema.properties).map(([k, v]) => [k, {
          type: v.type,
          required: schema.required.includes(k),
          default: v.default
        }])
      )
    case 'full':
      return schema.properties
  }
}
```

## Pattern 5: Contextual Next Steps

Always provide actionable next steps:

### After Successful Query

```json
{
  "results": [...],
  "has_more": true,
  "total": 127,
  "next_steps": {
    "get_more": "search(pattern: \"User\", offset: 10)",
    "get_details": "get_definition(id: \"r1\")",
    "refine_search": "search(pattern: \"User\", filter: \"*.ts\")"
  }
}
```

### After Error

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "No results found for pattern 'xyzabc123'",
    "next_steps": {
      "broaden_search": "Try a simpler pattern or remove filters",
      "check_scope": "Use info() to see indexed paths",
      "alternatives": [
        "search(pattern: \"xyz\")",
        "search(pattern: \"abc\")",
        "list_files()"
      ]
    }
  }
}
```

### After Partial Success

```json
{
  "results": [...],
  "warnings": ["Some paths were not accessible"],
  "partial": true,
  "next_steps": {
    "retry_failed": "search(pattern: \"User\", include_errors: true)",
    "check_permissions": "info(detail: \"permissions\")",
    "proceed_anyway": "Results shown are valid, continue with get_definition(id)"
  }
}
```

## Pattern 6: Preemptive Guidance

Include helpful hints even in successful responses:

### Query Tool Response

```json
{
  "results": [
    {"id": "r1", "name": "User.authenticate", "confidence": 0.95},
    {"id": "r2", "name": "Auth.validate", "confidence": 0.72}
  ],
  "has_more": true,
  "total": 47,
  "tips": {
    "high_results": "Use filter: \"*.ts\" to narrow to TypeScript files",
    "get_details": "Use get_definition(id) for full code and documentation",
    "pagination": "Use offset: 10 to see more results"
  }
}
```

### When Approaching Limits

```json
{
  "results": [...],
  "returned": 100,
  "total": 100,
  "limit_reached": true,
  "guidance": {
    "at_limit": "Showing maximum 100 results",
    "recommendations": [
      "Add filter to narrow results: filter: \"src/**\"",
      "Use more specific pattern",
      "Results are sorted by relevance, best matches shown first"
    ]
  }
}
```

## Error Severity and Response Strategy

### Severity Levels

| Severity | Action | Include Schema | Suggest Similar |
|----------|--------|----------------|-----------------|
| Critical | Reject | Full schema | Yes |
| High | Reject | Typed schema | Yes |
| Medium | Warn + Continue | Minimal | Yes |
| Low | Warn only | No | Optional |

### Decision Matrix

```typescript
function determineErrorSeverity(error: ValidationError): Severity {
  // Critical: Security risks, data corruption potential
  if (error.type === 'injection_attempt') return 'critical'
  if (error.type === 'path_traversal') return 'critical'

  // High: Required field missing, type mismatch
  if (error.type === 'missing_required') return 'high'
  if (error.type === 'type_mismatch') return 'high'

  // Medium: Unknown params, out of range (correctable)
  if (error.type === 'unknown_param') return 'medium'
  if (error.type === 'out_of_range') return 'medium'

  // Low: Deprecation warnings, style issues
  if (error.type === 'deprecated_param') return 'low'

  return 'medium'
}
```

## Complete Error Response Template

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "severity": "high|medium|low",
    "details": {
      "field": "affected_field",
      "value": "provided_value",
      "expected": "what was expected"
    },
    "suggestions": {
      "did_you_mean": "closest_match",
      "alternatives": ["option1", "option2"],
      "auto_correctable": true
    },
    "schema_hint": {
      "required": ["field1"],
      "optional": ["field2"],
      "types": {"field1": "string", "field2": "integer"}
    },
    "next_steps": {
      "fix": "Corrected call example",
      "help": "info(tool: \"tool_name\")",
      "docs": "https://docs.example.com/tool"
    }
  }
}
```

## Implementation Checklist

**For every MCP tool:**

- [ ] Unknown tool calls suggest similar tools
- [ ] Unknown parameters suggest similar parameters
- [ ] Missing required fields show schema hint
- [ ] Type errors include expected vs received
- [ ] Out of range errors show valid range
- [ ] All errors include next_steps
- [ ] High-confidence typos offer auto-correction
- [ ] Schema hints match error severity
- [ ] Successful responses include tips when relevant
- [ ] Warnings are actionable, not just informational

## Testing Client Guidance

Use the mcp-fuzzer agent to validate:

```markdown
## Test: Unknown Tool Handling

**Input:** Call non-existent tool "serach"
**Expected:**
- Error code: UNKNOWN_TOOL
- did_you_mean present
- similar_tools array with "search"
- hint for correction

## Test: Unknown Parameter Handling

**Input:** search(patern: "User")
**Expected:**
- Warnings array present
- Suggestion for "pattern"
- Results still returned (graceful handling)

## Test: Schema Hints on Missing Required

**Input:** search() with no parameters
**Expected:**
- Error code: MISSING_REQUIRED
- schema_hint.required includes "pattern"
- Example usage provided
```

## Quick Reference

**Client guidance principles:**

1. **Never just reject** - Always suggest alternatives
2. **Fuzzy match everything** - Tools, params, values
3. **Progressive schema** - More detail for bigger errors
4. **Auto-correct when safe** - High confidence typos
5. **Next steps always** - What should client do now?
6. **Preemptive tips** - Help before they need it

**Error response must include:**
- `code` - Machine-readable error code
- `message` - Human-readable explanation
- `suggestions` - Did you mean / alternatives
- `next_steps` - How to proceed

**Similarity thresholds:**
- Auto-correct: >0.9 confidence
- Suggest first: >0.7 confidence
- Show in list: >0.4 confidence
- Omit: <0.4 confidence
