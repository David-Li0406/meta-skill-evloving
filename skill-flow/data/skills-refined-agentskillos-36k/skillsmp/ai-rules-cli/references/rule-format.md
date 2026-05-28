# AI Rules File Format Reference

Complete reference for ai-rules source file format and frontmatter options.

## Standard Mode Format

Rule files use markdown with optional YAML frontmatter:

```markdown
---
description: Context description for when to apply this rule
alwaysApply: true
fileMatching: "**/*.ts"
---

# Rule Title

Your markdown content here...
```

## Frontmatter Fields

All frontmatter fields are optional.

### `description`

Context description that helps agents understand when to apply this rule.

**Usage:**
- Required when `alwaysApply: false` (for contextual rules)
- Optional when `alwaysApply: true` (for always-applied rules)
- Helps agents determine when to load the rule

**Example:**
```yaml
description: React Router v7 route type imports and type generation workflow
```

### `alwaysApply`

Controls when this rule is applied.

**Values:**
- `true` - Rule is always included in agent rule files (default)
- `false` - Rule is included as optional/contextual (loaded when relevant)

**Default:** `true` (if not specified)

**Example:**
```yaml
alwaysApply: false  # Only load when working with test files
```

**When to use `false`:**
- Rules specific to certain file types
- Optional best practices
- Context-dependent guidelines
- Large reference documentation

### `fileMatching`

Glob patterns for which files this rule applies to.

**Format:** Glob pattern string (e.g., `"**/*.ts"`, `"src/**/*.py"`)

**Currently supported in:** Cursor

**Example:**
```yaml
fileMatching: "apps/ralph-monitoring/app/routes/**/*.tsx"
```

**Common patterns:**
- `"**/*.ts"` - All TypeScript files
- `"**/*.test.ts"` - Test files
- `"app/routes/**/*.tsx"` - Route files
- `"**/*.md"` - Markdown files

## Symlink Mode Format

For simple setups, use a single `AGENTS.md` file without frontmatter:

```markdown
# Project Rules

- Use TypeScript for all new code
- Write comprehensive tests
- Follow conventional commits
- Prefer explicit types over `any`
```

**Requirements:**
- Must be named `AGENTS.md`
- Must be the only file in `ai-rules/` directory
- Must not start with `---` (no YAML frontmatter)
- Content is used directly by all supported agents via symlinks

## Rule Content Structure

### Recommended Structure

```markdown
---
description: Brief description
alwaysApply: true
---

# Rule Title

## Context & Problem
- What problem does this rule solve?
- Where does it apply?

## ✅ DO
- Correct patterns with examples
- Real code from the repo when possible

## ❌ DON'T
- Anti-patterns with explanations
- Deprecated approaches

## 🔍 Verification
- Commands to run
- Files to check
- Lints to validate
```

### Best Practices

**High-level context first:**
- Problem statement
- Scope definition
- Workflow alignment

**Essential elements:**
- Required imports
- SDK/gateway usage
- Error handling patterns
- Naming conventions
- Security constraints

**Example quality:**
- Real code from the repo
- DO/DON'T pairs
- Contextual explanations
- Edge case handling

## Examples

### Always-Applied Rule

```markdown
---
description: React Router v7 route type imports and type generation workflow
alwaysApply: true
---

# React Router v7 Type Safety

## ✅ DO
```typescript
import type { Route } from './+types/product';
```

## ❌ DON'T
```typescript
import type { Route } from '../+types/product'; // wrong path
```
```

### Contextual Rule

```markdown
---
description: React Testing Library best practices for component tests
alwaysApply: false
fileMatching: "**/*.test.tsx"
---

# Testing Best Practices

- Prefer user-centric queries (getByRole, getByLabelText)
- Avoid implementation details (testId, class names)
- Test behavior, not implementation
```

### Project Context Rule

```markdown
---
description: DevAgent project context and structure for AI agents
alwaysApply: true
---

# DevAgent Project — AI Agent Context

This file provides high-level context about the DevAgent project.

## Project Structure

- `.devagent/workspace/` - Workspace files
- `apps/ralph-monitoring/` - Main application
```

## File Naming Conventions

### Recommended Patterns

- Use descriptive names: `react-router-7.md`, `testing-best-practices.md`
- Prefix foundational rules: `00-project-context.md`
- Use kebab-case: `error-handling.md`
- Group related rules: `testing-unit.md`, `testing-integration.md`

### Examples

```
ai-rules/
├── 00-project-context.md
├── react-router-7.md
├── testing-best-practices.md
├── error-handling.md
└── cursor-rules.md
```

## Cross-Referencing

Reference other rules using markdown links:

```markdown
## Related Rules

- [react-router-7.mdc](mdc:.cursor/rules/react-router-7.mdc)
- [testing-best-practices.mdc](mdc:.cursor/rules/testing-best-practices.mdc)
```

## See Also

- [AI Rules CLI Commands](cli-commands.md)
- [AI Rules GitHub Repository](https://github.com/block/ai-rules)
- [Cursor Rules Best Practices](../cursor-rules.mdc)
