---
name: add-skill
description: Create or improve agent skills. Load when creating SKILL.md files, writing skill descriptions, or structuring skill content for OpenCode or Claude.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Creating Agent Skills

Skills extend agent capabilities with domain-specific knowledge. Use skills for procedural knowledge the agent lacks, not concepts it already understands.

If guidance is project-specific or one-off, use `INSTRUCTIONS.md` or inline context instead.

Create new skills under `/Users/nicholasgriffin/Documents/GitHub/machine-setup/ai-tooling/skills`.

## Structure

### Required Frontmatter

Every `SKILL.md` must start with YAML frontmatter on line 1:

```yaml
---
name: my-skill-name
description: What this skill does and when to use it. Third-person.
---
```

Field requirements:
- `name`: lowercase, hyphens only, max 64 chars, no reserved words ("anthropic", "claude")
- `description`: max 1024 chars, specific triggers + capabilities

### File Organisation

```
skill-name/
├── SKILL.md              # Required. Under 200 lines.
└── references/           # Optional. For detailed content.
    ├── api.md
    └── examples.md
```

Use `references/` when `SKILL.md` exceeds 200 lines. Keep references one level deep and avoid nested references.

## Writing Descriptions

The description determines when the skill activates. Include both what it does and when to use it.

Always use third-person (the description is injected into the system prompt):

| Quality | Example |
|---------|---------|
| Good | `Manages GitLab MRs and pipelines via glab CLI. Load before running glab commands.` |
| Good | `Analyses web performance with Chrome DevTools MCP. Use when auditing page load or Lighthouse scores.` |
| Bad | `I help you with GitLab operations.` |
| Bad | `Useful for various tasks.` |

Include key terms users might mention: tool names, file extensions, and specific operations.

## Content Guidelines

### Match Specificity to Task Fragility

High freedom (multiple valid approaches):
```markdown
Review code for potential bugs, readability, and adherence to project conventions.
```

Medium freedom (preferred pattern with variation):
```markdown
Use pdfplumber for text extraction. For scanned PDFs requiring OCR, use pdf2image instead.
```

Low freedom (fragile operations):
```markdown
Run exactly: `python scripts/migrate.py --verify --backup`
Do not modify flags.
```

### Writing Style

- Use imperative form: "Use X" not "You should use X"
- Assume competence; skip explanations of concepts the agent knows
- Use one term consistently: pick "endpoint" or "route", not both
- Avoid time-sensitive content

### Quick Reference Tables

For CLIs and APIs, provide lookup tables:

```markdown
| Task | Command |
|------|---------|
| Check status | `glab ci status` |
| View logs | `glab ci trace <job>` |
| Retry job | `glab ci retry <job>` |
```

## Common Patterns

### Prerequisite Verification

Check requirements before proceeding:

```markdown
## FIRST: Verify Installation

Run this before any commands. If it fails, stop; this skill does not apply.

\`\`\`bash
glab --version
\`\`\`
```

### Workflow Checklists

For multi-step tasks, provide a copyable checklist:

```markdown
## Workflow

Copy this checklist to track progress:

\`\`\`
- [ ] Step 1: Analyse input
- [ ] Step 2: Validate mapping
- [ ] Step 3: Apply changes
- [ ] Step 4: Verify output
\`\`\`
```

### Concrete Examples

Show input/output pairs instead of abstract descriptions:

```markdown
**Input**: Added user authentication with JWT tokens
**Output**:
\`\`\`
feat(auth): implement JWT-based authentication
\`\`\`
```

## Anti-patterns

- Verbose explanations: do not explain what PDFs are or how libraries work
- Multiple options without defaults: recommend one approach, mention alternatives briefly
- Vague descriptions: "Helps with documents" will not activate correctly
- Deeply nested references: `SKILL.md` → file.md → another.md breaks navigation
- Magic constants: document why values were chosen, or let the agent decide

## Checklist

Before finalising a skill:

- [ ] Frontmatter starts on line 1 with `---`
- [ ] `name` is lowercase with hyphens only
- [ ] `description` includes triggers and capabilities (third-person)
- [ ] `SKILL.md` is under 200 lines (use `references/` if larger)
- [ ] References are one level deep from `SKILL.md`
- [ ] Imperative form throughout ("Use X" not "You should")
- [ ] Quick reference table for any CLI/API commands
- [ ] Prerequisite verification if the skill depends on tools or config
- [ ] No time-sensitive information
- [ ] Tested with representative tasks
