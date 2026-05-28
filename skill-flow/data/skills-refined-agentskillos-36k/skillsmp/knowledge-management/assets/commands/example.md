---
description: Save reusable code examples to the examples library
---

# Example - Code Examples Library

Save and organize reusable code snippets with metadata.

## Usage

```
/example [language] [name]
```

**Output:** `$PROJECT_ROOT/docs/examples/[language]/[name].[ext]`

## Instructions

1. **Parse arguments**: language (go, typescript, python, bash, etc.) and name (kebab-case)
2. **Determine file extension** from language:
   - go → .go
   - typescript/ts → .ts
   - javascript/js → .js
   - python/py → .py
   - bash/sh → .sh
   - rust → .rs
   - java → .java
3. **Gather context**: Look at recent code in conversation, ask user what code to save if unclear
4. **Create directory**: `docs/examples/[language]/`
5. **Generate file** with metadata header and code
6. **Confirm** with user

## File Format

### Go Example
```go
// Title: [Descriptive Title]
// Tags: [tag1, tag2, tag3]
// Related: [link to knowledge-base or learnings if any]
// Created: YYYY-MM-DD

package examples

// [Description of what this code does]
// Usage:
//   [usage example]
[code]
```

### TypeScript/JavaScript Example
```typescript
// Title: [Descriptive Title]
// Tags: [tag1, tag2, tag3]
// Related: [link to knowledge-base if any]
// Created: YYYY-MM-DD

// [Description]
// Usage:
//   [usage example]
[code]
```

### Python Example
```python
# Title: [Descriptive Title]
# Tags: [tag1, tag2, tag3]
# Related: [link to knowledge-base if any]
# Created: YYYY-MM-DD

# [Description]
# Usage:
#   [usage example]
[code]
```

### Bash Example
```bash
#!/bin/bash
# Title: [Descriptive Title]
# Tags: [tag1, tag2, tag3]
# Related: [link to knowledge-base if any]
# Created: YYYY-MM-DD

# [Description]
# Usage:
#   [usage example]
[code]
```

## Guidelines

- Code should be **runnable** or at minimum compilable
- Include usage examples in comments
- Add relevant tags for searchability
- Link to related knowledge-base entries if they exist
- Keep examples focused on one concept/pattern
- Use descriptive names (e.g., `retry-with-backoff`, `api-client-wrapper`)

## Listing Examples

To browse existing examples:
```bash
find docs/examples -type f | sort
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/mem` | Quick knowledge capture |
| `/distill` | Extract patterns to knowledge base |
| `/example` | Save code examples (you are here) |
