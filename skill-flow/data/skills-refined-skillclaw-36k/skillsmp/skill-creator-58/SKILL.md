---
name: skill-creator
description: Guide for creating effective skills that extend agent capabilities with specialized knowledge, workflows, or tool integrations. Use this skill when the user asks to; (1) create a new skill, (2) make a skill, (3) build a skill, (4) set up a skill, (5) initialize a skill, (6) scaffold a skill, (7) update or modify an existing skill, (8) validate a skill, (9) learn about skill structure, (10) understand how skills work, or (11) get guidance on skill design patterns. Trigger on phrases like "create a skill", "new skill", "make a skill", "skill for X", "how do I create a skill", or "help me build a skill".
---

# Skill Creator

This skill provides guidance for creating effective skills.

## About Skills

Skills are modular, self-contained packages that extend agent capabilities by providing
specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific
domains or tasks—they transform a general-purpose agent into a specialized agent
equipped with procedural knowledge and domain expertise.

### Skill Location for Deepagents

In opencode, skills are stored in `~/.config/opencode/skill/` (note the singular dirname `skill` - not plural `skills`). For example, with the default configuration, skills live at:

```
~/.config/opencode/skill/
├── skill-name-1/
│   └── SKILL.md
├── skill-name-2/
│   └── SKILL.md
└── ...
```

### What Skills Provide

1. Specialized workflows for specific domains
2. Tool integrations for file formats or APIs
3. Domain expertise (company knowledge, schemas, business logic)
4. Bundled resources (scripts, references, assets)

## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else the agent needs: system prompt, conversation history, other Skills' metadata, and the actual user request.

**Default assumption: The agent is already very capable.** Only add context the agent doesn't already have. Challenge each piece of information: "Does the agent really need this explanation?" and "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match specificity to task fragility:

- High freedom (text instructions) - multiple valid approaches, context-dependent
- Medium freedom (parameterized scripts) - preferred pattern with variation
- Low freedom (specific scripts) - fragile operations, critical consistency

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

- Frontmatter (YAML): `name` and `description` fields. The agent reads only these to determine when to use the skill - be clear about what it does and when to trigger it.
- Body (Markdown): Instructions loaded only after the skill triggers.

#### Bundled Resources (optional)

##### Scripts (`scripts/`)

Executable code for tasks requiring deterministic reliability or repeatedly rewritten.

- Include when: same code rewritten repeatedly, or deterministic reliability needed
- Example: `scripts/rotate_pdf.py`
- Benefits: token efficient, deterministic, executable without loading into context
- Scripts may still need reading for patching or environment adjustments

##### References (`references/`)

Documentation loaded as needed into context.

- Include when: agent needs to reference while working (schemas, API docs, policies)
- Examples: `references/finance.md`, `references/api_docs.md`
- Benefits: keeps SKILL.md lean, loaded only when needed
- For large files (>10k words), include search patterns in SKILL.md
- Avoid duplication: info lives in SKILL.md OR references, not both

##### Assets (`assets/`)

Files used in output, not loaded into context.

- Include when: skill needs files for final output (templates, images, boilerplate)
- Examples: `assets/logo.png`, `assets/slides.pptx`, `assets/frontend-template/`
- Benefits: agent uses files without loading into context

#### What to Not Include

Do NOT create extraneous files: README.md, INSTALLATION_GUIDE.md, CHANGELOG.md, etc. Only include what the agent needs to do the job.

### Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (\<5k words)
3. **Bundled resources** - As needed by the agent (Unlimited because scripts can be executed without reading into context window)

#### Progressive Disclosure Patterns

Keep SKILL.md under 500 lines. Split content into separate files when approaching this limit, and reference them clearly from SKILL.md.

For skills with multiple variations/frameworks: keep core workflow in SKILL.md, move variant-specific details to reference files.

Pattern 1: High-level guide with references

```markdown
# PDF Processing

## Quick start

Extract text with pdfplumber:
[code example]

## Advanced features

- **Form filling**: See [FORMS.md](FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
```

The agent loads FORMS.md, REFERENCE.md, or EXAMPLES.md only when needed.

Pattern 2: Domain-specific organization

For skills with multiple domains, organize by domain:

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

When a user asks about sales metrics, the agent only reads sales.md.

Pattern 3: Conditional details

```markdown
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

The agent reads REDLINING.md or OOXML.md only when needed.

Guidelines:

- Keep references one level deep from SKILL.md
- For files >100 lines, include a table of contents

## Skill Creation Process

1. Understand with concrete examples
2. Plan reusable contents (scripts, references, assets)
3. Initialize (run init_skill.py)
4. Edit (implement resources and write SKILL.md)
5. Validate (run quick_validate.py)
6. Iterate based on real usage

### Step 1: Understand with Concrete Examples

Skip if usage patterns are already clear. Ask clarifying questions:

- What functionality should the skill support?
- Examples of how it would be used?
- What phrases should trigger this skill?

Conclude when functionality scope is clear.

### Step 2: Plan Reusable Contents

For each example, identify what scripts, references, and assets would help when executing repeatedly:

- `pdf-editor`: "rotate this PDF" -> `scripts/rotate_pdf.py`
- `frontend-webapp-builder`: "build me a todo app" -> `assets/hello-world/` template
- `big-query`: "how many users logged in?" -> `references/schema.md`

### Step 3: Initialize

Skip if skill already exists. Run:

```bash
scripts/init_skill.py <skill-name> --path ~/.config/opencode/skill
```

Creates skill directory with SKILL.md template and example `scripts/`, `references/`, `assets/` directories.

### Step 4: Edit

Include non-obvious info that helps the agent. Use imperative form.

#### Implement Resources

Start with `scripts/`, `references/`, `assets/` from Step 2. Test scripts by running them. Delete unused example files.

#### Update SKILL.md

Frontmatter:

- `name`: skill name
- `description`: what it does AND when to trigger. Include all trigger info here (body loads after triggering). Example: "Document creation/editing with tracked changes. Use for .docx files: creating, modifying, tracked changes, comments."

Body: Instructions for using the skill and its bundled resources.

### Step 5: Validate

```bash
scripts/quick_validate.py <path/to/skill-folder>
```

Checks: frontmatter format, naming (hyphen-case, max 64 chars), description (no angle brackets, max 1024 chars), required fields (`name`, `description`).

### Step 6: Iterate

Use on real tasks -> notice struggles -> update -> test again.

## References

See [Agent Skills specification](references/agent-skills-spec.md)
