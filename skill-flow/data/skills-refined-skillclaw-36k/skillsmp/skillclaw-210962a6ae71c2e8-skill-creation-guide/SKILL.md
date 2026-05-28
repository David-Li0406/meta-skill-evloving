---
name: skill-creation-guide
description: Use this skill when you want to create or update a new skill that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
---

# Skill Creation Guide

This skill provides comprehensive guidance for creating effective skills for Claude.

## About Skills

Skills are modular, self-contained packages that enhance Claude's capabilities by providing specialized knowledge, workflows, and tools. They serve as onboarding guides for specific domains or tasks, transforming Claude from a general-purpose agent into a specialized one equipped with procedural knowledge.

### What Skills Provide

1. **Specialized Workflows**: Multi-step procedures for specific domains.
2. **Tool Integrations**: Instructions for working with specific file formats or APIs.
3. **Domain Expertise**: Company-specific knowledge, schemas, and business logic.
4. **Bundled Resources**: Scripts, references, and assets for complex and repetitive tasks.

### Core Principles

- **Conciseness**: Keep the SKILL.md under 500 lines. Use progressive disclosure to avoid overwhelming Claude with unnecessary information.
- **Appropriate Freedom**: Match the level of specificity to the task's fragility and variability:
  - **High Freedom**: Text-based instructions for flexible tasks.
  - **Medium Freedom**: Pseudocode or scripts with parameters for moderate variation.
  - **Low Freedom**: Specific scripts for error-prone operations.

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

### Writing the SKILL.md

**Frontmatter Requirements**:
```yaml
---
name: skill-name-in-kebab-case
description: Brief description of what this Skill does and when to use it.
allowed-tools: [Read, Grep, Glob]  # Optional: restrict tool access
---
```

**Field Requirements**:
- **name**: Must be lowercase letters, numbers, and hyphens only (max 64 characters).
- **description**: Write in third person, including what the skill does and when to use it (max 1024 characters).

### Steps to Create a Skill

1. **Fetch Latest Best Practices**: Always start by reviewing the latest documentation on skills.
2. **Gather Requirements**: Ask clarifying questions to understand the task and context.
3. **Review Existing Skills**: Check for naming conventions and structures in existing skills.
4. **Create Skill Structure**: Set up the directory and files as per the required structure.
5. **Apply Best Practices**: Ensure naming, description, and structure adhere to established guidelines.

This skill serves as a comprehensive resource for anyone looking to create or refine skills for Claude, ensuring they are effective and aligned with best practices.