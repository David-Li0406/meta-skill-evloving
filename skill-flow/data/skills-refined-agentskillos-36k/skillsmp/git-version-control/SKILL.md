---
name: git-version-control
description: Always use this skill when using git!
---
# git-version-control

- Never use `git add -A` or `git add .` or checking to make sure only your changes are going to be included.
  - Always prefer running `git add <filename> <filename2>`.
- Commit message titles should be imperative, start capitalized, limited to 50 chars, and finish with no punctuation.
  - Bulletpoint lists and other markdown syntaxes are encouraged inside commit message descriptions.
- Do not create branches or commits unless explicitly told to do so.
- When updating from the remote, always use `git pull --rebase` to avoid unnecessary merge commits.
