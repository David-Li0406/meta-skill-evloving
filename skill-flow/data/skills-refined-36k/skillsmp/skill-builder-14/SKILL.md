---
name: Skill Builder
description: Specialized instructions for building high-quality, reusable agent skills following the Vercel/Agentic standards. Use this when creating new skills or documentation for the agent.
---

# Skill Builder

This skill provides the core principles and process for creating new agent skills. Follow these guidelines to ensure skills are concise, effective, and maintainable.

## 1. Core Principles

### 1.1 Concise is Key

The context window is a public good. Only add context the agent doesn't already have.

- **Challenge every sentence**: "Does the agent really need this explanation?"
- **Prefer examples**: Use concise code snippets over verbose explanations.

### 1.2 Set Appropriate Degrees of Freedom

Match the level of specificity to the task:

- **High freedom**: Use text-based instructions when many approaches are valid.
- **Medium freedom**: Use pseudocode or scripts with parameters for preferred patterns.
- **Low freedom**: Use specific scripts for fragile, error-prone, or critical sequences.

### 1.3 Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/ - Executable code (Python/Bash)
    ├── references/ - Documentation to be loaded as needed
    └── assets/ - Templates, icons, fonts, boilerplate
```

## 2. Skill Creation Process

### Step 1: Understanding & Examples

Identify the specific domain and gather concrete examples of "Incorrect" vs "Correct" patterns.

### Step 2: Planning

Decide on the structure:

- What belongs in `SKILL.md` (core procedural instructions)?
- What belongs in `references/` (detailed schemas, docs)?
- What scripts are needed?

### Step 3: Initialization

Create the folder and `SKILL.md` with accurate YAML frontmatter. The `description` is critical as it triggers the skill.

### Step 4: Iteration

Test the skill and prune unnecessary text. Move detailed reference material to separate files in the `references/` folder to keep the main skill lean.

## 3. Progressive Disclosure

Don't overwhelm the agent. Mention that detailed docs exist in `references/` and provide `grep` patterns or specific file names so the agent can fetch them only when needed.
