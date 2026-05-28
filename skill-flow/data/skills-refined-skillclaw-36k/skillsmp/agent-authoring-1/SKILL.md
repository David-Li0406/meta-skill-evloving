---
name: agent-authoring
description: "Use when creating AGENTS.md files, writing SKILL.md files, or improving agentic coding developer experience. Triggers include create AGENTS.md, write SKILL.md, agent configuration, agentic DX, AI assistant context, agent instructions, skill documentation, and onboarding AI agents."
---

# Agent Authoring Skill

## Overview

This skill provides the methodology for authoring AGENTS.md and SKILL.md files that give AI coding agents the context they need to work effectively. These files serve as "onboarding documentation" that helps agents understand project conventions, avoid common mistakes, and leverage existing patterns.

---

## AGENTS.md Standards

### Purpose

AGENTS.md provides project-wide context, conventions, and explicit boundaries for AI agents. It is **distinct from README**—it contains technical details agents need but would clutter human documentation.

### Behavior

- Always loaded when agent works in that directory or below
- **Nearest file takes precedence** (nested overrides root)
- Automatically included in agent context

### Format Requirements

| Requirement    | Specification                             |
| -------------- | ----------------------------------------- |
| Format         | Pure Markdown                             |
| Maximum Length | ~150 lines                                |
| Content Style  | Concrete commands and examples, not prose |
| Commands       | Copy-pasteable, not pseudo-code           |

### Hierarchy Strategy

Use progressive disclosure through nested files:

```
repo/
├── AGENTS.md              ← Always (root context)
├── packages/
│   ├── api/
│   │   └── AGENTS.md      ← If distinct stack/conventions
│   └── web/
│       └── AGENTS.md      ← If distinct stack/conventions
├── scripts/
│   └── AGENTS.md          ← If scripts have special patterns
└── generated/
    └── AGENTS.md          ← "Do not edit" warning
```

### Placement Criteria

| Location             | When to Create                                                 |
| -------------------- | -------------------------------------------------------------- |
| **Root**             | Always—project-wide context, main build/test commands          |
| **Subdirectory**     | When directory has distinct conventions that differ from root  |
| **Package/Module**   | In monorepos, each package with its own build/test/conventions |
| **Generated/Vendor** | Directories agents should avoid modifying                      |

---

## SKILL.md Standards

### Purpose

SKILL.md files capture domain-specific, bounded procedures with reusable capabilities. They teach agents how to perform specific multi-step tasks.

### Location

Always place in `.github/skills/{skill-name}/SKILL.md`:

```
repo/
├── .github/
│   └── skills/
│       ├── database-migration/
│       │   ├── SKILL.md              ← Migration procedure
│       │   └── migrate.sh            ← Supporting script
│       ├── deployment/
│       │   ├── SKILL.md              ← Deploy procedure
│       │   └── deploy-checklist.md   ← Reference doc
│       └── api-versioning/
│           └── SKILL.md              ← Versioning procedure
```

### Behavior

- Auto-discovered but loaded **on-demand**
- Only YAML frontmatter loaded initially (saves tokens)
- Full content loaded when description matches user intent

### Format Requirements

| Requirement    | Specification                                   |
| -------------- | ----------------------------------------------- |
| Frontmatter    | YAML with `name` and `description` **required** |
| Maximum Length | <500 lines                                      |
| Description    | Must include "Use when..." with trigger phrases |
| Structure      | SKILL.md + optional scripts and reference files |

### YAML Frontmatter

The `description` field is **critical**—it determines when agents load the skill:

```yaml
---
name: database-migration
description: |
  Run database migrations, create new migrations, and rollback changes.
  Use when working with database schema changes, when the user mentions
  migrations, or when database errors reference missing columns or tables.
---
```

**Key insight**: Make descriptions **trigger-clear** with specific scenarios.

---

## AGENTS.md Template

`````markdown
# AGENTS.md

> Agent instructions for [project-name]

## Commands

```bash
# Install dependencies
[exact command]

# Run tests
[exact command]

# Type checking
[exact command]

# Linting
[exact command]
```

## Code Style

- [Specific style rule with example]
- [Another concrete convention]
- Import design tokens from `src/lib/theme/tokens.ts`

## Architecture

### Key Components

- `src/components/` - React components using [pattern]
- `src/api/` - API routes following [convention]

### Module Boundaries

- [Explain key architectural decisions]

## Do Not

- ❌ Hard-code colors—use design tokens
- ❌ Use `any` types—add proper type annotations
- ❌ Modify files in `generated/` or `vendor/`
- ❌ Install packages without asking first

## Safety

- ✅ **Can do**: Read files, run type checks, run tests
- ⚠️ **Ask first**: Install packages, git operations, delete files

## See Also

- [README.md](README.md) - Project overview
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

---

## SKILL.md Template

````markdown
---
name: [skill-name]
description: |
  [What the skill does in one sentence].
  Use when [specific trigger scenario 1], when [trigger scenario 2],
  or when [trigger scenario 3].
---

# [Skill Name]

## When to Use

- User asks to [specific action]
- [Condition] requires this procedure
- Errors reference [specific symptoms]

## Prerequisites

- [Required setup item]
- [Environment configuration]

## Procedure

1. Check current state:
   ```bash
   [exact command]
   ```
````
`````

2. Perform main action:

   ```bash
   [exact command]
   ```

3. Verify success:
   ```bash
   [exact command]
   ```

## Rollback

If something fails:

```bash
[recovery command]
```

## Common Issues

| Problem               | Solution           |
| --------------------- | ------------------ |
| "[Error message]"     | [Specific fix]     |
| [Symptom description] | [Resolution steps] |

````

---

## Quality Criteria

### AGENTS.md Quality Checklist

- [ ] **Concise**: Under 150 lines, no walls of text
- [ ] **Concrete**: Commands are copy-pasteable, not pseudo-code
- [ ] **Current**: Matches actual project state (commands work, paths exist)
- [ ] **Complete**: Covers build, test, lint, and key conventions
- [ ] **Non-redundant**: Doesn't duplicate README content (references it instead)
- [ ] **Actionable**: Every statement helps agents make correct decisions
- [ ] **Boundary-setting**: Clear "Do Not" section with ❌ markers
- [ ] **Hierarchical**: Nested files only where truly needed

### SKILL.md Quality Checklist

- [ ] **YAML frontmatter**: Has required `name` and `description` fields
- [ ] **Trigger-clear description**: Includes "Use when..." with specific scenarios
- [ ] **Bounded**: Task has clear start and end states
- [ ] **Procedural**: Numbered steps with exact commands
- [ ] **Self-contained**: References supporting files in same skill folder
- [ ] **Under 500 lines**: Detailed content goes in referenced files
- [ ] **Problem/Solution pairs**: Common issues documented with fixes

---

## Anti-Patterns to Avoid

### AGENTS.md Anti-Patterns

| Anti-Pattern              | Problem                                | Fix                                      |
| ------------------------- | -------------------------------------- | ---------------------------------------- |
| **Duplicating README**    | Wastes tokens, goes stale              | Reference with `See [README.md]`         |
| **Vague guidance**        | "Write good code" is useless           | "Use guard clauses for early returns"    |
| **Stale commands**        | Commands that don't work               | Test every command before documenting    |
| **Over-nesting**          | AGENTS.md in every folder              | Only where conventions truly differ      |
| **Mega-files**            | Single 500-line AGENTS.md              | Split into hierarchy                     |
| **Missing boundaries**    | No "Do Not" section                    | Always include explicit prohibitions     |
| **Implicit knowledge**    | Assumes agents know project terms      | Define project-specific terminology      |

### SKILL.md Anti-Patterns

| Anti-Pattern              | Problem                                | Fix                                      |
| ------------------------- | -------------------------------------- | ---------------------------------------- |
| **Missing frontmatter**   | Skill won't be discovered              | Always include YAML with name/description|
| **Weak descriptions**     | Description lacks trigger phrases      | Add "Use when..." with specific scenarios|
| **Skill sprawl**          | SKILL.md for trivial procedures        | Only multi-step, bounded tasks           |
| **Unbounded scope**       | No clear start/end states              | Define prerequisites and success criteria|
| **Abstract principles**   | General knowledge, not procedures      | Use AGENTS.md for conventions instead    |

---

## Good vs Poor Skill Candidates

| Good SKILL.md Candidates                           | Poor Candidates                          |
| -------------------------------------------------- | ---------------------------------------- |
| Multi-step workflows (deploy, release, migration)  | Simple one-liners                        |
| Procedures with scripts or tooling                 | General knowledge                        |
| Domain-specific tasks (database ops, API patterns) | Project-wide conventions (use AGENTS.md) |
| Bounded, completable tasks                         | Open-ended guidance                      |
| Tasks requiring specific file references           | Abstract principles                      |

---

## Content Deduplication Guidelines

### What Belongs Where

| Content Type                  | Location                               |
| ----------------------------- | -------------------------------------- |
| Project overview              | README.md                              |
| Build/test commands for agents| AGENTS.md                              |
| Code conventions              | AGENTS.md                              |
| Multi-step procedures         | SKILL.md                               |
| API documentation             | Dedicated docs (reference from AGENTS) |
| Contributing guidelines       | CONTRIBUTING.md (reference from AGENTS)|

### Reference Pattern

Instead of duplicating, reference existing docs:

```markdown
## See Also

- [README.md](README.md) - Project overview and setup
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution workflow
- [docs/api.md](docs/api.md) - API reference
```

---

## Exemplary Patterns

### Effective Description (Trigger-Clear)

```yaml
description: |
  Guide for creating effective skills. Use when users want to create a new skill
  (or update an existing skill) that extends Claude's capabilities with specialized
  knowledge, workflows, or tool integrations.
```

**Why it works**: Includes specific trigger phrases ("create a new skill", "update an existing skill")

### Effective Do Not Section

```markdown
## Do Not

- ❌ Hard-code colors—use design tokens from `src/theme/tokens.ts`
- ❌ Use `any` types—add proper type annotations
- ❌ Modify files in `generated/` or `vendor/`
- ❌ Create new API endpoints without updating OpenAPI spec
```

**Why it works**: Specific prohibitions with alternatives provided

### Effective Gotchas Documentation

```markdown
## Development Gotchas

### 1. SDK Version
**Problem**: `container` parameter not recognized
**Solution**: Use `client.beta.messages.create()` instead of `client.messages.create()`

### 2. Beta Namespace Required
```python
# ❌ Wrong
response = client.messages.create(container={...})

# ✅ Correct
response = client.beta.messages.create(...)
```

**Why it works**: Problem/Solution pairs with concrete code examples

---

## Core Principles

### Context Window is a Public Good

Skills share the context window with everything else the agent needs. Keep files concise.

**Default assumption**: AI agents are already very smart. Only add context they don't already have.

### Calibrate Freedom to Fragility

Match specificity to the task's risk level:

| Freedom Level | When to Use                              | Format                           |
| ------------- | ---------------------------------------- | -------------------------------- |
| **High**      | Multiple valid approaches                | Text instructions                |
| **Medium**    | Preferred pattern exists                 | Pseudocode, parameterized scripts|
| **Low**       | Fragile, error-prone operations          | Specific scripts, exact commands |

### Agent Perspective

Write for AI assistants, not human developers:
- Assume technical competence
- Provide exact commands, not concepts
- Include error messages agents might encounter
- Define project-specific terminology

---

## Validation Checklist

Before finalizing any AGENTS.md or SKILL.md:

1. [ ] Commands actually work when executed
2. [ ] File paths exist in the repository
3. [ ] No content duplicated from README
4. [ ] Line count within limits (150 for AGENTS, 500 for SKILL)
5. [ ] SKILL.md has valid YAML frontmatter
6. [ ] Description includes trigger phrases
7. [ ] "Do Not" section has specific prohibitions
8. [ ] All project-specific terms are defined
````
