# Git Workflow Template

Use this template for git operations that need context awareness.

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: [What the git operation does]
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes, [specific task instruction].

You have the capability to call multiple tools in a single response. [Specific execution instruction]. Do not use any other tools or do anything else. Do not send any other text or messages besides these tool calls.
```

## Example: Simple Commit

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit with auto-generated message
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes, create a single git commit.

You have the capability to call multiple tools in a single response. Stage all changed files and create the commit using a single message that follows conventional commit format. Do not use any other tools or do anything else. Do not send any other text or messages besides these tool calls.
```

## Example: Full PR Workflow

```markdown
---
allowed-tools: Bash(git checkout -b:*), Bash(git add:*), Bash(git status:*), Bash(git push:*), Bash(git commit:*), Bash(gh pr create:*)
description: Commit, push, and open a PR
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`

## Your task

Based on the above changes:
1. Create a new branch if currently on main/master
2. Stage all changes and create a single commit with an appropriate message
3. Push the branch to origin
4. Create a pull request using `gh pr create` with a descriptive title and body

You have the capability to call multiple tools in a single response. You MUST do all of the above in a single message. Do not use any other tools or do anything else. Do not send any other text or messages besides these tool calls.
```

## Example: Amend Last Commit

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit --amend:*)
description: Amend the last commit with current changes
---

## Context

- Current git status: !`git status`
- Current git diff: !`git diff HEAD`
- Last commit: !`git log -1 --format="%h %s"`

## Your task

Based on the above changes, amend the last commit to include the current staged and unstaged changes.

Stage all changes and amend the last commit. Keep the existing commit message unless the changes significantly alter the commit's purpose. Do not use any other tools or do anything else.
```

## Tips

1. **Context injection is key** - Use `!`bash`` to give Claude awareness of current state
2. **Granular tool permissions** - Only allow the specific git commands needed
3. **Include recent commits** - Helps Claude match commit message style
4. **Multi-tool efficiency** - Tell Claude it can execute multiple tools at once
5. **Explicit constraints** - Prevent Claude from doing extra work
