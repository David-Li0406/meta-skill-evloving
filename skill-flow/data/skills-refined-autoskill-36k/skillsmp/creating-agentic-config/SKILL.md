---
name: creating-agentic-config
description: Create or update AGENTS.md configuration files for AI coding assistants following research-backed best practices. Use when initializing projects, improving agent context, creating AGENTS.md files, or when user mentions project initialization, agent configuration, context files, or /init command.
---

# Create Agentic Configuration Files

Create AGENTS.md configuration files that provide AI coding assistants with project context. Follow research-backed best practices: keep under 100 lines, include only universal instructions, and use progressive disclosure to reference external documentation for task-specific guidance.

## Critical Research-Backed Principles

### The Core Constraint: Token Budget

**LLMs can reliably follow only ~150-200 instructions, and the system prompt already consumes ~50.**

This means your AGENTS.md has a budget of approximately **60-100 lines maximum** for optimal effectiveness. Beyond this, instruction-following degrades uniformly across ALL instructions.

### The Golden Rules

1. **Universal Instructions Only**: Include ONLY instructions that apply to EVERY task
2. **Progressive Disclosure**: Reference external docs instead of bloating the file
3. **Actionable Commands**: Exact syntax for build/test/lint commands
4. **Avoid Anti-Patterns**: No style rules (use linters), no code snippets (they go stale), no task-specific instructions

### The WHAT-WHY-HOW Framework

Every effective AGENTS.md follows this structure:

1. **WHAT**: Your stack, versions, key tools
2. **WHY**: Architecture decisions, critical conventions
3. **HOW**: Commands to verify changes work

## AGENTS.md Structure

### Required Sections

```markdown
# Project Name - Brief Description

## Quick Commands

- **Dev**: Exact command
- **Test**: Exact command with coverage flags
- **Lint**: Exact command
- **Build**: Exact command

## Tech Stack

- **Backend**: Language version, framework, database
- **Frontend**: Framework, TypeScript, styling
- **Testing**: Test framework, coverage tools
- **Quality**: Linters, formatters, static analysis

## Key Directories

- `src/components/` - React components (one per file)
- `tests/` - Test files mirror src/ structure

## Architecture Decisions

3-5 CRITICAL decisions that affect daily work:

- State management approach
- Code organization pattern
- Key conventions that can't be automated

## Before Committing

Clear checklist of what must pass:

- Run X to verify no type errors
- Hooks handle Y automatically
- Coverage must be ≥ Z%

## For More Context (Progressive Disclosure)

- @docs/frontend-patterns.md for component conventions
- @docs/api-design.md for endpoint patterns
```

### Optional Sections (Use Sparingly)

Only include these if universally relevant:

- **Environment Notes**: If non-standard (e.g., Laravel Herd auto-HTTPS)
- **Available Skills**: If custom skills are configured
- **Custom Commands**: If custom slash commands are defined
- **Specialized Agents**: If custom agents are configured

## Anti-Patterns to Avoid

### Don't Do This

**Style rules:**

```markdown
- Use single quotes for strings
- Max line length 100 characters
```

_Issue: Use linter config, not AGENTS.md._

**Code snippets:**

```markdown
## Action Example

\`\`\`php
// 30 lines of code
\`\`\`
```

_Issue: Code goes stale. Use skills or reference file:line._

**Task-specific instructions:**

```markdown
## Creating User Registration

1. Create the Action...
2. Create the DTO...
```

_Issue: Use a skill or custom command instead._

**Vague instructions:**

```markdown
Write good tests for all features.
```

_Issue: Not actionable. What commands? What coverage?_

**Bloating (200+ lines):**
_Issue: Beyond ~100 lines, ALL instruction-following degrades._

### Do This Instead

**Reference linter configs:**

```markdown
## Code Quality

Formatters run on save (Pint for PHP, Prettier for JS).
Run `composer run checks` to verify quality.
```

**Reference skills:**

```markdown
Use skill `creating-actions` for Action class patterns.
```

**Specific, actionable instructions:**

```markdown
## Testing

Run `composer test -- --coverage` before committing.
Minimum 90% code coverage required.
```

**Ruthless prioritization:**

```markdown
# Project Name

[Only 60-80 lines of UNIVERSAL, ACTIONABLE instructions]

## For More Context

- @docs/detailed-patterns.md for comprehensive patterns
```

## Common Questions

### Q: Should I include all available commands?

**A:** No. Only include commands used for **daily development**:

**Include:**

- ✅ Dev server, test runner, linter/formatter, build

**Exclude:**

- ❌ Database migrations, deployment, cache clearing, one-off scripts

### Q: How do I handle monorepos?

**A:** Use hierarchical configuration:

1. **Root AGENTS.md:** Cross-cutting concerns, workspace commands
2. **Package-level AGENTS.md:** Package-specific conventions

### Q: What if the project has no tests?

**A:** Document current state honestly:

```markdown
## Before Committing

- Run build to verify no errors: `npm run build`
- ESLint must pass: `npm run lint`

Note: Test suite is not yet implemented.
```

### Q: How do I handle pre-commit hooks?

**A:** Document what runs automatically:

```markdown
## Before Committing

Pre-commit hooks run automatically:

- Pint formats PHP code
- Prettier formats JS/TS/JSON

Additional manual checks:

- Run `composer test` to verify tests pass
```

## Quality Checklist

Before finalizing AGENTS.md:

- [ ] File is 60-100 lines (optimal)
- [ ] Project name and brief description at top
- [ ] Quick Commands section with exact syntax
- [ ] Tech Stack section with versions
- [ ] Key Directories mapped with PURPOSE
- [ ] Architecture Decisions (3-5 critical ones)
- [ ] Before Committing checklist is actionable
- [ ] All commands tested and work
- [ ] No style rules (use linters)
- [ ] No code snippets (they go stale)
- [ ] No task-specific instructions (use skills/commands)
- [ ] Every instruction is universal (applies to every task)
- [ ] Progressive disclosure used if needed

## Summary

Creating effective AGENTS.md files requires:

1. **Thorough research** - Analyze project structure, configs, and patterns
2. **Ruthless prioritization** - Only universal, actionable instructions
3. **Optimal length** - 60-100 lines for best LLM instruction-following
4. **WHAT-WHY-HOW framework** - Stack, decisions, verification
5. **Progressive disclosure** - External docs for detailed guides
6. **Freshness** - No content that goes stale
7. **Actionability** - Exact commands, no vague instructions

**Remember: Your AGENTS.md is the highest-leverage customization point for AI coding assistants. Treat it like a carefully-crafted prompt.**

## References

- `references/examples.md` - Full AGENTS.md examples for different project types
- `references/research-process.md` - Step-by-step process for analyzing projects
