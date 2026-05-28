---
name: resolve-conflicts
description: Use this skill immediately when the user mentions merge conflicts that need to be resolved. It provides a structured framework for merging changes while preserving the intent of both branches.
---

# Git Conflict Resolution

Resolve Git merge conflicts by intelligently combining changes from both branches while preserving the intent of both changes. This skill follows a plan-first approach: assess conflicts, create a detailed resolution plan, get approval, then execute.

## Core Principles

1. **Plan Before Executing**: Always create a structured resolution plan and get user approval before making changes.
2. **Prefer Both Changes**: Default to keeping both changes unless they directly contradict.
3. **Merge, Don't Choose**: Especially for imports, tests, and configuration files.
4. **Regenerate Generated Files**: Never manually merge generated files - always regenerate them from their sources.
5. **Backup Before Resolving**: For deleted-modified files, create backups first.
6. **Validate with Tests**: Always run tests after resolution.
7. **Explain All Resolutions**: For each conflict resolved, provide a one-line explanation of the resolution strategy.
8. **Ask When Unclear**: When the correct resolution isn't clear from the diff, present options to the user and ask for their choice.

## Workflow

### Step 1: Assess the Conflict Situation

Run initial checks to understand the conflict scope:

```bash
git status
```

Identify and categorize all conflicted files:

- Regular file conflicts (both modified)
- Deleted-modified conflicts (one deleted, one modified)
- Generated file conflicts (lock files, build artifacts, generated code)
- Test file conflicts
- Import/configuration conflicts
- Binary file conflicts

For each conflicted file, gather information:

- File type and purpose
- Nature of the conflict (content, deletion, type change)
- Scope of changes (lines changed, sections affected)
- Whether the file is generated or hand-written

### Step 2: Create Merge Resolution Plan

Based on the assessment, create a structured plan before resolving any conflicts. Present the plan in the following markdown format:

```markdown
## Merge Resolution Plan

### Conflict Summary

- **Total conflicted files**: [N]
- **Deleted-modified conflicts**: [N]
- **Generated files**: [N]
```