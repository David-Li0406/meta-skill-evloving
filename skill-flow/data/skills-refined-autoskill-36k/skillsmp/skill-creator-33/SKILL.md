---
name: skill-creator
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
---

# Skill Creator

## Core Principles

- **Concise is key**: Context window is shared. Only add what Claude doesn't already know.
- **Keep skills short**: SKILL.md under 100 lines preferred, 500 lines max. Split to references/ if longer.
- **Degrees of freedom**: Match specificity to task fragility. Scripts for fragile operations, text for flexible ones.

## Skill Structure

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter: name, description (required)
│   └── Markdown body (required)
└── Bundled Resources (optional)
    ├── scripts/     - Executable code for deterministic/repeated tasks
    ├── references/  - Documentation loaded as needed
    └── assets/      - Files used in output (templates, images)
```

### SKILL.md

- **Frontmatter**: `name` and `description` only. Description is the trigger mechanism—include when to use.
- **Body**: Instructions for using the skill and its bundled resources.

### Resources

- **scripts/**: Reusable code. Test before including.
- **references/**: Domain knowledge, schemas, detailed guides. Load only when needed.
- **assets/**: Templates, images for output. Not loaded into context.

**Do NOT include**: README.md, CHANGELOG.md, or auxiliary documentation.

## Creation Process

1. **Understand** - Gather concrete usage examples from user
2. **Plan** - Identify reusable scripts, references, assets
3. **Initialize** - Run `scripts/init_skill.py <name> --path <dir>`
4. **Edit** - Implement resources, write SKILL.md
5. **Iterate** - Improve based on real usage

### Design Patterns

See references/ for detailed patterns:

- **references/workflows.md** - Multi-step processes, conditional logic
- **references/output-patterns.md** - Templates, quality standards

### init_skill.py

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

Creates skill directory with SKILL.md template and example resources.

**Note**: In this repo, create skills in `modules/home/profile-dev/programs/claude-code/skills/`.
