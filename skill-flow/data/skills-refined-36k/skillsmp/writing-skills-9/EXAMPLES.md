# Skill Examples

Real-world examples demonstrating effective skill patterns.

## Example 1: API Debugging Skill

A well-structured skill for debugging API endpoints.

```markdown
---
name: debugging-api-endpoints
description: Systematic troubleshooting for API endpoints returning unexpected errors (404, 500, validation failures). Use when endpoints fail despite correct-looking code. Guides through clean restarts, log analysis, and layer-by-layer debugging.
allowed-tools: ["Read", "Bash", "Glob", "Grep"]
---

# Debugging API Endpoints

Systematic approach to troubleshooting API failures.

## Quick Reference

| Status | Common Causes |
|--------|---------------|
| 404 | Route not registered, wrong path |
| 500 | Unhandled exception, DB error |
| 400 | Validation failure, bad payload |

## Diagnostic Workflow

### Step 1: Clean Environment
- [ ] Stop running servers
- [ ] Clear caches
- [ ] Restart with fresh state

### Step 2: Verify Route Registration
- [ ] Check route file exists
- [ ] Verify route is imported
- [ ] Confirm middleware order

### Step 3: Trace Request Flow
- [ ] Add logging at entry point
- [ ] Check middleware execution
- [ ] Verify handler is called

### Step 4: Database Layer
- [ ] Confirm connection
- [ ] Check query syntax
- [ ] Verify data exists

## Common Fixes

| Symptom | Solution |
|---------|----------|
| Route not found | Check import order in router |
| Silent failures | Add try/catch with logging |
| Wrong response | Verify response format |
```

**Why this works:**
- Clear description with specific triggers
- Quick reference for fast diagnosis
- Step-by-step workflow with checkboxes
- Common fixes table for rapid resolution

## Example 2: Documentation Skill

A skill for maintaining documentation standards.

```markdown
---
name: writing-api-docs
description: Guide for writing API documentation. Use when documenting endpoints, creating OpenAPI specs, or writing SDK guides. Covers request/response formats, authentication, and error handling.
allowed-tools: ["Read", "Write", "Edit", "Glob"]
---

# Writing API Documentation

Standards for clear, consistent API documentation.

## Quick Reference

| Section | Required |
|---------|----------|
| Endpoint | Yes |
| Auth | Yes |
| Request | Yes |
| Response | Yes |
| Errors | Yes |

## Endpoint Documentation Template

### Format

```markdown
## `METHOD /path/:param`

Brief description.

### Authentication

Required auth type or "None".

### Request

**Path Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| param | string | Yes | Description |

**Body:**
\`\`\`json
{
  "field": "value"
}
\`\`\`

### Response

**Success (200):**
\`\`\`json
{
  "data": {}
}
\`\`\`

**Errors:**
| Status | Description |
|--------|-------------|
| 400 | Invalid input |
| 401 | Unauthorized |
| 404 | Not found |
```

## Workflow

1. **Identify Endpoint**
   - [ ] HTTP method
   - [ ] Path with parameters
   - [ ] Purpose

2. **Document Request**
   - [ ] Path parameters
   - [ ] Query parameters
   - [ ] Request body

3. **Document Response**
   - [ ] Success format
   - [ ] Error formats

4. **Add Examples**
   - [ ] cURL example
   - [ ] SDK example
```

**Why this works:**
- Focused scope (API docs only)
- Ready-to-use template
- Checklist-driven workflow

## Example 3: Testing Skill

A skill for writing comprehensive tests.

```markdown
---
name: writing-unit-tests
description: Guide for writing unit tests with Bun test runner. Use when adding tests for new code, improving coverage, or fixing flaky tests. Covers mocking, assertions, and test organization.
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
---

# Writing Unit Tests

Patterns for effective unit tests using Bun.

## Quick Reference

| Pattern | Use When |
|---------|----------|
| describe/it | Grouping related tests |
| beforeEach | Setup shared state |
| mock | Isolating dependencies |

## Test Structure

### Basic Test File

```typescript
import { describe, it, expect, beforeEach } from 'bun:test';
import { functionUnderTest } from './module';

describe('functionUnderTest', () => {
  beforeEach(() => {
    // Reset state
  });

  it('should handle normal input', () => {
    const result = functionUnderTest('input');
    expect(result).toBe('expected');
  });

  it('should handle edge cases', () => {
    expect(() => functionUnderTest(null)).toThrow();
  });
});
```

## Workflow: Adding Tests

### Prerequisites
- [ ] Understand code being tested
- [ ] Identify edge cases

### Steps

1. **Create Test File**
   - [ ] Name: `module.test.ts`
   - [ ] Location: Same directory or `__tests__/`

2. **Write Happy Path**
   - [ ] Test normal inputs
   - [ ] Verify expected outputs

3. **Add Edge Cases**
   - [ ] Empty inputs
   - [ ] Invalid inputs
   - [ ] Boundary values

4. **Run and Verify**
   ```bash
   bun test module.test.ts
   ```
   - [ ] All tests pass
   - [ ] Coverage adequate

## Mocking Patterns

### Mock Function

```typescript
import { mock } from 'bun:test';

const mockFn = mock(() => 'mocked');
expect(mockFn).toHaveBeenCalled();
```

### Mock Module

```typescript
import { mock } from 'bun:test';

mock.module('./dependency', () => ({
  dep: mock(() => 'mocked')
}));
```
```

**Why this works:**
- Concrete code examples
- Progressive complexity (basic → mocking)
- Runnable workflow

## Example 4: Minimal Skill

Sometimes less is more.

```markdown
---
name: formatting-code
description: Format code using Biome. Use when code needs formatting or linting fixes.
allowed-tools: ["Bash"]
---

# Formatting Code

Run Biome formatter and linter.

## Commands

```bash
# Format
bun run format

# Lint
bun run lint

# Fix lint issues
bun run lint:fix
```

## Workflow

1. **Format**
   ```bash
   bun run format
   ```
   - [ ] No errors

2. **Lint**
   ```bash
   bun run lint
   ```
   - [ ] No warnings
```

**Why this works:**
- Simple task = simple skill
- Direct commands
- No unnecessary complexity

## Anti-Patterns

### Too Vague

```markdown
---
name: coding
description: Help with coding.
---

# Coding

This skill helps with coding tasks.
```

**Problems:**
- Name not descriptive
- Description too vague
- No specific guidance

### Too Long

A 1000+ line SKILL.md with everything in one file.

**Fix:** Split into reference files:
- SKILL.md (core, under 500 lines)
- PATTERNS.md (code patterns)
- TROUBLESHOOTING.md (issues)

### Wrong Tool Restrictions

```markdown
allowed-tools: ["Read"]
---
# Fixing Bugs

Guide for fixing bugs.
```

**Problem:** Can't fix bugs without Edit/Write tools.

**Fix:** Match tools to skill purpose.
