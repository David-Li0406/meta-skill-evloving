---
name: skill-architect
description: Facilitates the creation and refactoring of Agent Skills compliant with
  the official specification. Use this to scaffold new skills or audit existing ones.
license: MIT
metadata:
  author: agent-starter
  version: '1.0'
allowed-tools: Bash(python:*) Read Write
tags: 30_Resources
---
# Skill Architect

This skill automates the creation of new Agent Skills and provides standards for refactoring existing ones to ensure compliance with the [Agent Skills Specification](https://agentskills.io/specification).

## Purpose

Creating a new skill requires following a specific directory structure, naming convention, and frontmatter format. This skill abstracts those details into a simple command, allowing you to focus on the skill logic. It also provides reference checklists for auditing.

## Usage

### Creating a New Skill

To generate a new skill, use the provided Python script. You need to provide a name (kebab-case) and a description.

```bash
python .claude/skills/skill-architect/scripts/create.py "my-new-skill" --description "Description of what it does"
```

The script will:
1. Validate the name against the spec.
2. Create the folder structure (`scripts/`, `references/`, `assets/`).
3. Generate `SKILL.md` with the required frontmatter.

### Refactoring an Existing Skill

To refactor a skill:
1. Read the standards checklist at `.claude/skills/skill-architect/references/standards.md`.
2. Compare the target skill's `SKILL.md` and folder structure against the checklist.
3. Make necessary edits manually or using file editing tools.

## Instructions

1. **Scaffold**: Run the `create.py` script.
   ```bash
   python .claude/skills/skill-architect/scripts/create.py <skill-name> -d "<description>"
   ```

3. **Populate**:
   - **Consult Guidelines**: Read `references/instruction_authoring.md` for best practices on writing clear instructions.
   - **Edit SKILL.md**: Add detailed usage steps, examples, and edge case handling to the generated file.
   - **Add Scripts**: Create necessary scripts in the `scripts/` directory, following the "Solve, don't punt" pattern.

4. **Verify**:
   - Check `SKILL.md` frontmatter for completeness.
   - validation against `references/standards.md`.

## Example

**Command:**
```bash
python .claude/skills/skill-architect/scripts/create.py "data-fetcher" -d "Fetches data from API"
```

**Output:**
- Creates `.claude/skills/data-fetcher/`
- Creates `.claude/skills/data-fetcher/SKILL.md`
- Creates `.claude/skills/data-fetcher/scripts/example.py`

## References

- [Agent Skills Specification](https://agentskills.io/specification)
- [Local Standards Checklist](references/standards.md)
