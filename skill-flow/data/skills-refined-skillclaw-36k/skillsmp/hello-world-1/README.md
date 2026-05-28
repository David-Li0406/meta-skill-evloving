# Hello World Skill Example

## Purpose

This is the simplest possible Agent Skill. It demonstrates:

1. **Minimal structure** - Only `SKILL.md` is required
2. **Required frontmatter** - `name` and `description` fields
3. **Basic body sections** - When to Use, Commands, Process
4. **Self-contained** - No dependencies on external files

## Why This Example Exists

Many skill examples are complex, showing advanced features like:
- Multiple bundled files (references/, scripts/, templates/)
- Complex workflows
- Integration with external tools

This example strips away all that complexity to show: **What is the absolute minimum for a working skill?**

## How to Use This Example

### As a Learning Tool

1. Read the `SKILL.md` file
2. Note the frontmatter structure (YAML between `---` markers)
3. Observe the markdown body sections
4. Try invoking it: `@claude Hello world skill, show me your example`

### As a Template

1. Copy `SKILL.md` to your new skill directory
2. Change the `name` field
3. Update the `description` field
4. Replace the body content
5. Test and iterate

## What's Missing (Intentionally)

This example intentionally omits:
- `references/` directory - Not needed for simple skills
- `scripts/` directory - Not needed unless you have executable helpers
- `templates/` directory - Not needed unless generating files
- `assets/` directory - Not needed unless using images/data
- Optional frontmatter fields - `license`, `requirements`, `metadata`

**All of these are optional.** Start simple, add complexity only when needed.

## Comparison: Minimal vs. Complete

### Minimal Skill (This Example)
```
hello-world/
└── SKILL.md (frontmatter + body)
```

**Use when:** Simple command reference, workflow guide, or code style documentation

### Complete Skill
```
complex-skill/
├── SKILL.md
├── scripts/
│   ├── validate.py
│   └── transform.sh
├── references/
│   ├── DETAILS.md
│   └── API_DOCS.md
├── templates/
│   └── output.template
└── assets/
    └── diagram.png
```

**Use when:** Complex workflows, validation logic, or extensive documentation

## Next Steps

After understanding this example:
1. Read [SKILL_ANATOMY.md](../../skill-foundry/references/SKILL_ANATOMY.md) for structure details
2. Read [BEST_PRACTICES.md](../../skill-foundry/references/BEST_PRACTICES.md) for authoring tips
3. Read [QUICK_START.md](../../skill-foundry/references/QUICK_START.md) for creating your first real skill
4. Study more complex examples in the wild
