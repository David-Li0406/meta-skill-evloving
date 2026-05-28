---
name: updating-nojodocs
description: Use this skill when you have finished making code changes and you are ready to update the documentation based on those changes.
---

# Skill body

## Overview

Nojodocs are docs.md files throughout the codebase that document each folder's purpose, architecture, and implementation. Update them after code changes using the nojo-change-documenter subagent.

**Core principle:** Provide context → Dispatch subagent → Verify updates.

**Announce at start:** "I'm using the Updating Nojodocs skill to update documentation."

## The Process

### Step 1: Gather Context

**Prepare information for the subagent:**

- [ ] What changed? (feature added, bug fixed, refactor, etc.)
- [ ] Why was it changed? (motivation, problem being solved)
- [ ] Which folders/files were modified?
- [ ] Any architectural changes or new patterns?

### Step 2: Dispatch nojo-change-documenter Subagent

**Use Task tool with nojo-change-documenter type:**

```bash
Task(subagent_type: nojo-change-documenter)
```

**In the prompt, provide:**

- Clear description of what changed and why
- File paths that were modified
- Relevant context from PR/commits
- Any architectural implications
- Any out of date documentation that you noticed that is not directly related to your change

### Step 3: Verify Updates

**Check that documentation was updated:**

- [ ] Run `git status` to see which docs.md files changed
- [ ] Review the diffs to ensure updates are accurate
- [ ] Verify updates focus on system architecture, not minutiae

### Step 4: Sync Remote docs.md Files

- Check if the 'nojo-sync-docs' skill exists at `{{skills_dir}}/nojo-sync-docs/SKILL.md`.
  - If it does not exist, skip this step.
- Ask the user if they want to sync all docs.md files to the remote server.
  - If the user declines, skip this step.
- Read and follow `{{skills_dir}}/nojo-sync-docs/SKILL.md` to sync all nojodocs to the remote server.

## Nojodocs Format

Each docs.md follows this structure:

```
# Nojodoc: [Folder Name]

Path: [Path to the folder from the repository root. Always start with @. For
  example, @/src/endpoints or @/docs ]

### Overview
[2-3 bullet summary of the folder]

### How it fits into the larger codebase

[2-10 bullet description of how the folder interacts with and fits into other
 parts of the codebase. Focus on system invariants, architecture, internal
 dependencies, places that call into this folder, and places that this folder
 calls out to]
```