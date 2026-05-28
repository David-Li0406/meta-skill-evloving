---
name: conventional-commit
description: Use this skill when you need to create commits that follow the Conventional Commits specification, automatically categorizing and splitting changes as necessary.
---

# Skill body

## Execution Flow

### 1. Check Changes

Run the following commands to review your changes:

```bash
git status
git diff
git diff --staged
git log --oneline -5
```

- Review the changed files and differences.
- Refer to recent commit styles.

### 2. Determine Classification and Splitting

Automatically decide whether to **split commits** based on the following criteria:

- Changes involve different features.
- Both `feat` and `fix` are present.
- Changes include independent revertable modifications.
- The diff is too large (over 300 lines is a guideline).

### 3. Generate Commit Message

Follow the conventions outlined in the commit message guidelines to generate the message.

**For the Body's "Why":**
- If the reason for the change can be inferred from the code diff or conversation context, include it.
- If it cannot be inferred, **ask the user** (e.g., "Please provide the background or reason for this change").
- Omit the body for simple changes (e.g., typo fixes, formatting).

### 4. User Confirmation

If splitting commits is necessary, present the reasons and the units for splitting. If no split is needed, no confirmation is required.

### 5. Execute Commit

After confirmation, run `git add` and `git commit`.

If splitting is required, stage and commit each logical unit separately.

## Notes

- Do not use `git commit --amend` unless explicitly instructed.
- Do not use `--no-verify` unless explicitly instructed.
- Do not perform a push unless explicitly instructed.