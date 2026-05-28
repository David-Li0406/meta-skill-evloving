---
name: skill-installer
description: Use this skill to install Codex skills from a curated list or a GitHub repository path, including private repositories. It is applicable when a user requests to list installable skills or install specific skills.
---

# Skill Installer

This skill helps install Codex skills, primarily from the curated list at `https://github.com/openai/skills/tree/main/skills/.curated`, but users can also provide other locations, including experimental skills from `https://github.com/openai/skills/tree/main/skills/.experimental`.

## When to Use
- When the user asks to list installable skills.
- When the user requests to install a curated skill by name.
- When the user provides a GitHub repository/path for skill installation.

## Inputs
- Skill source (curated list, GitHub repo URL, or repo/path).
- Destination path or `$CODEX_HOME` override.
- User confirmation for overwrites or updates.

## Outputs
- Installed skill directory under a category folder (e.g., `$CODEX_HOME/skills/<skill-name>`).
- A summary of what was installed and from where.
- A reminder to restart Codex to pick up new skills.

## Communication
When listing skills, output approximately as follows, depending on the context of the user's request:
```
Skills from {repo}:
1. skill-1
2. skill-2 (already installed)
3. ...
Which ones would you like installed?
```
After installing a skill, inform the user: "Restart Codex to pick up new skills."

## Scripts
All scripts require network access, so request escalation when running in a restricted environment:
- `scripts/list-curated-skills.py` (prints curated list with installed annotations)
- `scripts/list-curated-skills.py --format json`
- `scripts/install-skill-from-github.py --repo <owner>/<repo> --path <path/to/skill> [<path/to/skill> ...]`
- `scripts/install-skill-from-github.py --url https://github.com/<owner>/<repo>/tree/<ref>/<path>`

## Behavior and Options
- Defaults to direct download for public GitHub repositories.
- If download fails due to auth/permission errors, falls back to git sparse checkout.
- Aborts if the destination skill directory already exists.
- Installs into `$CODEX_HOME/skills/<skill-name>` (defaults to `~/.codex/skills`).
- Multiple `--path` values can install multiple skills in one run, each named from the path basename unless `--name` is supplied.
- Options: `--ref <ref>` (default `main`), `--dest <path>`, `--method auto|download|git`.

## Notes
- Curated listings are fetched from `https://github.com/openai/skills/tree/main/skills/.curated` via the GitHub API. If unavailable, explain the error and exit.
- Private GitHub repositories can be accessed via existing git credentials or optional `GITHUB_TOKEN`/`GH_TOKEN` for download.
- The skills at `https://github.com/openai/skills/tree/main/skills/.system` are preinstalled, so no need to assist users in installing those. If they ask, just explain this. If they insist, you can download and overwrite.

## Validation
- Run any relevant checks or scripts when available.
- Fail fast and report errors before proceeding.

## Procedure
1. Clarify scope and inputs.
2. Execute the core workflow.
3. Summarize outputs and next steps.

## Anti-patterns to Avoid
- Installing from unverified or ambiguous sources.
- Overwriting existing skills without explicit consent.
- Skipping the restart reminder after installation.