---
name: commit-message
description: Generate Git commit messages from staged changes using a conventional commit subject (English, <= 72 chars) and a Korean body (wrapped at 72 chars). Use when asked to write, suggest, or refine a git commit message.
---

# Commit Message Convention

Based on the following git diff of staged changes, generate a conventional commit message with a clear subject line (max 72 chars) and body (wrapped at 72 chars).
The message should clearly explain what changed and why.
To create a commit message, focus on staged files ONLY. Run `git diff --cached` to see the changes.
Sometimes, you have to `git add` files by yourself -- pre-commit fail, unstaged files, or manual edit by a user. In this case, NEVER USE `git add -u` or `git add -A`; instead, add each file.

Format the commit message as plain text (no markdown):
- First line: conventional commit format (feat:, fix:, docs:, etc.) under 72 chars in English
- Empty line
- Body: wrapped at 72 chars, explaining what and why in Korean
- Use heredoc syntax for multi-line commit messages to preserve formatting
