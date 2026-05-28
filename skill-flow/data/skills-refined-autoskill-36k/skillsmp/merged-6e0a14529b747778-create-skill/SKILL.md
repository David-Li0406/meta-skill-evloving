---
name: create-skill
description: Use this skill to create new Agent Skills for GitHub Copilot, including generating SKILL.md files and structuring directories with optional resources.
---

# Creating Agent Skills

This skill provides a comprehensive guide for creating new Agent Skills that can be utilized by AI agents like GitHub Copilot. It covers the necessary steps to scaffold a skill folder, generate a SKILL.md file, and include any required resources.

## When to Use This Skill

- User asks to "create a skill", "make a new skill", or "scaffold a skill".
- User wants to document a repeatable workflow or teach a new capability.
- User needs to add specialized capabilities to their GitHub Copilot setup.
- User requires help structuring a skill with bundled resources.

## Prerequisites

- Understanding of what the skill should accomplish.
- A clear, keyword-rich description of capabilities and triggers.
- Knowledge of any bundled resources needed (scripts, references, assets, templates).

## Creating a New Skill

### Step 1: Create the Skill Directory

Create a new folder with a lowercase, hyphenated name:

```
.github/skills/<skill-name>/
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

### Step 3: Write the Skill Body

After the frontmatter, add markdown instructions. Recommended sections:

| Section                     | Purpose                         |
| --------------------------- | ------------------------------- |
| `# Title`                   | Brief overview                  |
| `## When to Use This Skill` | Reinforces description triggers |
| `## Prerequisites`          | Required tools, dependencies    |
| `## Step-by-Step Workflows` | Numbered steps for tasks        |
| `## Troubleshooting`        | Common issues and solutions     |
| `## References`             | Links to bundled docs           |

### Step 4: Add Optional Directories (If Needed)

| Folder        | Purpose                            | When to Use                         |
| ------------- | ---------------------------------- | ----------------------------------- |
| `scripts/`    | Executable code (Python, Bash, JS) | Automation that performs operations |
| `references/` | Documentation agent reads          | API references, schemas, guides     |
| `assets/`     | Static files used AS-IS            | Images, fonts, templates            |
| `templates/`  | Starter code agent modifies        | Scaffolds to extend                 |

## Example: Complete Skill Structure

```
.github/skills/my-awesome-skill/
├── SKILL.md                    # Required instructions
├── LICENSE.txt                 # Optional license file
├── scripts/
│   └── helper.py               # Executable automation
├── references/
│   ├── api-reference.md        # Detailed docs
│   └── examples.md             # Usage examples
├── assets/
│   └── diagram.png             # Static resources
└── templates/
    └── starter.ts              # Code scaffold
```

## Quick Start: Duplicate This Template

1. Copy the `create-skill/` folder.
2. Rename to your skill name (lowercase, hyphens).
3. Update `SKILL.md`:
   - Change `name:` to match folder name.
   - Write a keyword-rich `description:`.
   - Replace body content with your instructions.
4. Add bundled resources as needed.
5. Validate with `npm run skill:validate`.

## Validation Checklist

- [ ] Folder name is lowercase with hyphens.
- [ ] `name` field matches folder name exactly.
- [ ] `description` is 10-1024 characters.
- [ ] `description` explains WHAT and WHEN.
- [ ] Body content is under 500 lines.

## Troubleshooting

| Issue                    | Solution                                                 |
| ------------------------ | -------------------------------------------------------- |
| Skill not discovered     | Improve description with more keywords and triggers      |
| Validation fails on name | Ensure lowercase, no consecutive hyphens, matches folder |
| Description too short    | Add capabilities, triggers, and keywords                 |

## References

- [Agent Skills official spec](https://agentskills.io/specification)
- [VS Code Agent Skills Documentation](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Reference Skills Repository](https://github.com/anthropics/skills)