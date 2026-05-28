---
name: use-skilo
description: Creates, installs, validates, and formats Agent Skills. Use when developing skills from templates, installing skills from git repositories, linting against the specification, or managing skills across AI coding agents.
license: MIT OR Apache-2.0
---

# Use Skilo

Skilo is a CLI tool for developing [Agent Skills](https://agentskills.io/specification).

## Installation

```bash
curl -sSfL https://raw.githubusercontent.com/manuelmauro/skilo/main/install.sh | sh
```

## Quick Start

```bash
skilo new my-skill        # Create from template
skilo add owner/repo      # Install from git
skilo lint .              # Validate against spec
skilo fmt .               # Format SKILL.md files
```

Run `skilo -h` for all commands and options.

## ALWAYS Validate Skills

**Run `skilo lint` and `skilo fmt` before committing any skill changes.** These commands enforce the [Agent Skills Specification](https://agentskills.io/specification) and catch common issues.

```bash
# Validate and format in one command
skilo check .

# Strict mode for CI (warnings become errors)
skilo check --strict .
```

## Skill Structure

```
my-skill/
├── SKILL.md        # Required: manifest with YAML frontmatter
├── scripts/        # Optional: executable code
├── references/     # Optional: additional docs (loaded on-demand)
└── assets/         # Optional: static resources
```

## Frontmatter Requirements

### Required Fields

**`name`** (1-64 characters)
- Lowercase alphanumeric and hyphens only (`a-z`, `0-9`, `-`)
- Must NOT start/end with `-` or contain `--`
- Must match parent directory name

**`description`** (1-1024 characters)
- Describe WHAT the skill does AND WHEN to use it
- Include keywords that help agents match user requests

### Optional Fields

- **`license`** - Keep short, reference LICENSE file for details
- **`compatibility`** (max 500 chars) - Environment requirements (e.g., `Requires git, docker`)
- **`metadata`** - Key-value pairs for custom properties
- **`allowed-tools`** - Space-delimited list of pre-approved tools (experimental)

## Best Practices

### Write Effective Descriptions

The description is how agents decide when to activate your skill. Be specific.

```yaml
# Good - specific, keyword-rich
description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.

# Bad - vague, no activation cues
description: Helps with PDFs.
```

### Keep Body Content Concise

The entire `SKILL.md` body loads when the skill activates. Keep it under 500 lines.

- Include step-by-step instructions
- Add examples of inputs and outputs
- Cover common edge cases
- Move detailed material to `references/`

### Use Progressive Disclosure

Structure skills to minimize context usage:

1. **Metadata** (~100 tokens) - `name` + `description` loaded at startup for all skills
2. **Instructions** (<5000 tokens) - Full body loaded when skill activates
3. **Resources** (on-demand) - `scripts/`, `references/`, `assets/` loaded only when needed

### Write Self-Contained Scripts

Scripts in `scripts/` should:
- Be self-contained or clearly document dependencies
- Include helpful error messages
- Handle edge cases gracefully

### Organize References Effectively

Files in `references/` are loaded on-demand:
- Keep files focused (one file = one concept)
- Use relative paths from skill root
- Avoid deeply nested reference chains

## Lint Rules

Skilo enforces these rules (configure in `.skilorc.toml`):

| Code | Rule                   | Default    |
|------|------------------------|------------|
| E001 | `name_format`          | enabled    |
| E002 | `name_length`          | 64 chars   |
| E003 | `name_directory`       | enabled    |
| E004 | `description_required` | enabled    |
| E005 | `description_length`   | 1024 chars |
| E006 | `compatibility_length` | 500 chars  |
| E009 | `references_exist`     | enabled    |
| W001 | `body_length`          | 500 lines  |
| W002 | `script_executable`    | enabled    |
| W003 | `script_shebang`       | enabled    |

## CI Integration

```yaml
- name: Validate skills
  run: |
    curl -sSfL https://raw.githubusercontent.com/manuelmauro/skilo/main/install.sh | sh
    skilo check --strict .claude/skills/
```
