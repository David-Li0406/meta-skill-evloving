---
name: skill-installer
description: Use this skill to install Codex skills from a curated list or a GitHub repository path when a user requests to list or install skills.
---

# Skill Installer

## Overview
This skill helps install Codex skills into `$CODEX_HOME/skills` from a curated list or a GitHub repository path. By default, skills are sourced from [OpenAI's curated skills repository](https://github.com/openai/skills/tree/main/skills/.curated), but users can also provide other locations, including private repositories.

## When to Use
- When a user asks to list installable skills.
- When a user requests to install a specific curated skill by name.
- When a user provides a GitHub repository or path for skill installation.

## Inputs
- **Skill Source**: Curated list, GitHub repository URL, or repository/path.
- **Destination Path**: Optional override for the installation path.
- **User Confirmation**: Required for overwriting existing skills.

## Outputs
- Installed skill directory under `$CODEX_HOME/skills/<skill-name>`.
- A summary of what was installed and from where.
- A reminder to restart Codex to pick up new skills.

## Compliance and Safety
- Check against GOLD Industry Standards.
- Redact secrets/PII by default.
- Do not overwrite existing skills without explicit consent.
- Use network access only when required; request escalation in restricted environments.

## Scripts
Utilize the following scripts based on the task:
- `scripts/list-curated-skills.py`: Lists available curated skills.
- `scripts/install-skill-from-github.py`: Installs skills from a specified GitHub repository.

## Behavior and Options
- Defaults to direct download for public GitHub repositories.
- If download fails due to authentication errors, falls back to git sparse checkout.
- Aborts if the destination skill directory already exists.
- Supports multiple `--path` values to install multiple skills in one run.

## Communication
When listing skills, output approximately as follows:
```
Skills from {repo}:
1. skill-1
2. skill-2 (already installed)
3. ...
Which ones would you like installed?
```
After installing a skill, inform the user: "Restart Codex to pick up new skills."