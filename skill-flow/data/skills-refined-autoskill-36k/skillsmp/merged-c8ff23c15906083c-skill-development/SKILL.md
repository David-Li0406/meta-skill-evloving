---
name: skill-development
description: Use this skill when the user wants to "create a skill", "add a skill to plugin", "write a new skill", "improve skill description", "organize skill content", or needs guidance on skill structure, progressive disclosure, or skill development best practices for Claude Code plugins.
---

# Skill Development for Claude Code Plugins

This skill provides guidance for creating effective skills for Claude Code plugins.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains or tasks—they transform Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge that no model can fully possess.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

### Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

#### SKILL.md (required)

**Metadata Quality:** The `name` and `description` in YAML frontmatter determine when Claude will use the skill. Be specific about what the skill does and when to use it. Use the third-person (e.g. "This skill should be used when..." instead of "Use this skill when...").

### Bundled Resources (optional)

#### Scripts (`scripts/`)

Executable code (Python/Bash/etc.) for tasks that require deterministic reliability or are repeatedly rewritten.

- **When to include**: When the same code is being rewritten repeatedly or deterministic reliability is needed.
- **Example**: `scripts/rotate_pdf.py` for PDF rotation tasks.
- **Benefits**: Token efficient, deterministic, may be executed without loading into context.

#### References (`references/`)

Documentation and reference material intended to be loaded as needed into context to inform Claude's process and thinking.

- **When to include**: For documentation that Claude should reference while working.
- **Examples**: `references/schema.md` for database schemas, `references/api_docs.md` for API specifications.
- **Best practice**: If files are large (>10k words), include grep search patterns in SKILL.md.
- **Avoid duplication**: Information should live in either SKILL.md or references files, not both.

#### Assets (`assets/`)

Files not intended to be loaded into context, but rather used within the output Claude produces.

- **When to include**: When the skill needs files that will be used in the final output.
- **Examples**: `assets/logo.png` for brand assets, `assets/slides.pptx` for templates.

### Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude (Unlimited*)

## Skill Creation Process

To create a skill, follow these steps:

1. **Understand the Skill**: Gather concrete examples of how the skill will be used through user questions and feedback.
2. **Plan Reusable Contents**: Analyze examples to identify what scripts, references, and assets would be helpful.
3. **Create Structure**: Set up the skill directory with `mkdir -p skills/skill-name/{references,examples,scripts}`.
4. **Edit the Skill**: Write SKILL.md with proper frontmatter and imperative-form body; create bundled resources.
5. **Validate and Test**: Check structure, trigger phrases, writing style, and progressive disclosure.
6. **Iterate**: Improve based on real-world usage and feedback.

### Key Writing Guidelines

- **Description**: Use third-person ("This skill should be used when...") with specific trigger phrases.
- **Body**: Use imperative/infinitive form ("To create X, do Y"), not second person ("You should...").
- **Size**: Target 1,500-2,000 words; move detailed content to references/.

## Validation Checklist

Before finalizing a skill:

- [ ] SKILL.md file exists with valid YAML frontmatter.
- [ ] Frontmatter has `name` and `description` fields.
- [ ] Markdown body is present and substantial.
- [ ] Referenced files actually exist.

## Additional Resources

### Example Skills

Copy-paste ready skill templates in `examples/`:

- **`examples/minimal-skill.md`** - Bare-bones skill with just SKILL.md.
- **`examples/complete-skill.md`** - Full skill with references/, examples/, and scripts/.
- **`examples/frontmatter-templates.md`** - Quick-reference frontmatter patterns for common use cases.

### Reference Files

For detailed guidance, consult:

- **`references/skill-creation-workflow.md`** - Plugin-specific skill creation workflow.
- **`references/skill-creator-original.md`** - Original generic skill-creator methodology.

## Best Practices Summary

**DO:**

- Use third-person in description ("This skill should be used when...").
- Include specific trigger phrases ("create X", "configure Y").
- Keep SKILL.md lean (1,500-2,000 words).
- Use progressive disclosure (move details to references/).
- Write in imperative/infinitive form.
- Reference supporting files clearly.
- Provide working examples.
- Create utility scripts for common operations.

**DON'T:**

- Use second person ("You should...").
- Have vague trigger conditions.
- Put everything in SKILL.md (>3,000 words without references/).
- Leave resources unreferenced.
- Include broken or incomplete examples.