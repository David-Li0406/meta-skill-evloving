---
name: address-pr-comments
description: Process and address GitHub Pull Request review comments. Use when the user asks to address PR comments, check PR comments, review PR feedback, or fix PR review comments, including fetching comments, updating code, running lint/tests, committing, and replying in GitHub.
---

# Address PR Comments

## Overview

Handle GitHub PR review comments end-to-end: fetch comments, decide which need code changes, apply fixes, run quality checks, commit, and reply to each comment with resolution details.

## Workflow

### 1. Fetch PR comments

Use `gh` to identify the PR and list comments with context.

```bash
gh pr view --json number,title,url
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments \
  --jq '.[] | "\n---\nFile: \(.path):\(.original_line)\nAuthor: \(.user.login)\nBody: \(.body)\n"'
```

### 2. Analyze and group

- Identify which comments require code changes vs. explanation only.
- Group related comments and address them together.
- Ask for clarification if intent is unclear.

### 3. Address comments sequentially (one task at a time)

For each comment or group, complete the full cycle below before moving to the next task:

1. Read relevant files to confirm intent.
2. Make code changes when needed.
3. Run the project linter on modified files.
4. Run the full project test suite (not a subset).
5. Commit with a descriptive message.
6. Push the commit.
7. Reply to the PR comment with the fix and a link to the GitHub commit.
   Include a short author note in the reply body:
   - Codex: "Reply authored by Codex"
   - Claude Code: "Reply authored by Claud"

```bash
git add <files> && git commit -m "Describe the fix"
git push
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments \
  -F in_reply_to={comment_id} \
  -F body="Fixed in {commit_url} - {brief description of the change}\nReply authored by Codex"
```

### 4. Respond when no code change is needed

If a comment is a question or requires only explanation, reply directly without code changes.

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments \
  -F in_reply_to={comment_id} \
  -F body="Explain the reasoning or answer the question\nReply authored by Codex"
```

## Rules

- Run the linter before committing.
- Run the full test suite before committing.
- Address one comment or group at a time.
- Push after each task is completed before replying.
- Include the GitHub commit link in comment replies for traceability.
