# Agent Skills - Complete Guide

## What are Agent Skills?

Agent Skills are modular capabilities that extend Claude's functionality in Claude Code. They package expertise into discoverable, reusable components through organized folders containing:
- A `SKILL.md` file with instructions
- Optional supporting files (scripts, templates, documentation)

**Key distinction**: Skills are **model-invoked** (Claude autonomously decides when to use them based on your request and the Skill's description), unlike slash commands which are **user-invoked**.

## Creating Skills

### Directory Structure

Skills are stored in one of three locations:

1. **Personal Skills** - `~/.claude/skills/skill-name/`
   - Available across all projects
   - For individual workflows and preferences

2. **Project Skills** - `.claude/skills/skill-name/`
   - Shared with your team via git
   - For team workflows and project-specific expertise

3. **Plugin Skills** - Bundled with Claude Code plugins

### SKILL.md Format

```yaml
---
name: doing-your-skill-name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
Provide clear, step-by-step guidance for Claude.

## Examples
Show concrete examples of using this Skill.
```

- The name of a skill should always be "active" / verb-based:
  - Good: e.g., `extracting-pdf`, `reviewing-code`
  - Bad: e.g., `pdf-extractor`, `code-review`

**Field requirements:**
- `name`: Lowercase letters, numbers, and hyphens only (max 64 characters)
- `description`: What it does and when to use it (max 1024 characters)

### Supporting Files

```
doing-my-skill/
├── SKILL.md (required)
├── reference.md (optional documentation)
├── examples.md (optional examples)
├── scripts/
│   └── helper.py (optional utility)
└── templates/
    └── template.txt (optional template)
```

Reference files from SKILL.md:
````markdown
For advanced usage, see [reference.md](reference.md).

Run the helper script:
```bash
python scripts/helper.py input.txt
```
````

## Restricting Tool Access

Use the `allowed-tools` field to limit which tools Claude can use:

```yaml
---
name: reading-files-safely
description: Read files without making changes. Use when you need read-only file access.
allowed-tools: Read, Grep, Glob
---
```

This is useful for:
- Read-only Skills that shouldn't modify files
- Limited-scope Skills (e.g., data analysis only)
- Security-sensitive workflows

## Using and Managing Skills

### View Available Skills

Ask Claude directly:
```
What Skills are available?
```

Or check the filesystem:
```bash
# Personal Skills
ls ~/.claude/skills/

# Project Skills
ls .claude/skills/

# View a specific Skill's content
cat ~/.claude/skills/my-skill/SKILL.md
```

### Test a Skill

Test by asking questions matching your description:
```
Can you help me extract text from this PDF?
```

Claude autonomously decides to use the Skill—no explicit invocation needed.

### Sharing Skills with Your Team

**Via Project Repository:**
1. Create a project Skill in `.claude/skills/`
2. Commit to git and push
3. Team members automatically get the Skill when pulling

**Via Plugin:**
1. Create a plugin with Skills in the `skills/` directory
2. Add to marketplace
3. Team members install the plugin

## Debugging Skills

### Common Issues

**Claude doesn't use the Skill:**
- **Make description specific** - Include both what it does and when to use it
  ```yaml
  # Too vague
  description: Helps with documents

  # Specific
  description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
  ```
- **Verify file path** - Check `~/.claude/skills/skill-name/SKILL.md` exists
- **Check YAML syntax** - Ensure valid frontmatter with proper indentation
- **View errors** - Run `claude --debug`

**Multiple Skills conflict:**
Use distinct trigger terms in descriptions to help Claude choose correctly.

## Best Practices

1. **Keep Skills focused** - One Skill per capability
2. **Write clear descriptions** - Include specific triggers users would mention
3. **Test with your team** - Gather feedback on activation and clarity
4. **Document versions** - Track changes in SKILL.md content
5. **Use allowed-tools** - Restrict capabilities when appropriate

## Examples

### Simple Skill (single file)
```yaml
---
name: generating-commit-messages
description: Generates clear commit messages from git diffs. Use when writing commit messages or reviewing staged changes.
---

# Generating Commit Messages

## Instructions

1. Run `git diff --staged` to see changes
2. I'll suggest a commit message with:
   - Summary under 50 characters
   - Detailed description
   - Affected components

## Best practices
   
- Use present tense
- Explain what and why, not how
```

### Skill with Tool Permissions
```yaml
---
name: reviewing-code
description: Review code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
allowed-tools: Read, Grep, Glob
---

# Reviewing Code

## Review checklist
1. Code organization and structure
2. Error handling
3. Performance considerations
4. Security concerns
5. Test coverage
```

### Multi-file Skill Structure
```
pdf-processing/
├── SKILL.md
├── FORMS.md
├── REFERENCE.md
└── scripts/
    ├── fill_form.py
    └── validate.py
```

## Updating and Removing Skills

**Update**: Edit SKILL.md directly; changes take effect on next Claude Code restart

**Remove**:
```bash
# Personal
rm -rf ~/.claude/skills/my-skill

# Project
rm -rf .claude/skills/my-skill
git commit -m "Remove unused Skill"
```
