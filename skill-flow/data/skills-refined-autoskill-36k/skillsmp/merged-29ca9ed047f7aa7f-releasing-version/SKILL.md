---
name: releasing-version
description: Use this skill to automate the process of managing releases, including updating documentation, generating changelogs, and handling versioning.
---

# Releasing Version Skill

Automate the process of managing releases, including:
  - updating documentation, 
  - generating changelogs, 
  - and handling versioning.

Use terminal git commands as needed.

## Step 1: Update Documentation

- [ ] [AGENTS.md](/AGENTS.md): update to reflect changes.
  - Ensure tech stack, setup/dev instructions, and folder structure are accurate.
- [ ] Update other relevant project files, such as [PRD.md](/PRD.md) and/or [specs](/specs) for current features status.
- [ ] Update/add architectural decisions in [ADD.md](/ADD.md) if applicable.

## Step 2: Generate Changelog

- [ ] Commit all pending changes, grouping them by type of change.
- [ ] Follow [Semantic Versioning (SemVer)](./sem-ver.md) principles.
- [ ] Update [CHANGELOG.md](/CHANGELOG.md) with entries based on commit history.
- [ ] Include other relevant project files (e.g., `package.json`).

## Step 3: Versioning

- [ ] If there is an issue/ticket ID in the context, commit with `Close #ID`.
- [ ] Merge into the default branch.
- [ ] Generate a git tag for the new version.