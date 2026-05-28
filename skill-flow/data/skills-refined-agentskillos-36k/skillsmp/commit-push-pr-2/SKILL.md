---
name: commit-push-pr
description: Create a git commit, push a branch, and open a Pull Request with gh. Use when asked to commit changes, push to origin, or create PRs, especially when conventional commits and PR templates are required.
---

# Commit, Push, and PR Workflow

## Workflow

1. Detect PR language by reading `README` / `README.md`.
   - If the README contains Japanese text, use Japanese for PR title/body; otherwise use English.
2. Ensure a feature branch.
   - Run `git branch --show-current`.
   - If on `main` or `master`, infer branch naming from `git branch -r --list 'origin/*' | grep -v 'HEAD\|main\|master'`, propose a name, then run `git switch -c <branch-name>`.
3. Try signed commit first, fallback if it fails.
   - Attempt a signed commit with `git commit -S`.
   - If the signed commit fails, retry without signing using `git -c commit.gpgsign=false commit` and note the fallback in the response.
4. Create a Conventional Commit.
   - Format:
     - `<type>[optional scope]: <description>`
     - Optional body
     - Conversation log:
       - `prompt: <user prompt>`
       - `----`
       - `<assistant response>`
       - Repeat for each exchange
     - Optional footer(s)
   - Use `feat|fix|docs|style|refactor|test|chore|ci|build|perf` as needed.
   - Keep description present tense, lowercase, under 50 chars, no period.
5. Push the branch.
   - If no upstream: `git push -u origin <branch-name>`.
   - Otherwise: `git push`.
6. Create a PR with `gh pr create`.
   - Look for PR templates in `.github/PULL_REQUEST_TEMPLATE.md`, `.github/PULL_REQUEST_TEMPLATE/`, or `docs/PULL_REQUEST_TEMPLATE.md`.
   - If no template, use a language-appropriate default template.
   - Use a HEREDOC body:
     ```bash
     gh pr create --title "<title>" --body "$(cat <<'EOF'
     <body>
     EOF
     )"
     ```
7. Output the PR URL.

## Default PR templates

**English**
```
## Summary
- <1-3 bullets>

## Changes
- <specific changes>

## Test Plan
- <how to test>

## Notes
- <extra context>
```

**Japanese**
```
## 概要
- <1〜3点>

## 変更点
- <具体的な変更>

## テスト方法
- <テスト手順>

## 備考
- <補足>
```
