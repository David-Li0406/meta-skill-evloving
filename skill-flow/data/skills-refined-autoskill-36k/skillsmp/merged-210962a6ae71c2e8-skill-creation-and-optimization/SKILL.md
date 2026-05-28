---
name: skill-creation-and-optimization
description: Use this skill when creating, updating, or optimizing Claude Code Skills, including guidance on structure, best practices, and activation patterns.
---

# Skill Creation and Optimization

This skill provides comprehensive guidance for creating and optimizing Claude Code Skills, ensuring they follow best practices and meet validation requirements.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. They transform Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge.

### What Skills Provide

1. **Specialized Workflows**: Multi-step procedures for specific domains.
2. **Tool Integrations**: Instructions for working with specific file formats or APIs.
3. **Domain Expertise**: Company-specific knowledge, schemas, and business logic.
4. **Bundled Resources**: Scripts, references, and assets for complex and repetitive tasks.

## Core Principles

- **Conciseness**: Keep `SKILL.md` under 500 lines. Use progressive disclosure to manage context efficiently.
- **Appropriate Freedom**: Use text for flexible tasks, pseudocode for moderate variation, and scripts for error-prone operations.
- **Cross-Model Testing**: Validate skills across different models (e.g., Haiku, Sonnet, Opus).

## Skill Structure

Every skill consists of a required `SKILL.md` file and optional bundled resources:

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

### SKILL.md (required)

**Frontmatter**: Contains `name` and `description` fields. Be clear and comprehensive in describing what the skill does and when to use it.

**Body**: Instructions and guidance for using the skill. Only loaded after the skill triggers.

### Bundled Resources (optional)

- **Scripts (`scripts/`)**: Executable code for tasks that require deterministic reliability or are repeatedly rewritten.
- **References (`references/`)**: Documentation and reference material intended to be loaded as needed into context.
- **Assets (`assets/`)**: Files used in the final output, such as templates and images.

## Skill Creation Process

1. **Understand the Skill with Concrete Examples**: Gather user requirements and clarify the skill's purpose.
2. **Plan Reusable Skill Contents**: Identify scripts, references, and assets needed for the skill.
3. **Initialize the Skill**: Create the skill directory and generate a `SKILL.md` template.
4. **Edit the Skill**: Implement resources and write the `SKILL.md` file.
5. **Package the Skill**: Validate and create a distributable `.skill` file.
6. **Iterate**: Test the skill and make improvements based on user feedback.

## Writing Effective Descriptions

The description is critical for Claude to discover your skill. Use the formula: `[What it does] + [When to use it] + [Key triggers]`.

### Example Descriptions

- **Good**: "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."
- **Too vague**: "Helps with documents."

## Validation Checklist

Before finalizing a skill, verify:

- **File Structure**: Ensure `SKILL.md` exists in the correct location.
- **YAML Frontmatter**: Check for valid syntax and required fields.
- **Content Quality**: Confirm clear instructions and concrete examples are provided.

## Common Patterns

- **Read-only Skill**: Skills that only read data without making changes.
- **Script-based Skill**: Skills that utilize scripts for processing data.
- **Multi-file Skill**: Skills that use multiple files for progressive disclosure.

## Resources

- [Claude Code Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)
- [Agent Skills Best Practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices)

Use this skill to create, update, and optimize Claude Code Skills effectively, ensuring they are well-structured and follow best practices.