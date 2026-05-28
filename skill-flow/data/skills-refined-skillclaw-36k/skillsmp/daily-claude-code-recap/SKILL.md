---
name: daily-claude-code-recap
description: What did I do today, summarize my sessions, daily standup, recap work. Use when you want a summary of Claude Code activity, need to see what was accomplished, or prepare for standup.
argument-hint: Optional date (YYYY-MM-DD), defaults to today
context: fork
agent: Explore
disable-model-invocation: true
---

# Daily Claude Code Recap

Summarize Claude Code activity for $ARGUMENTS (defaults to today).

## Data Locations

| Source       | Path                    | Content                         |
| ------------ | ----------------------- | ------------------------------- |
| Session logs | `~/.claude/projects/*/` | JSONL conversation files        |
| Scries       | `~/scries/YYYY-MM-DD-*` | Date-prefixed research sessions |

Session files use UUID names. Sub-agent files (`agent-*.jsonl`) inherit context from parent sessions.

Project directories encode filesystem paths: hyphens replace `/`, double-hyphens represent literal hyphens. Decode these to locate actual repos.

---

## Process

### 1. Discover Sessions

Run these commands to find session files from the target date:

```bash
find ~/.claude/projects -name "*.jsonl" -mtime -1 -type f 2>/dev/null | xargs ls -la 2>/dev/null | sort -k6,7
```

Count sessions per project to see where work concentrated:

```bash
find ~/.claude/projects -name "*.jsonl" -mtime -1 -type f 2>/dev/null | xargs dirname | sort | uniq -c | sort -rn
```

Check for scries:

```bash
ls -la ~/scries/ | grep "YYYY-MM-DD"
```

### 2. Analyze Sessions by Project

For each project directory with activity, use an Explore agent to read its JSONL files. Provide this prompt:

> Analyze session files in [PROJECT_DIR]. For each session, extract:
>
> 1. Initial user request (first human message)
> 2. Actions taken (tool calls, edits, commands)
> 3. Artifacts created (files, commits, PRs, docs)
> 4. Status: completed, in-progress, or blocked
>
> For large files: read first 100 lines (intent) and last 150 lines (outcome). Search for: `git commit`, `gh pr create`, `Write`, `Edit`.

Group findings by project directory—multiple sessions in the same directory often represent continued work on one task, which reveals more activity than file size alone.

### 3. Check Git Repos

Decode project directory names to filesystem paths. For paths containing git repos:

```bash
git -C [REPO_PATH] log --oneline --since="$DATE 00:00" --all | head -15
gh pr list --state all --search "created:>=$DATE" 2>/dev/null
```

### 4. Compile Summary

Structure output as:

```markdown
## Your Day with Claude — [DATE]

[One-sentence theme]

---

### [Category]

**[Task]** ✓ Complete / → In progress

- Accomplishment
- Artifacts: PR, commit, file

---

### Surface Areas

| Domain | Projects |
| ------ | -------- |

**Sessions:** N across M projects | **Artifacts:** [list] | **Theme:** [pattern]
```
