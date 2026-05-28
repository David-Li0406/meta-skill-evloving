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

- [ ] [AGENTS.md](/AGENTS.md) : update to reflect changes.
  - tech stack, 
  - setup/dev instructions, 
  - folder structure are accurate.
- [ ] Update other relevant project files, such as [PRD.md](/PRD.md) and/or [specs](/specs) for current features status.
- [ ] [ADD.md](/ADD.md) : update/add architectural decisions if any.

## Step 2: Generate Changelog

- [ ] Commit all pending changes, grouping them by type of change.
- [ ] Use [Semantic Versioning (SemVer)](./sem-ver.md) principles.
- [ ] [CHANGELOG.md](/CHANGELOG.md) : Add entries based on commit history.
- [ ] Update other relevant project files (e.g., `package.json`).

## Step 3: Versioning

- [ ] If there is an issue/ticket ID in the context, commit with `Close #ID`.
- [ ] Merge into the default branch.
- [ ] Generate a git tag for the new version.