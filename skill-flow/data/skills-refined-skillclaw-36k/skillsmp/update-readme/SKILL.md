---
name: update-readme
description: Update README.md to reflect changes in project structure, skills, and agents. Use when new components are added or architecture changes.
license: Apache-2.0
metadata:
  author: yu-iskw
  version: "1.0"
---

# Documentation Sync: README.md

## Purpose

Ensure that the `README.md` file accurately reflects the current state of the repository, including its architecture, core skills, and orchestrator agents.

## Workflow

1.  **Detect Changes**: Identify new or modified files in the following directories:
    - `skills/`: Core library of Agent Skills.
    - `agents/`: High-level orchestrator agents.
    - `.cursor/`: Cursor-specific meta-resources.
2.  **Analyze Impact**: Determine how these changes affect the `README.md`:
    - Do new skills need to be added to the "Featured Skills" table?
    - Has the directory structure changed, requiring an update to the "Architecture" section?
    - Are there new prerequisites or installation steps?
3.  **Update README.md**:
    - Revise the **Architecture** section if new top-level directories or tool-specific folders were added.
    - Update the **Featured Skills** and **Featured Agents** lists with high-impact components.
    - Ensure all links to `SKILL.md` files or agent documentation are correct.
4.  **Verify Links**: Use `ls` or `Glob` to verify that all relative links in the `README.md` are valid.

## Sync Checklist

- [ ] "Architecture" section matches the actual directory structure.
- [ ] "Featured Skills" table includes the most relevant and up-to-date skills.
- [ ] "Featured Agents" section reflects the current set of orchestrators.
- [ ] All links to files within the repository are valid and functional.
- [ ] "Development" section correctly references current linting and formatting tools.

## Examples

### Scenario: Adding a New Skill

- **Change**: Added `skills/software_development/rust/rust-upgrade-workflow/SKILL.md`.
- **Action**: Add a new entry to the "Featured Skills" table in `README.md` describing the Rust upgrade workflow.

### Scenario: Restructuring Cursor Meta-Resources

- **Change**: Moved `.cursor/rules/` to `.cursor/configs/rules/`.
- **Action**: Update the "Architecture" section in `README.md` to reflect the new path for Cursor rules.
