# Agent Skills Best Practices

Adhere to these standards to ensure high-quality, maintainable, and context-efficient Agent Skills.

## 1. Naming & Structure

- **Directory Name**: Must match `name` in `SKILL.md`.
- **Naming Style**: kebab-case (e.g., `my-new-skill`).
- **Required Files**: `SKILL.md` in the root of the skill directory.
- **Optional Folders**:
  - `scripts/`: Executable scripts (Python, Bash, JS).
  - `references/`: Detailed documentation, APIs, or SOPs.
  - `assets/`: Templates, images, or static data.

## 2. SKILL.md Frontmatter

Every `SKILL.md` must start with YAML frontmatter.

```yaml
---
name: [skill-name]
description: [Action] [Context] to [Goal]. Use when [Trigger/Scenario].
license: Apache-2.0
metadata:
  author: [Author]
  version: "1.0"
---
```

## 3. Description Guidelines

The `description` is the most important field for skill discovery.

- **Format**: `[Action] [Context] to [Goal]. Use when [Trigger/Scenario].`
- **Keywords**: Include specific terms the user might use.
- **Length**: Keep it concise but descriptive (max 1024 chars).

## 4. Progressive Disclosure

Keep the main `SKILL.md` file focused on core instructions and triggers.

- **Conciseness**: Aim for `< 500 lines` in `SKILL.md`.
- **References**: Move deep technical documentation or long tables to `references/`.
- **Assets**: Store boilerplate and static templates in `assets/`.
- **Scripts**: Move complex logic to `scripts/`.

## 5. Security & Reliability

- **CLI Help**: Always verify tool syntax with `--help` before finalizing instructions.
- **Sandboxing**: Be mindful of commands that can delete data or modify system settings.
- **Error Handling**: Provide instructions on what to do if a command fails.
