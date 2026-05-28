---
name: diary
description: Append session work summary to Obsidian diary. Use when the user says "diary", "record this session", "log what we did", or wants to save session activities to their daily note.
disable-model-invocation: true
allowed-tools: Bash(date *), Bash(git *), Edit("~/Documents/Obsidian Vault/Diary/*.md"), Read("~/Documents/Obsidian Vault/Diary/*.md"), Write("~/Documents/Obsidian Vault/Diary/*.md")
---

# Diary

## Context

- Date: !`date "+%Y%m%d"`
- Time: !`date "+%H:%M"`
- Repository: !`git rev-parse --show-toplevel`

Target: `~/Documents/Obsidian Vault/Diary/YYYYMMDD.md`

## Entry Format

```markdown
### repository-name

#### HH:MM

- [What was done]
  - [Reason for decision, if applicable]

> 💭
```

- **repository-name**: basename of git root (extract from command output, do not use `basename` command)
- **HH:MM**: Current time via `date "+%H:%M"`
- **Reason**: Add only when a decision or choice was made
- **💭**: Reflection placeholder for user

## Steps

1. **Analyze**: Review conversation and `git log` for completed tasks

2. **Read/Create**: `~/Documents/Obsidian Vault/Diary/<date>.md`

   New file template:

   ```markdown
   ## Tasks

   - [ ]

   ## Meeting

   -

   ## Memo
   ```

3. **Append**: Add new time entry under existing repository section, or create new repository section

4. **Confirm**: Show appended content

## Guidelines

- Factual, concise, past tense
- Append only - never overwrite
