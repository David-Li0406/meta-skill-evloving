---
name: skill-creator
description: Use this skill when you need guidance on creating or updating skills to enhance Claude's capabilities in specialized knowledge, workflows, or tool integration.
---

# Skill Creator

This skill provides guidance for creating effective skills.

## What is a Skill?

A skill is a modular, self-contained package that extends Claude's capabilities by providing specialized knowledge, workflows, and tools. They can be viewed as "onboarding guides" for specific domains or tasks, transforming Claude from a generalist agent into a specialized agent equipped with procedural knowledge.

### Purpose of Skills

- **Specialized Workflows**: Multi-step procedures for specific domains.
- **Tool Integration**: Instructions for handling specific file formats or APIs.
- **Domain Knowledge**: Company-specific knowledge, patterns, and business logic.
- **Bundled Resources**: Scripts, reference materials, and assets for complex and repetitive tasks.

## Core Principles

### 1. Simplicity is Key

The context window is a shared resource. Skills share this window with system prompts, conversation history, metadata from other skills, and actual user requests. 

**Default Assumption**: Claude is already very intelligent. Only add context that Claude does not already possess. Challenge every piece of information: "Does Claude really need this explanation?" and "Is the token cost of this paragraph reasonable?" Prioritize concise examples over lengthy explanations.

### 2. Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

- **High Freedom (Text-based Instructions)**: Use when multiple methods are valid, and decisions depend on context or heuristic guidance.
- **Medium Freedom (Parameterized Pseudocode or Scripts)**: Use when a preferred pattern exists, some variation is acceptable, or configuration affects behavior.
- **Low Freedom (Specific Scripts, Few Parameters)**: Use when operations are fragile, consistency is crucial, or a specific sequence must be followed.

Imagine Claude exploring paths: narrow bridges with cliffs require specific guardrails (low freedom), while open fields allow many routes (high freedom).

## Skill Structure Guidelines

Each skill consists of a required SKILL.md file and optional references:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML Front Matter (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown Instructions (required)
└── references (optional)
    ├── scripts/          - Executable code (TypeScript/Node.js/etc.)
    ├── references/       - Documents to be loaded into context as needed
    └── assets/           - Files used in the output (templates, icons, fonts, etc.)
```

### SKILL.md (Required)

Each SKILL.md must include:

- **Front Matter (YAML)**: Contains `name` and `description` fields. These are the only fields Claude reads to determine when to use the skill, so clarity and comprehensiveness are crucial.
- **Body (Markdown)**: Instructions and guidance for using the skill, loaded only after the skill is triggered (if applicable).

### References (Optional)

#### Scripts (`scripts/`)

Executable code (TypeScript/Node.js/etc.) for tasks requiring deterministic reliability or repetitive rewriting.

- **When to Include**: When the same code is rewritten repeatedly or requires deterministic reliability.
- **Example**: `scripts/rotate_pdf.ts` for PDF rotation tasks.
- **Benefits**: Token-efficient, deterministic, can be executed without loading into context.

#### References (`references/`)

Documents and reference materials intended to be loaded into context as needed to guide Claude's processes and reasoning.

- **When to Include**: For documents that Claude should reference while working.
- **Example**: `references/finance.md` for financial models, `references/mnda.md` for company NDA templates.
- **Use Cases**: Database schemas, API documentation, domain knowledge, company policies, detailed workflow guides.
- **Benefits**: Keeps SKILL.md concise, loads information only when Claude determines it is needed.

#### Assets (`assets/`)

Files not intended to be loaded into context but used in Claude's generated output.

- **When to Include**: When files are needed in the final output.
- **Example**: `assets/logo.png` for branding assets, `assets/slides.pptx` for PowerPoint templates.
- **Use Cases**: Templates, images, icons, sample documents.

## Quality Checklist

### Metadata Check
- [ ] name is in lowercase, spaces are replaced with hyphens.
- [ ] description clearly describes functionality and usage scenarios.

### Content Check
- [ ] Instructions use imperative tone.
- [ ] Include specific examples.
- [ ] Total lines < 500.

### Structure Check
- [ ] Skill is in an independent folder.
- [ ] Folder contains SKILL.md.
- [ ] Resource files are organized logically.