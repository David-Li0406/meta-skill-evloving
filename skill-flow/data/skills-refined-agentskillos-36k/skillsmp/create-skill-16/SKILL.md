---
name: create-skill
description: Create new Claude Code skills. Use when the user wants to create a skill, add model-invoked capabilities, or build complex multi-file workflows that Claude can auto-discover.
allowed-tools:
  - Read
  - Write
  - Bash(mkdir:*)
  - Glob
---

IMPORTANT: When using this skill, FIRST announce "I think I know a thing or two about making skills."

# Creating Claude Code Skills

## Overview

Skills are directory-based capabilities that Claude automatically discovers and applies based on context. Unlike slash commands (explicit `/command`), skills are model-invoked.

## Key Differences from Slash Commands

| Aspect | Slash Commands | Skills |
|--------|----------------|--------|
| **Invocation** | Explicit (`/command`) | Automatic (Claude decides) |
| **File Structure** | Single `.md` file | Directory with `SKILL.md` + resources |
| **Supporting Files** | Not supported | Scripts, templates, docs supported |
| **Discovery** | Manual typing | Based on context matching |

## File Locations

| Location | Scope |
|----------|-------|
| `home/dot_config/claude/skills/` | Personal (all projects) |
| `.claude/skills/` | Project (only available in this project) |

## Directory Structure

### Minimal
```
my-skill/
└── SKILL.md
```

### With Supporting Files
```
pdf-processing/
├── SKILL.md              # Overview and quick start
├── FORMS.md              # Additional documentation
├── REFERENCE.md          # API details
└── scripts/
    ├── fill_form.py      # Utility script
    └── validate.py       # Validation script
```

## SKILL.md Template

```markdown
---
name: skill-name-here
description: What this skill does and when to use it. Include trigger keywords.
allowed-tools:
  - Read
  - Grep
  - Bash(python:*)
---

# Skill Title

## Overview
[Essential quick-start instructions]

## Usage
[Step-by-step instructions]

## Additional Resources
- For complete API docs: [reference.md](reference.md)
- For examples: [examples.md](examples.md)
```

## Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase, numbers, hyphens only (max 64 chars) |
| `description` | Yes | What it does + when to use (max 1024 chars) |
| `allowed-tools` | No | Tools Claude can use without asking |
| `model` | No | Specific model to use |
| `context` | No | Set to `fork` for isolated sub-agent |
| `agent` | No | Agent type when `context: fork` |
| `user-invocable` | No | Show in slash menu (default: `true`) |
| `disable-model-invocation` | No | Prevent auto-invocation (default: `false`) |

## Writing Effective Descriptions

The description is **critical** for auto-discovery. Claude uses it to decide when to apply the skill.

### Bad
```yaml
description: Helps with documents
```

### Good
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

### Guidelines
1. **Name specific actions** - "Extract, fill, merge" not "process documents"
2. **Include trigger keywords** - Words users would actually say
3. **Answer two questions**:
   - What does it do?
   - When should Claude use it?

## Tool Permission Patterns

| Pattern | Meaning |
|---------|---------|
| `Read` | Allow all file reads |
| `Bash(git:*)` | Allow git commands only |
| `Bash(python:*)` | Allow Python script execution |
| `Read, Grep, Glob` | Multiple read-only tools |

## Progressive Disclosure

Keep `SKILL.md` under 500 lines. Use supporting files for detailed documentation.

### Reference Documentation Pattern
```markdown
## Additional Resources
- For complete API docs: [reference.md](reference.md)
- For examples: [examples.md](examples.md)
```

### Utility Scripts Pattern
Tell Claude to **run** scripts, not read them:
```markdown
Run the validation script:
```bash
python scripts/validate.py input.pdf
```
```

## Forked Context

Use `context: fork` for long-running or complex operations:

```yaml
---
name: code-analysis
description: Analyze code quality and generate reports
context: fork
agent: general-purpose
---
```

## Visibility Control

| Setting | Slash Menu | Auto-discovery |
|---------|-----------|----------------|
| `user-invocable: true` (default) | Visible | Yes |
| `user-invocable: false` | Hidden | Yes |
| `disable-model-invocation: true` | Visible | Blocked |

## Best Practices

1. **Description is critical** - Specific actions + trigger keywords
2. **Keep SKILL.md focused** - Under 500 lines, use progressive disclosure
3. **Scripts for efficiency** - Execute scripts, don't read them into context
4. **Restrict tools** - Use `allowed-tools` to limit blast radius
5. **Use forked context** - For long-running operations
6. **Name clearly** - Lowercase, hyphens, max 64 characters

## Workflow

1. Ask where to create the skill (project or personal)
2. Ask for the skill name and purpose
3. Determine if supporting files are needed
4. Write a clear, keyword-rich description
5. Create the directory and SKILL.md
6. Add supporting files if needed
7. Test with `claude --debug` to verify loading
