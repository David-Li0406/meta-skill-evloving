---
name: writing-skills
description: Guide for creating effective Claude Code skills. Use when creating new skills, refactoring existing skills, or validating skill structure. Covers YAML frontmatter, progressive disclosure, naming conventions, and best practices.
---

# Writing Skills

Create effective Claude Code skills that are concise, well-structured, and follow official best practices.

## Quick Reference

| Element | Requirement |
|---------|-------------|
| Filename | `SKILL.md` in skill directory |
| Name | Lowercase, hyphens, numbers only (max 64 chars) |
| Description | Third person, max 1024 chars |
| Main file | Under 500 lines |
| References | One level deep from SKILL.md |

## YAML Frontmatter

Every skill requires frontmatter:

```yaml
---
name: skill-name
description: Third person description of what skill does and when to use it. Include trigger phrases.
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]  # Optional
model: sonnet  # Optional: opus, sonnet, haiku
---
```

### Frontmatter Fields

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | Lowercase letters, numbers, hyphens. Max 64 chars |
| `description` | Yes | Third person. Max 1024 chars. Include when to use |
| `allowed-tools` | No | Restricts which tools the skill can use |
| `model` | No | Force specific model (opus, sonnet, haiku) |
| `context` | No | Set to `fork` to run in sub-agent context |
| `agent` | No | Agent type when `context: fork` (requires context) |
| `hooks` | No | Lifecycle-scoped hooks (PreToolUse, PostToolUse, Stop) |
| `user-invocable` | No | `false` hides from slash menu but allows Skill tool |
| `disable-model-invocation` | No | `true` blocks Skill tool invocation |

## Naming Conventions

**Use gerund form** (verb ending in -ing):

| Good | Avoid |
|------|-------|
| `writing-skills` | `skill-writer` |
| `debugging-api` | `api-debugger` |
| `creating-hooks` | `hook-creator` |

**Rules:**
- Lowercase letters, numbers, hyphens only
- No spaces or underscores
- Maximum 64 characters
- Descriptive of what the skill helps accomplish

## Progressive Disclosure

Keep SKILL.md focused. Split detailed content to reference files.

### Pattern 1: Table of Contents

```markdown
## Reference Files

| File | Contents |
|------|----------|
| [TEMPLATES.md](./TEMPLATES.md) | Starter templates |
| [EXAMPLES.md](./EXAMPLES.md) | Real-world examples |
| [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) | Common issues |
```

### Pattern 2: Inline Links

```markdown
For detailed templates, see [TEMPLATES.md](./TEMPLATES.md).
```

### Pattern 3: Conditional Loading

```markdown
## Advanced Configuration

If you need custom model settings, see [ADVANCED.md](./ADVANCED.md).
```

## Skill Structure

### Recommended Sections

1. **Quick Reference** - Table with key requirements
2. **Core Instructions** - Main guidance (bulk of skill)
3. **Workflows** - Step-by-step procedures with checklists
4. **Examples** - Input/output pairs
5. **Reference Files** - Links to detailed content

### File Organization

```
skills/
└── skill-name/
    ├── SKILL.md           # Main skill file (required)
    ├── TEMPLATES.md       # Starter templates (optional)
    ├── EXAMPLES.md        # Detailed examples (optional)
    └── TROUBLESHOOTING.md # Common issues (optional)
```

### Skill Discovery Locations

Skills are discovered from these locations:

| Location | Scope | Priority |
|----------|-------|----------|
| `.claude/skills/` | Current project | Highest |
| `~/.claude/skills/` | All your projects | Lower |
| Plugin `skills/` | Where plugin enabled | Lowest |

**Nested Skills Discovery (2.1.6+):** When working with files in subdirectories, Claude Code automatically discovers skills from nested `.claude/skills` directories. This enables monorepos and multi-package projects to have package-specific skills.

```
my-monorepo/
├── .claude/skills/          # Root skills (always available)
│   └── deploy/
├── packages/
│   ├── frontend/
│   │   └── .claude/skills/  # Auto-discovered when working in frontend/
│   │       └── component-generator/
│   └── backend/
│       └── .claude/skills/  # Auto-discovered when working in backend/
│           └── api-scaffolder/
```

## Writing Effective Descriptions

Descriptions appear in skill discovery. Make them count.

### Structure

```
[What it does]. [When to use it]. [Key triggers/phrases].
```

### Examples

**Good:**
```
Guide for creating effective Claude Code skills. Use when creating new
skills, refactoring existing skills, or validating skill structure.
Covers YAML frontmatter, progressive disclosure, and naming conventions.
```

**Avoid:**
```
A skill for writing skills.
```

## Workflows

Include step-by-step workflows with copyable checklists.

### Workflow Template

```markdown
## Workflow: [Name]

### Prerequisites
- [ ] Requirement 1
- [ ] Requirement 2

### Steps

1. **Step Name**
   - [ ] Action item
   - [ ] Action item

2. **Step Name**
   - [ ] Action item

### Validation
- [ ] Check 1
- [ ] Check 2
```

## Examples Section

Show concrete input/output pairs.

### Example Template

```markdown
## Examples

### Example: [Scenario Name]

**Input:**
```
User request or context
```

**Output:**
```
Expected result or response
```

**Why:** Brief explanation of approach.
```

## Validation Checklist

Before finalizing a skill:

- [ ] Name uses gerund form
- [ ] Name is lowercase with hyphens only
- [ ] Description is third person
- [ ] Description includes when to use
- [ ] SKILL.md is under 500 lines
- [ ] Reference files are one level deep
- [ ] Workflows have copyable checklists
- [ ] Examples show input/output pairs

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Over 500 lines | Split to reference files |
| Vague description | Add specific triggers and use cases |
| No workflows | Add step-by-step procedures |
| Missing examples | Add input/output pairs |
| Deep file nesting | Keep references one level deep |

## Advanced Configuration

### Forked Context

Run skills in an isolated sub-agent context using `context: fork`:

```yaml
---
name: complex-analysis
description: Deep analysis that benefits from isolated context
context: fork
agent: Explore  # Optional: specify agent type
---
```

**When to use:**
- Long-running analysis that shouldn't pollute main context
- Skills that generate large outputs
- Isolated workflows that should not affect main conversation

### Visibility Control

Control how skills appear and can be invoked:

| Setting | Slash Menu | Skill Tool | Use Case |
|---------|------------|------------|----------|
| (default) | Visible | Allowed | Normal skill |
| `user-invocable: false` | Hidden | Allowed | Model-only skills |
| `disable-model-invocation: true` | Visible | Blocked | User-only skills |
| Both false/true | Hidden | Blocked | Completely hidden |

```yaml
---
name: internal-helper
description: Helper skill only invoked by other skills
user-invocable: false  # Hide from slash menu
---
```

### Skills with Hooks

Add lifecycle hooks that run during skill execution:

```yaml
---
name: validated-deploy
description: Deploy with validation hooks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./validate.sh"
          once: true
---
```

See [creating-hooks](../creating-hooks/FRONTMATTER-HOOKS.md) for complete hook documentation.

### Skills in Subagents

Skills can be auto-loaded for custom subagents using the `skills` field in agent definitions:

```yaml
# .claude/agents/code-reviewer.md
---
name: code-reviewer
description: Reviews code using specialized skills
skills:
  - code-review
  - security-practices
---
```

**Note:** Built-in agents (Explore, Plan, general-purpose) do not have skill access.

## Reference Files

| File | Contents |
|------|----------|
| [TEMPLATES.md](./TEMPLATES.md) | Starter templates for new skills |
| [EXAMPLES.md](./EXAMPLES.md) | Real-world skill examples |
