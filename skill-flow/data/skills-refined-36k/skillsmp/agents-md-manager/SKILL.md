---
name: agents-md-manager
description: Build and maintain effective AGENTS.md files that improve AI coding agent efficiency. Use when creating a new AGENTS.md file, auditing/improving an existing one, setting up progressive disclosure with agent documentation, or optimizing context window usage for AI-assisted coding projects.
---

# AGENTS.md Manager

Build and maintain high-quality AGENTS.md files that maximize AI coding agent efficiency.

## Core Principle

AI coding agents are stateless. AGENTS.md is the **only file** that goes into every conversation. It must onboard the agent to your codebase efficiently without bloating the context window.

**Critical insight**: AI agents may ignore AGENTS.md contents if deemed irrelevant. Overstuffed files with non-universal instructions get ignored entirely.

## Three Pillars of a Good AGENTS.md

Every AGENTS.md should answer three questions concisely:

1. **WHAT** - Tech stack, project structure, key directories
2. **WHY** - Project purpose, what each part does
3. **HOW** - Essential commands, verification steps, workflows

## Hard Constraints

| Constraint | Limit | Rationale |
|------------|-------|-----------|
| Total lines | < 300 (ideal: < 100) | Context window is shared with system prompt, conversation, tools |
| Instructions | < 100 | Frontier models reliably follow ~150-200 instructions; system prompt uses ~50 |
| Applicability | 100% universal | Non-universal instructions cause entire file to be ignored |

## What NOT to Include

- **Code style guidelines** - Use linters/formatters instead. LLMs learn from codebase patterns.
- **One-off task instructions** - Put in slash commands or separate docs
- **Code snippets** - Become stale; use `file:line` pointers instead
- **Auto-generated content** - Auto-init output is generic; craft manually
- **Conditional instructions** - Use progressive disclosure instead

## Progressive Disclosure Pattern

Keep AGENTS.md lean by pointing to detailed docs:

```
project/
├── AGENTS.md              # Core onboarding only (<100 lines)
└── agent_docs/            # Detailed docs loaded on demand
    ├── building.md
    ├── testing.md
    ├── database_schema.md
    ├── architecture.md
    └── deployment.md
```

In AGENTS.md, include a brief index:

```markdown
## Documentation

Read relevant docs from `agent_docs/` before starting work:
- `building.md` - Build commands and dependencies
- `testing.md` - Test execution and coverage
- `database_schema.md` - Table schemas and relationships
- `architecture.md` - Service structure and communication
- `deployment.md` - Deployment procedures and environments
```

**Prefer pointers to copies** - Reference `file:line` instead of embedding code.

## AGENTS.md Template Structure

See `references/template.md` for a complete template.

Minimal structure:

```markdown
# Project Name

Brief one-line description.

## Stack

- Language/Framework: X
- Database: Y
- Key dependencies: Z

## Project Structure

app/          - Main application code
lib/          - Shared utilities
tests/        - Test suite

## Commands

Build:  `command here`
Test:   `command here`
Lint:   `command here`

## Documentation

Read from `agent_docs/` as needed:
- `file.md` - Description
```

## Creating a New AGENTS.md

1. **Analyze the project** - Identify stack, structure, key workflows
2. **Start minimal** - Begin with <50 lines covering essentials
3. **Create agent_docs/** - Move detailed documentation there
4. **Add pointers** - Reference agent_docs from AGENTS.md
5. **Validate** - Run checklist from `references/checklist.md`

## Auditing an Existing AGENTS.md

1. **Count lines** - Flag if >300 lines
2. **Check universality** - Every instruction should apply to every task
3. **Find embedded code** - Replace with file:line pointers
4. **Identify style rules** - Move to linter config
5. **Extract conditionals** - Move to agent_docs/
6. **Validate** - Run checklist from `references/checklist.md`

## Integrations

### Pre-commit Hooks (for formatting/linting)

Instead of style instructions, configure pre-commit hooks:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: lint-fix
        name: Auto-fix lint issues
        entry: npm run lint:fix && npm run format
        language: system
        pass_filenames: false
```

### Custom Commands (for specific workflows)

Create project-specific commands directory for task-specific instructions that shouldn't bloat AGENTS.md.

## Reference Files

- `references/template.md` - Complete AGENTS.md template with examples
- `references/checklist.md` - Validation checklist for auditing
- `references/progressive-disclosure.md` - Guide for organizing agent_docs/
