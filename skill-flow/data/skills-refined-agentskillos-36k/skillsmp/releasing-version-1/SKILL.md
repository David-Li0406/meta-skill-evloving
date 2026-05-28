---
name: releasing-version
description: >  
  Updates documentation, generates changelogs, and handles versioning.
  To be used for automating release tasks. 
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
- [ ] [PRD.md](/PRD.md) and/or [specs](/specs) current features status (If any).
- [ ] [ADD.md](/ADD.md) update/add architectural decisions (If any).

## Step 2: Generate Changelog

- [ ] Commit all pending changes grouping them by type of change.
- [ ] Use [Semantic Versioning (SemVer)](./sem-ver.md) principles.
- [ ] [CHANGELOG.md](/CHANGELOG.md) : Add entries to based on commit history.
- [ ] Other relevant project files (`package.json` ... ).

## Step 3: Versioning

- [ ] If there is an issue/ticket id in the context, commit with `Close #ID`.
- [ ] Merge it into default branch.
- [ ] Generate a git tag for the new version.
