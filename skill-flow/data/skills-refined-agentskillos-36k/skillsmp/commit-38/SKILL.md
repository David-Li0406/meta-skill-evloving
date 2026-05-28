---
name: commit
description: Stage and commit updated files with a commit message
disable-model-invocation: true
allowed-tools: Bash(git:*)
---

Stage the updated files and commit them with an appropriate commit message.

Follow these steps:
1. Run `git status` to see what files have changed
2. Run `git diff` to understand the changes
3. Stage the relevant changed files with `git add`
4. Commit with a clear, concise message following conventional commits:
   - feat: new feature
   - fix: bug fix
   - style: formatting/styling changes
   - perf: performance improvement
   - refactor: code refactoring
   - chore: maintenance tasks
   - docs: documentation changes

End the commit message with:
Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
