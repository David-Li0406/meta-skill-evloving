---
name: commit-msg
description: Generate commit message from git diff with security check
allowed-tools: Bash(git status *), Bash(git diff *), Bash(git log *), Read, Grep, Glob, LS
disable-model-invocation: true
---

# Git Add, Commit, Push Command Generator

## Your task

1. Check git status and diff to understand changes
2. Analyze recent commits for style reference
3. Security check for confidential information
4. Generate a single-line commit message
5. Output 3 executable git commands (add, commit, push)

### Step 1: Check Git Status and Changes

```bash
git status
git diff --cached
git diff
```

### Step 2: Analyze Recent Commits (for style reference)

```bash
git log --oneline -10
```

### Step 3: Security Check (IMPORTANT)

Before generating commands, verify the diff does NOT contain:

- Real project/client names (actual company names, project codes)
- Personal information (real names, emails, phone numbers)
- Credentials (API keys, passwords, tokens)
- Internal URLs or IP addresses
- Confidential business information

If any confidential information is found:

1. List the specific items found
2. DO NOT output git commands
3. Ask user to remove confidential information first

### Step 4: Generate Single-Line Commit Message

Generate a single-line commit message following these rules:

1. Format: `<type>(<scope>): <description>`
    - Type: feat, fix, docs, style, refactor, test, chore, etc.
    - Scope (optional): component or file affected
    - Description: concise summary of changes in English

2. Best Practices:
    - Use imperative mood ("add" not "added")
    - Keep under 72 characters
    - No period at end
    - Focus on what changed

### Step 5: Output Executable Commands

Only if security check passes, output exactly 3 lines of executable git commands:

```bash
git add .
git commit -m "<generated commit message>"
git push
```

IMPORTANT:

- Do NOT execute the commands
- Only output the 3 command lines
- User can copy and execute them manually
