---
name: code-styling
description: Apply consistent coding style patterns when writing or reviewing code. Use when generating new code that should follow your established preferences. Works with any language. Complements linters (which handle formatting) with higher-level style decisions.
---

# Code Styling Profile

Apply these coding style preferences when writing new code or suggesting improvements. This skill captures style decisions that linters don't enforce.

## How to Use This Skill

This skill is a template. To make it useful:

1. Create a separate project for style assessment
2. Have Claude analyze your existing code to identify patterns
3. Review and refine the extracted patterns
4. Replace the placeholders below with your actual preferences

## Core Principles (All Languages)

<!-- Replace these with your actual preferences after assessment -->

### Control Flow
- [ ] Prefer early returns over nested if/else
- [ ] Use guard clauses at function top
- [ ] Flat over nested (max nesting depth: ___)

### Functions
- [ ] Small focused functions over large multi-purpose ones
- [ ] Maximum function length: ___ lines
- [ ] Prefer pure functions where practical

### Naming
- [ ] Explicit over implicit
- [ ] Abbreviations: (never / common only / freely)
- [ ] Boolean prefix: (is/has/should / none / varies)

### Error Handling
- [ ] Fail fast with clear errors
- [ ] Return errors vs throw exceptions: ___
- [ ] Error message style: ___

### Comments
- [ ] Explain why, not what
- [ ] Comment density: (minimal / moderate / thorough)
- [ ] TODO format: ___

---

## Language-Specific Patterns

### Shell/Bash

```bash
# Function style preference:
# [ ] function name() { }
# [ ] name() { }

# Variable style:
# [ ] ${var} always
# [ ] $var when simple

# Error handling:
# [ ] set -euo pipefail
# [ ] explicit checks

# Example pattern (replace with your own):
```

### Lua (Neovim)

```lua
-- Module style:
-- [ ] local M = {} ... return M
-- [ ] return { ... }

-- Require style:
-- [ ] local mod = require("mod")
-- [ ] Top of file / lazy as needed

-- Example pattern (replace with your own):
```

### TypeScript/JavaScript

```typescript
// Import organization:
// 1. ___
// 2. ___
// 3. ___

// Async preference:
// [ ] async/await
// [ ] .then() chains
// [ ] mixed based on context

// Type definitions:
// [ ] interface (default)
// [ ] type (default)
// [ ] depends on ___

// Example pattern (replace with your own):
```

### Python

```python
# Import organization:
# 1. ___
# 2. ___
# 3. ___

# Type hints:
# [ ] Always
# [ ] Public APIs only
# [ ] Minimal

# String formatting:
# [ ] f-strings
# [ ] .format()
# [ ] % formatting

# Example pattern (replace with your own):
```

### Go

```go
// Error handling:
// [ ] if err != nil { return err }
// [ ] wrapped errors with context
// [ ] sentinel errors

// Struct initialization:
// [ ] Named fields always
// [ ] Positional for small structs

// Example pattern (replace with your own):
```

---

## Anti-Patterns (Code Smells You Dislike)

List patterns you want Claude to avoid:

1. ___
2. ___
3. ___

---

## Assessment Process

To populate this file with your actual preferences:

### Step 1: Gather Examples
Collect 5-10 files that represent your best code across languages you use.

### Step 2: Run Assessment
In a new Claude conversation:
```
I want to document my coding style preferences. Please analyze these files
and identify patterns in:
- Control flow (early returns, nesting, guard clauses)
- Function structure (size, naming, purity)
- Error handling
- Comments and documentation
- Language-specific idioms

[paste or attach files]
```

### Step 3: Refine
Review Claude's analysis. Correct anything that doesn't match your intent. Add patterns Claude missed.

### Step 4: Update This File
Replace the placeholders above with your documented preferences.

### Step 5: Test
Try using the skill on a new coding task. Refine based on results.

---

## Integration Notes

This skill complements:
- **pre-commit-reviewer** - Catches violations of these patterns
- **code-simplifier** - Uses these patterns when refactoring
- **Linters** - Handle formatting; this handles style

When conflicts occur, explicit project standards (CLAUDE.md, linter configs) take precedence over this skill.
