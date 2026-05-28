---
name: commit
description: Reviews staged git changes and drafts a concise commit message. Use when the user wants to commit, needs a commit message, or asks to review staged changes for committing.
---

# Commit Skill

Draft and commit staged changes using a task subagent (isolated context).

## Step 1: Check for Staged Files

```bash
git diff --cached --name-only
```

**If NO staged files:** STOP immediately. Tell the user:
> "Nothing staged. Run `git add <files>` first."

Do not proceed.

## Step 2: Delegate Everything to Task Subagent

Use the `task` tool to review, draft, and commit:

```json
{
  "description": "Review staged changes, draft a commit message, and commit",
  "prompt": "1. Run `git diff --cached` to see staged changes.\n2. Draft a 1-line commit message: short phrase, brevity over grammar, explicitly describes changes, NO prefixes (feat:, fix:, etc.), NO verbose descriptions. Examples: 'task tool for parallel subagents', 'fix token expiry edge case', 'refactor auth middleware'.\n3. Run `git commit -m \"<your message>\"`\n4. Return the commit hash and message."
}
```

Report the commit hash and message returned by the task.

## Rules

- **NEVER** run `git add`
- **NEVER** run `git push`
- **NEVER** create branches
