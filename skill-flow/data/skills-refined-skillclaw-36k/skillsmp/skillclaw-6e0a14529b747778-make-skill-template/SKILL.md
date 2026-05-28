---
name: make-skill-template
description: Use this skill when you need to create new Agent Skills for GitHub Copilot, whether by generating a new skill from prompts or duplicating an existing template.
---

# Make Skill Template

This skill helps you scaffold new Agent Skills by generating the necessary folder structure and SKILL.md file. 

## When to Use This Skill

- When asked to "create a skill", "make a new skill", or "scaffold a skill"
- To add specialized capabilities to your GitHub Copilot setup
- When you need help structuring a skill with bundled resources
- To duplicate this template as a starting point for a new skill

## Prerequisites

- Understanding of the skill's intended functionality
- A clear, keyword-rich description of capabilities and triggers
- Knowledge of any bundled resources needed (scripts, references, assets)

## Creating a New Skill

### Step 1: Create the Skill Directory

Create a new folder with a lowercase, hyphenated name:

```
skills/<skill-name>/
└── SKILL.md          # Required
```

### Step 2: Generate SKILL.md with Frontmatter

Every skill requires YAML frontmatter with `name` and `description`:

```yaml
---
name: <skill-name>
description: '<What it does>. Use when <specific triggers, scenarios, keywords users might say>.'
---
```

#### Frontmatter Field Requirements

| Field           | Required | Constraints                                                                |
| --------------- | -------- | -------------------------------------------------------------------------- |
| `name`          | **Yes**  | 1-64 chars, lowercase letters/numbers/hyphens only, must match folder name |
| `description`   | **Yes**  | 1-1024 chars, must describe WHAT it does AND WHEN to use it                |
| `license`       | No       | License name or reference to bundled LICENSE.txt                           |
| `compatibility` | No       | 1-500 chars, environment requirements if needed                            |
| `metadata`      | No       | Key-value pairs for additional properties                                  |
| `allowed-tools` | No       | Space-delimited list of pre-approved tools (experimental)                  |

### Writing Effective Descriptions

The `description` is crucial for automatic skill discovery. Include:

1. **WHAT** the skill does (capabilities)
2. **WHEN** to use it (triggers, scenarios, file types)
3. **Keywords** users might mention in prompts

**Good example:**

```yaml
description: 'Toolkit for testing and debugging code. Use when you need to troubleshoot issues or validate functionality.'
```